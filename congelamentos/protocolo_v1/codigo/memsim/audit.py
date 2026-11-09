"""Auditoria independente dos registros exportados, sem executar as políticas."""

import csv
import gzip
import math
from pathlib import Path

from .storage import now, read_json, sha256, write_csv, write_json
from .traces import load_trace


def require(condition, message):
    if not condition:
        raise ValueError(message)


def close(actual, expected, name):
    if expected is None:
        require(actual in (None, ""), f"{name}: deveria ser ausente")
    else:
        require(actual not in (None, "") and math.isclose(float(actual), expected, rel_tol=1e-10, abs_tol=1e-10),
                f"{name}: {actual} != {expected}")


def gaps(active, capacity):
    # Reconstrói os intervalos livres a partir dos ocupados, independentemente
    # da lista livre usada pelo simulador. Detecta sobreposições e limites.
    cursor, free = 0, []
    for start, size, _ in sorted(active.values()):
        require(0 <= cursor <= start and size > 0 and start + size <= capacity, "Sobreposição/limites no replay")
        if start > cursor:
            free.append((cursor, start - cursor))
        cursor = start + size
    if cursor < capacity:
        free.append((cursor, capacity - cursor))
    return free


def check_state(row, free, capacity):
    total = sum(size for _, size in free)
    largest = max((size for _, size in free), default=0)
    close(row["free"], total, "F")
    close(row["largest"], largest, "B")
    close(row["holes"], len(free), "blocos livres")
    close(row["occupancy"], 1 - total / capacity, "U")
    close(row["dispersion"], 1 - largest / total if total else None, "D")


def audit_run(directory, trace, summary, capacity, warmup):
    active = {}
    values = {key: [] for key in ("free", "largest", "holes", "occupancy", "dispersion", "examined")}
    n = accepted = volume = accepted_volume = fragmentation = space = zero = releases_count = 0
    previous_release = (-1, -1)
    with gzip.open(directory / "tentativas.csv.gz", "rt", encoding="utf-8", newline="") as fa, \
         gzip.open(directory / "liberacoes.csv.gz", "rt", encoding="utf-8", newline="") as fr:
        attempts, releases = csv.DictReader(fa), iter(csv.DictReader(fr))
        pending_release = next(releases, None)

        def apply_release(row):
            nonlocal previous_release, releases_count
            time, identifier = int(row["time"]), int(row["id"])
            require((time, identifier) > previous_release, "Ordem de liberações inválida")
            previous_release = (time, identifier)
            require(identifier in active, "Liberação sem aceite, duplicada ou de recusa")
            start, size, death = active.pop(identifier)
            require((int(row["address"]), int(row["size"]), time) == (start, size, death), "Dados da liberação incorretos")
            expected_phase = "drenagem" if time >= len(trace) else "aquecimento" if time < warmup else "coleta"
            require(row["phase"] == expected_phase, "Fase de liberação incorreta")
            check_state(row, gaps(active, capacity), capacity)
            releases_count += 1

        for request in trace:
            row = next(attempts, None)
            require(row is not None, "Tentativa ausente")
            require(tuple(int(row[k]) for k in ("id", "time", "size", "duration")) ==
                    (request.id, request.arrival, request.size, request.duration), "Entrada diverge do rastro")
            for key in ("scenario", "algorithm"):
                require(row[key] == summary[key], "Contexto de tentativa incorreto")
            require(int(row["seed"]) == summary["seed"], "Semente incorreta")
            while pending_release is not None and int(pending_release["time"]) <= request.arrival:
                apply_release(pending_release)
                pending_release = next(releases, None)
            free = gaps(active, capacity)
            total = sum(size for _, size in free)
            largest = max((size for _, size in free), default=0)
            close(row["free_before"], total, "F anterior")
            close(row["largest_before"], largest, "B anterior")
            possible = [(index, start, size) for index, (start, size) in enumerate(free) if size >= request.size]
            # Oráculo declarativo: seleção por mínimos/máximos, distinto dos
            # laços operacionais cujo esforço está sendo medido.
            algorithm = summary["algorithm"]
            if algorithm == "first_fit":
                choice = possible[0] if possible else None
                examined = choice[0] + 1 if choice else len(free)
            elif algorithm == "best_fit":
                choice = min(possible, key=lambda p: (p[2], p[1])) if possible else None
                examined = choice[0] + 1 if choice and choice[2] == request.size else len(free)
            else:
                choice = min(possible, key=lambda p: (-p[2], p[1])) if possible else None
                examined = len(free)
            close(row["examined"], examined, "blocos examinados")
            if choice:
                require(row["result"] == "aceita" and row["cause"] == "", "Aceite/causa incorretos")
                close(row["address"], choice[1], "endereço escolhido")
                active[request.id] = (choice[1], request.size, request.arrival + request.duration)
            else:
                require(row["result"] == "recusada" and row["address"] == "", "Recusa/endereço incorretos")
                require(row["cause"] == ("espaco_total" if total < request.size else "fragmentacao"), "Causa incorreta")
            check_state(row, gaps(active, capacity), capacity)
            require(row["phase"] == ("aquecimento" if request.arrival < warmup else "coleta"), "Fase incorreta")
            if request.arrival >= warmup:
                n += 1
                volume += request.size
                if choice:
                    accepted += 1
                    accepted_volume += request.size
                elif total < request.size:
                    space += 1
                else:
                    fragmentation += 1
                for key in values:
                    if row[key] != "":
                        values[key].append(float(row[key]))
                zero += int(row["free"]) == 0
        require(next(attempts, None) is None, "Tentativas extras")
        while pending_release is not None:
            apply_release(pending_release)
            pending_release = next(releases, None)
    require(not active and gaps(active, capacity) == [(0, capacity)], "Drenagem inválida")
    expected = {"n": n, "accepted": accepted, "requested_volume": volume, "accepted_volume": accepted_volume,
        "fragmentation_count": fragmentation, "space_count": space,
        "acceptance_pct": 100 * accepted / n, "volume_pct": 100 * accepted_volume / volume,
        "fragmentation_pct": 100 * fragmentation / n, "space_pct": 100 * space / n,
        "zero_free_count": zero, "zero_free_fraction": zero / n,
        "dispersion_valid_count": len(values["dispersion"]), "dispersion_valid_fraction": len(values["dispersion"]) / n,
        "search_mean": math.fsum(values["examined"]) / n, "search_max": max(values["examined"]),
        "effective_releases": releases_count}
    for key in ("free", "largest", "holes", "occupancy", "dispersion"):
        expected[key + "_mean"] = math.fsum(values[key]) / len(values[key]) if values[key] else None
    for key, expected_value in expected.items():
        close(summary[key], expected_value, key)
    return n


def audit_results(input_directory, output):
    directory, output = Path(input_directory), Path(output)
    manifest = read_json(directory / "manifest.json")
    require(manifest["status"] == "complete", "Só auditar lote concluído")
    config = read_json(directory / "config.json")
    require(sha256(directory / "resumo_execucoes.csv") == manifest["summary_csv_sha256"], "Resumo CSV alterado")
    require(sha256(directory / "series_temporais.csv") == manifest["temporal_csv_sha256"], "Séries alteradas")
    output.mkdir(parents=True, exist_ok=False)
    records = []
    try:
        for entry in manifest["runs"]:
            s, seed, algorithm = entry["scenario"], entry["seed"], entry["algorithm"]
            run_dir = directory / "execucoes" / s / f"seed_{seed:04d}" / algorithm
            for filename, key in (("tentativas.csv.gz", "attempts_sha256"), ("liberacoes.csv.gz", "releases_sha256"), ("resumo.json", "summary_sha256")):
                require(sha256(run_dir / filename) == entry[key], f"Hash alterado: {run_dir / filename}")
            trace_file = Path(manifest["traces"]) / s / f"seed_{seed:04d}.csv"
            require(sha256(trace_file) == entry["trace_sha256"], "Rastro alterado")
            summary = read_json(run_dir / "resumo.json")
            n = audit_run(run_dir, load_trace(trace_file), summary, config["capacity"], config["warmup"])
            records.append({"scenario": s, "seed": seed, "algorithm": algorithm, "collected_attempts": n, "status": "valid"})
            if len(records) % 9 == 0:
                print(f"Auditoria independente: {len(records)}/{len(manifest['runs'])} execuções", flush=True)
        write_csv(output / "execucoes_auditadas.csv", records)
        write_json(output / "manifest.json", {"status": "complete", "runs": len(records), "completed_at_utc": now(),
            "input_manifest_sha256": sha256(directory / "manifest.json"), "method": "replay independente dos ocupados e oráculo declarativo"})
        print(f"Auditoria aprovada: {len(records)} execuções", flush=True)
    except Exception as exc:
        write_json(output / "manifest.json", {"status": "failed", "runs_checked": len(records), "error": str(exc)})
        raise

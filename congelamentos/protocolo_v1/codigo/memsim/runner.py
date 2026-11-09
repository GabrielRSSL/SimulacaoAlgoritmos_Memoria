"""Execuções sequenciais, registros completos e publicação só após sucesso."""

import csv
import gzip
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path

from .simulation import ATTEMPT_FIELDS, RELEASE_FIELDS, simulate
from .storage import (ROOT, config_hash, environment, now, read_json, sha256, snapshot,
                      source_digest, write_csv, write_json)
from .traces import generate, load_trace, save_trace, stream_seed, validate_trace


def trace_path(root, scenario, seed):
    return Path(root) / scenario / f"seed_{seed:04d}.csv"


def generate_traces(config, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "config.json", config)
    manifest = {"status": "running", "created_at_utc": now(), "config_hash": config_hash(config),
                "environment": environment(), "traces": []}
    write_json(output / "manifest.json", manifest)
    diagnostics = []
    for scenario in config["scenarios"]:
        (output / scenario).mkdir()
        for seed in config["seeds"]:
            requests = generate(config, scenario, seed)
            validate_trace(requests, config, scenario)
            path = trace_path(output, scenario, seed)
            save_trace(path, requests)
            sizes = [r.size for r in requests]
            durations = [r.duration for r in requests]
            manifest["traces"].append({"scenario": scenario, "seed": seed,
                "path": path.relative_to(output).as_posix(), "sha256": sha256(path),
                "size_stream_seed": str(stream_seed(scenario, seed, "tamanho")),
                "duration_stream_seed": str(stream_seed(scenario, seed, "permanencia"))})
            diagnostics.append({"scenario": scenario, "seed": seed, "n": len(requests),
                "size_mean": statistics.mean(sizes), "size_sd": statistics.stdev(sizes),
                "size_min": min(sizes), "size_max": max(sizes),
                "duration_mean": statistics.mean(durations), "duration_sd": statistics.stdev(durations),
                "duration_min": min(durations), "duration_max": max(durations),
                "large_fraction": sum(s >= 220 for s in sizes) / len(sizes) if scenario[:2] == "P3" else None,
                "size_duration_correlation": statistics.correlation(sizes, durations)})
    write_csv(output / "distribuicoes.csv", diagnostics)
    manifest.update(status="complete", completed_at_utc=now(), count=len(diagnostics))
    write_json(output / "manifest.json", manifest)
    print(f"Rastros preservados: {len(diagnostics)} em {output}", flush=True)


def verify_traces(config, directory):
    directory = Path(directory)
    manifest = read_json(directory / "manifest.json")
    if manifest["status"] != "complete" or manifest["config_hash"] != config_hash(config):
        raise ValueError("Rastros incompletos ou de outra configuração.")
    expected = {(s, seed) for s in config["scenarios"] for seed in config["seeds"]}
    actual = {(r["scenario"], r["seed"]) for r in manifest["traces"]}
    if actual != expected or len(actual) != len(manifest["traces"]):
        raise ValueError("Matriz de rastros incompleta ou duplicada.")
    for entry in manifest["traces"]:
        path = trace_path(directory, entry["scenario"], entry["seed"])
        if sha256(path) != entry["sha256"]:
            raise ValueError(f"Hash do rastro alterado: {path}")
    return {(r["scenario"], r["seed"]): r["sha256"] for r in manifest["traces"]}


def batch(config, traces, output, scenario=None, seed=None, algorithm=None, frozen=None):
    traces, output = Path(traces), Path(output)
    hashes = verify_traces(config, traces)  # Todos os rastros já existem antes de qualquer política.
    scenarios = [scenario] if scenario else config["scenarios"]
    seeds = [seed] if seed is not None else config["seeds"]
    algorithms = [algorithm] if algorithm else config["algorithms"]
    if not set(scenarios) <= set(config["scenarios"]) or not set(seeds) <= set(config["seeds"]) or not set(algorithms) <= set(config["algorithms"]):
        raise ValueError("Filtro fora da configuração.")
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "config.json", config)
    digest = snapshot(output / "codigo")
    manifest = {"status": "running", "started_at_utc": now(), "config_hash": config_hash(config),
                "code_hash": digest, "environment": environment(), "traces": str(traces.resolve()),
                "frozen_protocol": str(Path(frozen).resolve()) if frozen else None,
                "expected_runs": len(scenarios) * len(seeds) * len(algorithms),
                "selected_scenarios": scenarios, "selected_seeds": seeds, "selected_algorithms": algorithms,
                "runs": []}
    write_json(output / "manifest.json", manifest)
    summaries, bins = [], []
    started = time.perf_counter()
    try:
        for s in scenarios:
            for number in seeds:
                requests = load_trace(trace_path(traces, s, number))
                validate_trace(requests, config, s)
                for name in algorithms:
                    run_dir = output / "execucoes" / s / f"seed_{number:04d}" / name
                    run_dir.mkdir(parents=True)
                    # Os nomes .parcial impedem confundir uma falha com uma execução válida.
                    attempts = run_dir / "tentativas.csv.gz.parcial"
                    releases = run_dir / "liberacoes.csv.gz.parcial"
                    with gzip.open(attempts, "wt", encoding="utf-8", newline="", compresslevel=1) as fa, \
                         gzip.open(releases, "wt", encoding="utf-8", newline="", compresslevel=1) as fr:
                        wa = csv.DictWriter(fa, fieldnames=ATTEMPT_FIELDS, lineterminator="\n")
                        wr = csv.DictWriter(fr, fieldnames=RELEASE_FIELDS, lineterminator="\n")
                        wa.writeheader()
                        wr.writeheader()
                        summary, temporal = simulate(requests, name, config["capacity"], config["warmup"], s, number,
                            wa.writerow, wr.writerow, config["temporal_bin"])
                    attempts.rename(run_dir / "tentativas.csv.gz")
                    releases.rename(run_dir / "liberacoes.csv.gz")
                    summary["trace_sha256"] = hashes[s, number]
                    write_json(run_dir / "resumo.json", summary)
                    summaries.append(summary)
                    bins.extend(temporal)
                    manifest["runs"].append({"scenario": s, "seed": number, "algorithm": name,
                        "trace_sha256": hashes[s, number], "attempts_sha256": sha256(run_dir / "tentativas.csv.gz"),
                        "releases_sha256": sha256(run_dir / "liberacoes.csv.gz"),
                        "summary_sha256": sha256(run_dir / "resumo.json")})
                    write_json(output / "manifest.json", manifest)
                    print(f"[{len(summaries)}/{manifest['expected_runs']}] {s} semente={number} {name}: "
                          f"{summary['acceptance_pct']:.2f}% aceitas; "
                          f"{time.perf_counter() - started:.1f}s acumulados", flush=True)
        if source_digest() != digest:
            raise ValueError("Código/configuração mudou durante a execução.")
        write_csv(output / "resumo_execucoes.csv", summaries)
        write_csv(output / "series_temporais.csv", bins)
        manifest.update(status="complete", completed_at_utc=now(), completed_runs=len(summaries),
                        wall_seconds=time.perf_counter() - started,
                        summary_csv_sha256=sha256(output / "resumo_execucoes.csv"),
                        temporal_csv_sha256=sha256(output / "series_temporais.csv"))
        write_json(output / "manifest.json", manifest)
    except Exception as exc:
        manifest.update(status="failed", failed_at_utc=now(), error=str(exc), completed_runs=len(summaries))
        write_json(output / "manifest.json", manifest)
        raise


def run_tests(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run([sys.executable, "-X", "utf8", "-m", "pytest", "-v", "--junitxml", str(output / "pytest.xml")],
                               cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    (output / "pytest.txt").write_text(completed.stdout + completed.stderr, encoding="utf-8")
    write_json(output / "test_status.json", {"exit_code": completed.returncode, "time_utc": now(),
                                            "source_digest": source_digest()})
    print(completed.stdout, flush=True)
    if completed.returncode:
        raise RuntimeError("Testes falharam; coleta bloqueada. Consulte pytest.txt.")


def freeze(config, pilot, assessment, output):
    pilot, output = Path(pilot), Path(output)
    manifest = read_json(pilot / "execucao" / "manifest.json")
    tests = read_json(pilot / "validacao" / "test_status.json")
    decision = read_json(assessment)
    pilot_config = read_json(pilot / "execucao" / "config.json")
    methodological = [k for k in config if k not in ("seeds", "illustrative_seed")]
    if any(config[k] != pilot_config[k] for k in methodological):
        raise ValueError("Parâmetros metodológicos do piloto e da coleta diferem.")
    if manifest["status"] != "complete" or manifest["completed_runs"] != 54 or tests["exit_code"] != 0:
        raise ValueError("Piloto completo com 54 execuções e testes aprovados é obrigatório.")
    if pilot_config["seeds"] != [1001, 1002, 1003] or decision.get("prosseguir") is not True:
        raise ValueError("Sementes do piloto ou decisão metodológica inválida.")
    if manifest["code_hash"] != source_digest():
        raise ValueError("Código mudou desde o piloto; repetir o piloto antes do congelamento.")
    output.mkdir(parents=True, exist_ok=False)
    digest = snapshot(output / "codigo")
    write_json(output / "config.json", config)
    shutil.copy2(assessment, output / "decisao_piloto.json")
    shutil.copy2(ROOT / "docs/protocolo_v1.md", output / "protocolo_v1.md")
    write_json(output / "manifest.json", {"status": "frozen", "frozen_at_utc": now(),
        "config_hash": config_hash(config), "code_hash": digest, "environment": environment(),
        "pilot_manifest_sha256": sha256(pilot / "execucao" / "manifest.json"),
        "assessment_sha256": sha256(assessment), "pilot_path": str(pilot.resolve())})
    print(f"Protocolo congelado: {output}", flush=True)

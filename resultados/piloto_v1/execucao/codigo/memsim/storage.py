"""CSV UTF-8, hashes, configurações e identificação do ambiente."""

import csv
import gzip
import hashlib
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import __version__
from .policies import POLICIES

ROOT = Path(__file__).resolve().parent.parent


def now():
    return datetime.now(timezone.utc).isoformat()


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path, rows, fieldnames=None):
    rows = list(rows)
    if fieldnames is None:
        if not rows:
            raise ValueError("CSV vazio requer nomes das colunas.")
        fieldnames = list(rows[0])
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_config(path):
    config = read_json(path)
    for key in ("capacity", "requests", "temporal_bin"):
        if type(config[key]) is not int or config[key] <= 0:
            raise ValueError(f"Configuração inválida: {key}")
    if type(config["warmup"]) is not int or not 0 <= config["warmup"] < config["requests"]:
        raise ValueError("Aquecimento inválido.")
    if config["check_invariants"] is not True:
        raise ValueError("Este projeto exige invariantes em todas as operações.")
    for key in ("scenarios", "seeds", "algorithms"):
        if not config[key] or len(set(config[key])) != len(config[key]):
            raise ValueError(f"Lista vazia ou duplicada: {key}")
    if any(a not in POLICIES for a in config["algorithms"]):
        raise ValueError("Algoritmo desconhecido.")
    if any(s not in ("P1D1", "P1D2", "P2D1", "P2D2", "P3D1", "P3D2") for s in config["scenarios"]):
        raise ValueError("Cenário desconhecido.")
    if any(type(s) is not int or s <= 0 for s in config["seeds"]):
        raise ValueError("Sementes devem ser inteiros positivos.")
    if config["illustrative_seed"] not in config["seeds"]:
        raise ValueError("A semente ilustrativa deve pertencer à configuração.")
    for bounds in [config["sizes"]["P1"], config["sizes"]["P2"],
                   config["sizes"]["P3"]["small"], config["sizes"]["P3"]["large"],
                   *config["durations"].values()]:
        if len(bounds) != 2 or any(type(x) is not int for x in bounds) or not 0 < bounds[0] <= bounds[1]:
            raise ValueError("Intervalo uniforme inválido.")
    if not 0 <= config["sizes"]["P3"]["small_probability"] <= 1:
        raise ValueError("Probabilidade inválida.")
    return config


def config_hash(config):
    return hashlib.sha256(json.dumps(config, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def code_files():
    paths = [*ROOT.glob("memsim/*.py"), *ROOT.glob("tests/*.py"), *ROOT.glob("configs/*.json")]
    paths += [ROOT / name for name in ("AGENTS.md", "README.md", "requirements.txt", "requirements-lock.txt",
                                       "pytest.ini", "docs/protocolo_v1.md", "docs/conferencia_artigo.md",
                                       "docs/guia_estudo.md", "docs/dicionario_dados.md")]
    paths += list(ROOT.glob("scripts/*.py")) + list(ROOT.glob("scripts/*.ps1"))
    return sorted(p for p in paths if p.is_file())


def source_hashes():
    return {p.relative_to(ROOT).as_posix(): sha256(p) for p in code_files()}


def source_digest(hashes=None):
    hashes = source_hashes() if hashes is None else hashes
    return hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()


def environment():
    def git(*args):
        run = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        return run.stdout.strip() if run.returncode == 0 else None
    packages = {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()}
    return {"captured_at_utc": now(), "python": sys.version, "executable": sys.executable,
            "implementation": platform.python_implementation(), "platform": platform.platform(),
            "machine": platform.machine(), "processor": platform.processor(),
            "packages": dict(sorted(packages.items())), "simulator_version": __version__,
            "rng_library": "random da biblioteca padrão CPython; Mersenne Twister",
            "rng_version": platform.python_version(), "git_commit": git("rev-parse", "HEAD"),
            "git_status": git("status", "--porcelain"), "source_digest": source_digest()}


def snapshot(destination):
    destination.mkdir(parents=True, exist_ok=False)
    for path in code_files():
        target = destination / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    hashes = source_hashes()
    write_json(destination / "hashes.json", hashes)
    return source_digest(hashes)

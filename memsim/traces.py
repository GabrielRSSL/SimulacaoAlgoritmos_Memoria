"""Rastros independentes da execução; Random da biblioteca padrão do Python."""

import csv
import hashlib
import random

from .models import Request


def stream_seed(scenario, seed, stream):
    # Não usar hash() do Python: ele pode mudar entre processos.
    label = f"memsim-v1|{scenario}|{seed}|{stream}"
    return int.from_bytes(hashlib.sha256(label.encode("utf-8")).digest(), "big")


def generate(config, scenario, seed):
    size_rng = random.Random(stream_seed(scenario, seed, "tamanho"))
    duration_rng = random.Random(stream_seed(scenario, seed, "permanencia"))
    profile = config["sizes"][scenario[:2]]
    duration_range = config["durations"][scenario[2:]]
    requests = []
    for arrival in range(config["requests"]):
        if scenario[:2] == "P3":
            component = "small" if size_rng.random() < profile["small_probability"] else "large"
            size = size_rng.randint(*profile[component])
        else:
            size = size_rng.randint(*profile)
        requests.append(Request(arrival + 1, arrival, size, duration_rng.randint(*duration_range)))
    return requests


def save_trace(path, requests):
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["id", "arrival", "size", "duration"])
        writer.writerows((r.id, r.arrival, r.size, r.duration) for r in requests)


def load_trace(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return [Request(**{key: int(value) for key, value in row.items()}) for row in csv.DictReader(handle)]


def validate_trace(requests, config, scenario):
    if len(requests) != config["requests"]:
        raise ValueError("Quantidade de solicitações diferente da configuração.")
    profile = config["sizes"][scenario[:2]]
    low_d, high_d = config["durations"][scenario[2:]]
    for index, request in enumerate(requests):
        if request.id != index + 1 or request.arrival != index:
            raise ValueError("IDs e chegadas devem ser consecutivos, iniciando em 1 e 0.")
        ranges = [profile["small"], profile["large"]] if isinstance(profile, dict) else [profile]
        if not any(low <= request.size <= high for low, high in ranges):
            raise ValueError("Tamanho fora do suporte configurado.")
        if not low_d <= request.duration <= high_d:
            raise ValueError("Permanência fora do suporte configurado.")

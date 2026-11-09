"""Fórmulas por execução; amostras temporais não são réplicas independentes."""


def state(memory):
    free = sum(block.size for block in memory.free)
    largest = max((block.size for block in memory.free), default=0)
    return {
        "free": free,
        "largest": largest,
        "holes": len(memory.free),
        "occupancy": 1 - free / memory.capacity,
        "dispersion": 1 - largest / free if free > 0 else None,
    }


class Accumulator:
    def __init__(self):
        self.n = self.accepted = self.volume = self.accepted_volume = 0
        self.fragmentation = self.space = self.valid_d = self.zero_free = 0
        self.sums = {key: 0.0 for key in ("free", "largest", "holes", "occupancy", "dispersion", "examined")}
        self.max_examined = 0

    def add(self, row):
        self.n += 1
        self.volume += row["size"]
        if row["result"] == "aceita":
            self.accepted += 1
            self.accepted_volume += row["size"]
        elif row["cause"] == "fragmentacao":
            self.fragmentation += 1
        elif row["cause"] == "espaco_total":
            self.space += 1
        else:
            raise ValueError("Resultado/causa desconhecido.")
        for key in ("free", "largest", "holes", "occupancy"):
            self.sums[key] += row[key]
        if row["dispersion"] is not None:
            self.valid_d += 1
            self.sums["dispersion"] += row["dispersion"]
        else:
            self.zero_free += 1
        self.sums["examined"] += row["examined"]
        self.max_examined = max(self.max_examined, row["examined"])

    def summary(self):
        if not self.n:
            raise ValueError("Janela de coleta vazia.")
        if self.accepted + self.fragmentation + self.space != self.n:
            raise ValueError("As categorias não somam o número de solicitações.")
        if self.valid_d + self.zero_free != self.n:
            raise ValueError("Contagem de D inconsistente.")
        result = {
            "n": self.n, "accepted": self.accepted,
            "requested_volume": self.volume, "accepted_volume": self.accepted_volume,
            "fragmentation_count": self.fragmentation, "space_count": self.space,
            "acceptance_pct": 100 * self.accepted / self.n,
            "volume_pct": 100 * self.accepted_volume / self.volume,
            "fragmentation_pct": 100 * self.fragmentation / self.n,
            "space_pct": 100 * self.space / self.n,
            "dispersion_mean": self.sums["dispersion"] / self.valid_d if self.valid_d else None,
            "dispersion_valid_count": self.valid_d,
            "dispersion_valid_fraction": self.valid_d / self.n,
            "zero_free_count": self.zero_free,
            "zero_free_fraction": self.zero_free / self.n,
            "search_max": self.max_examined,
        }
        for key in ("free", "largest", "holes", "occupancy"):
            result[key + "_mean"] = self.sums[key] / self.n
        result["search_mean"] = self.sums["examined"] / self.n
        return result

"""Eventos: liberações por (instante, ID), chegada e registro do estado."""

import heapq

from .memory import InvariantError, Memory
from .metrics import Accumulator, state
from .policies import POLICIES

ATTEMPT_FIELDS = ["scenario", "seed", "algorithm", "phase", "time", "id", "size", "duration",
                  "result", "cause", "address", "examined", "free_before", "largest_before",
                  "free", "largest", "holes", "occupancy", "dispersion"]
RELEASE_FIELDS = ["scenario", "seed", "algorithm", "phase", "time", "id", "address", "size",
                  "free", "largest", "holes", "occupancy", "dispersion"]


def check_schedule(memory, scheduled, requests_by_id):
    if len(scheduled) != len(memory.active):
        raise InvariantError("Quantidade de liberações difere dos IDs ativos.")
    ids = set()
    for time, identifier in scheduled:
        request = requests_by_id[identifier]
        if identifier in ids or identifier not in memory.active:
            raise InvariantError("Liberação duplicada ou sem alocação ativa.")
        if time != request.arrival + request.duration:
            raise InvariantError("Instante de liberação incorreto.")
        if memory.active[identifier].size != request.size:
            raise InvariantError("Tamanho alocado difere do rastro.")
        ids.add(identifier)


def simulate(requests, algorithm, capacity=4096, warmup=2000, scenario="teste", seed=0,
             attempt_sink=None, release_sink=None, bin_size=500):
    if not 0 <= warmup < len(requests) or bin_size <= 0:
        raise ValueError("Aquecimento e tamanho das janelas temporais inválidos.")
    for index, request in enumerate(requests):
        if request.id != index + 1 or request.arrival != index:
            raise ValueError("É necessária uma chegada por instante, com IDs consecutivos.")
    policy = POLICIES[algorithm]
    memory = Memory(capacity)
    scheduled = []
    requests_by_id = {r.id: r for r in requests}
    collected = Accumulator()
    temporal = {}
    context = {"scenario": scenario, "seed": seed, "algorithm": algorithm}
    effective_releases = drainage_releases = accepted_all = 0
    event = "inicialização"

    def release_one(time, identifier, phase):
        block = memory.release(identifier)
        check_schedule(memory, scheduled, requests_by_id)
        if release_sink:
            release_sink({**context, "phase": phase, "time": time, "id": identifier,
                          "address": block.start, "size": block.size, **state(memory)})

    try:
        for request in requests:
            phase = "aquecimento" if request.arrival < warmup else "coleta"
            while scheduled and scheduled[0][0] <= request.arrival:
                time, identifier = heapq.heappop(scheduled)
                event = f"liberação t={time} id={identifier}"
                release_one(time, identifier, phase)
                effective_releases += 1
            event = f"tentativa t={request.arrival} id={request.id}"
            before = state(memory)
            address, examined = memory.allocate(request.id, request.size, policy)
            cause = ""
            if address is not None:
                heapq.heappush(scheduled, (request.arrival + request.duration, request.id))
                accepted_all += 1
            elif before["free"] < request.size:
                cause = "espaco_total"
            elif before["largest"] < request.size:
                cause = "fragmentacao"
            else:
                raise InvariantError("Política recusou uma solicitação que caberia.")
            check_schedule(memory, scheduled, requests_by_id)
            row = {**context, "phase": phase, "time": request.arrival, "id": request.id,
                   "size": request.size, "duration": request.duration,
                   "result": "aceita" if address is not None else "recusada", "cause": cause,
                   "address": address, "examined": examined,
                   "free_before": before["free"], "largest_before": before["largest"], **state(memory)}
            if attempt_sink:
                attempt_sink(row)
            if phase == "coleta":
                collected.add(row)
            key = (phase, request.arrival // bin_size)
            if key not in temporal:
                temporal[key] = Accumulator()
            temporal[key].add(row)

        while scheduled:
            time, identifier = heapq.heappop(scheduled)
            event = f"drenagem t={time} id={identifier}"
            release_one(time, identifier, "drenagem")
            effective_releases += 1
            drainage_releases += 1
        memory.require_drained()
        if effective_releases != accepted_all:
            raise InvariantError("Número de liberações efetivas difere das aceitações.")
    except Exception as exc:
        raise InvariantError(f"{scenario=} {seed=} {algorithm=} evento={event}: {exc}") from exc

    summary = {**context, **collected.summary(), "attempts_all": len(requests),
               "accepted_all": accepted_all, "effective_releases": effective_releases,
               "drainage_releases": drainage_releases, "drained": True}
    bins = [{**context, "phase": phase, "bin_start": index * bin_size,
             "bin_end": min((index + 1) * bin_size, len(requests)) - 1, **acc.summary()}
            for (phase, index), acc in temporal.items()]
    return summary, bins

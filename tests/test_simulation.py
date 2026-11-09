import pytest

from memsim.memory import InvariantError, Memory
from memsim.models import Request
from memsim.policies import first_fit
from memsim.simulation import check_schedule, simulate


def run(items, capacity=10, warmup=0, algorithm="first_fit"):
    attempts, releases = [], []
    requests = [Request(i + 1, i, size, duration) for i, (size, duration) in enumerate(items)]
    summary, bins = simulate(requests, algorithm, capacity, warmup, attempt_sink=attempts.append,
                             release_sink=releases.append, bin_size=1)
    return summary, attempts, releases, bins


def test_release_before_arrival_and_same_time_id_order():
    summary, attempts, releases, _ = run([(3, 2), (4, 1), (10, 1)])
    assert [(r["time"], r["id"]) for r in releases] == [(2, 1), (2, 2), (3, 3)]
    assert attempts[2]["free_before"] == 10
    assert attempts[2]["result"] == "aceita"
    assert summary["drained"]


def test_total_rejection_no_future_release():
    summary, attempts, releases, _ = run([(10, 3), (1, 1), (1, 1), (10, 1)])
    assert [r["id"] for r in releases] == [1, 4]
    assert attempts[1]["cause"] == "espaco_total"
    assert attempts[2]["free_before"] == 0
    assert summary["acceptance_pct"] == 50
    assert summary["space_pct"] == 50
    assert summary["effective_releases"] == summary["accepted_all"] == 2


@pytest.mark.parametrize("algorithm", ["first_fit", "best_fit", "worst_fit"])
def test_fragmentation_rejection_and_unchanged_state(algorithm):
    summary, attempts, _, _ = run([(4, 3), (2, 10), (4, 1), (5, 1)], algorithm=algorithm)
    row = attempts[3]
    assert (row["free_before"], row["largest_before"]) == (8, 4)
    assert row["cause"] == "fragmentacao"
    assert row["free"] == row["free_before"]
    assert row["examined"] == 2
    assert summary["fragmentation_pct"] == 25


def test_warmup_preserved_and_drainage_excluded():
    summary, attempts, releases, bins = run([(6, 5), (5, 1), (4, 8)], warmup=1)
    assert attempts[1]["free_before"] == 4  # ID 1 continua ativo na coleta.
    assert summary["n"] == 2
    assert summary["acceptance_pct"] == 50
    assert summary["volume_pct"] == pytest.approx(100 * 4 / 9)
    assert summary["occupancy_mean"] == pytest.approx(0.8)
    assert summary["free_mean"] == 2
    assert summary["search_mean"] == 1
    assert summary["search_max"] == 1
    assert summary["drainage_releases"] == 2
    assert all(r["phase"] == "drenagem" for r in releases)
    assert sum(r["n"] for r in bins) == 3


def test_dispersion_missing_for_zero_free_and_all_missing_summary():
    summary, attempts, _, _ = run([(10, 5), (1, 1)])
    assert all(r["dispersion"] is None for r in attempts)
    assert summary["dispersion_mean"] is None
    assert summary["dispersion_valid_count"] == 0
    assert summary["zero_free_count"] == 2
    assert summary["zero_free_fraction"] == 1
    assert summary["search_mean"] == 0.5


def test_schedule_consistency_and_context_error():
    memory = Memory(10)
    memory.allocate(1, 2, first_fit)
    requests = {1: Request(1, 0, 2, 3)}
    for scheduled in ([], [(4, 1)], [(3, 1), (3, 1)]):
        with pytest.raises(InvariantError):
            check_schedule(memory, scheduled, requests)
    with pytest.raises(InvariantError, match="scenario='P1D1'.*seed=91.*algorithm='first_fit'.*tentativa"):
        simulate([Request(1, 0, 1, 1)], "first_fit", 10, 0, "P1D1", 91,
                 attempt_sink=lambda row: (_ for _ in ()).throw(ValueError("falha injetada")))


@pytest.mark.parametrize("fields", [(0, 0, 1, 1), (1, -1, 1, 1), (1, 0, 0, 1), (1, 0, 1, 0), (1, 0, 1.5, 1)])
def test_invalid_request(fields):
    with pytest.raises(ValueError):
        Request(*fields)


def test_trace_order_required():
    with pytest.raises(ValueError):
        simulate([Request(2, 0, 1, 1)], "first_fit", warmup=0)

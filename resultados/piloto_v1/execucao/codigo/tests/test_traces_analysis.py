import copy
import math

import pytest

from memsim.analysis import METRICS, aggregate, paired
from memsim.runner import batch, generate_traces, verify_traces
from memsim.storage import ROOT, load_config, read_json
from memsim.traces import generate, load_trace, save_trace, validate_trace


@pytest.fixture
def config():
    return load_config(ROOT / "configs/principal.json")


@pytest.mark.parametrize("scenario", ["P1D1", "P1D2", "P2D1", "P2D2", "P3D1", "P3D2"])
def test_reproducibility_support_and_independent_streams(config, scenario, tmp_path):
    config["requests"] = 200
    one, two = generate(config, scenario, 1), generate(config, scenario, 1)
    assert one == two
    assert one != generate(config, scenario, 2)
    validate_trace(one, config, scenario)
    path = tmp_path / "trace.csv"
    save_trace(path, one)
    assert load_trace(path) == one
    changed = copy.deepcopy(config)
    changed["sizes"]["P1"] = [16, 16]
    changed["sizes"]["P2"] = [1, 1]
    changed["sizes"]["P3"]["small_probability"] = 1
    assert [r.duration for r in generate(changed, scenario, 1)] == [r.duration for r in one]


def test_p3_proportion_not_forced(config):
    requests = generate(config, "P3D1", 1001)
    assert sum(r.size >= 220 for r in requests) != 1200


def test_aggregation_sd_missing_and_paired_direction():
    rows = []
    for seed, first, best in [(1, 10, 6), (2, 14, 12), (3, 18, 10)]:
        for algorithm, value in [("first_fit", first), ("best_fit", best)]:
            rows.append({"scenario": "P1D1", "seed": seed, "algorithm": algorithm,
                         **{m: value for m in METRICS}})
    rows[0]["dispersion_mean"] = None
    rows[1]["dispersion_mean"] = None
    aggregated = aggregate(rows)
    first = next(r for r in aggregated if r["algorithm"] == "first_fit" and r["metric"] == "acceptance_pct")
    assert first["mean"] == 14
    assert first["sd"] == 4  # DP amostral, não populacional nem erro padrão.
    diff, summary = paired(rows)
    entry = next(r for r in summary if r["metric"] == "acceptance_pct")
    assert entry["mean"] == pytest.approx(14 / 3)
    assert entry["sd"] == pytest.approx(math.sqrt(28 / 3))
    assert entry["unit"] == "p.p."
    d = next(r for r in summary if r["metric"] == "dispersion_mean")
    assert d["n_valid"] == 2 and d["n_pairs"] == 3
    assert any(r["difference"] is None for r in diff)


def test_missing_group_never_imputed_zero():
    rows = [{"scenario": "P1D1", "seed": 1, "algorithm": "first_fit", **{m: None for m in METRICS}}]
    assert all(r["mean"] is None and r["sd"] is None and r["n_valid"] == 0 for r in aggregate(rows))


def test_end_to_end_export_audit_and_protect_existing(config, tmp_path):
    from memsim.audit import audit_results
    config.update(requests=40, warmup=10, temporal_bin=5, seeds=[1], scenarios=["P1D1"])
    traces, output = tmp_path / "traces", tmp_path / "run"
    generate_traces(config, traces)
    batch(config, traces, output)
    assert read_json(output / "manifest.json")["completed_runs"] == 3
    audit_results(output, tmp_path / "audit")
    assert read_json(tmp_path / "audit/manifest.json")["runs"] == 3
    with pytest.raises(FileExistsError):
        batch(config, traces, output)
    with pytest.raises(FileExistsError):
        generate_traces(config, traces)
    path = traces / "P1D1/seed_0001.csv"
    path.write_text(path.read_text() + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Hash"):
        verify_traces(config, traces)


def test_failed_execution_never_publishes_valid_summary(config, tmp_path, monkeypatch):
    from memsim import runner
    config.update(requests=5, warmup=1, seeds=[1], scenarios=["P1D1"])
    traces, output = tmp_path / "traces", tmp_path / "failed"
    generate_traces(config, traces)

    def broken(*args, **kwargs):
        raise RuntimeError("violação de invariante injetada")

    monkeypatch.setattr(runner, "simulate", broken)
    with pytest.raises(RuntimeError, match="injetada"):
        batch(config, traces, output)
    assert read_json(output / "manifest.json")["status"] == "failed"
    assert not (output / "resumo_execucoes.csv").exists()
    assert not list(output.rglob("resumo.json"))
    assert list(output.rglob("*.parcial"))

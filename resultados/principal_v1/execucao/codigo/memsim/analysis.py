"""Agregação entre sementes e gráficos descritivos a partir das saídas."""

import itertools
import math
import os
import statistics
from collections import defaultdict
from pathlib import Path

from .policies import LABELS
from .storage import ROOT, now, read_csv, read_json, sha256, write_csv, write_json

METRICS = {
    "acceptance_pct": ("Atendimento por quantidade", "%"),
    "volume_pct": ("Atendimento por volume", "%"),
    "fragmentation_pct": ("Recusa por fragmentação", "%"),
    "space_pct": ("Recusa por espaço total", "%"),
    "occupancy_mean": ("Ocupação U", "fração"),
    "free_mean": ("Memória livre F", "unidades"),
    "largest_mean": ("Maior bloco B", "unidades"),
    "holes_mean": ("Número de blocos livres", "blocos"),
    "dispersion_mean": ("Dispersão D nos instantes válidos", "índice"),
    "dispersion_valid_count": ("Instantes com D válido", "instantes"),
    "dispersion_valid_fraction": ("Proporção com D válido", "fração"),
    "zero_free_count": ("Instantes com F=0", "instantes"),
    "zero_free_fraction": ("Proporção com F=0", "fração"),
    "search_mean": ("Esforço médio de busca", "blocos/tentativa"),
    "search_max": ("Máximo de busca de cada execução", "blocos"),
}
PAIRS = [("first_fit", "best_fit"), ("first_fit", "worst_fit"), ("best_fit", "worst_fit")]


def numeric(value):
    return None if value in (None, "") else float(value)


def descriptive(values):
    values = [v for v in values if v is not None]
    return {"n_valid": len(values), "mean": statistics.mean(values) if values else None,
            "sd": statistics.stdev(values) if len(values) >= 2 else None,
            "minimum": min(values) if values else None, "maximum": max(values) if values else None}


def aggregate(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row["scenario"], row["algorithm"]].append(row)
    output = []
    for (scenario, algorithm), group in sorted(groups.items()):
        if len({int(r["seed"]) for r in group}) != len(group):
            raise ValueError("Semente duplicada na agregação.")
        for metric, (_, unit) in METRICS.items():
            output.append({"scenario": scenario, "algorithm": algorithm, "metric": metric, "unit": unit,
                           "n_runs": len(group), **descriptive([numeric(r[metric]) for r in group])})
    return output


def paired(rows):
    indexed = {(r["scenario"], int(r["seed"]), r["algorithm"]): r for r in rows}
    if len(indexed) != len(rows):
        raise ValueError("Execuções duplicadas.")
    differences = []
    for scenario in sorted({r["scenario"] for r in rows}):
        for seed in sorted({int(r["seed"]) for r in rows if r["scenario"] == scenario}):
            for left, right in PAIRS:
                if (scenario, seed, left) not in indexed or (scenario, seed, right) not in indexed:
                    continue
                for metric, (_, unit) in METRICS.items():
                    a = numeric(indexed[scenario, seed, left][metric])
                    b = numeric(indexed[scenario, seed, right][metric])
                    differences.append({"scenario": scenario, "seed": seed,
                        "comparison": f"{left}_minus_{right}", "metric": metric,
                        "unit": "p.p." if unit == "%" else unit,
                        "difference": a - b if a is not None and b is not None else None})
    grouped = defaultdict(list)
    for row in differences:
        grouped[row["scenario"], row["comparison"], row["metric"], row["unit"]].append(row["difference"])
    summary = [{"scenario": s, "comparison": p, "metric": m, "unit": u, "n_pairs": len(values),
                **descriptive(values)} for (s, p, m, u), values in sorted(grouped.items())]
    return differences, summary


def fmt(value, digits=3):
    return "NA" if value is None else f"{value:.{digits}f}"


def markdown_table(headers, rows):
    return "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n" + "".join(
        "| " + " | ".join(str(x) for x in row) + " |\n" for row in rows)


def transient_table(temporal):
    grouped = defaultdict(list)
    for row in temporal:
        grouped[row["scenario"], int(row["seed"]), row["algorithm"]].append(row)
    out = []
    for (scenario, seed, algorithm), rows in sorted(grouped.items()):
        record = {"scenario": scenario, "seed": seed, "algorithm": algorithm}
        for name, start, end in (("early", 2000, 4000), ("late", 4000, 12000)):
            window = [r for r in rows if start <= int(r["bin_start"]) < end]
            for metric in ("acceptance_pct", "occupancy_mean", "dispersion_mean"):
                weight_key = "dispersion_valid_count" if metric == "dispersion_mean" else "n"
                valid = [(float(r[metric]), int(r[weight_key])) for r in window if r[metric] != ""]
                count = sum(n for _, n in valid)
                record[f"{metric}_{name}"] = sum(v * n for v, n in valid) / count if count else None
        for metric in ("acceptance_pct", "occupancy_mean", "dispersion_mean"):
            a, b = record[f"{metric}_early"], record[f"{metric}_late"]
            record[f"{metric}_late_minus_early"] = b - a if a is not None and b is not None else None
        out.append(record)
    return out


def plot_results(aggregated, temporal, config, output):
    # Diretório local evita escrita no perfil do usuário e dispensa interface gráfica.
    os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplconfig"))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                         "svg.fonttype": "none", "figure.facecolor": "white"})
    colors = {"first_fit": "#2166ac", "best_fit": "#d97706", "worst_fit": "#238443"}
    lookup = {(r["scenario"], r["algorithm"], r["metric"]): r for r in aggregated}
    scenarios = sorted({r["scenario"] for r in aggregated})
    algorithms = [a for a in LABELS if any(r["algorithm"] == a for r in aggregated)]
    output.mkdir()

    def save(fig, name):
        fig.savefig(output / f"{name}.png", dpi=170, bbox_inches="tight")
        fig.savefig(output / f"{name}.svg", bbox_inches="tight")
        plt.close(fig)

    specifications = [
        ("atendimento_quantidade", ["acceptance_pct"]),
        ("atendimento_volume", ["volume_pct"]),
        ("recusas", ["fragmentation_pct", "space_pct"]),
        ("ocupacao_dispersao", ["occupancy_mean", "dispersion_mean"]),
        ("esforco_busca", ["search_mean"]),
    ]
    for filename, metrics in specifications:
        fig, axes = plt.subplots(1, len(metrics), figsize=(7.2 * len(metrics), 4.9), squeeze=False)
        for ax, metric in zip(axes[0], metrics):
            width = 0.24
            for index, algorithm in enumerate(algorithms):
                entries = [lookup.get((s, algorithm, metric)) for s in scenarios]
                means = [r["mean"] if r and r["mean"] is not None else math.nan for r in entries]
                sds = [r["sd"] if r and r["sd"] is not None else 0 for r in entries]
                positions = [i + (index - (len(algorithms) - 1) / 2) * width for i in range(len(scenarios))]
                ax.bar(positions, means, width, yerr=sds, capsize=3, label=LABELS[algorithm], color=colors[algorithm])
            ax.set_xticks(range(len(scenarios)), scenarios)
            ax.set_title(METRICS[metric][0])
            ax.set_ylabel(METRICS[metric][1])
            ax.set_ylim(bottom=0)
            ax.grid(axis="y", alpha=0.2)
            ax.set_axisbelow(True)
        axes[0, 0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False)
        fig.suptitle("Médias por execução; barras de erro = desvio-padrão entre sementes", fontsize=11)
        fig.tight_layout(rect=(0, 0.04, 1, 0.94))
        save(fig, filename)

    illustrative = config["illustrative_seed"]
    for scenario in scenarios:
        fig, axes = plt.subplots(3, 1, figsize=(10, 8.5), sharex=True)
        for ax, metric in zip(axes, ["acceptance_pct", "occupancy_mean", "dispersion_mean"]):
            for algorithm in algorithms:
                selected = [r for r in temporal if r["scenario"] == scenario and int(r["seed"]) == illustrative and r["algorithm"] == algorithm]
                selected.sort(key=lambda r: int(r["bin_start"]))
                ax.plot([(int(r["bin_start"]) + int(r["bin_end"])) / 2 for r in selected],
                        [numeric(r[metric]) for r in selected], marker=".", color=colors[algorithm], label=LABELS[algorithm])
            ax.axvspan(0, config["warmup"], color="#dddddd", alpha=0.6)
            ax.axvline(config["warmup"], color="#555555", linestyle="--", linewidth=1)
            ax.set_ylabel(METRICS[metric][0].replace(" nos instantes válidos", ""))
            ax.grid(alpha=0.2)
        axes[0].legend(ncol=3, frameon=False)
        axes[-1].set_xlabel("Instante simulado; faixa cinza = aquecimento")
        fig.suptitle(f"{scenario} — semente {illustrative} definida previamente\nMédias em janelas de {config['temporal_bin']} chegadas; drenagem excluída")
        fig.tight_layout(rect=(0, 0, 1, 0.94))
        save(fig, f"serie_{scenario}_semente_{illustrative}")

    if config["seeds"] == [1001, 1002, 1003]:
        # Mostrar as três réplicas permite examinar tendências sem escolher uma curva.
        for scenario in scenarios:
            fig, axes = plt.subplots(3, 3, figsize=(15, 9), sharex=True, sharey="row")
            for column, algorithm in enumerate(algorithms):
                axes[0, column].set_title(LABELS[algorithm])
                for row_index, metric in enumerate(["acceptance_pct", "occupancy_mean", "dispersion_mean"]):
                    ax = axes[row_index, column]
                    for seed, linestyle in zip(config["seeds"], ["-", "--", ":"]):
                        selected = [r for r in temporal if r["scenario"] == scenario and r["algorithm"] == algorithm and int(r["seed"]) == seed]
                        selected.sort(key=lambda r: int(r["bin_start"]))
                        ax.plot([int(r["bin_start"]) + config["temporal_bin"] / 2 for r in selected],
                                [numeric(r[metric]) for r in selected], linestyle=linestyle, label=str(seed), color=colors[algorithm])
                    ax.axvline(config["warmup"], color="#555555", linestyle="--", linewidth=0.8)
                    ax.grid(alpha=0.2)
                    if column == 0:
                        ax.set_ylabel(METRICS[metric][0].replace(" nos instantes válidos", ""))
                axes[0, column].legend(title="Semente", frameon=False)
                axes[-1, column].set_xlabel("Instante simulado")
            fig.suptitle(f"Piloto {scenario} — todas as sementes; janelas de {config['temporal_bin']} chegadas")
            fig.tight_layout(rect=(0, 0, 1, 0.96))
            save(fig, f"piloto_todas_{scenario}")


def analyze_results(input_directory, output):
    directory, output = Path(input_directory), Path(output)
    manifest = read_json(directory / "manifest.json")
    if manifest["status"] != "complete":
        raise ValueError("A análise exige um lote concluído; lotes falhos não são resultados válidos.")
    if sha256(directory / "resumo_execucoes.csv") != manifest["summary_csv_sha256"] or sha256(directory / "series_temporais.csv") != manifest["temporal_csv_sha256"]:
        raise ValueError("Hash dos resumos ou séries foi alterado.")
    rows = read_csv(directory / "resumo_execucoes.csv")
    if len(rows) != manifest["completed_runs"]:
        raise ValueError("Quantidade de resumos inconsistente.")
    config = read_json(directory / "config.json")
    temporal = read_csv(directory / "series_temporais.csv")
    aggregated = aggregate(rows)
    differences, paired_summary = paired(rows)
    output.mkdir(parents=True, exist_ok=False)
    tables = output / "tabelas"
    tables.mkdir()
    write_csv(tables / "resumo_cenario_algoritmo.csv", aggregated)
    write_csv(tables / "diferencas_pareadas_por_semente.csv", differences,
              ["scenario", "seed", "comparison", "metric", "unit", "difference"])
    write_csv(tables / "diferencas_pareadas_resumo.csv", paired_summary,
              ["scenario", "comparison", "metric", "unit", "n_pairs", "n_valid", "mean", "sd", "minimum", "maximum"])
    write_csv(tables / "diagnostico_temporal.csv", transient_table(temporal))
    lookup = {(r["scenario"], r["algorithm"], r["metric"]): r for r in aggregated}
    combinations = sorted({(r["scenario"], r["algorithm"]) for r in rows})
    table_strings = {}
    sets = {"atendimento": ["acceptance_pct", "volume_pct", "fragmentation_pct", "space_pct"],
            "estado": ["occupancy_mean", "free_mean", "largest_mean", "holes_mean", "dispersion_mean"],
            "cobertura_D": ["dispersion_valid_count", "dispersion_valid_fraction", "zero_free_count", "zero_free_fraction"],
            "busca": ["search_mean", "search_max"]}
    for name, metrics in sets.items():
        table_rows = []
        for scenario, algorithm in combinations:
            cells = [scenario, LABELS[algorithm]]
            for metric in metrics:
                item = lookup[scenario, algorithm, metric]
                cells.append(f"{fmt(item['mean'])} ± {fmt(item['sd'])}")
            table_rows.append(cells)
        title = "Média ± desvio-padrão amostral entre execuções. NA indica ausência.\n\n"
        table_strings[name] = title + markdown_table(["Cenário", "Algoritmo"] + [f"{METRICS[m][0]} ({METRICS[m][1]})" for m in metrics], table_rows)
        (tables / f"{name}.md").write_text(table_strings[name], encoding="utf-8")
    (tables / "diferencas_pareadas.md").write_text(
        "Diferença = primeiro algoritmo menos segundo, por mesma semente e cenário.\n\n" +
        markdown_table(["Cenário", "Comparação", "Métrica", "Unidade", "Pares válidos", "Média", "DP"],
            [[r["scenario"], r["comparison"], r["metric"], r["unit"], r["n_valid"], fmt(r["mean"]), fmt(r["sd"])]
             for r in paired_summary]), encoding="utf-8")
    plot_results(aggregated, temporal, config, output / "graficos")
    is_full = len(rows) == 540 and config["seeds"] == list(range(1, 31))
    kind = "Coleta principal completa" if is_full else "Piloto" if config["seeds"] == [1001, 1002, 1003] else "Lote parcial explicitamente selecionado"
    report = [f"# Relatório descritivo da simulação\n\n{kind}: {len(rows)} execuções válidas, "
              f"{len({(r['scenario'], r['seed']) for r in rows})} rastros e {config['requests'] - config['warmup']} tentativas de coleta por execução. "
              f"Capacidade {config['capacity']}; aquecimento {config['warmup']}; drenagem verificada e excluída das médias.\n",
              "## Atendimento\n\n" + table_strings["atendimento"],
              "## Organização do espaço livre\n\n" + table_strings["estado"],
              "## Cobertura da dispersão\n\n" + table_strings["cobertura_D"],
              "## Busca\n\n" + table_strings["busca"]]
    report.append("O máximo de cada execução consta em `search_max`. A média desses máximos aparece na tabela de busca; "
                  "a coluna `maximum` do resumo agregado, para essa métrica, é o máximo global do grupo. "
                  "Essas três grandezas não são intercambiáveis.\n")
    report.append("## Comparações descritivas por cenário\n")
    for scenario in sorted({r["scenario"] for r in rows}):
        available = [a for a in LABELS if (scenario, a, "acceptance_pct") in lookup]
        report.append(f"**{scenario}.** " + "; ".join(
            f"{LABELS[a]}: {lookup[scenario, a, 'acceptance_pct']['mean']:.3f}% por quantidade, "
            f"{lookup[scenario, a, 'volume_pct']['mean']:.3f}% por volume e "
            f"{lookup[scenario, a, 'search_mean']['mean']:.3f} blocos examinados por tentativa" for a in available) + ".\n")
    report.append("## Diferenças pareadas e leitura\n\nAs diferenças são First Fit menos Best Fit, First Fit menos Worst Fit e "
        "Best Fit menos Worst Fit. Valores positivos indicam maior valor da métrica no primeiro algoritmo. Para atendimento isso "
        "significa mais atendimento; para recusas e busca, mais recusas ou mais blocos examinados. Ocupação e D exigem interpretação "
        "conjunta com atendimento e tamanhos. Diferenças de métricas em % são expressas em pontos percentuais. "
        "As tabelas preservam cada diferença por semente e o desvio-padrão das diferenças, não a diferença dos desvios-padrão.\n")
    report.append("## Método de agregação e limitações\n\nCada execução é resumida primeiro. Cada semente tem peso igual na média "
        "do cenário; o desvio-padrão é amostral (denominador n−1). Os eventos sucessivos compartilham o estado e não são tratados "
        "como observações independentes. Não foram realizados testes inferenciais nem calculados intervalos de confiança.\n\n"
        "D é definido somente quando F>0. Execuções sem D válido permanecem ausentes e são excluídas apenas da agregação dessa "
        "métrica; `n_valid` e `n_runs` expõem o denominador. Diferenças de D exigem ambos os valores presentes; caso contrário, "
        "o par permanece ausente. Um único valor não permite desvio-padrão amostral. Não se imputam zeros.\n\n"
        "D mede a distribuição do espaço livre e não uma fração definitivamente perdida. Blocos examinados medem somente a busca, "
        "não tempo de CPU. A demanda nominal de 62,5% em D1 e 93,75% em D2 é carga oferecida teórica. "
        "As distribuições são sintéticas, com tamanhos e permanências independentes, capacidade única e pedidos recusados descartados. "
        "Os conjuntos aceitos podem divergir entre políticas. Os resultados não representam aplicações reais nem estabelecem superioridade universal.\n\n"
        f"As séries ilustrativas usam a semente {config['illustrative_seed']}, definida antes da execução. As janelas temporais "
        f"têm {config['temporal_bin']} chegadas; servem à descrição e não são réplicas adicionais. "
        "A avaliação do aquecimento está no relatório específico do piloto. O artigo original não foi alterado.\n")
    (output / "relatorio_resultados.md").write_text("\n".join(report), encoding="utf-8")
    write_json(output / "manifest.json", {"status": "complete", "generated_at_utc": now(),
        "input": str(directory.resolve()), "input_manifest_sha256": sha256(directory / "manifest.json"),
        "runs": len(rows), "kind": kind, "error_bars": "desvio-padrão amostral entre sementes",
        "files": {p.relative_to(output).as_posix(): sha256(p) for p in sorted(output.rglob("*")) if p.is_file()}})
    print(f"Tabelas, gráficos PNG/SVG e relatório: {output}", flush=True)

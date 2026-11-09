"""Interface de linha de comando; execute python -m memsim --help."""

import argparse
import sys
from pathlib import Path

from .runner import batch, freeze, generate_traces, run_tests
from .storage import config_hash, load_config, read_json, source_digest


def main(argv=None):
    parser = argparse.ArgumentParser(description="Comparação descritiva de alocação contígua de memória")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("traces", "pilot", "run", "full", "freeze"):
        command = commands.add_parser(name)
        command.add_argument("--config", required=True, type=Path)
        command.add_argument("--out", required=True, type=Path)
        if name == "run":
            command.add_argument("--traces", required=True, type=Path)
            command.add_argument("--scenario")
            command.add_argument("--seed", type=int)
            command.add_argument("--algorithm", choices=["first_fit", "best_fit", "worst_fit"])
        if name == "full":
            command.add_argument("--frozen", required=True, type=Path)
        if name == "freeze":
            command.add_argument("--pilot", required=True, type=Path)
            command.add_argument("--assessment", required=True, type=Path)
    analyze = commands.add_parser("analyze")
    analyze.add_argument("--input", required=True, type=Path)
    analyze.add_argument("--out", required=True, type=Path)
    audit = commands.add_parser("audit")
    audit.add_argument("--input", required=True, type=Path)
    audit.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    if args.command == "analyze":
        from .analysis import analyze_results
        analyze_results(args.input, args.out)
        return
    if args.command == "audit":
        from .audit import audit_results
        audit_results(args.input, args.out)
        return
    config = load_config(args.config)
    if args.command == "traces":
        generate_traces(config, args.out)
    elif args.command == "freeze":
        freeze(config, args.pilot, args.assessment, args.out)
    elif args.command == "run":
        batch(config, args.traces, args.out, args.scenario, args.seed, args.algorithm)
    elif args.command in ("pilot", "full"):
        if args.command == "full":
            frozen = read_json(args.frozen / "manifest.json")
            if frozen["status"] != "frozen" or frozen["config_hash"] != config_hash(config) or frozen["code_hash"] != source_digest():
                raise ValueError("Configuração/código diferente do protocolo congelado.")
        elif config["seeds"] != [1001, 1002, 1003]:
            raise ValueError("Piloto exige sementes 1001, 1002 e 1003.")
        args.out.mkdir(parents=True, exist_ok=False)
        run_tests(args.out / "validacao")
        generate_traces(config, args.out / "rastros")
        batch(config, args.out / "rastros", args.out / "execucao",
              frozen=args.frozen if args.command == "full" else None)
        from .analysis import analyze_results
        analyze_results(args.out / "execucao", args.out / "analise")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, FileExistsError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        sys.exit(1)

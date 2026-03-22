"""Personica 실험 엔진 CLI 진입점.

사용법:
  python -m shipcheck.cli run configs/experiment_1.yaml
  python -m shipcheck.cli generate-personas configs/experiment_1.yaml
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def cmd_run(args: argparse.Namespace) -> None:
    """실험 실행."""
    from .runner.experiment import ExperimentRunner

    runner = ExperimentRunner(config_path=Path(args.config))
    output = runner.run()
    print(f"\n실험 완료. 결과: {output}")


def cmd_generate_personas(args: argparse.Namespace) -> None:
    """페르소나 배치 생성."""
    from .layer1_persona.generator import generate_experiment_personas

    config_path = Path(args.config)
    generate_experiment_personas(config_path)


def cmd_compare_g2(args: argparse.Namespace) -> None:
    """합성 리뷰 vs G2 리뷰 비교."""
    from .analysis.g2_compare import compare_g2_cli

    compare_g2_cli(
        run_dir_str=args.run_dir,
        g2_path_str=args.g2_path,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="shipcheck",
        description="Personica 페르소나 시뮬레이션 실험 엔진",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command")

    # run
    p_run = sub.add_parser("run", help="실험 실행")
    p_run.add_argument("config", help="실험 설정 YAML 경로")

    # generate-personas
    p_gen = sub.add_parser("generate-personas", help="페르소나 배치 생성")
    p_gen.add_argument("config", help="실험 설정 YAML 경로")

    # compare-g2
    p_cmp = sub.add_parser("compare-g2", help="합성 리뷰 vs G2 리뷰 비교")
    p_cmp.add_argument("run_dir", help="실험 결과 디렉토리 (예: runs/g2_validation_001)")
    p_cmp.add_argument("--g2-path", dest="g2_path", default=None, help="G2 리뷰 JSONL 경로 (생략 시 자동 탐색)")

    args = parser.parse_args()
    setup_logging(args.verbose)

    if args.command == "run":
        cmd_run(args)
    elif args.command == "generate-personas":
        cmd_generate_personas(args)
    elif args.command == "compare-g2":
        cmd_compare_g2(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

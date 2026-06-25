from __future__ import annotations

import argparse
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent


def parse_bool(value: str) -> bool:
    lowered = value.lower()
    if lowered in {"true", "1", "yes", "y"}:
        return True
    if lowered in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError(f"Expected a boolean value, got: {value}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Hugging Face trajectory measurements.")
    parser.add_argument("--model-name", default="gpt2", help="Hugging Face model name.")
    parser.add_argument("--prompts-path", default=str(PROJECT_ROOT / "datasets" / "prompts_clean.json"))
    parser.add_argument("--results-dir", default=str(PROJECT_ROOT / "results"))
    parser.add_argument("--output-dir", default=None, help="Output folder for this model run.")
    parser.add_argument("--max-new-tokens", type=int, default=48)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--do-sample", type=parse_bool, default=True)
    parser.add_argument("--angle-threshold-degrees", type=float, default=90.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--analysis-only",
        action="store_true",
        help="Load existing results.csv and regenerate summary/charts without running GPT-2.",
    )
    parser.add_argument(
        "--trajectory-structure-only",
        action="store_true",
        help="Compute trajectory structure metrics from existing results.csv and raw_internal_data.npz.",
    )
    parser.add_argument(
        "--compare-models",
        nargs="+",
        help="Compare two or more model output folders, e.g. results/gpt2 results/distilgpt2.",
    )
    parser.add_argument(
        "--search-invariants",
        nargs="+",
        help="Search existing model output folders for stable ratios, e.g. results/gpt2 results/distilgpt2.",
    )
    parser.add_argument(
        "--diagnostic-signals",
        nargs="+",
        help="Create a diagnostic signal report from model output folders.",
    )
    parser.add_argument(
        "--trajectory-monitor",
        nargs="+",
        help="Create a standalone trajectory monitor dashboard from model output folders.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir or args.results_dir

    if args.compare_models:
        from src.model_comparison import compare_model_results

        comparison_path = PROJECT_ROOT / "results" / "model_comparison_report.md"
        outputs = compare_model_results(args.compare_models, comparison_path)
        print("Model comparison completed.")
        print(f"Compared models: {', '.join(Path(path).name for path in args.compare_models)}")
        print(f"Saved report: {comparison_path}")
        print(f"Stability rows: {len(outputs['stability'])}")
        return

    if args.search_invariants:
        from src.invariant_search import run_invariant_search

        report_path = PROJECT_ROOT / "results" / "invariant_search_report.md"
        outputs = run_invariant_search(args.search_invariants, report_path)
        print("Invariant ratio search completed.")
        print(f"Compared models: {', '.join(Path(path).name for path in args.search_invariants)}")
        print(f"Saved report: {report_path}")
        print(f"Ranked ratios: {len(outputs['stability'])}")
        return

    if args.diagnostic_signals:
        from src.diagnostic_signals import run_diagnostic_signal_report

        report_path = PROJECT_ROOT / "results" / "diagnostic_signal_report.md"
        outputs = run_diagnostic_signal_report(args.diagnostic_signals, report_path)
        print("Diagnostic signal report completed.")
        print(f"Compared models: {', '.join(Path(path).name for path in args.diagnostic_signals)}")
        print(f"Saved report: {report_path}")
        print(f"Ranked metrics: {len(outputs['portable_scores'])}")
        return

    if args.trajectory_monitor:
        from src.trajectory_monitor import create_trajectory_monitor

        monitor = create_trajectory_monitor(args.trajectory_monitor, PROJECT_ROOT / "results")
        print("Trajectory monitor completed.")
        print(f"Saved HTML: {PROJECT_ROOT / 'results' / 'trajectory_monitor.html'}")
        print(f"Saved CSV: {PROJECT_ROOT / 'results' / 'trajectory_monitor.csv'}")
        print(f"Rows: {len(monitor)}")
        return

    if args.trajectory_structure_only:
        from src.trajectory_structure import run_trajectory_structure_analysis

        outputs = run_trajectory_structure_analysis(output_dir)
        print("Trajectory structure analysis completed.")
        print(f"Updated CSV: {Path(output_dir) / 'results.csv'}")
        print(f"Saved report: {Path(output_dir) / 'trajectory_structure_report.md'}")
        print(f"Category rows: {len(outputs['category_means'])}")
        return

    if args.analysis_only:
        from src.analysis import load_results_with_evaluation, run_statistical_analysis

        results_csv = Path(output_dir) / "results.csv"
        if not results_csv.exists():
            raise FileNotFoundError(f"Cannot run --analysis-only because {results_csv} does not exist.")

        frame = load_results_with_evaluation(output_dir, args.prompts_path)
        run_statistical_analysis(frame, output_dir)
        print(f"Analysis-only completed for {len(frame)} prompts.")
        print(f"Loaded CSV: {results_csv}")
        print(f"Saved summary: {Path(output_dir) / 'summary.md'}")
        print(f"Saved charts: {Path(output_dir) / 'charts'}")
        print(f"Saved analysis log: {Path(output_dir) / 'analysis.log'}")
        return

    from src.experiment import TrajectoryExperiment
    from src.utils import set_seed

    set_seed(args.seed)

    top_k = args.top_k if args.top_k > 0 else None
    experiment = TrajectoryExperiment(
        prompts_path=args.prompts_path,
        results_dir=output_dir,
        model_name=args.model_name,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        top_k=top_k,
        do_sample=args.do_sample,
        angle_threshold_degrees=args.angle_threshold_degrees,
    )
    frame = experiment.run()

    print(f"Completed {len(frame)} prompts.")
    print(f"Saved CSV: {output_dir}/results.csv")
    print(f"Saved JSON: {output_dir}/results.json")
    print(f"Saved raw internals: {output_dir}/raw_internal_data.npz")
    print(f"Saved charts: {output_dir}/charts")


if __name__ == "__main__":
    main()

"""Backward-compatible entry point for the documented data pipeline."""

from pipeline import acquire, prepare, validate


if __name__ == "__main__":
    acquire()
    prepare()
    report = validate()
    print(f"Created the participant dataset; {len(report['checks'])} validation checks passed.")

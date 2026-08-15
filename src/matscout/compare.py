"""Compare existing raw vs fit markdown files already saved on disk."""

from pathlib import Path

RAW_DIR = Path("data/raw")
FIT_DIR = Path("data/fit")


def compare_all():
    raw_files = sorted(RAW_DIR.glob("*.md"))

    if not raw_files:
        print(f"No files found in {RAW_DIR}")
        return

    for raw_path in raw_files:
        name = raw_path.stem  # filename without .md
        fit_path = FIT_DIR / f"{name}.md"

        raw_text = raw_path.read_text(encoding="utf-8")
        fit_text = fit_path.read_text(encoding="utf-8") if fit_path.exists() else ""

        raw_len = len(raw_text)
        fit_len = len(fit_text)

        has_density_raw = "density" in raw_text.lower()
        has_density_fit = "density" in fit_text.lower()

        status = "OK" if has_density_fit else "MISSING in fit"

        print(f"{name:25s} | raw: {raw_len:6d} chars | fit: {fit_len:6d} chars | "
              f"density in raw: {has_density_raw} | density in fit: {has_density_fit} ")


if __name__ == "__main__":
    compare_all()
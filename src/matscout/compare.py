"""Part 4 — compare raw_markdown vs fit_markdown across all five pages."""

import asyncio
from pathlib import Path

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
FIT_DIR = DATA_DIR / "fit"

PAGES = [
    ("aluminium_6061", "https://en.wikipedia.org/wiki/6061_aluminium_alloy"),
    ("carbon_fiber", "https://en.wikipedia.org/wiki/Carbon_fiber_reinforced_polymer"),
    ("e_glass", "https://en.wikipedia.org/wiki/E-glass"),
    ("epoxy", "https://en.wikipedia.org/wiki/Epoxy"),
    ("titanium", "https://en.wikipedia.org/wiki/Titanium"),
]

CONFIG = CrawlerRunConfig(
    markdown_generator=DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(
            threshold=0.48,
            threshold_type="fixed",
            min_word_threshold=5,
        )
    )
)


async def crawl_and_compare(crawler: AsyncWebCrawler, name: str, url: str) -> dict:
    result = await crawler.arun(url, config=CONFIG)

    raw = result.markdown.raw_markdown or ""
    fit = result.markdown.fit_markdown or ""

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    FIT_DIR.mkdir(parents=True, exist_ok=True)

    (RAW_DIR / f"{name}.md").write_text(raw, encoding="utf-8")
    (FIT_DIR / f"{name}.md").write_text(fit or raw, encoding="utf-8")

    return {
        "name": name,
        "raw_chars": len(raw),
        "fit_chars": len(fit),
        "kept_pct": (100 * len(fit) / len(raw)) if raw else 0,
    }


async def main():
    results = []
    async with AsyncWebCrawler() as crawler:
        for name, url in PAGES:
            stats = await crawl_and_compare(crawler, name, url)
            results.append(stats)
            print(f"{name}: raw={stats['raw_chars']} chars, "
                  f"fit={stats['fit_chars']} chars "
                  f"({stats['kept_pct']:.0f}% kept)")
            await asyncio.sleep(2)  # never hammer a server

    # summary table for LOG.md
    print("\n| Page | Raw chars | Fit chars | % kept |")
    print("|------|-----------|-----------|--------|")
    for r in results:
        print(f"| {r['name']} | {r['raw_chars']} | {r['fit_chars']} | {r['kept_pct']:.0f}% |")

    avg_kept = sum(r["kept_pct"] for r in results) / len(results)
    print(f"\nAverage kept across all pages: {avg_kept:.0f}%")


if __name__ == "__main__":
    asyncio.run(main())
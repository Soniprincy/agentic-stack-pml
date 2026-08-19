"""Part 4 — crawling real pages: URL in, clean markdown files out (raw + fit + cleaned)."""

import asyncio
import re
from pathlib import Path

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

RAW_DIR = Path("data/raw")
FIT_DIR = Path("data/fit")

PAGES = [
    # original required five
    ("aluminium_6061", "https://en.wikipedia.org/wiki/6061_aluminium_alloy"),
    ("carbon_fiber", "https://en.wikipedia.org/wiki/Carbon_fiber_reinforced_polymer"),
    ("e_glass", "https://en.wikipedia.org/wiki/E-glass"),
    ("epoxy", "https://en.wikipedia.org/wiki/Epoxy"),
    ("titanium", "https://en.wikipedia.org/wiki/Titanium"),
    # extension: ten more
    ("stainless_steel_304", "https://en.wikipedia.org/wiki/SAE_304_stainless_steel"),
    ("hdpe", "https://en.wikipedia.org/wiki/High-density_polyethylene"),
    ("polycarbonate", "https://en.wikipedia.org/wiki/Polycarbonate"),
    ("kevlar", "https://en.wikipedia.org/wiki/Kevlar"),
    ("magnesium_alloy", "https://en.wikipedia.org/wiki/Magnesium_alloy"),
    ("copper", "https://en.wikipedia.org/wiki/Copper"),
    ("silicon_nitride", "https://en.wikipedia.org/wiki/Silicon_nitride"),
    ("borosilicate_glass", "https://en.wikipedia.org/wiki/Borosilicate_glass"),
    ("nylon_6", "https://en.wikipedia.org/wiki/Nylon_6"),
    ("cast_iron", "https://en.wikipedia.org/wiki/Cast_iron"),
]

CONFIG = CrawlerRunConfig(
    markdown_generator=DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(
            threshold=0.48,
            threshold_type="fixed",
            min_word_threshold=1, # before 5
        )
    )
)


async def crawl_and_save(crawler: AsyncWebCrawler, name: str, url: str) -> tuple[str, str]:
    result = await crawler.arun(url, config=CONFIG)

    raw = result.markdown.raw_markdown or ""
    fit = result.markdown.fit_markdown or ""

    RAW_DIR.mkdir(parents=True, exist_ok=True) # parent:create missing folder is not exist, exist_ok: no error when folder already present
    FIT_DIR.mkdir(parents=True, exist_ok=True)

    raw_path = RAW_DIR / f"{name}.md"
    fit_path = FIT_DIR / f"{name}.md"

    raw_path.write_text(raw, encoding="utf-8")
    fit_path.write_text(fit, encoding="utf-8")

    print(f"Saved raw: {len(raw)} | fit: {len(fit)}")
    return raw, fit

################################### for part 7 ##################################################

async def crawl_page(url: str) -> str:
    """Crawl a single URL for the A2A agent (Part 7) — reuses crawl_and_save
    so the exact same CONFIG and crawl call is used everywhere in this file."""
    slug = re.sub(r"[^a-z0-9]+", "_", url.lower()).strip("_")[:50] or "a2a_request"
    async with AsyncWebCrawler() as crawler:
        raw, fit = await crawl_and_save(crawler, slug, url)
        return fit or raw

#################################################################################################


async def main():
    async with AsyncWebCrawler() as crawler:
        for name, url in PAGES:
            await crawl_and_save(crawler, name, url)
            await asyncio.sleep(2)  # never hammer a server


if __name__ == "__main__":
    asyncio.run(main())
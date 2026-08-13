"""Part 4 — crawling real pages: URL in, clean markdown file out."""

import asyncio
from pathlib import Path

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

DATA_DIR = Path("data")

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
            min_word_threshold=5,
        )
    )
)

async def crawl_and_save(crawler: AsyncWebCrawler, name: str, url: str) -> None:
    result = await crawler.arun(url, config=CONFIG) # before no config(pruning) just url

    DATA_DIR.mkdir(exist_ok=True)
    out_path = DATA_DIR / f"{name}.md"
    content = result.markdown.fit_markdown or result.markdown.raw_markdown
    out_path.write_text(content, encoding="utf-8")

    print(f"Saved {out_path} ({len(content)} chars)")


async def main():
    async with AsyncWebCrawler() as crawler:
        for name, url in PAGES:
            await crawl_and_save(crawler, name, url)
            await asyncio.sleep(2)  #before no sleep time, never hammer a server


if __name__ == "__main__":
    asyncio.run(main())
"""Quick test — run pipeline.py's extractor across the 5 required pages."""

import asyncio
from matscout.pipeline import run_pipeline

PAGES = [
    ("carbon_fiber", "https://en.wikipedia.org/wiki/Carbon_fiber_reinforced_polymer"),
    ("titanium", "https://en.wikipedia.org/wiki/Titanium"),
    ("stainless_steel_304", "https://en.wikipedia.org/wiki/SAE_304_stainless_steel"),
    ("magnesium_alloy", "https://en.wikipedia.org/wiki/Magnesium_alloy"),
    ("borosilicate_glass", "https://en.wikipedia.org/wiki/Borosilicate_glass"),
]


async def test_all():
    for name, url in PAGES:
        print(f"\n--- {name} ---")
        material = await run_pipeline(url)
        print(material.model_dump_json(indent=2))



if __name__ == "__main__":
    asyncio.run(test_all())
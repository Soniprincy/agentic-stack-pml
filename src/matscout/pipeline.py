"""Part 5 — LangChain: URL in → crawl → extract → validated Material out."""

import asyncio
import sys

from crawl4ai import AsyncWebCrawler
from langchain_ollama import ChatOllama

from matscout.models import Material

MODEL = "qwen2.5:3b"

async def run_pipeline(url: str) -> Material:
    # Step 1: crawl
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url)
        markdown_text = result.markdown.raw_markdown or ""

    # Step 2: extract with LangChain
    model = ChatOllama(model=MODEL, temperature=0,top_p=1.0, top_k=1, seed=42)
    extractor = model.with_structured_output(Material)
    material = extractor.invoke(f"Extract material properties from: {markdown_text}")

    # setting source url
    material.source_url = url
    return material


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run python -m matscout.pipeline <wikipedia_url>")
        sys.exit(1)

    url = sys.argv[1]
    material = asyncio.run(run_pipeline(url))
    print(material.model_dump_json(indent=2))


if __name__ == "__main__":
    main()


"""Part 6 — LangGraph: extract → check → retry loop (max 3 attempts)."""

import asyncio
import sys
from typing import TypedDict, Optional

from crawl4ai import AsyncWebCrawler
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END

from matscout.models import Material

MODEL = "qwen3:4b" #before "qwen2.5:3b"
MAX_ATTEMPTS = 3


class GraphState(TypedDict):
    markdown_text: str
    source_url: str
    material: Optional[Material]
    feedback: Optional[str]
    attempts: int
    status: str  # "good" | "bad" | "gave_up" | "pending"


def extract_node(state: GraphState) -> dict:
    """Ask the model for a Material. On retries, fold in the specific
    complaint from the last failed check instead of just repeating the prompt."""
    model = ChatOllama(model=MODEL, temperature=0)  
    extractor = model.with_structured_output(Material)

    prompt = f"Extract material properties from: {state['markdown_text']}"
    if state.get("feedback"):
        prompt += f"\n\nCorrection needed: {state['feedback']}"

    material = extractor.invoke(prompt)
    material.source_url = state["source_url"]

    return {
        "material": material,
        "attempts": state["attempts"] + 1,
    }


def check_node(state: GraphState) -> dict:
    """Verify density is present and physically plausible (0.1-25 g/cm3)."""
    material = state["material"]
    density = material.density_g_cm3
    tensile = material.tensile_strength_mpa # added in extension

    if density is None:
        return {"status": "bad", "feedback": "No density value was returned"}

    if density > 25:
        return {
            "status": "bad",
            "feedback": (
                f"You returned {density} g/cm3, denser than any known material "
                f"(osmium, the densest, is ~22.6 g/cm3) — you probably misread "
                f"the units or picked up the wrong number. Try again."
            ),
        }

    if density < 0.1:
        return {"status": "bad", "feedback": f"You returned {density} g/cm3, implausibly low for a solid material. Try again."}

    if tensile is None:
        return {"status": "bad", "feedback": "No tensile strength value was returned — re-read the text and find the tensile strength figure."}

    if tensile >= 10000:
        return {
            "status": "bad",
            "feedback": (
                f"You returned {tensile} MPa for tensile strength, far beyond any "
                f"known engineering material — you probably misread the units "
                f"(e.g. picked up a value in kPa or psi). Try again."
            ),
        }

    return {"status": "good"}


def route_after_check(state: GraphState) -> str:
    if state["status"] == "good":
        return "done"
    if state["attempts"] >= MAX_ATTEMPTS:
        return "give_up"
    return "retry"


def build_graph():
    graph = StateGraph(GraphState)
    graph.add_node("extract", extract_node)
    graph.add_node("check", check_node)
    graph.set_entry_point("extract")
    graph.add_edge("extract", "check")
    graph.add_conditional_edges(
        "check",
        route_after_check,
        {"done": END, "retry": "extract", "give_up": END},
    )
    return graph.compile()


async def run_graph_pipeline(url: str) -> GraphState:
    # Step 1: crawl (same as pipeline.py — inline, raw_markdown, no cleanup)
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url)
        markdown_text = result.markdown.raw_markdown or ""

    app = build_graph()
    initial_state: GraphState = {
        "markdown_text": markdown_text,
        "source_url": url,
        "material": None,
        "feedback": None,
        "attempts": 0,
        "status": "pending",
    }
    final_state = await app.ainvoke(initial_state)
    return final_state


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run python -m matscout.graph_pipeline <wikipedia_url>")
        sys.exit(1)

    url = sys.argv[1]
    final_state = asyncio.run(run_graph_pipeline(url))

    print(f"Status: {final_state['status']} (attempts: {final_state['attempts']})")
    print(final_state["material"].model_dump_json(indent=2))

    app = build_graph()
    print("\n--- Mermaid graph ---")
    print(app.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()
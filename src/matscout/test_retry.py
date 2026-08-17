# scratch test — not permanent
import asyncio
from matscout.graph_pipeline import build_graph

async def test_retry():
    app = build_graph()
    state = {
        "markdown_text": "This material has a density of 900000 g/cm3 and is very strong.",
        "source_url": "https://example.com/fake",
        "material": None,
        "feedback": None,
        "attempts": 0,
        "status": "pending",
    }
    final = await app.ainvoke(state)
    print(f"Final status: {final['status']}, attempts: {final['attempts']}")
    print(final["material"].model_dump_json(indent=2))

asyncio.run(test_retry())
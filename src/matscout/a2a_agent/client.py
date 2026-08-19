import asyncio
from uuid import uuid4

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import MessageSendParams, SendMessageRequest


async def main(url_to_crawl: str) -> None:
    base_url = "http://localhost:9001"

    async with httpx.AsyncClient(timeout=300.0) as httpx_client:

        # ── 1. DISCOVER ────────────────────────────────────────────
        # GET /.well-known/agent-card.json → the Agent Card (business card)
        print("[1] DISCOVER — fetching agent card...")
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)
        card = await resolver.get_agent_card()
        print(f"    name: {card.name}")
        print(f"    endpoint: {card.url}")

        # ── 2. CHECK ────────────────────────────────────────────────
        # Read its skills — can it do what we need?
        print("[2] CHECK — reading skills...")
        skill_ids = [s.id for s in card.skills]
        print(f"    skills offered: {skill_ids}")
        if "crawl_material_page" not in skill_ids:
            raise RuntimeError("Agent doesn't offer crawl_material_page — stopping.")
        print("    'crawl_material_page' is available")

        # ── 3. ASK ──────────────────────────────────────────────────
        # message/send — send the request
        print("[3] ASK — sending message/send request...")
        client = A2AClient(httpx_client=httpx_client, agent_card=card)
        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(
                message={
                    "role": "user",
                    "parts": [{"type": "text", "text": url_to_crawl}],
                    "messageId": uuid4().hex,
                }
            ),
        )
        response = await client.send_message(request)
        task = response.root.result
        print(f"    task id: {task.id}")

        # ── 4. TRACK ────────────────────────────────────────────────
        # A Task with an ID and a state: submitted → working → completed (or failed)
        print("[4] TRACK — task state:")
        print(f"    state: {task.status.state}")
        if task.status.state == "failed":
            fail_msg = task.status.message
            reason = (
                fail_msg.parts[0].root.text
                if fail_msg and fail_msg.parts
                else "no message"
            )
            print(f"    task failed — reason: {reason}")
            return

        # ── 5. COLLECT ──────────────────────────────────────────────
        # The result arrives as an Artifact
        print("[5] COLLECT — reading artifact...")
        artifact_text = task.artifacts[0].parts[0].root.text
        print(f"    artifact ({len(artifact_text)} chars):")
        print(f"    {artifact_text[:300]}...")


if __name__ == "__main__":
    import sys
    asyncio.run(
        main(sys.argv[1] if len(sys.argv) > 1 else "https://en.wikipedia.org/wiki/Titanium")
    )
import json
from uuid import uuid4

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import MessageSendParams, Part, SendMessageRequest, TaskState, TextPart
from a2a.utils import new_agent_text_message, new_task

from matscout.crawl import crawl_page


class CrawlerAgentExecutor(AgentExecutor):
    EXTRACTOR_URL = "http://localhost:9002"

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        task = context.current_task
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)

        await updater.update_status(
            TaskState.working,
            message=new_agent_text_message("Crawling page..."),
        )

        url = context.get_user_input().strip()
        try:
            markdown = await crawl_page(url)
        except Exception as e:
            await updater.update_status(
                TaskState.failed, message=new_agent_text_message(str(e))
            )
            return

        # ── hand off to the extractor agent ────────────────────────
        await updater.update_status(
            TaskState.working,
            message=new_agent_text_message("Handing off to extractor agent..."),
        )
        try:
            async with httpx.AsyncClient(timeout=120.0) as httpx_client:
                resolver = A2ACardResolver(
                    httpx_client=httpx_client, base_url=self.EXTRACTOR_URL
                )
                extractor_card = await resolver.get_agent_card()
                extractor_client = A2AClient(
                    httpx_client=httpx_client, agent_card=extractor_card
                )

                request = SendMessageRequest(
                    id=str(uuid4()),
                    params=MessageSendParams(
                        message={
                            "role": "user",
                            "parts": [{"type": "text", "text": markdown}],
                            "messageId": uuid4().hex,
                        }
                    ),
                )
                response = await extractor_client.send_message(request)
                extractor_task = response.root.result
                result_text = extractor_task.artifacts[0].parts[0].root.text

                result_dict = json.loads(result_text)
                result_dict["source_url"] = url
                result_text = json.dumps(result_dict)
        except Exception as e:
            await updater.update_status(
                TaskState.failed,
                message=new_agent_text_message(f"Extractor call failed: {e}"),
            )
            return

        await updater.add_artifact(
            parts=[Part(root=TextPart(text=result_text))],
            name="extracted_material",
        )
        await updater.complete()

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError
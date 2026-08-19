import asyncio

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import Part, TaskState, TextPart
from a2a.utils import new_agent_text_message, new_task

from matscout.extract import extract_material


class ExtractorAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        task = context.current_task
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)

        await updater.update_status(
            TaskState.working,
            message=new_agent_text_message("Extracting material properties..."),
        )

        markdown_text = context.get_user_input()
        try:
            material = await asyncio.to_thread(
                extract_material, markdown_text, ""
            )
        except Exception as e:
            await updater.update_status(
                TaskState.failed,
                message=new_agent_text_message(str(e)),
            )
            return

        await updater.add_artifact(
            parts=[Part(root=TextPart(text=material.model_dump_json()))],
            name="extracted_material",
        )
        await updater.complete()

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError
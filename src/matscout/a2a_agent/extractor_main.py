import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from matscout.a2a_agent.extractor_agent import ExtractorAgentExecutor

skill = AgentSkill(
    id="extract_material_properties",
    name="Extract material properties",
    description="Takes crawled markdown and returns validated density/strength JSON.",
    tags=["extraction", "materials"],
)

agent_card = AgentCard(
    name="MatScout Extractor Agent",
    description="Extracts structured material properties from markdown.",
    url="http://localhost:9002/",
    version="1.0.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(),
    skills=[skill],
)

request_handler = DefaultRequestHandler(
    agent_executor=ExtractorAgentExecutor(),
    task_store=InMemoryTaskStore(),
)

app = A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler)

if __name__ == "__main__":
    uvicorn.run(app.build(), host="0.0.0.0", port=9002)
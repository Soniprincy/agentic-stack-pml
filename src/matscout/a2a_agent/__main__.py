import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from matscout.a2a_agent.crawler_agent import CrawlerAgentExecutor

skill = AgentSkill(
    id="crawl_material_page",
    name="Crawl a materials web page",
    description="Fetches a URL and returns cleaned markdown of the page content.",
    tags=["crawling", "materials"],
    examples=["https://en.wikipedia.org/wiki/Titanium"],
)

agent_card = AgentCard(
    name="MatScout Crawler Agent",
    description="Crawls material data pages and returns clean markdown.",
    url="http://localhost:9001/",
    version="1.0.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(),
    skills=[skill],
)

request_handler = DefaultRequestHandler(
    agent_executor=CrawlerAgentExecutor(),
    task_store=InMemoryTaskStore(),
)

app = A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler)

if __name__ == "__main__":
    uvicorn.run(app.build(), host="0.0.0.0", port=9001)
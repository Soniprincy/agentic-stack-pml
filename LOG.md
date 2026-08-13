## Part 1 — Setup

**Done:** Installed uv, created the matscout project, added the needed
packages (ollama, pydantic, httpx, crawl4ai). Ran crawl4ai-setup and
crawl4ai-doctor — both worked fine. Installed Ollama and pulled the
qwen2.5:3b model (switched from 4b because it was too slow).

**Learned:** Crawl4AI needs an extra setup step (crawl4ai-setup) on top of
just installing it with uv — it installs a browser in the background.

**Time:** ~1h


## Part 2 — Python + local model

**Done:** Wrote ask.py to send a question to Ollama and print the answer.
Did it two ways — first using the `ollama` package, then again using
`httpx` to call the API directly. Both work and give a proper answer.

**Learned:** The `ollama` package is really just a shortcut — underneath,
it's sending the same kind of request that httpx sends manually.

**Time:** ~1h


## Part 3 — Structured output

**Done:** Made a Material class using Pydantic (name, density, tensile
strength, source URL). Sent this schema to Ollama using `format=`, which
forces the model to reply in that exact JSON shape. Parsed the reply with
Pydantic and got a clean object back. Tested it on 5 paragraphs about
different materials. I tested my sanity_check() by giving the model a made-up
sentence saying a material has a density of 4,500,000 g/cm3, the extract_material
return its a "valid" object but sanity_check correctly caught it and flag 
it as too high. Set temperature = 0 to avoid different answers. — all worked.

**Learned:** Even though the model always replies in the right JSON shape,
it can still make up wrong numbers. I tested this by giving it a fake
huge density value, and it accepted it without complaint — so I added a
simple check that rejects anything above 25 g/cm3 (nothing is that dense).

**Time:** ~1.5h
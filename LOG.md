## Part 1 — Setup

**Done:** Installed uv, created the matscout project, added the needed
packages (ollama, pydantic, httpx, crawl4ai). Ran crawl4ai-setup and
crawl4ai-doctor — both worked fine. Installed Ollama and pulled the
qwen2.5:3b model (switched from 4b because it was too slow).

**Learned:** Crawl4AI needs an extra setup step (crawl4ai-setup) on top of
just installing it with uv — it installs a browser in the background.

**stuck on:** ollama installation, i have esser free RAM so contacted PML team, now using 4b and 3b model.

**Time:** ~2h


## Part 2 — Python + local model

**Done:** Wrote ask.py to send a question to Ollama and print the answer.
Did it two ways — first using the `ollama` package, then again using
`httpx` to call the API directly. Both work and give a proper answer.

**Learned:** The `ollama` package is really just a shortcut — underneath,
it's sending the same kind of request that httpx sends manually. usually larger model tales time to execute but give much deeper and better answer than smaller model, we can se some repetitions and basic answers in small model. as i run ollama list, i can see 3 models 8b, 3b and 4b.

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
it can still make up wrong numbers. i also tried changing density value to character-number (two,three), then it give "model output failed validation...". I tested this by giving it a fake huge density value, and it accepted it without complaint — so I added a
simple check that rejects anything above 25 g/cm3 (nothing is that dense).

**Time:** ~1.5h

## Part 4 — crawling

**Done** created a crawl.py file where i web scrap using crawl4ai. created a async model to crawl from website using asyncwebcrawler and pruning parameter. Feed five website to my model. Created a compare.py file to compare raw and transformed/fit markdown files to check how many data we kept and remove. then i fed 10 more websites to crawl with asyncio.sleep(2), that waits for 2 second for every website to crawl. yes async/await is important because real browser are slow and heavy.

**Learned** firstly i tried crawn_and_save without pruning parameter, then it give full raw file as transformed, but when i applied pruning factor, it prune all unnecessary noises.

**Didn't understand:** fit_markdown on the 304 stainless steel page dropped the tensile yield strength and density values entirely — they show up as empty in the prose ("The density is , and...") even though the infobox numbers survived. Checked raw_markdown and confirmed the values are present there but not in fit. Pruning is a density/link-ratio heuristic with no awareness that a specific span holds a needed number — it can silently drop data as easily as it drops boilerplate.
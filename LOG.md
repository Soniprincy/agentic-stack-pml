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

**Done** created a crawl.py file where i web scrap using crawl4ai. created a async model to crawl from website using asyncwebcrawler. Feed five website to my model. Created and compare.py file to compare raw and transformed/fit markdown files to check how many data we kept and remove. then i fed 10 more websites to crawl with asyncio.sleep(2), that runs and stop for 2 second so that we can not deceted as fraud to the website. yes async/await is important because real browser are slow and heavy.

**Learned** firstly i tried crawl_and_save without pruning parameter, then it give full raw file as transformed, but when i applied pruning factor, it prune all unnecessary noises. now i under stand why i am facing vanishing number issues because i am fixing my min_word_threshold=5, now tried 4,3,2, then 1 works perfectly fine. 

**Didn't understand:** fit_markdown on the 304 stainless steel page dropped the tensile yield strength and density values entirely — they show up as empty in the prose ("The density is , and...") even though the infobox numbers survived. Checked raw_markdown and confirmed the values are present there but not in fit. i applied many techniques using clause but do not resolve this problem. Now under stand the problem of vanishing off.

## Part 5 — Langchain

**Done** firstly create a file pipeline, then write a code which uses langchain wrapper for ollama, crawl -> extract -> validate that return values in material format. then run the code with steel website that gives good answer. create a test.pipeline to test my code on 5 material pages/websites.
it works better in my 5 pages.

**Extension** — did LangChain make this easier, or just add a layer?
for this assignment, it is just add a layer, real work was what we do earlier.
it replaces 15 lines of httpx, pydantric code in part 3, that become 2 lines of code
it wins on line count, i can easily under stand it but i already build and understand manual part also. it gives different answers in different runs (sometime null).

**Conclusion:** not worth the extra dependency for a single-model,
single-call pipeline like this one — the manual Part 3 version was
already clear and I understood every line of it. I'd reconsider if this
pipeline needed to support multiple model providers.

**Learned:** Assignment flagged that a lot of LangChain material online
is outdated post-1.0. if any doubt docs.langchain.com before
trusting any tutorial in later parts.

## Part 6 — Langgraph

**Done** firstly created a file named graph_pipeline where i write a pipeline with langgraph. Extract -> check -> route_after_check, where conditions are set, if density is none, more than 25 and less than 0.1 gives status bad, retry if attempts < 3 else return good, end the process. created a file test_retry.py for a quick checkup. Returns try again if density is more than 900000g/cm**3. capped it at 3 attempts. Also return mermaid graph in our output. then i add a tensile validation step, is tensite present and under 10000.
Added a third validation in check: is tensile_strength_mpa present and under 10,000 MPa? Same pattern as the density check — specific feedback on failure, folded back into the next extract attempt.

**Learned** when i run my code with small model "quen2.5:3b" it return output as bad, sometimes capture density sometime not. but as i run "qwen3:4b" it resolve this problem.

- URL: (page that failed first try)
- Attempt 1: model returned density_g_cm3 = bad value → check failed: 
- Attempt 2: model returned density_g_cm3 = correct value → check passed.

## Part 7 — A2A: agents talking to each other

## Part 7 — A2A

**Done:**
- Started from the provided a2a-starter repository.
- Converted GreetingAgent into MaterialCrawlerAgent.
- Added Crawl4AI to crawl Wikipedia material pages.
- Added `crawl_material_page` to the Agent Card.
- Connected the crawler through MaterialCrawlerExecutor.
- Client successfully completed Discover → Check → Ask → Track → Collect.
- Received the crawled Wikipedia content as an A2A Artifact.

**Task ID:**
62a24b2c-5713-4f23-8817-c11813df981d

**Final state:**
completed

**Done:**
- Created a second A2A agent for material extraction.
- Started the extractor agent on port 9002.
- Published an Agent Card with the `extract_material` skill.
- Modified the crawler agent to discover the extractor through its Agent Card.
- The crawler handed the Crawl4AI Markdown to the extractor using A2A.
- The extractor received the Markdown and returned an A2A Artifact.

**Test URL:**
https://en.wikipedia.org/wiki/Aluminium

**Result:**
Extractor Agent received the material page.
Markdown length: 358947 characters.

**Still unclear:**
- How A2A handles task updates internally.
- How Artifact Parts are represented.

**Time:** ~ 1 day

-------------------------------------------------------------------------------------

## Part 8 – Work Completed

* Updated the extractor.py file.
* Created a Material model using **Pydantic**.
* Added material details such as:

  * Material name
  * Density
  * Tensile strength
* Made some fields optional to handle missing data.
* Used **Ollama AsyncClient** to connect with the local LLM.
* Implemented asynchronous processing for material extraction.
* Converted the extracted information into a structured format.
* Used Pydantic validation to make the output more organized and reliable.
* Tested the updated code.
* Learned how **Pydantic** and **AsyncClient** can be used together for structured data extraction.

### Status

* **Part 8 Completed Successfully.**

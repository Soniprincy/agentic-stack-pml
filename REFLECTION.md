 What clicked / what's still fuzzy?

-- i understand till landchain and langgraph, but i solve by code but i am still stuck in my head about "A2A : agent talking to each other" part. like how a2a work backend.

 Look at your earliest code against your final code. What would you change about the early version
now?

-- No error handling — ask.py had no raise_for_status(), no try/except, timeout=None as a workaround for hangs. I'd add real error handling from day one instead of adding it only by part 3.
--Dead code left in the file — three implementations (ollama package, raw httpx, argparse) sat in one file, two just commented out. I'd delete and split into separate modules earlier, like I eventually did with models.py/extract.py.
--Wasted time on model-size trial-and-error — tried 8b → 4b → 7b, each hanging the laptop, before settling on qwen2.5:3b. I'd go straight to the small model given the known 5.85GB RAM constraint.
--No output validation — ask.py trusted whatever the model returned; sanity checks (density/tensile plausibility) and the retry-with-feedback loop only showed up by part 3/6.

 Where did AI assistance help, and where did it mislead you?

Where it helped:
--Explaining unfamiliar concepts fast — LangGraph state machines, A2A's Agent Card/Task lifecycle, with_structured_output — probably saved the most time here since these were all new to you.
--Debugging the fit_markdown returning empty issue in part 4 — if AI helped you trace it to the missing PruningContentFilter config, that's a concrete win.
Where it misled you:
--make me confuse in part 7 and 8, i started creating A2A from scratch, which results in more confusion.

----------------------- part 8 ------------------------------------

4. The injection question from Part 8, half a page

Injection and Dependency Management

In Part 8, dependency injection was used to manage the different components of the agentic application in a clean and modular way. Instead of creating dependencies directly inside every function or class, the required components were provided from outside. This approach makes the system easier to maintain, test, and modify.

For example, components such as the Ollama client, extraction service, or agent configuration can be injected where required. This reduces tight coupling between different parts of the application. If a model, configuration, or service needs to be changed later, it can be replaced without significantly modifying the core application logic.

Dependency injection also improves testing because mock objects or alternative implementations can be provided during testing. Overall, using dependency injection in the project helped create a more modular, flexible, and maintainable agentic system.
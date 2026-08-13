## 2026-08-13

**Done:** Part 2 (Python + local model) complete. Wrote ask.py two ways:
first using the ollama package, then redone with httpx hitting
http://localhost:11434/api/chat directly. Both produce a sensible answer
for `uv run python ask.py "what is carbon fibre"`.

**Didn't understand at first:** What the ollama package was actually doing
under the hood — rewriting the same call with raw httpx made it clear it's
just a wrapper around a POST request to /api/chat with a messages array,
same shape as any REST API call from JS.

**Watch out (caught this myself):** Ollama has to actually be running as a
background process before either script works — `ollama list` confirms
which models are pulled locally.

**Time:** ~1h

## 2026-08-13 (Part 3)

**Done:** Part 3 (structured output) complete. Defined a Material Pydantic
model. extract_material() sends format=Material.model_json_schema() to
Ollama and parses the response with Material.model_validate_json(). Ran
across all five test paragraphs (aluminium 6061, carbon fiber, E-glass,
epoxy, titanium) — all validated into clean Material objects. Set
temperature=0 for repeatable output.

**Didn't understand at first:** Assumed format= alone was enough to trust
the output. Tested this by feeding a paragraph with a fabricated density
(4,500,000 g/cm3) — the model returned it as a perfectly valid Material
object; schema validation passed with no complaint. That's the gap
sanity_check() is for — valid JSON shape doesn't mean correct data.

**Question:** At what point should this kind of plausibility checking move
into the schema itself instead of a separate
function? 

**Time:** ~1.5h
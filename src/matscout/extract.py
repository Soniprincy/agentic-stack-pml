"""Part 3 — structured output: paragraph in, validated Material out."""

import httpx
from pydantic import ValidationError

from matscout.models import Material

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:3b" # 4b model takes to long to respond

PARAGRAPHS = [
    ("Aluminium 6061 is a precipitation-hardened alloy with magnesium and "
     "silicon as its main alloying elements. Its density is approximately "
     "2.70 g/cm3, and its ultimate tensile strength in the T6 temper is "
     "around 310 MPa.",
     "https://en.wikipedia.org/wiki/6061_aluminium_alloy"),

    ("Carbon fiber reinforced polymer is a composite of carbon fibers in a "
     "polymer matrix. Density is roughly 1.55 g/cm3, and tensile strength "
     "of the fibers alone can reach 3500 MPa.",
     "https://en.wikipedia.org/wiki/Carbon_fiber_reinforced_polymer"),

    ("E-glass fiberglass has a density of about 2.58 g/cm3 and a tensile "
     "strength around 3400 MPa for individual filaments.",
     "https://en.wikipedia.org/wiki/E-glass"),

    ("Cured epoxy resin typically has a density between 1.1 and 1.4 g/cm3 "
     "and a tensile strength in the range of 40 to 90 MPa.",
     "https://en.wikipedia.org/wiki/Epoxy"),

    ("Titanium has a density of 4.51 g/cm3 and, in common alloy form, a "
     "tensile strength of roughly 900 MPa.",
     "https://en.wikipedia.org/wiki/Titanium"),
]


def extract_material(text: str, source_url: str, model: str = MODEL) -> Material:
    prompt = (
        "Extract the material name, density (g/cm3), and tensile strength "
        f"(MPa) from this text. Use null for anything not mentioned.\n\n{text}"
    )

    response = httpx.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "format": Material.model_json_schema(),   # constrains token output
            "options": {"temperature": 0},              # 0 for same answer
            "stream": False,
        },
        timeout=None,
    )
    response.raise_for_status()
    content = response.json()["message"]["content"]

    # print(f'checking output type : {type(content)}')
    # print(f'this is to check the type of output : {content}')

    try:
        material = Material.model_validate_json(content)
    except ValidationError as e:
        raise ValueError(f"Model output failed validation: {e}\nRaw: {content}") from e

    material.source_url = source_url  
    return material


def sanity_check(material: Material) -> list[str]:
    """Extension: nothing is denser than osmium (~22.6 g/cm3)."""
    problems = []
    if material.density_g_cm3 is not None and material.density_g_cm3 > 25:
        problems.append(f"density {material.density_g_cm3} g/cm3 exceeds physical limit")
    return problems


if __name__ == "__main__":
    for text, url in PARAGRAPHS:
        m = extract_material(text, url)
        print(m.model_dump_json(indent=2))
        for p in sanity_check(m):
            print(f"  ⚠ {p}")
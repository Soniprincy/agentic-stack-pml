from pydantic import BaseModel


class Material(BaseModel):
    name: str
    density_g_cm3: float | None = None
    tensile_strength_mpa: float | None = None
    source_url: str
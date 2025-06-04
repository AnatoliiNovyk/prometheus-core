 import yaml
from pathlib import Path

ARCHETYPES_PATH = Path(__file__).parent.parent / "presets" / "archetypes.yaml"

def load_archetypes():
    with open(ARCHETYPES_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return {a['name']: a for a in data['archetypes']}

_ARCHETYPES_CACHE = None

def load_archetype(name):
    global _ARCHETYPES_CACHE
    if _ARCHETYPES_CACHE is None:
        _ARCHETYPES_CACHE = load_archetypes()
    archetype = _ARCHETYPES_CACHE.get(name)
    if archetype is None:
        raise ValueError(f"Архетип '{name}' не найден")
    return archetype

import yaml
from pathlib import Path

ARCHETYPES_PATH = Path(__file__).parent.parent / "presets" / "archetypes.yaml"

class ArchetypeValidationError(Exception):
    pass

def validate_archetype(data):
    required_keys = {"name", "description", "personality"}
    personality_keys = {"honesty", "ethics", "language", "aggression"}

    for archetype in data.get("archetypes", []):
        missing = required_keys - archetype.keys()
        if missing:
            raise ArchetypeValidationError(f"Архетип '{archetype.get('name', '<unknown>')}' пропущены поля: {missing}")

        personality = archetype.get("personality", {})
        missing_personality = personality_keys - personality.keys()
        if missing_personality:
            raise ArchetypeValidationError(
                f"Архетип '{archetype['name']}' в personality пропущены поля: {missing_personality}"
            )

def load_archetypes():
    try:
        with open(ARCHETYPES_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        validate_archetype(data)
        return {a['name']: a for a in data['archetypes']}
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл архетипов не найден по пути: {ARCHETYPES_PATH}")
    except yaml.YAMLError as e:
        raise RuntimeError(f"Ошибка при разборе YAML: {e}")
    except ArchetypeValidationError as ve:
        raise RuntimeError(f"Ошибка валидации архетипов: {ve}")

_ARCHETYPES_CACHE = None

def load_archetype(name):
    global _ARCHETYPES_CACHE
    if _ARCHETYPES_CACHE is None:
        _ARCHETYPES_CACHE = load_archetypes()
    archetype = _ARCHETYPES_CACHE.get(name)
    if archetype is None:
        raise ValueError(f"Архетип '{name}' не найден")
    return archetype

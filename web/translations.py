"""
Translations system for the web app.
Loads EN/AR translations from JSON — mirrors the Next.js i18n setup.
"""
import json
from pathlib import Path

_TRANSLATIONS = {}
_BASE = Path(__file__).resolve().parent.parent / "frontend_source" / "messages"


def _load():
    global _TRANSLATIONS
    if _TRANSLATIONS:
        return
    for lang in ("en", "ar"):
        fpath = _BASE / f"{lang}.json"
        if fpath.exists():
            with open(fpath, "r", encoding="utf-8") as f:
                _TRANSLATIONS[lang] = json.load(f)
        else:
            _TRANSLATIONS[lang] = {}


def reload_translations():
    """Force-reload translations from disk (useful during development)."""
    global _TRANSLATIONS
    _TRANSLATIONS = {}
    _load()


class TranslationProxy:
    """
    Dot-access wrapper for nested translation dicts.
    Usage in templates: {{ t.home.heroTitle }}
    """

    def __init__(self, data: dict):
        self._data = data

    def __getattr__(self, key):
        val = self._data.get(key)
        if isinstance(val, dict):
            return TranslationProxy(val)
        if val is not None:
            return val
        return ""

    def __str__(self):
        return str(self._data) if isinstance(self._data, str) else ""

    def __contains__(self, item):
        return item in self._data

    def __getitem__(self, key):
        val = self._data.get(key)
        if isinstance(val, dict):
            return TranslationProxy(val)
        if val is not None:
            return val
        return ""


def get_translations(lang: str) -> TranslationProxy:
    _load()
    data = _TRANSLATIONS.get(lang, _TRANSLATIONS.get("en", {}))
    return TranslationProxy(data)

from flask import current_app


def auto_complete(prompt: str, all_eng_words: list[str]) -> list[str]:
    if current_app.config["enable_autocomplete"]:
        return [word for word in all_eng_words if word.startswith(prompt)][:10]
    else:
        return []

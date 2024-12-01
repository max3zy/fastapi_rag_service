from app.utils.preprocess.preprocess_regex import (
    TABS_REGEXP,
    TAGS_REGEXP,
    SYMBOLS_WITHDASH_REGEXP,
    SYMBOLS_REGEXP,
    SPACES_REGEXP,
    HTML_REGEXP
)


def text_cleanup_preprocessor(text: str, keep_dash: bool = False) -> str:
    result = str(text)
    result = result.lower()
    result = result.replace("ё", "е")
    result = TABS_REGEXP.sub(" ", result)
    result = TAGS_REGEXP.sub(" ", result)
    if keep_dash:
        result = SYMBOLS_WITHDASH_REGEXP.sub(" ", result)
    else:
        result = SYMBOLS_REGEXP.sub(" ", result)
    result = result.strip()
    result = SPACES_REGEXP.sub(" ", result)
    return result


def clean_html(text: str) -> str:
    """
    Удаление html-тегов (производится перед text_cleanup_preprocessor,
    если текст может содержать теги)
    """
    text = HTML_REGEXP.sub(" ", text)
    return SPACES_REGEXP.sub(" ", text).strip()
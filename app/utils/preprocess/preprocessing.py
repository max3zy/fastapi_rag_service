import re
from re import Match
from typing import Optional

import markdown

from app.utils.constants import (
    DOCUMENT_SEPARATOR,
    EMPTY_STRING,
    SPACE,
    STRING_SEPARATOR,
)
from app.utils.preprocess.preprocess_regex import (
    HTML_REGEXP,
    REGEX_BETWEEN_LI_TAGS,
    REGEX_BOLD_TAGS,
    REGEX_CHAR_AFTER_LI_FIX,
    REGEX_MD_FIX,
    REGEX_P_TAGS,
    REGEX_QUOT_CLOSE,
    REGEX_QUOT_OPEN,
    SPACES_REGEXP,
    SYMBOLS_REGEXP,
    SYMBOLS_WITHDASH_REGEXP,
    TABS_REGEXP,
    TAGS_REGEXP,
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


def clean_text_from_spec_simbols(text: str) -> Optional[str]:
    return re.sub(r"(\.\n)|(\. \n)|;\n", "\n", text.strip())


def remove_p_tags_between_li(answer: str) -> str:
    result = REGEX_BETWEEN_LI_TAGS.sub(
        lambda m: REGEX_P_TAGS.sub(EMPTY_STRING, m.group(0)), answer
    )
    return SPACE.join(
        [x.strip() for x in result.split(SPACE) if x != EMPTY_STRING]
    )


def fix_char_after_li(found_li: Match) -> str:
    result = found_li.group()
    return result[:-1] + result[-1].upper()


def answer_postprocessing(answer: str) -> str:
    answer = markdown.markdown(
        REGEX_MD_FIX.sub(
            DOCUMENT_SEPARATOR,
            clean_text_from_spec_simbols(answer),
        )
    ).replace(STRING_SEPARATOR, EMPTY_STRING)
    answer = REGEX_BOLD_TAGS.sub(EMPTY_STRING, answer)
    answer = remove_p_tags_between_li(answer)
    answer = REGEX_QUOT_CLOSE.sub("»", REGEX_QUOT_OPEN.sub("«", answer))
    answer = REGEX_CHAR_AFTER_LI_FIX.sub(fix_char_after_li, answer)
    return answer

import re

TABS_REGEXP_TEXT = r"[\n\t\r]+"
TABS_REGEXP = re.compile(TABS_REGEXP_TEXT)
TAGS_REGEXP_TEXT = r"(\<(/?[^>]+)>)"
TAGS_REGEXP = re.compile(TAGS_REGEXP_TEXT)
SYMBOLS_REGEXP_TEXT = r"[^a-zа-я0-9]"
SYMBOLS_REGEXP = re.compile(SYMBOLS_REGEXP_TEXT)
SYMBOLS_WITHDASH_REGEXP_TEXT = r"(\s\-\s)|(\-\s)|(\s\-)|([^a-zа-я0-9\-])"
SYMBOLS_WITHDASH_REGEXP = re.compile(SYMBOLS_WITHDASH_REGEXP_TEXT)
SPACES_REGEXP_TEXT = r"\s+"
SPACES_REGEXP = re.compile(SPACES_REGEXP_TEXT)
HTML_REGEXP_TEXT = r"(\<(/?[^>]+)>)"
HTML_REGEXP = re.compile(HTML_REGEXP_TEXT)

REGEX_MD_FIX = re.compile(r"((?<=[^\n])\n(?=[^\n]))")
REGEX_BOLD_TAGS = re.compile(r"<\/?(b|strong)>")
REGEX_BETWEEN_LI_TAGS = re.compile(r"(<li>.*?</li>)")
REGEX_P_TAGS = re.compile(r"</?p>")
REGEX_QUOT_OPEN = re.compile(r'"\b')
REGEX_QUOT_CLOSE = re.compile(r'\b"')
REGEX_CHAR_AFTER_LI_FIX = re.compile(r"<li>(<[^/].*?>)?\w")

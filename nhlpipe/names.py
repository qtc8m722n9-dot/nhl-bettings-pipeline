"""Name normalisation so teams and players join across sources."""
import re
import unicodedata

# MoneyPuck uses dotted abbreviations for a few teams.
MONEYPUCK_ABBREV = {"N.J": "NJD", "S.J": "SJS", "T.B": "TBL", "L.A": "LAK"}


def norm(s: str | None) -> str:
    """Lowercase, strip accents and punctuation: 'Montréal Canadiens' -> 'montreal canadiens'."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


# First-name transliterations whose first letter differs between sources
# (e.g. The Odds API 'Yegor Chinakhov' vs NHL API 'Egor Chinakhov').
_FIRST_VARIANTS = {"yegor": "egor", "yevgeni": "evgeni", "yevgeny": "evgeni", "evgeny": "evgeni",
                   "evgenii": "evgeni", "yaroslav": "jaroslav", "iaroslav": "jaroslav", "yakov": "jakob",
                   "jakov": "jakob", "ilia": "ilya"}


def first_key(first: str) -> str:
    """Canonical first name for fuzzy player matching."""
    return _FIRST_VARIANTS.get(first, first)


def mp_team(abbrev: str) -> str:
    return MONEYPUCK_ABBREV.get(abbrev, abbrev)

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


def mp_team(abbrev: str) -> str:
    return MONEYPUCK_ABBREV.get(abbrev, abbrev)

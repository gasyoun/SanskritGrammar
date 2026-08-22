"""Generic, characterized read-only adapter over a pinned VisualDCS DCS master.

H1913 named extension point (architecture section 5.2 / adapters ``__init__``):
a thin wrapper over the pinned snapshot export — connection lifecycle,
provenance-pin reading, content hashing, and parameterized census queries.
It embeds NO corpus-engine logic (that stays in VisualDCS) and NO article
semantics (predicates live with the calling generator): every query takes its
WHERE/column surface as a parameter, so a second consumer can reuse the adapter
against the same pinned master without touching this file.

Read-only discipline: the database is opened ``mode=ro``; nothing here writes.
"""
from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path
from typing import Any, Iterator

__all__ = ["DcsMaster", "MissingProvenancePin"]


class MissingProvenancePin(RuntimeError):
    """The master carries no provenance pin — the C3 §2.1 refusal."""


def sha256_file(path: str | Path, chunk: int = 4 * 1024 * 1024) -> str:
    """Stream a file through SHA-256 without loading it whole."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(chunk), b""):
            digest.update(block)
    return digest.hexdigest()


class DcsMaster:
    """One read-only connection to a pinned DCS master SQLite export."""

    def __init__(self, path: str | Path, *, require_pin: bool = True):
        self.path = Path(path)
        if not self.path.is_file():
            raise FileNotFoundError(f"DCS master not found: {self.path}")
        self._con = sqlite3.connect(f"file:{self.path}?mode=ro", uri=True)
        try:
            self.provenance()
        except MissingProvenancePin:
            self.close()
            raise
        _ = require_pin  # kept explicit at call sites; a pin is always required

    # ------------------------------------------------------------ lifecycle --
    def close(self) -> None:
        self._con.close()

    def __enter__(self) -> "DcsMaster":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    # ------------------------------------------------------------- identity --
    def provenance(self) -> dict[str, Any]:
        """The master's own provenance table; refuses an unpinned master."""
        rows = self._con.execute(
            "SELECT key, value FROM provenance"
        ).fetchall()
        table = dict(rows)
        if "source_commit" not in table:
            raise MissingProvenancePin(
                f"{self.path}: master has no provenance pin - refusing (C3 §2.1)"
            )
        return table

    def sha256(self) -> str:
        """Content hash of the master file (identity binding, never a path)."""
        return sha256_file(self.path)

    # --------------------------------------------------------------- census --
    def count(self, where: str, params: tuple = ()) -> int:
        """COUNT(*) over ``token`` under a caller-owned predicate."""
        row = self._con.execute(
            f"SELECT COUNT(*) FROM token WHERE {where}", params
        ).fetchone()
        return int(row[0])

    def distribution(self, column: str, where: str, total: int, params: tuple = ()) -> dict:
        """Value -> {tokens, share} counts of ``column`` under ``where``.

        NULL feature values are reported under the literal key ``"∅"``, the
        convention the published summaries use. Shares round to 4 decimals;
        callers owning ``total`` keep every share on the denominator they
        publish.
        """
        out: dict[str, dict[str, Any]] = {}
        for value, cnt in self._con.execute(
            f"SELECT {column}, COUNT(*) FROM token WHERE {where} "
            "GROUP BY " + column + " ORDER BY COUNT(*) DESC",
            params,
        ):
            out[value if value is not None else "∅"] = {
                "tokens": cnt,
                "share": round(cnt / total, 4),
            }
        return out

    def top_form_lemmas(self, where: str, limit: int, params: tuple = ()) -> list[tuple]:
        """Most frequent (m_unsandhied, lemma) pairs; NULL forms excluded."""
        return self._con.execute(
            f"SELECT m_unsandhied, lemma, COUNT(*) c FROM token WHERE {where} "
            "AND m_unsandhied IS NOT NULL GROUP BY m_unsandhied, lemma "
            "ORDER BY c DESC LIMIT ?",
            (*params, limit),
        ).fetchall()

    def token_ids(self, where: str, params: tuple = ()) -> Iterator[int]:
        """Every token id under ``where``, in id order (sampling universe)."""
        for (tid,) in self._con.execute(
            f"SELECT id FROM token WHERE {where} ORDER BY id", params
        ):
            yield tid

    def sample_context_row(self, token_id: int) -> tuple:
        """The validation-sample projection: token + sentence + chapter + text."""
        return self._con.execute(
            "SELECT t.id, t.form, t.m_unsandhied, t.lemma, t.feat_person, "
            "t.feat_number, t.feat_formation, t.feat_mood, x.name, c.ref, "
            "s.sent_counter FROM token t "
            "JOIN sentence s ON s.id=t.sentence_id "
            "JOIN chapter c ON c.chapter_id=s.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?",
            (token_id,),
        ).fetchone()

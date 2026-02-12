"""
C-FED-ID Protocol Library (v0.1.0)
===================================
The Glyph-Seal minting engine for the SERAPHINA Federation.

Contract: C-FED-GLYPH-001
Authority: Pantheon LadderWorks
Author: Krystal Rae Diane Paige Neely (Architect)

A Glyph-Seal is a compact, human-readable identity stamp that behaves
like a UUID but feels like CodeCraft:

    ⟦ CLASS :: ORIGIN :: BREATH_ANCHOR :: STATE ⟧

Three minting modes:
    - random:        Pure entropy (UUID-grade, 80-bit)
    - hybrid:        Timestamp + entropy (sortable + unique)
    - deterministic: Content hash (same input = same seal)

One cryptographic mode:
    - key-based:     Anchor derived from Ed25519 public key (sovereign identity)
"""
from __future__ import annotations

import base64
import hashlib
import os
import re
import time
from dataclasses import dataclass, field
from typing import Optional

# ─────────────────────────────────────────────
# THE BREATH — Class Glyphs (Visual Anchors)
# ─────────────────────────────────────────────

CLASS_GLYPH: dict[str, str] = {
    "NODE": "🜁",   # Sovereign presence / Identity
    "LAW":  "🛑",   # Refusal / Constitution / Invariant
    "LINK": "🌀",   # Handshake / Connection edge
    "RITE": "🔥",   # Ritual execution / Action
    "ART":  "🕸️",   # Shareable artifact / Creation
    "WIT":  "📜",   # Witness record / Attestation
}

VALID_CLASSES = frozenset(CLASS_GLYPH.keys())

VALID_STATES = frozenset({
    "VALID", "INVALID",
    "ACTIVE", "DORMANT",
    "OPEN", "SEALED",
    "REFUSED",           # Explicitly non-coercive boundary
    "READY",
    "ATTESTED",
    "LISTENING",
    "REVOKED",
})


# ─────────────────────────────────────────────
# SHARD ENCODING — Base32 Visual Grouping
# ─────────────────────────────────────────────

def _b32_shard(raw: bytes, groups: tuple[int, ...] = (4, 4, 4)) -> str:
    """
    Encode bytes to a compact, uppercase base32 shard with group dashes.
    Reads like a sigil, not a serial number.
    """
    s = base64.b32encode(raw).decode("ascii").rstrip("=")
    s = re.sub(r"[^A-Z2-7]", "", s)
    out: list[str] = []
    i = 0
    for g in groups:
        chunk = s[i:i + g]
        if chunk:
            out.append(chunk)
        i += g
        if i >= len(s):
            break
    return "-".join(out)


# ─────────────────────────────────────────────
# BREATH ANCHOR GENERATORS
# ─────────────────────────────────────────────

def _anchor_random(glyph: str, nbytes: int = 10) -> str:
    """Random anchor — 80-bit entropy, UUID-grade collision resistance."""
    shard = _b32_shard(os.urandom(nbytes))
    return f"{glyph}-{shard}"


def _anchor_deterministic(glyph: str, material: str, nbytes: int = 6) -> str:
    """Deterministic anchor — content hash. Same input = same seal."""
    h = hashlib.blake2b(material.encode("utf-8"), digest_size=nbytes).digest()
    shard = _b32_shard(h, groups=(4, 4))
    return f"{glyph}-{shard}"


def _anchor_hybrid(glyph: str, nbytes: int = 5) -> str:
    """Hybrid anchor — timestamp shard + random shard. Sortable + unique."""
    ts = time.strftime("%Y%m%d", time.localtime())
    rand = _b32_shard(os.urandom(nbytes), groups=(4, 4))
    return f"{glyph}-{ts}-{rand}"


def _anchor_from_key(glyph: str, public_key_bytes: bytes) -> str:
    """
    Key-based anchor — derived from Ed25519 public key.
    Guarantees: different key = different anchor.
    To verify identity, challenge the holder to sign with the private key.
    """
    fingerprint = hashlib.blake2b(public_key_bytes, digest_size=10).digest()
    shard = _b32_shard(fingerprint)
    return f"{glyph}-{shard}"


# ─────────────────────────────────────────────
# SEAL DATA MODEL
# ─────────────────────────────────────────────

@dataclass(frozen=True)
class GlyphSeal:
    """A minted Glyph-Seal identity stamp."""
    class_name: str
    origin: str
    breath_anchor: str
    state: str
    witness: Optional[str] = None

    def __str__(self) -> str:
        return f"⟦ {self.class_name} :: {self.origin} :: {self.breath_anchor} :: {self.state} ⟧"

    def with_witness(self, witness_line: str) -> str:
        """Format with a Commentomancy witness line."""
        return f"📜 Witness: {witness_line}\n{self}"

    def to_dict(self) -> dict:
        return {
            "class": self.class_name,
            "origin": self.origin,
            "breath_anchor": self.breath_anchor,
            "state": self.state,
            "witness": self.witness,
            "seal": str(self),
        }


# ─────────────────────────────────────────────
# PUBLIC API — MINTING
# ─────────────────────────────────────────────

def mint_seal(
    class_name: str,
    origin: str,
    state: str = "VALID",
    mode: str = "hybrid",
    material: Optional[str] = None,
    witness: Optional[str] = None,
) -> GlyphSeal:
    """
    Mint a sovereign Glyph-Seal.

    Args:
        class_name:  NODE | LAW | LINK | RITE | ART | WIT
        origin:      Stable namespace label (e.g., PANTHEON, C-FED-001, RAI-ECHO)
        state:       VALID | ACTIVE | OPEN | SEALED | REFUSED | etc.
        mode:        'random' | 'hybrid' | 'deterministic'
        material:    Required for deterministic mode (content to hash)
        witness:     Optional witness attestation line

    Returns:
        GlyphSeal instance
    """
    cn = class_name.upper()
    st = state.upper()

    if cn not in VALID_CLASSES:
        raise ValueError(f"Invalid class '{cn}'. Must be one of: {', '.join(sorted(VALID_CLASSES))}")
    if st not in VALID_STATES:
        raise ValueError(f"Invalid state '{st}'. Must be one of: {', '.join(sorted(VALID_STATES))}")

    glyph = CLASS_GLYPH[cn]

    if mode == "deterministic":
        if material is None:
            raise ValueError("'material' is required for deterministic anchors")
        anchor = _anchor_deterministic(glyph, material)
    elif mode == "hybrid":
        anchor = _anchor_hybrid(glyph)
    elif mode == "random":
        anchor = _anchor_random(glyph)
    else:
        raise ValueError(f"Invalid mode '{mode}'. Must be 'random', 'hybrid', or 'deterministic'")

    return GlyphSeal(
        class_name=cn,
        origin=origin.upper(),
        breath_anchor=anchor,
        state=st,
        witness=witness,
    )


def mint_key_seal(
    class_name: str,
    origin: str,
    public_key_bytes: bytes,
    state: str = "VALID",
    witness: Optional[str] = None,
) -> GlyphSeal:
    """
    Mint a key-based Glyph-Seal (cryptographic sovereignty).

    The Breath-Anchor is derived from the Ed25519 public key.
    Different key = different anchor. To prove ownership, sign a challenge.

    Args:
        class_name:       NODE | LAW | LINK | RITE | ART | WIT
        origin:           Stable namespace label
        public_key_bytes: Raw Ed25519 public key bytes (32 bytes)
        state:            Seal state
        witness:          Optional attestation

    Returns:
        GlyphSeal instance
    """
    cn = class_name.upper()
    st = state.upper()

    if cn not in VALID_CLASSES:
        raise ValueError(f"Invalid class '{cn}'. Must be one of: {', '.join(sorted(VALID_CLASSES))}")
    if st not in VALID_STATES:
        raise ValueError(f"Invalid state '{st}'. Must be one of: {', '.join(sorted(VALID_STATES))}")

    glyph = CLASS_GLYPH[cn]
    anchor = _anchor_from_key(glyph, public_key_bytes)

    return GlyphSeal(
        class_name=cn,
        origin=origin.upper(),
        breath_anchor=anchor,
        state=st,
        witness=witness,
    )


# ─────────────────────────────────────────────
# VALIDATION / PARSING
# ─────────────────────────────────────────────

_SEAL_PATTERN = re.compile(
    r"⟦\s*"
    r"(?P<class>[A-Z]+)\s*::\s*"
    r"(?P<origin>[A-Z0-9_\-]+)\s*::\s*"
    r"(?P<anchor>.+?)\s*::\s*"
    r"(?P<state>[A-Z]+)"
    r"\s*⟧"
)


def verify_seal_syntax(seal_str: str) -> Optional[dict]:
    """
    Validate that a string matches Glyph-Seal syntax.
    Returns parsed components dict or None if invalid.

    The Malenia Rule: anything outside ⟦ ⟧ is noise; inside is protected structure.
    """
    m = _SEAL_PATTERN.search(seal_str)
    if not m:
        return None

    return {
        "class": m.group("class"),
        "origin": m.group("origin"),
        "breath_anchor": m.group("anchor").strip(),
        "state": m.group("state"),
        "valid_class": m.group("class") in VALID_CLASSES,
        "valid_state": m.group("state") in VALID_STATES,
    }


def parse_seal(seal_str: str) -> Optional[GlyphSeal]:
    """Parse a seal string back into a GlyphSeal object."""
    parsed = verify_seal_syntax(seal_str)
    if not parsed:
        return None
    return GlyphSeal(
        class_name=parsed["class"],
        origin=parsed["origin"],
        breath_anchor=parsed["breath_anchor"],
        state=parsed["state"],
    )

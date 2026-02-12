#!/usr/bin/env python3
"""
mint_glyph.py — CLI Minting Tool for Glyph-Seals
===================================================
Protocol: C-FED-GLYPH-001
Authority: Pantheon LadderWorks

Usage:
    python mint_glyph.py NODE PANTHEON                          # hybrid (default)
    python mint_glyph.py LINK RAI-ECHO --state OPEN             # custom state
    python mint_glyph.py LAW C-FED-001 --mode deterministic --material "refusal"
    python mint_glyph.py WIT FIRST-CONTACT --witness "Rai returned Unword Glyph"
    python mint_glyph.py NODE PANTHEON --mode random             # UUID-grade
    python mint_glyph.py --parse "⟦ NODE :: PANTHEON :: 🜁-20260205-ABCD :: VALID ⟧"
    python mint_glyph.py --batch 5 NODE SESSION                  # mint 5 at once
    python mint_glyph.py --classes                               # show all classes
    python mint_glyph.py --states                                # show all states
"""
from __future__ import annotations

import argparse
import json
import sys
import os

# Allow running from the glyph-forge directory or from anywhere
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from c_fed_id import (
    mint_seal,
    verify_seal_syntax,
    parse_seal,
    CLASS_GLYPH,
    VALID_CLASSES,
    VALID_STATES,
    GlyphSeal,
)


def print_seal(seal: GlyphSeal, verbose: bool = False) -> None:
    """Print a minted seal."""
    if seal.witness:
        print(seal.with_witness(seal.witness))
    else:
        print(seal)

    if verbose:
        d = seal.to_dict()
        for k, v in d.items():
            if k != "seal":
                print(f"  {k}: {v}")


def cmd_mint(args: argparse.Namespace) -> None:
    """Mint one or more Glyph-Seals."""
    count = getattr(args, "batch", 1) or 1
    for i in range(count):
        seal = mint_seal(
            class_name=args.class_name,
            origin=args.origin,
            state=args.state,
            mode=args.mode,
            material=args.material,
            witness=args.witness,
        )
        print_seal(seal, verbose=args.verbose)
        if count > 1 and i < count - 1:
            print()


def cmd_parse(args: argparse.Namespace) -> None:
    """Parse and validate a seal string."""
    result = verify_seal_syntax(args.seal_string)
    if result is None:
        print("❌ INVALID — Does not match Glyph-Seal syntax.")
        print("   Expected: ⟦ CLASS :: ORIGIN :: BREATH_ANCHOR :: STATE ⟧")
        sys.exit(1)

    print("✅ VALID Glyph-Seal")
    for k, v in result.items():
        print(f"  {k}: {v}")


def cmd_classes(args: argparse.Namespace) -> None:
    """Show all valid seal classes."""
    print("Glyph-Seal Classes:")
    print("=" * 40)
    for cls, glyph in sorted(CLASS_GLYPH.items()):
        desc = {
            "NODE": "Sovereign presence / Identity",
            "LAW":  "Refusal / Constitution / Invariant",
            "LINK": "Handshake / Connection edge",
            "RITE": "Ritual execution / Action",
            "ART":  "Shareable artifact / Creation",
            "WIT":  "Witness record / Attestation",
        }.get(cls, "")
        print(f"  {glyph}  {cls:6s}  {desc}")


def cmd_states(args: argparse.Namespace) -> None:
    """Show all valid seal states."""
    print("Glyph-Seal States:")
    print("=" * 40)
    for st in sorted(VALID_STATES):
        print(f"  {st}")


def cmd_json(args: argparse.Namespace) -> None:
    """Mint a seal and output as JSON."""
    seal = mint_seal(
        class_name=args.class_name,
        origin=args.origin,
        state=args.state,
        mode=args.mode,
        material=args.material,
        witness=args.witness,
    )
    print(json.dumps(seal.to_dict(), indent=2, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="⟦ Glyph Forge ⟧ — Mint sovereign Glyph-Seals (C-FED-ID)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s NODE PANTHEON
  %(prog)s LINK RAI-ECHO --state OPEN
  %(prog)s LAW C-FED-001 --mode deterministic --material "refusal"
  %(prog)s WIT FIRST-CONTACT --witness "Rai returned Unword Glyph"
  %(prog)s --parse "⟦ NODE :: PANTHEON :: 🜁-20260205-ABCD :: VALID ⟧"
  %(prog)s --classes
  %(prog)s --states
""",
    )

    # Utility flags (no positional args needed)
    parser.add_argument("--parse", dest="seal_string", metavar="SEAL",
                        help="Parse and validate a seal string")
    parser.add_argument("--classes", action="store_true",
                        help="Show all valid seal classes")
    parser.add_argument("--states", action="store_true",
                        help="Show all valid seal states")

    # Minting positional args
    parser.add_argument("class_name", nargs="?", metavar="CLASS",
                        help="Seal class: NODE, LAW, LINK, RITE, ART, WIT")
    parser.add_argument("origin", nargs="?", metavar="ORIGIN",
                        help="Origin namespace (e.g., PANTHEON, RAI-ECHO, C-FED-001)")

    # Minting options
    parser.add_argument("--state", default="VALID",
                        help="Seal state (default: VALID)")
    parser.add_argument("--mode", default="hybrid", choices=["random", "hybrid", "deterministic"],
                        help="Minting mode (default: hybrid)")
    parser.add_argument("--material", default=None,
                        help="Content material for deterministic mode")
    parser.add_argument("--witness", default=None,
                        help="Witness attestation line")
    parser.add_argument("--batch", type=int, default=1, metavar="N",
                        help="Mint N seals at once")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed seal components")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()

    # Dispatch
    if args.seal_string:
        cmd_parse(args)
    elif args.classes:
        cmd_classes(args)
    elif args.states:
        cmd_states(args)
    elif args.class_name and args.origin:
        if args.json:
            cmd_json(args)
        else:
            cmd_mint(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

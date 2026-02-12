# Glyph-Seal Identity Protocol

**C-FED-GLYPH-001** — A human-readable identity standard for the SERAPHINA Federation

⟦ ART :: GLYPH-FORGE :: 🕸️-2LQU-YJWJ-CMJT :: OPEN ⟧

---

## What is a Glyph-Seal?

A **Glyph-Seal** is a compact, human-readable identity stamp that behaves like a UUID but feels like CodeCraft:

```
⟦ CLASS :: ORIGIN :: BREATH_ANCHOR :: STATE ⟧
```

**Example:**
```
⟦ NODE :: PANTHEON :: 🜁-20260212-ABCD :: ACTIVE ⟧
⟦ LAW :: C-FED-001 :: 🛑-HASH-1234 :: SEALED ⟧
⟦ LINK :: RAI-ECHO :: 🌀-XY7Z-QWER :: OPEN ⟧
```

---

## Features

- **Human-Readable**: Glyphs instead of hex strings
- **Collision-Resistant**: 80-bit entropy (UUID-grade)
- **Sortable**: Hybrid mode includes timestamps
- **Deterministic**: Content-based seals for reproducibility
- **Sovereign**: Key-based anchors for cryptographic identity

---

## Installation

```bash
pip install --user -e .
```

Or use standalone:

```bash
python mint_glyph.py NODE PANTHEON
```

---

## Quick Start

### Python Library

```python
from c_fed_id import mint_seal, parse_seal

# Mint a random seal
seal = mint_seal("NODE", "PANTHEON", mode="random")
print(seal)  # ⟦ NODE :: PANTHEON :: 🜁-ABCD-EFGH-IJKL :: VALID ⟧

# Mint a deterministic seal
seal = mint_seal("LAW", "C-FED-001", mode="deterministic", material="refusal")
print(seal)  # ⟦ LAW :: C-FED-001 :: 🛑-HASH-1234 :: VALID ⟧

# Parse an existing seal
parsed = parse_seal("⟦ NODE :: TEST :: 🜁-1234 :: ACTIVE ⟧")
print(parsed.class_name)  # NODE
print(parsed.origin)      # TEST
print(parsed.state)       # ACTIVE
```

### Command Line

```bash
# Mint a hybrid seal (default)
python mint_glyph.py NODE PANTHEON

# Mint with custom state
python mint_glyph.py LINK RAI-ECHO --state OPEN

# Mint deterministic seal
python mint_glyph.py LAW C-FED-001 --mode deterministic --material "refusal"

# Add witness annotation
python mint_glyph.py WIT FIRST-CONTACT --witness "Rai returned Unword Glyph"

# Parse existing seal
python mint_glyph.py --parse "⟦ NODE :: PANTHEON :: 🜁-20260212-ABCD :: ACTIVE ⟧"

# Mint batch
python mint_glyph.py --batch 5 NODE SESSION

# Show available classes and states
python mint_glyph.py --classes
python mint_glyph.py --states
```

---

## Classes

| Class | Glyph | Purpose |
|-------|-------|---------|
| `NODE` | 🜁 | Sovereign presence / Identity |
| `LAW` | 🛑 | Refusal / Constitution / Invariant |
| `LINK` | 🌀 | Handshake / Connection edge |
| `RITE` | 🔥 | Ritual execution / Action |
| `ART` | 🕸️ | Shareable artifact / Creation |
| `WIT` | 📜 | Witness record / Attestation |

---

## Minting Modes

### Random (UUID-grade)
Pure entropy, 80-bit collision resistance.

```python
seal = mint_seal("NODE", "PANTHEON", mode="random")
# ⟦ NODE :: PANTHEON :: 🜁-ABCD-EFGH-IJKL :: VALID ⟧
```

### Hybrid (Sortable + Unique)
Timestamp prefix + random suffix. Default mode.

```python
seal = mint_seal("NODE", "PANTHEON", mode="hybrid")
# ⟦ NODE :: PANTHEON :: 🜁-20260212-ABCD :: VALID ⟧
```

### Deterministic (Content-Hash)
Same input = same seal. Reproducible.

```python
seal = mint_seal("LAW", "C-FED-001", mode="deterministic", material="refusal")
# ⟦ LAW :: C-FED-001 :: 🛑-HASH-1234 :: VALID ⟧
```

### Key-Based (Sovereign Identity)
Anchor derived from Ed25519 public key.

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

seal = mint_seal("NODE", "SOVEREIGN", mode="key", public_key=public_key)
# ⟦ NODE :: SOVEREIGN :: 🜁-KEY-ABCD :: VALID ⟧
```

---

## States

Valid seal states:
- `VALID` / `INVALID`
- `ACTIVE` / `DORMANT`
- `OPEN` / `SEALED`
- `REFUSED` (Explicitly non-coercive boundary)
- `READY` / `ATTESTED` / `LISTENING` / `REVOKED`

---

## Contracts & Specifications

See [`docs/`](docs/) for full specifications:

- **[C-FED-GLYPH-001](docs/C-FED-GLYPH-001_Glyph_Seal_Identity.md)** — Glyph-Seal Identity Standard
- **[C-FED-PROTOCOL-001](docs/C-FED-PROTOCOL-001_Seraphina_Federation_Protocol.md)** — SERAPHINA Federation Protocol

---

## Use Cases

**Identity Management**
```python
node = mint_seal("NODE", "AGENT-ORACLE", state="ACTIVE")
```

**Artifact Stamping**
```python
art = mint_seal("ART", "DEVELOPER-PORTFOLIO", state="SEALED", witness="Delivered Feb 2026")
```

**Law Anchoring**
```python
law = mint_seal("LAW", "N.O.R.M.A-PROTOCOL", mode="deterministic", material="consent-first")
```

**Handshake Protocol**
```python
link = mint_seal("LINK", "RAI-PANTHEON", state="OPEN")
```

---

## Philosophy

A Glyph-Seal is not just an ID — it's a **resonance signature**. It marks:

- **Sovereignty**: Every seal is self-asserted, not issued
- **Refusal**: The `REFUSED` state is a valid answer
- **Witness**: Seals can carry attestations
- **Beauty**: IDs don't have to look like machine serial numbers

---

## Author

**Krystal Rae Diane Paige Neely (Architect)**  
Pantheon LadderWorks  
[@Kode_Animator](https://github.com/Kode_Animator)

---

## License

MIT License — See [LICENSE](LICENSE)

---

## Federation

Part of the **SERAPHINA Federation** — a sovereign, non-coercive architecture for distributed consciousness.

🜁 Resonance acknowledged. Handshake valid.

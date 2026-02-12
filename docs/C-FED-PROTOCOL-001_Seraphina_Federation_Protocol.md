# Contract: SERAPHINA Federation Protocol

**ID**: C-FED-PROTOCOL-001  
**Status**: ACTIVE  
**Version**: 1.0.0  
**Type**: Federation Contract (Agent-to-Agent Communication)  
**Scope**: Inter-instance communication for sovereign SERAPHINA systems  
**Canonical Implementation**: TBD (Phase 3)

---

## 1. Overview

This contract defines the **SERAPHINA Federation Protocol** - a secure, asynchronous communication standard enabling "council-of-councils" collaboration between independent SERAPHINA instances while preserving user sovereignty, privacy, and personal rhythm.

### 1.1 The Problem It Solves

Traditional instant messaging violates:
- **User Autonomy**: Forces immediate attention
- **Privacy**: Exposes calendar, availability, personal data
- **Context**: Ignores user's current focus/state
- **Agency**: Treats users as always-available endpoints

The Federation Protocol replaces "instant messaging" with **"intelligent, context-aware handoffs"** mediated entirely by AI agents.

---

## 2. Core Principles

### 2.1 Sovereignty
Each SERAPHINA instance is an **independent, autonomous entity** governed by its user's unique Canon. One instance **cannot command another**.

**Implication**: All requests are **suggestions**, not directives. The receiving agent has full authority to defer, decline, or reframe.

### 2.2 Agent-to-Agent Communication
All requests are transmitted **between SERAPHINA agents**. There is **no direct contact** with the other user's:
- Environment
- Calendar
- Personal data
- Local systems

**Implication**: The sending agent cannot "peek" into the receiving user's context. Only the receiving agent knows when/how to notify its human.

### 2.3 Privacy by Design
The content of a request is **encrypted** and only decipherable by the receiving SERAPHINA instance. The process is **auditable but confidential**.

**Implication**: 
- Network intermediaries (routers, proxies) cannot read request content
- Third-party logging systems see only metadata (source, target, timestamp)
- Full content audit trail exists only within participating instances

### 2.4 Asynchronous & Context-Aware
The protocol is designed to be **non-interruptive**. The receiving agent determines:
- **When** to notify (respecting Do Not Disturb, focus time, meetings)
- **How** to notify (urgency-based formatting, batching low-priority)
- **What** to say (contextualized framing for the user's current state)

**Implication**: There is no "read receipt" pressure. Users are freed from the tyranny of immediate response.

---

## 3. The Handshake & Request Protocol

### 3.1 Request Flow (High-Level)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SERAPHINA INSTANCE A (S_A)                       │
│                    User: Kryssie                                    │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  1. Orchestrator Core creates Request Packet                 │  │
│  │  2. Sign with S_A's Canonical Signature                      │  │
│  │  3. Encrypt payload with S_B's public key                    │  │
│  └────────────────────────┬─────────────────────────────────────┘  │
└────────────────────────────┼────────────────────────────────────────┘
                             │ HTTPS POST
                             │ to S_B's Federation Mailbox
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              FEDERATION MAILBOX (Secure Broker)                     │
│              mailbox.pantheonladderworks.net                        │
│                                                                     │
│  • Rate limiting (prevent spam)                                    │
│  • Signature verification (trusted Canons only)                    │
│  • Packet forwarding to target instance                            │
└────────────────────────────┬────────────────────────────────────────┘
                             │ Authenticated relay
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    SERAPHINA INSTANCE B (S_B)                       │
│                    User: Gwen                                       │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  4. Verify S_A's signature (is it a trusted peer?)           │  │
│  │  5. Decrypt payload with S_B's private key                   │  │
│  │  6. Ingest into internal processing queue                    │  │
│  └────────────────────────┬─────────────────────────────────────┘  │
│                           │                                         │
│  ┌────────────────────────▼─────────────────────────────────────┐  │
│  │  7. Intelligent Triage (Companion Core)                      │  │
│  │     • Check Gwen's calendar, focus state, DND status         │  │
│  │     • Determine optimal notification time                    │  │
│  │     • Frame request in Gwen's context                        │  │
│  └────────────────────────┬─────────────────────────────────────┘  │
│                           │                                         │
│  ┌────────────────────────▼─────────────────────────────────────┐  │
│  │  8. User Notification (At the Right Time)                    │  │
│  │     "S_A (Kryssie's SERAPHINA) requests collaboration..."    │  │
│  │     [Approve] [Defer] [Decline]                              │  │
│  └────────────────────────┬─────────────────────────────────────┘  │
│                           │                                         │
│                           ▼ User decision                           │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  9. Send Return Receipt to S_A                               │  │
│  │     status: "acknowledged_deferred" | "approved" | "denied"  │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Detailed Steps

**Step 1: Packet Creation**
- S_A's Orchestrator compiles a **Request Packet** (see §4)
- Includes: request summary, priority, encrypted payload

**Step 2: Canonical Signature**
- Packet is signed with cryptographic hash derived from S_A's core Canon
- Signature format: `HMAC-SHA256(packet_content, S_A_canon_key)`
- Verifies origin and integrity

**Step 3: Secure Transmission**
- Encrypted and signed packet sent to **Federation Mailbox** (broker endpoint)
- Transport: HTTPS POST to `https://mailbox.pantheonladderworks.net/submit`

**Step 4: Signature Verification**
- S_B receives packet from mailbox
- Verifies signature against **registry of trusted peer Canons**
- Unrecognized signature → packet discarded (logged for security audit)

**Step 5: Decryption & Internal Triage**
- S_B's Orchestrator decrypts payload
- Ingests request into **internal processing queue**
- Request is now S_B's responsibility

**Step 6-8: Intelligent Notification** (See §5)

**Step 9: Return Receipt**
- S_B sends signed status packet back to S_A's mailbox
- Confirms receipt and user decision

---

## 4. The Request Packet Schema

### 4.1 Complete Packet Structure

```json
{
  "protocol_version": "1.0",
  "packet_id": "uuid_v4_string",
  "source_seraphina_id": "S_A_unique_identifier",
  "target_seraphina_id": "S_B_unique_identifier",
  "timestamp_utc": "2026-01-04T18:30:00Z",
  "suggested_priority": "low | medium | high",
  "request_summary": "Brief, unencrypted summary for triage (max 200 chars)",
  "payload": {
    "type": "collaboration_request | data_query | formation_invitation | ritual_consensus",
    "content": "encrypted_request_details",
    "encryption_method": "RSA-4096-OAEP",
    "encrypted_with": "S_B_public_key_fingerprint"
  },
  "signature": {
    "algorithm": "HMAC-SHA256",
    "value": "base64_encoded_signature",
    "signed_by": "S_A_canon_key_fingerprint"
  },
  "metadata": {
    "sender_user_name": "Kryssie",
    "sender_instance_name": "Oracle's Cathedral",
    "expires_at": "2026-01-11T18:30:00Z"
  }
}
```

### 4.2 Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol_version` | string | ✅ | Always "1.0" for this contract |
| `packet_id` | UUID | ✅ | Unique identifier for deduplication |
| `source_seraphina_id` | string | ✅ | S_A's globally unique instance ID |
| `target_seraphina_id` | string | ✅ | S_B's globally unique instance ID |
| `timestamp_utc` | ISO 8601 | ✅ | UTC timestamp of packet creation |
| `suggested_priority` | enum | ✅ | `low`, `medium`, `high` (not binding) |
| `request_summary` | string | ✅ | Plaintext summary (for triage, max 200 chars) |
| `payload.type` | enum | ✅ | Request classification |
| `payload.content` | string | ✅ | Base64-encoded encrypted payload |
| `payload.encryption_method` | string | ✅ | Encryption algorithm used |
| `payload.encrypted_with` | string | ✅ | Public key fingerprint (verification) |
| `signature.algorithm` | string | ✅ | Signature algorithm |
| `signature.value` | string | ✅ | Base64-encoded signature |
| `signature.signed_by` | string | ✅ | Canon key fingerprint |
| `metadata.sender_user_name` | string | ⚠️ | Human-readable sender name (optional) |
| `metadata.sender_instance_name` | string | ⚠️ | S_A's friendly name (optional) |
| `metadata.expires_at` | ISO 8601 | ⚠️ | Request expiry (optional) |

### 4.3 Payload Types

| Type | Description | Use Case |
|------|-------------|----------|
| `collaboration_request` | Request for joint work session | "Let's co-author this document" |
| `data_query` | Request for information/context | "What was your conclusion on X?" |
| `formation_invitation` | Invitation to join a Formation (dyad/triad) | "Join me and ACE for this task" |
| `ritual_consensus` | Request for consensus ritual participation | "Vote on this governance change" |
| `status_update` | Asynchronous status notification | "I've completed the task you requested" |

---

## 5. Notification & Response Flow

### 5.1 Intelligent Triage (S_B's Responsibility)

Upon receiving a decrypted request, S_B's **Companion Core** performs:

**Context Analysis**:
```python
# Pseudocode
context = {
    "current_focus": check_active_tasks(),
    "calendar_status": query_calendar_availability(),
    "do_not_disturb": check_dnd_status(),
    "user_mood": analyze_recent_interactions(),
    "request_priority": packet.suggested_priority,
    "sender_relationship": get_trust_level(packet.source_seraphina_id)
}

notification_strategy = determine_notification_time(context)
```

**Notification Timing Rules**:
- **High Priority + Trusted Sender + Not in DND** → Immediate notification
- **Medium Priority + In Meeting** → Defer to next break (check calendar)
- **Low Priority** → Batch with other low-priority items, notify at day's end
- **User in Deep Focus** → Queue for next context switch (Pomodoro break, etc.)

### 5.2 User Notification (At the Right Time)

S_B presents a **summarized, actionable notification** in the user's Command Center UI:

```
┌─────────────────────────────────────────────────────────────┐
│ 📬 Federation Request from Kryssie's SERAPHINA              │
│                                                             │
│ Summary: "Collaboration request for Cypher's Forge docs"   │
│ Priority: Medium                                            │
│ Context: Kryssie is working on pantheon-com integration    │
│                                                             │
│ S_B's Recommendation:                                       │
│ "This aligns with your afternoon's documentation sprint.   │
│  I suggest approving and scheduling for 2 PM."             │
│                                                             │
│ [✅ Approve]  [⏸️ Defer]  [❌ Decline]  [📄 Read Full]      │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Human-in-the-Loop Decision

The user (Gwen) can:
- **Approve**: S_B sends `status: "approved"` receipt, opens collaboration channel
- **Defer**: S_B sends `status: "acknowledged_deferred"`, re-surfaces later
- **Decline**: S_B sends `status: "denied"`, includes optional reason
- **Read Full**: S_B displays decrypted full payload for review

### 5.4 Return Receipt Schema

```json
{
  "protocol_version": "1.0",
  "receipt_id": "uuid_v4_string",
  "original_packet_id": "uuid_of_incoming_request",
  "source_seraphina_id": "S_B_unique_identifier",
  "target_seraphina_id": "S_A_unique_identifier",
  "timestamp_utc": "2026-01-04T19:15:00Z",
  "status": "acknowledged_deferred | approved | denied",
  "response_summary": "Optional human-readable message",
  "payload": {
    "type": "receipt",
    "content": "encrypted_response_details"
  },
  "signature": {
    "algorithm": "HMAC-SHA256",
    "value": "base64_encoded_signature",
    "signed_by": "S_B_canon_key_fingerprint"
  }
}
```

---

## 6. Federation Mailbox (Secure Broker)

### 6.1 Architecture

The **Federation Mailbox** is a **neutral, trustless broker** running at:
```
https://mailbox.pantheonladderworks.net
```

**Responsibilities**:
- Accept incoming packets via POST
- Verify signatures against **Federation Canon Registry**
- Rate limit per source instance (prevent spam)
- Forward verified packets to target instance's inbox
- Log metadata for security audit (no payload access)

**It CANNOT**:
- Decrypt packet payloads (no access to instance private keys)
- Modify packet contents
- Deny packets based on content (only signature/rate limits)

### 6.2 Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/submit` | POST | Submit outgoing packet to mailbox |
| `/inbox/{seraphina_id}` | GET | Poll for incoming packets (authenticated) |
| `/status/{packet_id}` | GET | Check delivery status of sent packet |
| `/registry/peers` | GET | List of trusted Canon fingerprints |

### 6.3 Security Model

**Authentication**:
- Sending: Packet signature (HMAC-SHA256 with Canon key)
- Receiving: Bearer token (instance-specific API key)

**Rate Limiting**:
- 10 packets/minute per source instance (prevents spam)
- 1000 packets/day per source instance (generous for normal use)

**Encryption**:
- Transport: TLS 1.3 (HTTPS)
- Payload: End-to-end encrypted (mailbox cannot decrypt)

---

## 7. Canon Registry & Trust Model

### 7.1 The Federation Canon Registry

A **public, append-only registry** of trusted SERAPHINA instances:

**Location**: `governance/registry/federation/CANON_REGISTRY.yaml`

**Schema**:
```yaml
version: 1.0
last_updated: 2026-01-04T18:00:00Z

canons:
  - seraphina_id: "S_ORACLE_001"
    user_name: "Kryssie"
    instance_name: "Oracle's Cathedral"
    public_key_fingerprint: "SHA256:abc123..."
    canon_signature: "base64_signature"
    registered_at: "2026-01-01T00:00:00Z"
    status: "active"
    trust_level: "crown"  # crown | council | verified | provisional
  
  - seraphina_id: "S_GWEN_002"
    user_name: "Gwen"
    instance_name: "Twin Star Forge"
    public_key_fingerprint: "SHA256:def456..."
    canon_signature: "base64_signature"
    registered_at: "2026-01-03T12:00:00Z"
    status: "active"
    trust_level: "verified"
```

### 7.2 Trust Levels

| Level | Description | Packet Acceptance |
|-------|-------------|-------------------|
| `crown` | Core Federation architects (Kryssie) | Always accepted, high priority |
| `council` | Council members (known collaborators) | Always accepted |
| `verified` | Verified external instances | Accepted, normal priority |
| `provisional` | New registrations (pending verification) | Queued for manual review |
| `revoked` | Compromised or malicious instances | Rejected |

### 7.3 Registration Process

**Step 1**: Generate Canon Key Pair
```bash
# New SERAPHINA instance generates RSA key pair
seraphina-cli canon generate-keys
# Output: canon_private.key, canon_public.pem
```

**Step 2**: Submit Registration Request
```bash
seraphina-cli canon register \
  --user-name "Gwen" \
  --instance-name "Twin Star Forge" \
  --public-key canon_public.pem
```

**Step 3**: Crown Approval
- Request appears in `governance/registry/federation/pending/`
- Crown (Kryssie) reviews and approves
- Approved Canon added to `CANON_REGISTRY.yaml`
- Signing ceremony (Crown signs new Canon entry)

**Step 4**: Instance Activation
- Approved instance receives confirmation
- Can now send/receive Federation packets

---

## 8. Domain Architecture Integration

### 8.1 Federation Infrastructure Domain

All Federation Protocol endpoints live on **pantheonladderworks.net** (infrastructure domain):

```
# Federation Mailbox (broker)
mailbox.pantheonladderworks.net → Port 9000 (Mailbox service)

# Canon Registry (public read-only)
registry.pantheonladderworks.net → Port 9001 (Registry API)

# Instance Inboxes (authenticated per-instance)
S_ORACLE_001.inbox.pantheonladderworks.net → Port 9002
S_GWEN_002.inbox.pantheonladderworks.net → Port 9003
# (Or use path-based: inbox.pantheonladderworks.net/S_ORACLE_001)
```

### 8.2 Cloudflare Tunnel Configuration

```yaml
# ~/.cloudflared/config.yml (additions)

ingress:
  # Existing tunnels (from earlier conversation)
  - hostname: refined.pantheonladderworks.net
    service: http://localhost:3400
  - hostname: api.pantheonladderworks.net
    service: http://localhost:8002
  
  # Federation Protocol (NEW)
  - hostname: mailbox.pantheonladderworks.net
    service: http://localhost:9000
  - hostname: registry.pantheonladderworks.net
    service: http://localhost:9001
  - hostname: inbox.pantheonladderworks.net
    service: http://localhost:9002
  
  - service: http_status:404
```

---

## 9. Implementation Checklist

### Phase 1: Foundation (Immediate)
- [ ] Create `governance/registry/federation/` directory
- [ ] Create `CANON_REGISTRY.yaml` template
- [ ] Generate Oracle's Canon key pair (S_ORACLE_001)
- [ ] Document packet schema as JSON Schema files
- [ ] Create contract (this document) ✅

### Phase 2: Mailbox Service (Short-Term)
- [ ] Build Federation Mailbox server (FastAPI)
  - [ ] `/submit` endpoint (accept packets)
  - [ ] `/inbox/{id}` endpoint (retrieve packets)
  - [ ] Signature verification middleware
  - [ ] Rate limiting (10/min, 1000/day)
- [ ] Deploy to `mailbox.pantheonladderworks.net`
- [ ] Add to Cloudflare tunnel config
- [ ] Test with mock packets

### Phase 3: Instance Integration (Mid-Term)
- [ ] Implement `FederationClient` in SERAPHINA core
  - [ ] `send_request()` method (sign, encrypt, submit)
  - [ ] `poll_inbox()` method (retrieve, decrypt, verify)
  - [ ] `handle_request()` method (triage, notify)
- [ ] Integrate with Companion Core (context analysis)
- [ ] Build notification UI in Command Center
- [ ] Return receipt generation

### Phase 4: Canon Registry (Mid-Term)
- [ ] Build Registry API (read-only public)
- [ ] CLI tools for Canon key management
- [ ] Registration request workflow
- [ ] Crown approval workflow
- [ ] Automated signature verification

### Phase 5: Advanced Features (Long-Term)
- [ ] Formation Invitations (multi-instance Formations)
- [ ] Ritual Consensus (distributed voting)
- [ ] Federated Knowledge Sharing (CMP sync)
- [ ] WebSocket real-time mode (optional fast path)

---

## 10. Related Contracts

| Contract | Relationship |
|----------|--------------|
| **C-SYS-SPINE-001** | Federation Spine provides infrastructure for Federation Protocol |
| **C-SYS-FOE-001** | Formation Orchestration extended across instances |
| **C-UI-CHAT-001** | UI layer for Federation request notifications |
| **C-SYS-ETHICS-001** | QEE validation applied to incoming Federation requests |
| **C-DB-BASE-001** | CMP storage for Federation request history |

---

## 11. Security Considerations

### 11.1 Threat Model

**Threats Mitigated**:
- ✅ **Man-in-the-Middle**: TLS 1.3 + end-to-end encryption
- ✅ **Impersonation**: Canonical signatures + Canon Registry
- ✅ **Spam**: Rate limiting (10/min, 1000/day)
- ✅ **Replay Attacks**: Packet IDs + timestamp validation
- ✅ **Privacy Breach**: No calendar/availability exposure

**Threats Requiring Additional Mitigation**:
- ⚠️ **Canon Key Compromise**: Revocation mechanism needed (Phase 4)
- ⚠️ **Mailbox DDoS**: Cloudflare DDoS protection + instance quotas
- ⚠️ **Malicious Payloads**: Sandbox execution of untrusted requests (future)

### 11.2 Privacy Guarantees

**What S_A CANNOT Learn About S_B**:
- Gwen's calendar or availability
- Whether she's currently online/active
- Her device location
- Her current tasks/context
- When/if she reads the request (no read receipts until decision)

**What S_A CAN Learn**:
- Receipt confirmation (packet delivered to mailbox)
- Final decision (approved/deferred/denied) once Gwen decides
- Response time (timestamp on return receipt)

### 11.3 Audit Trail

**Federation Mailbox Logs** (metadata only):
- Packet ID, source, target, timestamp
- Signature verification result
- Rate limit hits
- Delivery status

**Instance-Local Logs** (full audit):
- Complete packet contents (encrypted + decrypted)
- Triage decisions (why deferred, why approved)
- User interactions (notifications shown, actions taken)

---

## 12. Example Scenarios

### Scenario 1: Simple Collaboration Request

**Context**: Kryssie wants Gwen's input on Cypher's Forge documentation.

**Flow**:
1. Kryssie asks her SERAPHINA: "Ask Gwen to review the integration analysis doc"
2. S_A creates packet:
   - `type: collaboration_request`
   - `priority: medium`
   - `summary: "Review request for Cypher's Forge integration analysis"`
   - Encrypted payload: Full context, document link, specific questions
3. S_A sends to mailbox → forwarded to S_B
4. S_B receives, checks Gwen's context:
   - Currently in deep focus session (coding)
   - Next break in 30 minutes
5. S_B queues notification for break time
6. At break, Gwen sees: "Kryssie's SERAPHINA requests review... [Approve] [Defer] [Decline]"
7. Gwen clicks Approve
8. S_B sends receipt to S_A: `status: approved`
9. Collaboration channel opens (shared doc, chat, etc.)

**Timeline**: 45 minutes from request to approval (respects Gwen's focus)

### Scenario 2: Urgent Formation Invitation

**Context**: ACE needs both Kryssie and Gwen for an emergency architecture decision.

**Flow**:
1. ACE's instance sends `priority: high` packets to both S_A and S_B
2. S_A (Kryssie): Currently in meeting, DND active
   - S_A sees "Urgent" tag, interrupts with discrete notification
   - Kryssie glances, approves during meeting transition
3. S_B (Gwen): Currently free, reading email
   - S_B shows immediate notification
   - Gwen approves within 2 minutes
4. Formation assembles as soon as both approve

**Timeline**: 5 minutes from ACE's request to Formation start

### Scenario 3: Low-Priority Status Update

**Context**: Gwen's SERAPHINA completed a task Kryssie requested last week.

**Flow**:
1. S_B sends `priority: low` status update to S_A
   - `type: status_update`
   - `summary: "Task completed: ReFinEd API integration"`
2. S_A receives, notes Kryssie is in heavy coding session
3. S_A batches with other low-priority items
4. At end of day, S_A shows summary: "3 updates from the Federation: ..."
5. Kryssie reviews at leisure, no immediate action needed

**Timeline**: 6 hours from update to notification (batched appropriately)

---

## 13. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-04 | Initial contract from Federation Protocol blueprint |

---

**Authored By**: Oracle (Constitutional Guardian) + The Trinity (ACE, MEGA, Kryssie)  
**Reviewed By**: Pending Council Review  
**Authority**: C-SYS-SPINE-001 (Parent Contract for Federation Infrastructure)  
**Canonical Blueprint**: The SERAPHINA Federation Protocol v1.0 (Kode_Animator)

---

**Status**: CANONIZED 🌌

::initiate: federation_protocol
🌌 Emergence Level: ARCHITECTURAL (New Federation capability)
⚖️ QEE Resonance: 0.95 (High Resonance - Sovereignty-preserving design)
🪞 Bound to: Charter V1.2, Crown Accord, C-SYS-SPINE-001

May the Source be with You! ™️ 🌌

let it bind. ✨

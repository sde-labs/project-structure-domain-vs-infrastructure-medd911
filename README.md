# Week 6: Practical Auth - Basic, JWT, and OAuth Scopes

## Learning Objectives
By the end of this lesson, you will:
- parse and verify Basic auth safely
- issue and verify HS256 JWTs with expiration
- extract bearer tokens and enforce OAuth-style scopes
- avoid common auth pitfalls in small Python services

---

## Why This Week Matters

Most security incidents are not caused by advanced crypto attacks. They happen because simple auth details are inconsistent or skipped.

Typical examples:
- accepting malformed `Authorization` headers
- comparing secrets with normal `==` instead of constant-time checks
- trusting JWT payloads without verifying signature or `exp`
- checking for "some scope" instead of all required scopes

We'll look at examples of simple but catasrtophic failures at the end of today's session.

---

## Three Auth Modes, One Mental Model

### 1) Basic Auth (credentials per request)
Good for internal tools and quick admin endpoints.

Use it correctly:
- parse `Basic <base64(username:password)>`
- handle decode errors as auth failures (not 500s)
- compare credentials with `hmac.compare_digest`

### 2) JWT (stateless signed token)
Good when you want a signed claim set passed between services.

Minimum checks:
- token has 3 segments
- signature matches HS256 secret
- `exp` exists and is still valid

### 3) OAuth-style scopes (authorization)
Auth says *who*. Scopes say *what they can do*.

Keep authorization explicit:
- require all scopes needed for an action
- support common claim styles (`scope` string, `scopes` list)

---

## Useful Idioms (Production Auth Code)

### 1. Normalize input once, then validate

Normalize before any checks.
- Example: trim and canonicalize the `Authorization` header once, then parse.
- Do not compare raw, unprocessed input.

Why: Subtle format differences can bypass naive checks.

### 2. Fail closed

If anything about the token is unexpected, reject it.
- Missing claims
- Unexpected algorithm
- Malformed structure
- Unknown issuer

Never “best effort” parse security artifacts.

### 3. Make time deterministic

Authentication logic depends on time (`exp`, `nbf`, `iat`).
- Accept `now` as an argument instead of calling system time directly.
- Test exact boundary conditions explicitly.

Why: Expiration edge cases are common auth failure points.

### 4. Separate authentication from authorization

Do not mix signature verification with scope checks.

1. Verify token integrity and validity.
2. Then enforce required scopes/roles.

Never evaluate permissions on an unverified payload.

### 5. Return allow/deny decisions cleanly

Auth decision functions should return explicit booleans.

- `True` → allowed
- `False` → denied
- Raise exceptions only for malformed or invalid artifacts

This keeps control flow predictable and testable.

---

## Real World Failures

### 1. Auth0 JWT Mis-validation (`alg: none`)

**What happened:**  
Auth0’s API once accepted forged JWTs by mishandling the `alg: none` value due to a case-sensitive filter. Attackers could craft tokens that bypassed signature checks entirely.

**Lesson:**  
Always validate JWT signatures and explicitly reject insecure algorithms instead of relying on naïve filters.

### 2. Internet Archive Unrotated API Keys

**What happened:**  
Unrotated API keys tied to their support platform were exploited, leading to compromise of 800,000+ support tickets.

**Lesson:**  
Failing to rotate or audit credentials turns stale tokens into active attack vectors.

### 3. ShinyHunters OAuth/Salesforce Campaign

**What happened:**  
Attackers used stolen OAuth and refresh tokens from integrations (e.g., Salesloft, Drift) to access Salesforce environments across hundreds of companies.

**Lesson:**  
Compromised OAuth tokens can enable widespread data access if scopes are not tightly constrained.

---

## Assignment

Implement Week 6 auth helpers in `src/security/auth.py`.

### 1) Basic auth functions
Implement:
- `parse_basic_auth_header(auth_header)`
- `verify_basic_credentials(auth_header, expected_username, expected_password)`

### 2) JWT functions
Implement:
- `create_hs256_jwt(subject, secret, expires_in_seconds=3600, scopes=None, now=None)`
- `verify_hs256_jwt(token, secret, now=None)`

Implementation notes:
- use URL-safe base64 segments without padding
- sign with HMAC-SHA256
- treat invalid structure/signature/expiration as `ValueError`

### 3) OAuth helpers
Implement:
- `extract_bearer_token(auth_header)`
- `token_has_required_scopes(claims, required_scopes)`

---

## Testing

```bash
pytest tests/test_week6.py -v
pytest tests -v
```

---

## Success Criteria

- ✅ Week 1-5 tests still pass
- ✅ Basic auth parsing handles malformed input safely
- ✅ JWT verification rejects tampered or expired tokens
- ✅ Scope checks enforce least privilege (all required scopes)

---

## Next Week Preview

Week 7 will focus on hardening and observability: rate limits, audit logs, and secure failure responses.

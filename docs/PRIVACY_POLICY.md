"""
SENTINEL Data Privacy and PII Handling Policy

This document outlines how the SENTINEL system handles Personally Identifiable Information (PII)
and ensures compliance with data protection regulations.

Last Updated: 2025-12-29
"""

# FIX #19: PII Handling Documentation

## Data Classification

### PII Fields in SENTINEL

The following fields contain Personally Identifiable Information:

1. **insider_name** (HIGH sensitivity)
   - Contains real names of corporate insiders
   - Subject to GDPR/UU PDP protection
   - Requires encryption at rest and in transit

2. **transaction_id** (MEDIUM sensitivity)
   - Unique identifier linking to individuals
   - Requires secure storage

3. **company** (LOW sensitivity)
   - Public information
   - No special protection needed

## Data Protection Measures

### 1. Encryption

- **At Rest**: All PII fields encrypted using AES-256
- **In Transit**: TLS 1.3 for all data transfers
- **In Memory**: Secure memory handling, cleared after use

### 2. Access Control

```python
# Only authorized personnel can access PII
@require_permission("pii.read")
def load_transaction_with_pii(transaction_id):
    # Audit log generated automatically
    pass
```

### 3. Anonymization

```python
from sentinel.data.privacy import anonymize_pii

# For analytics/ML training: anonymize PII
df_anonymized = anonymize_pii(df, fields=['insider_name'])
# insider_name → "INSIDER_00123"
```

### 4. Data Retention

- **Transaction Data**: 7 years (regulatory requirement)
- **Audit Logs**: 10 years
- **ML Models**: No PII stored in models
- **Development/Test Data**: Synthetic only, no real PII

## Compliance Framework

### Indonesian UU PDP (2022)

- ✅ Explicit consent for data collection
- ✅ Data minimization principle
- ✅ Right to access, rectify, delete
- ✅ Breach notification within 72 hours

### GDPR (for EU data subjects)

- ✅ Lawful basis for processing
- ✅ Data Protection Impact Assessment (DPIA)
- ✅ Privacy by design
- ✅ Right to be forgotten

### OJK Regulations

- ✅ Financial data security standards
- ✅ Audit trail requirements
- ✅ Incident response procedures

## User Rights

### 1. Right to Access

Users can request their data:

```
POST /api/v1/data/access-request
{
  "user_id": "insider_123",
  "email": "user@example.com"
}
```

### 2. Right to Deletion

Users can request data deletion:

```
POST /api/v1/data/deletion-request
{
  "user_id": "insider_123",
  "reason": "withdraw_consent"
}
```

### 3. Right to Rectification

Users can correct their data:

```
PATCH /api/v1/data/rectify
{
  "field": "insider_name",
  "old_value": "John Doe",
  "new_value": "John D."
}
```

## Anonymization Techniques

### For ML Training

```python
# Hash-based pseudonymization
import hashlib

def pseudonymize(name: str, salt: str) -> str:
    """Convert name to irreversible hash"""
    return hashlib.sha256(f"{name}{salt}".encode()).hexdigest()[:16]

# Example: "John Doe" → "a3f5bc9d2e8f1234"
```

### For Analytics

```python
# K-anonymity: Group data to prevent re-identification
df_anonymized = k_anonymize(df, k=5, quasi_identifiers=['company', 'role'])
```

## Incident Response

### Data Breach Procedure

1. **Detect**: Automated monitoring alerts
2. **Contain**: Immediately isolate affected systems
3. **Assess**: Determine scope and impact
4. **Notify**:
   - Authorities within 72 hours
   - Affected users within 5 days
5. **Remediate**: Fix vulnerability
6. **Review**: Post-incident analysis

### Contact

- **Data Protection Officer**: <dpo@sentinel-project.id>
- **Security Team**: <security@sentinel-project.id>
- **Emergency Hotline**: +62-XXX-XXXX-XXXX

## Developer Guidelines

### DO's

✅ Use parameterized queries
✅ Validate all inputs
✅ Log access to PII (audit trail)
✅ Encrypt PII fields
✅ Use synthetic data for testing
✅ Implement least privilege access

### DON'Ts

❌ Store plaintext PII
❌ Log PII in application logs
❌ Share PII in error messages
❌ Use production data in development
❌ Email PII without encryption
❌ Hard-code credentials

## Code Examples

### Secure Data Loading

```python
from sentinel.data.loaders import TransactionDataLoader
from sentinel.data.privacy import encrypt_pii, audit_log

loader = TransactionDataLoader()
df = loader.load_latest_synthetic()

# Encrypt PII before storage
df['insider_name_encrypted'] = df['insider_name'].apply(encrypt_pii)
df = df.drop('insider_name', axis=1)

# Audit trail
audit_log.info(f"Data loaded by {user_id} from {ip_address}")
```

### Secure API Response

```python
@app.get("/api/transactions/{id}")
@require_auth
def get_transaction(id: str, user: User):
    # Audit log
    audit_logger.info(f"User {user.id} accessed transaction {id}")

    transaction = db.get_transaction(id)

    # Mask PII for non-admin users
    if not user.is_admin:
        transaction['insider_name'] = mask_pii(transaction['insider_name'])
        # "John Doe" → "J*** D**"

    return transaction
```

## Testing

### PII Detection Tests

```python
def test_no_pii_in_logs():
    """Ensure logs don't contain PII"""
    log_content = read_logs()
    assert not contains_pii(log_content), "PII found in logs!"

def test_pii_encryption():
    """Verify PII is encrypted"""
    df = load_data()
    assert is_encrypted(df['insider_name_encrypted'])
```

## Audit Schedule

- **Monthly**: Access log review
- **Quarterly**: Security audit
- **Annually**: DPIA update
- **Ad-hoc**: After any security incident

## Updates

This policy is reviewed and updated quarterly or whenever:

- Regulations change
- New PII fields are added
- Security incidents occur
- Technology changes

---

**Version**: 1.0
**Effective Date**: 2025-12-29
**Next Review**: 2025-03-29

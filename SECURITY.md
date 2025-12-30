# Security Policy

## Supported Versions

Currently supported versions for security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do Not** Open a Public Issue

Please do not create a public GitHub issue for security vulnerabilities.

### 2. Report Privately

Send details to: **<security@yourproject.com>** (or create a private security advisory on GitHub)

Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

### 3. Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 7 days
  - High: 14 days
  - Medium: 30 days
  - Low: Next release

## Security Features

### Implemented Protections

- ✅ **Path Traversal Prevention**: File operations validate paths
- ✅ **Prompt Injection Protection**: Input sanitization blocks dangerous patterns
- ✅ **No Hardcoded Secrets**: All credentials via environment variables
- ✅ **Input Validation**: Comprehensive Pandera schemas
- ✅ **PII Handling**: GDPR/UU PDP compliant procedures

### Known Limitations

- Demo uses local Ollama (not for production without auth)
- ChromaDB data not encrypted by default
- No rate limiting on API endpoints (implement in production)

## Best Practices

When deploying SENTINEL:

1. **Use Environment Variables** for all secrets
2. **Enable Encryption** for ChromaDB persistence
3. **Implement Rate Limiting** on public endpoints
4. **Regular Security Audits** recommended quarterly
5. **Keep Dependencies Updated** (automated with Dependabot)

## Security Audit History

- **2024-12-29**: Initial red team assessment (25 findings, 2 CRITICAL fixed)
- Grade: A- (CRITICAL issues resolved)

## Disclosure Policy

- Responsible disclosure: 90 days before public disclosure
- Credit given to security researchers in CHANGELOG
- CVE assignment for significant vulnerabilities

---

**Last Updated**: 2024-12-29

# Security Policy

## Supported Versions

We provide security updates for the following versions of SOVD Server:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. **DO NOT** create a public GitHub issue

Report security vulnerabilities privately to avoid exposing users to risk.

### 2. Report via Email

Please send an email to the maintainers (e.g. **dev@sovd.org** or your project contact).

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes or mitigations
- Your contact information (optional)

### 3. What to Expect

- **Acknowledgment**: We will acknowledge receipt within 48 hours
- **Initial Assessment**: Within 5 business days
- **Updates**: We will keep you informed of progress
- **Resolution**: We will work to resolve the issue as quickly as possible

## Security Best Practices

### For Users
1. Keep the server and dependencies updated
2. Run SOVD Server in a controlled network environment
3. Restrict access to the server port (default: 8080)
4. Review and secure configuration files
5. Monitor logs for suspicious activity

### For Developers
1. Keep dependencies updated
2. Run security tools (e.g. bandit, safety) as part of CI
3. Validate and sanitize inputs
4. Avoid exposing sensitive information in errors or logs

## Security Tools

- **Bandit**: Static security analysis
- **Safety**: Dependency vulnerability scanning
- **Flake8**: Code quality and linting

## Contact

For security-related questions, use the contact information in the repository or create a private security advisory on GitHub.

# Contributing to NOAA Alerts Pushover

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the project's security guidelines

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/noaa-alerts-pushover.git
   cd noaa-alerts-pushover
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/k9barry/noaa-alerts-pushover.git
   ```

## Development Setup

### Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose (for testing containers)
- Git

### Setup Development Environment

1. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration**:
   ```bash
   cp config.txt.example config.txt
   # Edit config.txt with your test credentials
   ```

4. **Initialize database**:
   ```bash
   python models.py
   ```

5. **Validate setup**:
   ```bash
   python test_setup.py
   ```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation only
- `refactor/description` - Code refactoring

Example:
```bash
git checkout -b feature/add-email-notifications
```

### Commit Messages

Write clear, descriptive commit messages:

```
Short summary (50 chars or less)

More detailed explanation if needed. Wrap at 72 characters.
Explain the problem this commit solves and why you chose
this solution.

- Bullet points are okay
- Use present tense ("Add feature" not "Added feature")
- Reference issues: "Fixes #123"
```

Examples:
- ✅ `Add support for email notifications`
- ✅ `Fix database connection timeout issue`
- ✅ `Update README with Docker Compose examples`
- ❌ `Fixed stuff`
- ❌ `Updated files`

## Testing

### Before Submitting

1. **Validate syntax**:
   ```bash
   python -m py_compile *.py
   ```

2. **Test imports**:
   ```bash
   python -c "import fetch; import models; print('OK')"
   ```

3. **Run validation**:
   ```bash
   python test_setup.py
   ```

4. **Test functionality** (if you have credentials):
   ```bash
   python fetch.py --nopush --debug
   ```

5. **Test Docker build** (if Docker changes):
   ```bash
   docker-compose build
   ```

### Test Coverage Areas

When making changes, consider testing:

- **Configuration parsing**: Does it handle invalid configs?
- **County matching**: Does it correctly filter alerts?
- **API interactions**: Does it handle errors gracefully?
- **Database operations**: Does it prevent duplicates?
- **Notification sending**: Does it format messages correctly?

## Submitting Changes

### Pull Request Process

1. **Update your fork**:
   ```bash
   git fetch upstream
   git rebase upstream/master
   ```

2. **Push your changes**:
   ```bash
   git push origin your-branch-name
   ```

3. **Create Pull Request** on GitHub with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots (if UI changes)
   - Test results

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG.md updated (for significant changes)
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] Security implications considered

### Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Your contribution will be included in the next release

## Coding Standards

### Python Style

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines:

- Use 4 spaces for indentation (no tabs)
- Max line length: 100 characters
- Use descriptive variable names
- Add docstrings to functions and classes

Example:
```python
def fetch_alerts(county_codes):
    """
    Fetch weather alerts for specified counties.
    
    Args:
        county_codes (list): List of county FIPS codes
        
    Returns:
        list: List of Alert objects
    """
    # Implementation
    pass
```

### Code Quality

- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple, Stupid
- **Error Handling**: Always handle exceptions appropriately
- **Logging**: Use logging instead of print statements
- **Comments**: Explain "why", not "what"

### File Organization

```python
# Standard library imports
import os
import sys

# Third-party imports
import requests
import arrow

# Local imports
from models import Alert
```

### Docker Best Practices

- Keep images small
- Use multi-stage builds if needed
- Pin dependency versions
- Don't include secrets in images
- Use .dockerignore effectively

## Documentation

### What to Document

- **New Features**: Add to README.md and relevant guides
- **Configuration**: Update config examples
- **API Changes**: Update CODE_EXPLANATION.md
- **Breaking Changes**: Highlight in CHANGELOG.md

### Documentation Style

- Use Markdown formatting
- Include code examples
- Add screenshots for UI changes
- Keep language clear and concise
- Use bullet points and numbered lists

## Security

### Security-Sensitive Changes

If your contribution involves security:

1. Review [SECURITY.md](SECURITY.md)
2. Don't commit secrets or credentials
3. Use environment variables for sensitive data
4. Consider security implications
5. Report vulnerabilities privately (see SECURITY.md)

### Security Checklist

- [ ] No hardcoded credentials
- [ ] Secure API calls (HTTPS, timeouts)
- [ ] Input validation
- [ ] Proper error handling (don't leak info)
- [ ] Dependencies are up-to-date

## Ideas for Contributions

### Good First Issues

- Documentation improvements
- Adding more event types to filter
- Improving error messages
- Adding more examples
- Fixing typos

### Feature Ideas

- Web interface for configuration
- Additional notification channels
- Alert severity filtering
- Multiple Pushover users
- Alert history viewer
- Statistics and reporting

### Improvements

- Better test coverage
- Performance optimizations
- Code refactoring
- Improved logging
- Better error handling

## Getting Help

### Resources

- [CODE_EXPLANATION.md](CODE_EXPLANATION.md) - Technical architecture
- [INSTALL.md](INSTALL.md) - Setup and troubleshooting
- [SECURITY.md](SECURITY.md) - Security guidelines
- [GitHub Issues](https://github.com/k9barry/noaa-alerts-pushover/issues) - Ask questions

### Communication

- **Questions**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions (if enabled)
- **Security**: Follow SECURITY.md reporting process

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be:
- Listed in CHANGELOG.md for significant contributions
- Credited in release notes
- Acknowledged in the project README

## Thank You!

Your contributions help make this project better for everyone. Whether it's code, documentation, bug reports, or ideas - all contributions are valued and appreciated!

---

**Questions?** Open an issue or reach out through GitHub.

# Contributing to NOAA Alerts Pushover

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Creating Releases](#creating-releases)
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

### Running the Test Suite

The project uses pytest for automated testing. **Always run tests before submitting a PR.**

1. **Run all tests**:
   ```bash
   python -m pytest tests/ -v
   ```

2. **Run tests with coverage**:
   ```bash
   python -m pytest tests/ --cov=. --cov-report=html
   ```

3. **Run specific test file**:
   ```bash
   python -m pytest tests/test_parser.py -v
   ```

See [tests/README.md](tests/README.md) for comprehensive testing documentation.

### Before Submitting

1. **Run the test suite** ✅ **REQUIRED**:
   ```bash
   python -m pytest tests/ -v
   ```
   All tests must pass before submitting a PR.

2. **Validate syntax**:
   ```bash
   python -m py_compile *.py
   ```

3. **Test imports**:
   ```bash
   python -c "import fetch; import models; print('OK')"
   ```

4. **Run validation**:
   ```bash
   python test_setup.py
   ```

5. **Test functionality** (if you have credentials):
   ```bash
   python fetch.py --nopush --debug
   ```

6. **Test Docker build** (if Docker changes):
   ```bash
   docker compose build
   ```

### Writing Tests

When adding new features, **write tests** to cover your changes:

- Place tests in the `tests/` directory
- Follow the naming convention: `test_*.py`
- Use descriptive test names
- Mock external API calls using `responses` library
- See [tests/README.md](tests/README.md) for examples

Example:
```python
import pytest
from fetch import Parser

def test_new_feature():
    """Test that new feature works correctly"""
    parser = Parser("token", "user", "api_url", "noaa_url", ".", None)
    result = parser.new_method()
    assert result == expected_value
```

### Test Coverage Areas

When making changes, consider testing:

- **Configuration parsing**: Does it handle invalid configs?
- **County matching**: Does it correctly filter alerts?
- **API interactions**: Does it handle errors gracefully?
- **Database operations**: Does it prevent duplicates?
- **Notification sending**: Does it format messages correctly?
- **Input validation**: Does it validate FIPS/UGC codes correctly?
- **Error handling**: Do custom exceptions work as expected?
- **Rate limiting**: Does it respect API rate limits?

### Current Test Coverage

The project has 13+ automated tests covering:
- Parser class methods
- County code validation
- API request handling
- Error scenarios (timeouts, invalid JSON)
- Pushover notification sending

See the CI/CD workflow (`.github/workflows/ci.yml`) for automated test execution.

## Submitting Changes

### Pull Request Process

1. **Update your fork**:
   ```bash
   git fetch upstream
   git rebase upstream/main
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
   - **Version bump label** (see Automatic Versioning below)

### Automatic Versioning

When your PR is merged to main, a new version is **automatically created** based on labels:

**Version Bump Labels** (add one to your PR):
- `major` or `breaking` - Breaking changes (e.g., 2.2.0 → 3.0.0)
- `minor` or `feature` - New features, backward compatible (e.g., 2.2.0 → 2.3.0)
- `patch` or `bugfix` or `fix` - Bug fixes (e.g., 2.2.0 → 2.2.1)

**If no label is added, the default is `patch`.**

**What happens automatically:**
1. Version number is calculated based on the label
2. CHANGELOG.md is updated with your PR information
3. Git tag is created (e.g., `v2.3.0`)
4. GitHub Release is created
5. Docker Hub images are built and published automatically

**Example:**
- PR titled "Add email notification support" with label `minor`
- Merges → Auto-creates version 2.3.0 → Builds Docker images

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] **All tests pass** (`python -m pytest tests/ -v`) ✅ **REQUIRED**
- [ ] New tests added for new features (if applicable)
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG.md updated (for significant changes)
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] Security implications considered
- [ ] **Version bump label added** (`major`, `minor`, or `patch`)

### Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Your contribution will be included in the next release

## Creating Releases

### Automatic Versioning (Default Method)

**New PRs automatically create versions when merged!** Just add the appropriate label (`major`, `minor`, or `patch`) to your PR before merging.

The workflow automatically:
- ✅ Calculates the new version number
- ✅ Updates CHANGELOG.md
- ✅ Creates the Git tag
- ✅ Creates a GitHub Release
- ✅ Triggers Docker Hub image build

See "Automatic Versioning" section above for details.

### Manual Release Creation (For Maintainers)

For complete instructions on versioning and releases, see:
- [docs/AUTO_VERSIONING.md](docs/AUTO_VERSIONING.md) - Complete automatic versioning guide
- [docs/VERSIONING_QUICK_REFERENCE.md](docs/VERSIONING_QUICK_REFERENCE.md) - Quick reference

**Manual methods (when needed):**

1. Use GitHub Actions workflow "Create Release" (`.github/workflows/release.yml`), or
2. Create tags manually with `git tag -a v2.X.Y -m "Release version 2.X.Y"`
3. Always follow [Semantic Versioning](https://semver.org/): Major.Minor.Patch

### Container Registry Publishing

The repository includes automated container image publishing to multiple registries via GitHub Actions.

#### Docker Hub Publishing

**For complete setup instructions**, see [docs/DOCKER_HUB_SETUP.md](docs/DOCKER_HUB_SETUP.md)

**Quick Overview:**
- **Workflow**: `.github/workflows/docker-publish.yml`
- **Triggers**:
  - Push to `main` branch → publishes `latest` tag
  - Git tag push (e.g., `v2.2.0`) → publishes version tags (`2.2.0`, `2.2`, `2`)
  - Manual workflow dispatch
- **Requirements**: Docker Hub credentials must be set as repository secrets:
  - `DOCKERHUB_USERNAME` - Your Docker Hub username
  - `DOCKERHUB_TOKEN` - Docker Hub access token (not password)
- **Multi-platform**: Images are built for `linux/amd64` and `linux/arm64`

**To publish to Docker Hub:**
1. Create and push a Git tag using the release workflow
2. The docker-publish workflow automatically builds and pushes to Docker Hub
3. Verify the image at https://hub.docker.com/r/DOCKERHUB_USERNAME/noaa-alerts-pushover

#### GitHub Container Registry (GHCR) Publishing

**For complete setup instructions**, see [docs/GHCR_SETUP.md](docs/GHCR_SETUP.md)

**Quick Overview:**
- **Workflow**: `.github/workflows/ghcr-publish.yml`
- **Triggers**:
  - Push to `main` branch → publishes `latest` tag
  - Git tag push (e.g., `v2.2.0`) → publishes version tags (`2.2.0`, `2.2`, `2`)
  - Manual workflow dispatch
- **Requirements**: No additional setup required (uses built-in `GITHUB_TOKEN`)
- **Multi-platform**: Images are built for `linux/amd64` and `linux/arm64`
- **Advantages**: 
  - No external credentials needed
  - Automatic authentication
  - Free for public repositories
  - Integrated with GitHub

**To publish to GHCR:**
1. Create and push a Git tag using the release workflow
2. The ghcr-publish workflow automatically builds and pushes to GHCR
3. Verify the image in the repository's Packages tab

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
- **API Changes**: Update docs/CODE_EXPLANATION.md
- **Breaking Changes**: Highlight in CHANGELOG.md

### Documentation Organization

**Important**: All detailed documentation files should be placed in the `docs/` folder to keep the repository root clean and organized.

- **Root directory**: Keep only essential files (README.md, INSTALL.md, CHANGELOG.md, CONTRIBUTING.md, SECURITY.md, LICENSE)
- **docs/ directory**: Place all other documentation files here
  - Technical guides (CODE_EXPLANATION.md, AUTO_VERSIONING.md, etc.)
  - Setup guides (DOCKER_HUB_SETUP.md, GHCR_SETUP.md, etc.)
  - Quick reference guides (DOCKER_HUB_QUICKSTART.md, GHCR_QUICKSTART.md, VERSIONING_QUICK_REFERENCE.md, etc.)
  - Implementation summaries and workflow documentation

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

- [CODE_EXPLANATION.md](docs/CODE_EXPLANATION.md) - Technical architecture
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

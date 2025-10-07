# Quick Start: Creating Tags

This repository now has automated tools for creating Git tags based on CHANGELOG.md.

## For Maintainers

### Quick Method: GitHub Actions (Recommended)

1. Go to **Actions** tab on GitHub
2. Select **"Create Release"** workflow
3. Click **"Run workflow"**
4. Enter version number (e.g., `2.2.0`)
5. ✅ Done! Tag and release created automatically

### Alternative: Manual Git Commands

```bash
# Create an annotated tag
git tag -a v2.2.0 -m "Release version 2.2.0"

# Push the tag
git push origin v2.2.0
```

Then create the GitHub Release manually through the web interface.

### What Gets Created

For version `2.2.0`, the GitHub Actions workflow will:
- ✅ Create Git tag `v2.2.0`
- ✅ Extract release notes from CHANGELOG.md
- ✅ Create GitHub Release with notes
- ✅ Push to remote repository

## Current Versions

Based on CHANGELOG.md:
- **v2.2.0** - Documentation improvements, enhanced setup validation (latest)
- **v2.1.0** - Removed XML dependencies, JSON parsing
- **v2.0.0** - Python 3 migration, Docker support, security improvements

## Full Documentation

See [TAGGING.md](TAGGING.md) for complete documentation including:
- Detailed workflow instructions
- Manual tagging process
- Troubleshooting guide
- Best practices for releases
- Version numbering guidelines

## Questions?

Check [CONTRIBUTING.md](../CONTRIBUTING.md) section "Creating Releases" for full details.

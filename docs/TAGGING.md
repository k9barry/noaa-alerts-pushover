# Creating Tags and Releases

This document explains how to create Git tags and GitHub releases for this project.

## Overview

Tags are created based on versions documented in `CHANGELOG.md`. Each version in the CHANGELOG should correspond to a Git tag in the format `vX.Y.Z` (e.g., `v2.2.0`).

## Methods

There are three ways to create tags:

### 1. GitHub Actions Workflow (Recommended)

The easiest and most consistent method:

1. Go to the **Actions** tab on GitHub
2. Select **"Create Release"** workflow
3. Click **"Run workflow"**
4. Enter the version number (e.g., `2.2.0`)
5. Click **"Run workflow"**

The workflow will:
- ✅ Validate the version exists in CHANGELOG.md
- ✅ Extract release notes automatically
- ✅ Create the Git tag
- ✅ Create a GitHub Release with notes
- ✅ Push everything to the repository

**Workflow file:** `.github/workflows/release.yml`

### 2. Using the create_tags.sh Script

A bash script for creating multiple tags locally:

**Interactive mode** (prompts for each version):
```bash
./create_tags.sh
```

**Automatic mode** (creates all tags):
```bash
./create_tags.sh --auto
```

**Specific version only**:
```bash
./create_tags.sh --version 2.2.0
```

**Features:**
- Extracts versions from CHANGELOG.md automatically
- Checks for existing tags to avoid duplicates
- Color-coded output for easy reading
- Option to push tags after creation
- Validates working directory state

### 3. Manual Git Commands

For direct control:

```bash
# 1. Ensure you're on the latest master
git checkout master
git pull origin master

# 2. Create an annotated tag
git tag -a v2.2.0 -m "Release version 2.2.0"

# 3. Push the tag
git push origin v2.2.0

# Or push all tags at once
git push origin --tags
```

Then create the GitHub Release manually through the web interface.

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):

- **Major (X.0.0)**: Breaking changes
  - Example: `v2.0.0` - Python 3 migration
- **Minor (X.Y.0)**: New features (backward compatible)
  - Example: `v2.1.0` - Removed XML dependencies
  - Example: `v2.2.0` - Documentation improvements
- **Patch (X.Y.Z)**: Bug fixes (backward compatible)
  - Example: `v2.2.1` - Fix configuration bug

## Current Versions

Based on CHANGELOG.md:

| Version | Description | Status |
|---------|-------------|--------|
| 2.2.0 | Documentation improvements, enhanced setup validation | Latest |
| 2.1.0 | Removed XML dependencies, JSON parsing | Previous |
| 2.0.0 | Python 3 migration, Docker support, security improvements | Previous |

## Creating Tags for Historical Versions

If you need to tag versions that are already in CHANGELOG.md but don't have tags:

**Option 1: Use the script**
```bash
# Interactive - prompts for each version
./create_tags.sh

# Automatic - creates all missing tags
./create_tags.sh --auto
```

**Option 2: Manual process**

1. Find the commit for each version:
   ```bash
   git log --oneline --all | grep "Version"
   ```

2. Create tags pointing to those commits:
   ```bash
   git tag -a v2.0.0 <commit-sha> -m "Release version 2.0.0"
   git tag -a v2.1.0 <commit-sha> -m "Release version 2.1.0"
   git tag -a v2.2.0 <commit-sha> -m "Release version 2.2.0"
   ```

3. Push all tags:
   ```bash
   git push origin --tags
   ```

4. Create GitHub Releases for each tag through the web interface

## After Creating Tags

### Verify Tags

```bash
# List all tags
git tag -l

# Show tag details
git show v2.2.0

# List remote tags
git ls-remote --tags origin
```

### Create GitHub Releases

For each tag, create a GitHub Release:

1. Go to repository → **Releases** → **Draft a new release**
2. Select the tag you created
3. Use the version as the release title (e.g., "Version 2.2.0")
4. Copy the relevant section from CHANGELOG.md as the release notes
5. Click **Publish release**

### Verify Docker Hub Image

After creating a tag, the Docker Hub workflow automatically builds and publishes the image:

```bash
# Wait a few minutes for the workflow to complete, then test
docker pull k9barry/noaa-alerts-pushover:v2.2.0
docker pull k9barry/noaa-alerts-pushover:2.2
docker pull k9barry/noaa-alerts-pushover:latest

# Verify the image runs
docker run --rm k9barry/noaa-alerts-pushover:v2.2.0 python --version
```

Check workflow status: **Actions** → **Build and Push to Docker Hub**

### Announce the Release

- Update project README.md if needed
- Notify users through appropriate channels
- Confirm Docker Hub image is available at https://hub.docker.com/r/k9barry/noaa-alerts-pushover

## Troubleshooting

### Tag Already Exists

If you get an error that a tag already exists:

```bash
# Delete local tag
git tag -d v2.2.0

# Delete remote tag (be careful!)
git push origin :refs/tags/v2.2.0

# Recreate the tag
git tag -a v2.2.0 -m "Release version 2.2.0"
git push origin v2.2.0
```

### Wrong Commit Tagged

If you tagged the wrong commit:

```bash
# Delete the tag locally and remotely
git tag -d v2.2.0
git push origin :refs/tags/v2.2.0

# Create tag on correct commit
git tag -a v2.2.0 <correct-commit-sha> -m "Release version 2.2.0"
git push origin v2.2.0
```

### Version Not in CHANGELOG

If the version isn't in CHANGELOG.md:

1. Add the version to CHANGELOG.md with proper format:
   ```markdown
   ## Version X.Y.Z - YYYY
   
   ### Changes
   - Change description
   ```
2. Commit the CHANGELOG update
3. Then create the tag on that commit

## Best Practices

1. **Always update CHANGELOG.md first** before creating tags
2. **Use annotated tags** (`git tag -a`) not lightweight tags
3. **Follow semantic versioning** for version numbers
4. **Test the release** before tagging (use `--nopush` or test in Docker)
5. **Write clear release notes** that help users understand changes
6. **Include migration instructions** for breaking changes
7. **Tag from master branch** (or main release branch)
8. **Don't force push** tags - delete and recreate if needed

## For Maintainers

### Release Checklist

- [ ] All changes merged to master
- [ ] CHANGELOG.md updated with version and changes
- [ ] Version number follows semantic versioning
- [ ] Documentation updated (README, INSTALL, etc.)
- [ ] All tests pass (CI/CD green)
- [ ] Docker build succeeds
- [ ] Configuration examples up-to-date
- [ ] Create the tag using preferred method
- [ ] Create GitHub Release with notes
- [ ] Verify Docker Hub image published successfully
- [ ] Test Docker Hub image: `docker pull k9barry/noaa-alerts-pushover:vX.Y.Z`
- [ ] Announce the release
- [ ] Update any external documentation/websites

## Examples

### Example 1: Create v2.2.0 Using GitHub Actions

1. Ensure CHANGELOG.md has:
   ```markdown
   ## Version 2.2.0 - 2024
   
   ### 📝 Documentation Improvements
   ...
   ```

2. Go to Actions → Create Release → Run workflow
3. Enter: `2.2.0`
4. Click "Run workflow"
5. ✅ Done! Tag and release created automatically

### Example 2: Create Multiple Tags with Script

```bash
# Review what versions will be tagged
grep "## Version" CHANGELOG.md

# Run script in interactive mode
./create_tags.sh

# Follow prompts:
# - Create tag v2.0.0? (y/N) y
# - Create tag v2.1.0? (y/N) y
# - Create tag v2.2.0? (y/N) y
# - Push tags to origin? (y/N) y

# ✅ All tags created and pushed
```

### Example 3: Quick Tag for Current Version

```bash
# Create and push tag for latest version
git tag -a v2.2.0 -m "Release version 2.2.0"
git push origin v2.2.0

# Create GitHub Release through web UI
# ✅ Done!
```

## Additional Resources

- [Semantic Versioning](https://semver.org/)
- [Git Tagging Documentation](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
- [GitHub Releases Documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [Contributing Guide](../CONTRIBUTING.md)
- [Changelog](../CHANGELOG.md)

## Questions?

If you have questions about tagging or releases:
- Check [CONTRIBUTING.md](../CONTRIBUTING.md)
- Open an issue on GitHub
- Contact the maintainers

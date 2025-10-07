# Automatic Versioning

This project uses **automatic semantic versioning** when Pull Requests are merged to the main branch.

## How It Works

When a PR is merged to main:
1. The auto-versioning workflow is triggered
2. It reads the PR labels to determine the version bump type
3. Calculates the new version number
4. Updates CHANGELOG.md with the PR information
5. Creates a Git tag (e.g., `v2.3.0`)
6. Creates a GitHub Release
7. Triggers the Docker Hub workflow to build and publish images

## PR Labels for Version Bumping

Add **one** of these labels to your PR to control the version bump:

| Label | Type | Example | When to Use |
|-------|------|---------|-------------|
| `major` or `breaking` | Major | 2.2.0 → 3.0.0 | Breaking changes, API changes |
| `minor` or `feature` | Minor | 2.2.0 → 2.3.0 | New features (backward compatible) |
| `patch` or `bugfix` or `fix` | Patch | 2.2.0 → 2.2.1 | Bug fixes, minor improvements |

**Default:** If no label is added, the workflow defaults to a **patch** bump.

## Semantic Versioning Rules

This project follows [Semantic Versioning 2.0.0](https://semver.org/):

Given a version number **MAJOR.MINOR.PATCH** (e.g., 2.3.1):

- **MAJOR** version: Incompatible API changes or breaking changes
- **MINOR** version: New functionality in a backward compatible manner
- **PATCH** version: Backward compatible bug fixes

## Example Scenarios

### Example 1: Bug Fix
```
Current version: 2.2.0
PR: "Fix database connection timeout"
Label: patch (or fix, bugfix)
Result: v2.2.1
```

### Example 2: New Feature
```
Current version: 2.2.1
PR: "Add email notification support"
Label: minor (or feature)
Result: v2.3.0
```

### Example 3: Breaking Change
```
Current version: 2.3.0
PR: "Migrate to Python 3.12+ only"
Label: major (or breaking)
Result: v3.0.0
```

### Example 4: No Label (Default)
```
Current version: 2.3.0
PR: "Update documentation"
Label: (none)
Result: v2.3.1 (defaults to patch)
```

## Workflow Details

### Workflow File
`.github/workflows/auto-version.yml`

### Triggers
- Event: Pull Request closed
- Condition: PR was merged (not just closed)
- Branch: main

### Process

1. **Determine Bump Type**
   - Reads PR labels
   - Maps to major/minor/patch
   - Defaults to patch if no label

2. **Get Current Version**
   - Checks latest Git tag matching `v*.*.*`
   - Falls back to CHANGELOG.md if no tags exist
   - Defaults to 2.2.0 if neither exist

3. **Calculate New Version**
   - Increments appropriate version component
   - Resets lower components (e.g., minor bump resets patch to 0)

4. **Update CHANGELOG.md**
   - Inserts new version section at top
   - Includes PR title, number, and author
   - Uses current date

5. **Commit and Tag**
   - Commits CHANGELOG.md update
   - Creates annotated Git tag
   - Pushes both to repository

6. **Create GitHub Release**
   - Uses the new tag
   - Includes PR information
   - Links to full changelog

7. **Trigger Docker Build**
   - Tag push automatically triggers `docker-publish.yml`
   - Builds multi-platform images
   - Publishes to Docker Hub with version tags

## Manual Override

If you need to create a version manually (bypassing the auto-versioning):

1. **Close the PR without merging**, or
2. **Use the manual release workflow**:
   - Go to Actions → "Create Release"
   - Enter desired version
   - Run workflow

## Disabling Auto-Versioning

If you need to merge a PR **without** creating a new version:

1. Add the label `skip-release` or `no-version` to the PR, **OR**
2. Merge to a different branch first, then cherry-pick to main

> **Note:** The `skip-release` functionality is not yet implemented. This is a placeholder for future enhancement.

## Troubleshooting

### Issue: Wrong version created

**Solution:** 
- Delete the tag: `git tag -d vX.Y.Z && git push origin :refs/tags/vX.Y.Z`
- Revert the CHANGELOG commit
- Create the correct version manually

### Issue: PR merged but no version created

**Possible causes:**
1. Workflow failed - Check Actions tab for errors
2. Permissions issue - Verify GITHUB_TOKEN has write access
3. PR was closed without merging

**Solution:** Check the workflow run in the Actions tab for details.

### Issue: Multiple versions created

**Cause:** Multiple PRs merged simultaneously

**Solution:** Git tags are unique, so only one will succeed. Check which version was created and adjust manually if needed.

### Issue: CHANGELOG.md merge conflicts

**Cause:** Multiple PRs updating CHANGELOG simultaneously

**Solution:** 
1. Resolve conflicts manually
2. Push the resolution
3. Re-run the workflow if needed

## Best Practices

1. **Always add a version label** to your PRs for clarity
2. **Use descriptive PR titles** - they appear in CHANGELOG
3. **Review the auto-generated changelog** after merge
4. **Test Docker images** after automatic release
5. **Document breaking changes** clearly in PR description

## Integration with Container Registries

The auto-versioning workflow integrates seamlessly with container registry publishing:

1. Auto-version creates tag `v2.3.0`
2. Tag push triggers both:
   - `.github/workflows/docker-publish.yml` (Docker Hub)
   - `.github/workflows/ghcr-publish.yml` (GitHub Container Registry)
3. Docker images are built for multiple platforms
4. Images are tagged as:
   - **Docker Hub**: `k9barry/noaa-alerts-pushover:2.3.0`, `2.3`, `2`, `latest`
   - **GHCR**: `ghcr.io/k9barry/noaa-alerts-pushover:2.3.0`, `2.3`, `2`, `latest`

## Related Documentation

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [VERSIONING_QUICK_REFERENCE.md](VERSIONING_QUICK_REFERENCE.md) - Quick reference for contributors
- [DOCKER_HUB_SETUP.md](DOCKER_HUB_SETUP.md) - Docker Hub publishing
- [GHCR_SETUP.md](GHCR_SETUP.md) - GitHub Container Registry publishing
- [CHANGELOG.md](../CHANGELOG.md) - Version history
- [WORKFLOW_DIAGRAM.md](WORKFLOW_DIAGRAM.md) - Visual guide to versioning workflows

## Questions?

If you have questions about automatic versioning:
- Check the workflow runs in the Actions tab
- Review the auto-generated CHANGELOG entries
- Open an issue for workflow improvements
- Contact the maintainers

---

**Workflow:** `.github/workflows/auto-version.yml`  
**Last Updated:** 2024  
**Status:** Active

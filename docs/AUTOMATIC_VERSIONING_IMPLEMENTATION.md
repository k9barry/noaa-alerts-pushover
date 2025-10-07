# Automatic Versioning Implementation

## Problem Statement

**Question:** Does the Build and Push to Docker Hub workflow create a new tag number when a PR is approved? If it does not, can it be made to do so, with the tag increasing either major or minor depending on the change?

**Answer:** The Docker Hub workflow previously only reacted to manually created tags. It has now been enhanced with an **automatic versioning system** that creates new version tags when PRs are merged, with the version bump type controlled by PR labels.

## Solution Overview

The solution implements a complete automatic versioning system that:
1. Triggers on PR merge to main
2. Reads PR labels to determine version bump type
3. Automatically creates version tags using semantic versioning
4. Triggers Docker Hub image builds automatically
5. Provides comprehensive documentation and tooling

## Implementation Details

### 1. Automatic Versioning Workflow

**File:** `.github/workflows/auto-version.yml`

**Trigger:** Pull request closed (merged to main)

**Process:**
1. **Check if merged** - Only runs if PR was actually merged (not just closed)
2. **Determine bump type** - Reads PR labels:
   - `major` or `breaking` → Major version bump (X.0.0)
   - `minor` or `feature` → Minor version bump (0.X.0)
   - `patch`, `bugfix`, or `fix` → Patch version bump (0.0.X)
   - No label → Defaults to patch bump
3. **Get current version** - Checks:
   - Latest Git tag matching `v*.*.*` pattern
   - Falls back to CHANGELOG.md if no tags exist
   - Defaults to 2.2.0 if neither exist
4. **Calculate new version** - Uses semantic versioning rules:
   - Major bump: Increments major, resets minor and patch to 0
   - Minor bump: Increments minor, resets patch to 0
   - Patch bump: Increments patch only
5. **Update CHANGELOG.md** - Inserts new version section with:
   - Version number and date
   - PR title, number, and author
6. **Commit and tag** - Creates:
   - Git commit with CHANGELOG update
   - Annotated Git tag (e.g., `v2.3.0`)
   - Pushes both to repository
7. **Create GitHub Release** - Automatically creates release with:
   - Version tag
   - PR information
   - Link to full changelog
8. **Trigger Docker build** - Tag push automatically triggers `docker-publish.yml`

### 2. Label Configuration

**File:** `.github/labels.yml`

Defines labels for version bumping:
- `major`, `breaking` - Red (breaking changes)
- `minor`, `feature` - Green (new features)
- `patch`, `bugfix`, `fix` - Yellow (bug fixes)
- Additional labels for documentation, dependencies, etc.

**File:** `.github/workflows/sync-labels.yml`

Automatically syncs labels to the repository when `labels.yml` is updated.

### 3. Pull Request Template

**File:** `.github/pull_request_template.md`

Guides contributors to:
- Choose appropriate version bump label
- Follow checklist for quality
- Understand automatic versioning behavior

### 4. Documentation

**New Documentation Files:**
- `docs/AUTO_VERSIONING.md` - Complete guide with examples (6KB)
- `docs/VERSIONING_QUICK_REFERENCE.md` - Quick reference for contributors (2.8KB)

**Updated Documentation:**
- `CONTRIBUTING.md` - Added automatic versioning section
- `README.md` - Added note about automatic versioning
- `docs/AUTO_VERSIONING.md` - Complete automatic versioning guide
- `docs/VERSIONING_QUICK_REFERENCE.md` - Quick reference for contributors
- `docs/DOCKER_HUB_SETUP.md` - Added auto-versioning trigger info

## Usage Examples

### Example 1: Bug Fix (Patch Bump)

**Scenario:** Fix database connection timeout

**Steps:**
1. Create PR with changes
2. Add label: `patch` (or `bugfix`, `fix`)
3. Get PR approved and merge
4. **Result:** Version automatically bumps from 2.2.0 → 2.2.1

**What happens:**
- ✅ CHANGELOG updated with "Fix database connection timeout (#123)"
- ✅ Tag `v2.2.1` created
- ✅ GitHub Release created
- ✅ Docker images built:
  - `k9barry/noaa-alerts-pushover:2.2.1`
  - `k9barry/noaa-alerts-pushover:2.2`
  - `k9barry/noaa-alerts-pushover:2`
  - `k9barry/noaa-alerts-pushover:latest`

### Example 2: New Feature (Minor Bump)

**Scenario:** Add email notification support

**Steps:**
1. Create PR with changes
2. Add label: `minor` (or `feature`)
3. Get PR approved and merge
4. **Result:** Version automatically bumps from 2.2.1 → 2.3.0

**What happens:**
- ✅ CHANGELOG updated with "Add email notification support (#124)"
- ✅ Tag `v2.3.0` created
- ✅ GitHub Release created
- ✅ Docker images built with version 2.3.0

### Example 3: Breaking Change (Major Bump)

**Scenario:** Require Python 3.12+ only

**Steps:**
1. Create PR with changes
2. Add label: `major` (or `breaking`)
3. Get PR approved and merge
4. **Result:** Version automatically bumps from 2.3.0 → 3.0.0

**What happens:**
- ✅ CHANGELOG updated with "Require Python 3.12+ only (#125)"
- ✅ Tag `v3.0.0` created
- ✅ GitHub Release created
- ✅ Docker images built with version 3.0.0

### Example 4: No Label (Default Behavior)

**Scenario:** Update documentation

**Steps:**
1. Create PR with changes
2. Forget to add label (or intentionally skip it)
3. Get PR approved and merge
4. **Result:** Version automatically bumps from 2.3.0 → 2.3.1 (defaults to patch)

## Integration with Container Registries

The automatic versioning workflow integrates seamlessly with container registry publishing workflows:

1. **Auto-version workflow creates tag** (e.g., `v2.3.0`)
2. **Tag push triggers both publishing workflows** (via `push.tags` trigger):
   - `.github/workflows/docker-publish.yml` (Docker Hub)
   - `.github/workflows/ghcr-publish.yml` (GitHub Container Registry)
3. **Docker metadata action generates tags**:
   - Full version: `2.3.0`
   - Major.minor: `2.3`
   - Major only: `2`
   - Latest: `latest` (if on main)
4. **Multi-platform images built** (linux/amd64, linux/arm64)
5. **Images pushed to registries** with all generated tags:
   - Docker Hub: `k9barry/noaa-alerts-pushover:*`
   - GHCR: `ghcr.io/k9barry/noaa-alerts-pushover:*`

## Workflow Diagram

```
PR Created → Add Label (major/minor/patch) → PR Merged
                                                  ↓
                                    auto-version.yml triggered
                                                  ↓
                           Read label → Calculate version
                                                  ↓
                              Update CHANGELOG.md → Commit
                                                  ↓
                                    Create Git tag (v2.3.0)
                                                  ↓
                              Push commit and tag to GitHub
                                                  ↓
                            Create GitHub Release (v2.3.0)
                                                  ↓
                    Tag push triggers publishing workflows
                                                  ↓
                          Build multi-platform Docker images
                                                  ↓
            Push to Docker Hub and GHCR with version tags
                                                  ↓
                                                Done!
```

## Semantic Versioning Rules

Given version **MAJOR.MINOR.PATCH** (e.g., 2.3.1):

- **MAJOR**: Incompatible API changes, breaking changes
  - Example: 2.3.1 → 3.0.0
  - Resets minor and patch to 0
  
- **MINOR**: New functionality, backward compatible
  - Example: 2.3.1 → 2.4.0
  - Resets patch to 0
  
- **PATCH**: Bug fixes, backward compatible
  - Example: 2.3.1 → 2.3.2
  - Only increments patch

## Benefits

### For Contributors
- ✅ No manual version management needed
- ✅ Simple label-based control
- ✅ Immediate feedback via GitHub Release
- ✅ Clear versioning guidelines

### For Maintainers
- ✅ Consistent versioning across all releases
- ✅ Automatic CHANGELOG maintenance
- ✅ Reduced manual work
- ✅ Clear audit trail via Git tags

### For Users
- ✅ Regular, predictable releases
- ✅ Clear version numbering
- ✅ Easy to track changes
- ✅ Automated Docker image availability

## Troubleshooting

### Issue: Wrong version created

**Cause:** Incorrect label on PR

**Solution:**
1. Delete the tag: `git tag -d vX.Y.Z`
2. Delete remote tag: `git push origin :refs/tags/vX.Y.Z`
3. Revert CHANGELOG commit
4. Manually create correct version

### Issue: Workflow failed

**Cause:** Various (check Actions logs)

**Solution:**
1. Go to Actions tab
2. Check "Auto Version on PR Merge" workflow
3. Review error logs
4. Fix issue and re-run if needed

### Issue: Multiple PRs merged simultaneously

**Cause:** Race condition

**Solution:**
- Only one will succeed (tags are unique)
- Check which version was created
- Manually adjust if needed

### Issue: CHANGELOG merge conflict

**Cause:** Multiple version updates

**Solution:**
- Resolve conflicts manually
- Commit resolution
- Re-run workflow if needed

## Manual Override

If you need to bypass automatic versioning:

1. **Merge without creating version**: Not yet implemented (future enhancement)
2. **Create manual version**: Use `.github/workflows/release.yml`
3. **Fix incorrect version**: Delete tag and recreate manually

## Testing

The implementation has been validated:
- ✅ All YAML files validated with Python yaml parser
- ✅ CHANGELOG update logic tested with sample data
- ✅ Workflow trigger conditions verified
- ✅ Documentation cross-references checked
- ✅ Python syntax validation passed

## Future Enhancements

Potential improvements:
1. **Skip release label** - Add `skip-release` label to merge without versioning
2. **Version validation** - Ensure version doesn't already exist
3. **Pre-release versions** - Support alpha/beta/rc tags
4. **Changelog categories** - Group changes by type (features, fixes, etc.)
5. **Custom version format** - Support alternative versioning schemes

## Related Files

### Workflows
- `.github/workflows/auto-version.yml` - Main auto-versioning workflow
- `.github/workflows/docker-publish.yml` - Docker Hub publishing (triggered by tags)
- `.github/workflows/ghcr-publish.yml` - GitHub Container Registry publishing (triggered by tags)
- `.github/workflows/release.yml` - Manual release creation (fallback)
- `.github/workflows/sync-labels.yml` - Label synchronization

### Configuration
- `.github/labels.yml` - Label definitions
- `.github/pull_request_template.md` - PR template

### Documentation
- `docs/AUTO_VERSIONING.md` - Complete automatic versioning guide
- `docs/VERSIONING_QUICK_REFERENCE.md` - Quick reference for contributors
- `docs/WORKFLOW_DIAGRAM.md` - Visual guide to versioning workflows
- `docs/DOCKER_HUB_SETUP.md` - Docker Hub setup
- `docs/GHCR_SETUP.md` - GitHub Container Registry setup
- `CONTRIBUTING.md` - Contribution guidelines
- `README.md` - Project overview

## Conclusion

The automatic versioning system fully addresses the original problem statement by:

1. ✅ **Automatically creating new version tags** when PRs are merged to main
2. ✅ **Controlling version bump type** (major/minor/patch) via PR labels
3. ✅ **Triggering container registry builds** automatically with new version tags
4. ✅ **Following semantic versioning** best practices
5. ✅ **Providing comprehensive documentation** for contributors and maintainers
6. ✅ **Publishing to multiple registries** (Docker Hub and GitHub Container Registry)

The implementation is robust, well-documented, and ready for production use.

---

**Implementation Date:** 2024-10-06  
**Workflow Files:** `.github/workflows/auto-version.yml`, `.github/workflows/sync-labels.yml`  
**Status:** Active and ready for use

# Versioning Quick Reference

## For Contributors

### Adding the Right Label to Your PR

Before merging, add **one** of these labels:

| Change Type | Labels | Version Bump | Example |
|------------|--------|--------------|---------|
| 🐛 Bug fix | `patch`, `bugfix`, `fix` | 2.2.0 → 2.2.1 | Fix database timeout |
| ✨ New feature | `minor`, `feature` | 2.2.0 → 2.3.0 | Add email notifications |
| 💥 Breaking change | `major`, `breaking` | 2.2.0 → 3.0.0 | Remove Python 2 support |
| **No label** | (none) | 2.2.0 → 2.2.1 | Defaults to patch |

### What Happens When You Merge

1. ✅ New version calculated automatically
2. ✅ CHANGELOG.md updated with your PR
3. ✅ Git tag created (e.g., `v2.3.0`)
4. ✅ GitHub Release created
5. ✅ Docker images built and published

### Quick Tips

- **Unsure?** Use `patch` or let it default
- **Adding features?** Use `minor`
- **Breaking existing functionality?** Use `major`
- **Check the template:** GitHub PR template has reminders

## For Maintainers

### Monitoring Automatic Releases

**Check workflow status:**
- Go to **Actions** tab
- Look for "Auto Version on PR Merge" workflow
- Review logs if something fails

**Verify release:**
```bash
# Check the new tag was created
git fetch --tags
git tag -l "v*.*.*" | tail -5

# Check Docker Hub
docker pull k9barry/noaa-alerts-pushover:latest
```

### Manual Override

If you need to skip automatic versioning or fix an issue:

1. **Before merge:** Add label `skip-release` (not yet implemented)
2. **After merge:** Delete tag and create manually:
   ```bash
   git tag -d vX.Y.Z
   git push origin :refs/tags/vX.Y.Z
   ```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Wrong version created | Delete tag, edit CHANGELOG, create correct version |
| Workflow failed | Check Actions logs, may need to retry manually |
| CHANGELOG conflict | Resolve manually, workflow handles updates |
| Missing Docker image | Check docker-publish.yml workflow logs |

## Semantic Versioning Reminder

Given version **MAJOR.MINOR.PATCH** (e.g., 2.3.1):

- **MAJOR** (2.x.x → 3.0.0): Breaking changes, incompatible API
- **MINOR** (2.3.x → 2.4.0): New features, backward compatible
- **PATCH** (2.3.1 → 2.3.2): Bug fixes, backward compatible

## Complete Documentation

- [AUTO_VERSIONING.md](AUTO_VERSIONING.md) - Complete automatic versioning guide
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [WORKFLOW_DIAGRAM.md](WORKFLOW_DIAGRAM.md) - Visual guide to versioning workflows

## Questions?

- Check workflow runs in the **Actions** tab
- See [AUTO_VERSIONING.md](AUTO_VERSIONING.md) for detailed troubleshooting
- Open an issue for help

---

**Workflows:**
- `.github/workflows/auto-version.yml` - Automatic versioning
- `.github/workflows/docker-publish.yml` - Docker Hub publishing
- `.github/workflows/release.yml` - Manual release creation

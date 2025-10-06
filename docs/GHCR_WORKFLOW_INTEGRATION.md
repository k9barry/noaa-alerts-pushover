# GitHub Container Registry Workflow Integration

This document explains how the GHCR publishing workflow integrates with the automatic versioning system and other workflows.

## Complete Workflow Flow

```
Developer Creates PR
        ↓
Adds Version Label (major/minor/patch)
        ↓
PR Gets Approved & Merged to Master
        ↓
════════════════════════════════════════════════════════════════
auto-version.yml Workflow Triggered
════════════════════════════════════════════════════════════════
        ↓
Reads PR Labels → Determines Bump Type
        ↓
Gets Current Version from Git Tags
        ↓
Calculates New Version (e.g., 2.3.0)
        ↓
Updates CHANGELOG.md
        ↓
Commits Changes to Master
        ↓
Creates Git Tag: v2.3.0
        ↓
Pushes Tag to GitHub
        ↓
Creates GitHub Release (v2.3.0)
        ↓
════════════════════════════════════════════════════════════════
Tag Push Triggers Multiple Workflows (Simultaneously)
════════════════════════════════════════════════════════════════
        ↓
┌───────────────────────┬───────────────────────────┐
│                       │                           │
▼                       ▼                           ▼
docker-publish.yml      ghcr-publish.yml           (other workflows)
        ↓                       ↓
Builds Multi-Platform   Builds Multi-Platform
Docker Images           Docker Images
(amd64, arm64)         (amd64, arm64)
        ↓                       ↓
Generates Tags:         Generates Tags:
• 2.3.0                • 2.3.0
• 2.3                  • 2.3
• 2                    • 2
• latest               • latest
        ↓                       ↓
Pushes to Docker Hub    Pushes to GHCR
k9barry/noaa-alerts-*   ghcr.io/k9barry/noaa-alerts-*
        ↓                       ↓
════════════════════════════════════════════════════════════════
Images Available in Both Registries
════════════════════════════════════════════════════════════════
```

## Trigger Matrix

| Workflow | Trigger Event | Result |
|----------|---------------|--------|
| `auto-version.yml` | PR merged to master | Creates Git tag (v2.3.0) |
| `docker-publish.yml` | Push to master | Publishes `latest` tag |
| `docker-publish.yml` | Git tag push (v2.3.0) | Publishes version tags |
| `ghcr-publish.yml` | Push to master | Publishes `latest` tag |
| `ghcr-publish.yml` | Git tag push (v2.3.0) | Publishes version tags |

## Tag Pattern Matching

The workflows use consistent tag patterns:

**Auto-version creates:**
```bash
v2.3.0    # Format: v[MAJOR].[MINOR].[PATCH]
```

**Publishing workflows match:**
```yaml
tags:
  - 'v*.*.*'    # Matches v2.3.0, v1.0.0, etc.
```

**Docker metadata generates:**
```
2.3.0     # Full semantic version
2.3       # Major.minor (tracks latest patch)
2         # Major (tracks latest minor.patch)
latest    # Latest on master branch
```

## Version Tag Examples

Given version tag `v2.3.5`:

### Docker Hub
- `k9barry/noaa-alerts-pushover:2.3.5` - Exact version
- `k9barry/noaa-alerts-pushover:2.3` - Latest 2.3.x
- `k9barry/noaa-alerts-pushover:2` - Latest 2.x.x
- `k9barry/noaa-alerts-pushover:latest` - Latest release

### GitHub Container Registry
- `ghcr.io/k9barry/noaa-alerts-pushover:2.3.5` - Exact version
- `ghcr.io/k9barry/noaa-alerts-pushover:2.3` - Latest 2.3.x
- `ghcr.io/k9barry/noaa-alerts-pushover:2` - Latest 2.x.x
- `ghcr.io/k9barry/noaa-alerts-pushover:latest` - Latest release

## Manual Triggers

Both publishing workflows support manual triggering:

### Trigger Docker Hub Build
```bash
# Via GitHub UI:
1. Go to Actions tab
2. Select "Build and Push to Docker Hub"
3. Click "Run workflow"
4. Select branch (usually master)
5. Click "Run workflow"
```

### Trigger GHCR Build
```bash
# Via GitHub UI:
1. Go to Actions tab
2. Select "Build and Push to GitHub Container Registry"
3. Click "Run workflow"
4. Select branch (usually master)
5. Click "Run workflow"
```

## Workflow Permissions

### Docker Hub Workflow
**Required Secrets:**
- `DOCKERHUB_USERNAME` - Docker Hub username
- `DOCKERHUB_TOKEN` - Docker Hub access token

**GitHub Permissions:**
- None (uses external service)

### GHCR Workflow
**Required Secrets:**
- None (uses built-in `GITHUB_TOKEN`)

**GitHub Permissions:**
- `contents: read` - Checkout code
- `packages: write` - Push to GHCR

## Build Process

Both workflows use identical build processes:

1. **Checkout code** - Clone repository
2. **Setup Buildx** - Configure multi-platform builder
3. **Login to registry** - Authenticate (Docker Hub or GHCR)
4. **Extract metadata** - Generate tags and labels
5. **Build images** - Create multi-platform images
6. **Push images** - Upload to registry
7. **Cache layers** - Speed up future builds

## Build Duration

Typical build times:

| Scenario | Docker Hub | GHCR |
|----------|------------|------|
| First build (no cache) | 8-12 min | 8-12 min |
| Cached build | 3-6 min | 3-6 min |
| Multi-platform | Same | Same |

*Build times may vary based on:*
- Code changes
- Dependency updates
- GitHub Actions runner load
- Cache hit rate

## Debugging

### Check Workflow Status

1. Go to **Actions** tab on GitHub
2. Look for recent workflow runs
3. Click on a run to see details
4. Expand steps to see logs

### Common Issues

#### Both workflows fail
- Check if auto-version workflow succeeded
- Verify tag was created and pushed
- Review error logs in failed workflows

#### Docker Hub works, GHCR fails
- Check workflow permissions in repo settings
- Ensure `GITHUB_TOKEN` has package write access
- Verify GHCR service is operational

#### GHCR works, Docker Hub fails
- Check Docker Hub secrets are configured
- Verify token hasn't expired
- Check Docker Hub service status

## Monitoring

### View Published Images

**Docker Hub:**
```
https://hub.docker.com/r/k9barry/noaa-alerts-pushover/tags
```

**GHCR:**
```
https://github.com/k9barry/noaa-alerts-pushover/pkgs/container/noaa-alerts-pushover
```

### Check Build History

1. Go to **Actions** tab
2. Filter by workflow:
   - "Build and Push to Docker Hub"
   - "Build and Push to GitHub Container Registry"
3. Review success/failure rates
4. Check build durations

## Best Practices

1. **Always add version labels** to PRs before merging
2. **Test manually** before first production use
3. **Monitor both registries** after tag creation
4. **Use specific versions** in production (not `latest`)
5. **Document breaking changes** in PR descriptions
6. **Verify images** pull and run correctly after publishing

## Security Considerations

### Docker Hub
- Token stored as GitHub secret (encrypted)
- Token scoped to Read & Write permissions
- Regular token rotation recommended
- Monitor for unauthorized access

### GHCR
- Uses ephemeral GitHub token (auto-rotates)
- Token scoped to repository only
- No manual token management needed
- Integrated with GitHub security features

## Advantages of Dual Registry Publishing

1. **Redundancy** - If one registry is down, use the other
2. **Choice** - Users can pick their preferred registry
3. **Migration path** - Easy to switch between registries
4. **Performance** - Some users may have better connectivity to GHCR
5. **Cost** - GHCR is free for public repos, no pull limits

## Related Documentation

- [docs/GHCR_SETUP.md](GHCR_SETUP.md) - GHCR setup guide
- [docs/GHCR_QUICKSTART.md](GHCR_QUICKSTART.md) - Quick start guide
- [docs/DOCKER_HUB_SETUP.md](DOCKER_HUB_SETUP.md) - Docker Hub setup
- [docs/AUTO_VERSIONING.md](AUTO_VERSIONING.md) - Automatic versioning
- [docs/AUTOMATIC_VERSIONING_IMPLEMENTATION.md](AUTOMATIC_VERSIONING_IMPLEMENTATION.md) - Implementation details
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines

---

**Last Updated**: 2024  
**Status**: Active  
**Workflows**: 
- `.github/workflows/ghcr-publish.yml`
- `.github/workflows/docker-publish.yml`
- `.github/workflows/auto-version.yml`

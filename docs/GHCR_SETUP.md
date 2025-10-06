# GitHub Container Registry Setup

This guide explains the automated GitHub Container Registry (GHCR) publishing workflow.

## Overview

The repository includes automated publishing to GitHub Container Registry via GitHub Actions. This workflow complements the existing Docker Hub publishing workflow and provides an alternative container registry option.

## Prerequisites

1. Repository maintainer or admin access on GitHub
2. The repository `.github/workflows/ghcr-publish.yml` workflow file
3. GitHub account (no additional setup required - uses GitHub's built-in authentication)

## Key Advantages of GHCR

- **No External Credentials Required**: Uses GitHub's built-in `GITHUB_TOKEN`
- **Integrated with GitHub**: Images are linked directly to the repository
- **Automatic Authentication**: GitHub Actions automatically authenticates
- **Free for Public Repositories**: No additional cost for public images
- **Same Multi-Platform Support**: Builds for linux/amd64 and linux/arm64

## Workflow Behavior

### Triggers

The workflow automatically runs when:

1. **Push to Master Branch**
   - Triggered on any commit to `master`
   - Publishes image with `latest` tag
   - Example: `ghcr.io/k9barry/noaa-alerts-pushover:latest`

2. **Git Tag Push** (Recommended for releases)
   - Triggered when a version tag is pushed (e.g., `v2.3.0`)
   - Automatically generates multiple tags:
     - Full version: `2.3.0`
     - Major.minor: `2.3`
     - Major only: `2`
     - Latest: `latest` (if on master branch)
   - Example tags:
     - `ghcr.io/k9barry/noaa-alerts-pushover:2.3.0`
     - `ghcr.io/k9barry/noaa-alerts-pushover:2.3`
     - `ghcr.io/k9barry/noaa-alerts-pushover:2`
     - `ghcr.io/k9barry/noaa-alerts-pushover:latest`

3. **Manual Workflow Dispatch**
   - Can be triggered manually from GitHub Actions tab
   - Useful for testing or re-publishing images

### Integration with Automatic Versioning

The GHCR workflow integrates seamlessly with the automatic versioning system:

1. **PR merged to master** → auto-version.yml creates tag (e.g., `v2.3.0`)
2. **Tag push** → ghcr-publish.yml automatically triggered
3. **Multi-platform images built** for linux/amd64 and linux/arm64
4. **Images pushed to GHCR** with all version tags
5. **Images visible** at `https://github.com/k9barry/noaa-alerts-pushover/pkgs/container/noaa-alerts-pushover`

## Setup Steps

### 1. Verify Workflow File Exists

Check that `.github/workflows/ghcr-publish.yml` exists in your repository. This file should already be present.

### 2. Enable GitHub Container Registry (First Time Only)

If this is the first time publishing to GHCR for this repository:

1. Go to your repository on GitHub
2. The workflow will automatically create the package on first run
3. After first publish, go to **Packages** tab to manage visibility

### 3. Set Package Visibility (Optional)

By default, GHCR packages inherit repository visibility. To change:

1. Go to `https://github.com/k9barry?tab=packages`
2. Click on the `noaa-alerts-pushover` package
3. Go to **Package settings**
4. Under **Danger Zone**, you can:
   - Change visibility (Public/Private)
   - Link to repository
   - Delete package

### 4. Test the Workflow

#### Option A: Manual Trigger (Recommended for First Test)

1. Go to **Actions** tab on GitHub
2. Select **Build and Push to GitHub Container Registry** workflow
3. Click **Run workflow**
4. Select branch: `master`
5. Click **Run workflow**
6. Monitor the workflow execution
7. Check GHCR for the new image at Packages tab

#### Option B: Push to Master

```bash
# Make a small change and push
git checkout master
git pull
# Make change, commit
git push origin master
```

The workflow will automatically run and push with `latest` tag.

#### Option C: Create a Tag

```bash
# Create and push a version tag
git tag -a v2.3.0 -m "Release version 2.3.0"
git push origin v2.3.0
```

The workflow will build and push with version tags (`2.3.0`, `2.3`, `2`, `latest`).

## Using Images from GHCR

### Pull the Image

```bash
# Pull latest version
docker pull ghcr.io/k9barry/noaa-alerts-pushover:latest

# Pull specific version
docker pull ghcr.io/k9barry/noaa-alerts-pushover:2.3.0

# Pull major.minor version (automatically gets latest patch)
docker pull ghcr.io/k9barry/noaa-alerts-pushover:2.3
```

### Authentication for Private Images

If the package is set to private:

```bash
# Create a GitHub Personal Access Token with read:packages scope
# Then login:
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull the image
docker pull ghcr.io/k9barry/noaa-alerts-pushover:latest
```

### Docker Compose with GHCR

Update your `docker-compose.yml` to use GHCR:

```yaml
services:
  noaa-alerts:
    image: ghcr.io/k9barry/noaa-alerts-pushover:latest
    # ... rest of configuration
```

## Workflow Details

### Platforms

Images are built for multiple platforms:
- `linux/amd64` - Standard x86_64 systems
- `linux/arm64` - ARM systems (Raspberry Pi 4, AWS Graviton, Apple Silicon)

Docker automatically pulls the correct architecture for your system.

### Caching

The workflow uses GitHub Actions cache to speed up builds:
- First build: ~5-10 minutes
- Subsequent builds: ~2-5 minutes (with cache)

### Permissions

The workflow requires:
- `contents: read` - To checkout code
- `packages: write` - To push to GHCR

These are automatically provided by `GITHUB_TOKEN` in GitHub Actions.

## Troubleshooting

### Issue: Workflow fails with "permission denied"

**Solution:** Check workflow permissions:
1. Go to repository **Settings** → **Actions** → **General**
2. Scroll to **Workflow permissions**
3. Ensure "Read and write permissions" is selected
4. Click **Save**

### Issue: Package not visible in Packages tab

**Solution:** 
1. Check workflow logs to ensure push succeeded
2. Verify the package wasn't created under your personal account instead of the org
3. Go to `https://github.com/USERNAME?tab=packages` to find it

### Issue: Cannot pull image (404 error)

**Solution:**
1. Ensure package visibility is set to Public (for public pulls)
2. If private, ensure you're authenticated with proper token
3. Check the exact image name matches: `ghcr.io/owner/repo:tag`

### Issue: Build fails on specific platform

**Solution:** Check the build logs for platform-specific errors. You may need to adjust the Dockerfile if there are architecture-specific dependencies.

### Issue: Tags not appearing on GHCR

**Solution:** 
1. Check the workflow logs to see which tags were created
2. Ensure the Git tag format matches `v*.*.*` pattern (e.g., `v2.3.0`)
3. Verify the metadata action output in workflow logs

## Monitoring

### View Workflow Runs

1. Go to **Actions** tab
2. Select **Build and Push to GitHub Container Registry**
3. View recent runs and their status

### View Published Images

1. Go to repository **Packages** tab
2. Click on **noaa-alerts-pushover**
3. View all published tags and their details

### Check Image Details

Each image includes:
- Labels with build information
- Platform architectures
- Creation date
- Git commit SHA
- Links back to source code

## Security Best Practices

### Token Security

- ✅ Workflow uses built-in `GITHUB_TOKEN` (no manual token management)
- ✅ Token is automatically scoped to repository
- ✅ Token expires after workflow completes
- ✅ No need to create or rotate tokens manually

### Package Security

- ✅ Enable vulnerability scanning (automatic with GHCR)
- ✅ Review package access logs regularly
- ✅ Set appropriate package visibility (public/private)
- ✅ Use signed commits when pushing tags

### Image Security

- ✅ Images built from source in GitHub Actions (transparent)
- ✅ Multi-stage builds to minimize image size
- ✅ Non-root user (UID 1000) in container
- ✅ No secrets included in images

## Comparison: GHCR vs Docker Hub

| Feature | GHCR | Docker Hub |
|---------|------|------------|
| Authentication | Automatic (GITHUB_TOKEN) | Manual (secrets required) |
| Cost | Free for public repos | Free with limitations |
| Integration | Native GitHub | External service |
| Setup Complexity | Minimal (1 step) | Medium (tokens + secrets) |
| Multi-platform | Yes | Yes |
| Visibility | Linked to repo | Separate service |
| Pull Rates | Generous | Limited for anonymous |

Both registries are fully supported and can be used simultaneously.

## Maintenance

### Updating the Workflow

If you need to modify the workflow:

1. Edit `.github/workflows/ghcr-publish.yml`
2. Test changes with manual trigger before merging
3. Document any changes in CHANGELOG.md

### Package Cleanup

To remove old or unused tags:

1. Go to package page
2. Click on specific tag version
3. Click **Delete** button
4. Confirm deletion

Note: Deleting tags doesn't affect existing deployments using those tags.

### Monitoring Usage

1. Go to package settings
2. View **Insights** tab (if available)
3. Monitor pull statistics and usage patterns

## Additional Resources

- [GitHub Container Registry Documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Docker Metadata Action](https://github.com/docker/metadata-action)
- [About GitHub Packages](https://docs.github.com/en/packages/learn-github-packages/introduction-to-github-packages)

## Related Documentation

- [docs/AUTO_VERSIONING.md](AUTO_VERSIONING.md) - Automatic versioning system
- [docs/DOCKER_HUB_SETUP.md](DOCKER_HUB_SETUP.md) - Docker Hub publishing
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines

## Support

For issues with the workflow, open an issue on GitHub with:
- Workflow run URL
- Error messages from logs
- Steps to reproduce
- Screenshot of error (if applicable)

---

**Last Updated**: 2024  
**Workflow File**: `.github/workflows/ghcr-publish.yml`  
**Status**: Active and ready for use

# Docker Hub Setup for Maintainers

This guide explains how to configure the automated Docker Hub publishing workflow.

## Prerequisites

1. A Docker Hub account
2. Repository maintainer access on GitHub
3. The repository `.github/workflows/docker-publish.yml` workflow file

## Setup Steps

### 1. Create Docker Hub Access Token

1. Log in to [Docker Hub](https://hub.docker.com/)
2. Go to **Account Settings** → **Security** → **Access Tokens**
3. Click **New Access Token**
4. Name it: `github-actions-noaa-alerts`
5. Set permissions: **Read & Write**
6. Click **Generate**
7. **Copy the token immediately** (you won't see it again)

### 2. Create Docker Hub Repository (Optional)

If the repository doesn't exist yet:

1. Go to [Docker Hub](https://hub.docker.com/)
2. Click **Create Repository**
3. Name: `noaa-alerts-pushover`
4. Visibility: **Public** (or Private if preferred)
5. Description: Copy from `DOCKER_HUB_README.md`
6. Click **Create**

### 3. Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add two secrets:

   **Secret 1:**
   - Name: `DOCKERHUB_USERNAME`
   - Value: Your Docker Hub username (e.g., `k9barry`)
   
   **Secret 2:**
   - Name: `DOCKERHUB_TOKEN`
   - Value: The access token you created in step 1

### 4. Verify Workflow Configuration

Check that `.github/workflows/docker-publish.yml` references your Docker Hub username:

```yaml
images: ${{ secrets.DOCKERHUB_USERNAME }}/noaa-alerts-pushover
```

This uses the secret, so it's dynamic and works for any maintainer.

### 5. Test the Workflow

#### Option A: Manual Trigger (Recommended for First Test)

1. Go to **Actions** tab on GitHub
2. Select **Build and Push to Docker Hub** workflow
3. Click **Run workflow**
4. Select branch: `master`
5. Click **Run workflow**
6. Monitor the workflow execution
7. Check Docker Hub for the new image

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

### 6. Update Docker Hub Repository Description

1. Go to your Docker Hub repository
2. Click **Edit** on the repository page
3. Copy content from `DOCKER_HUB_README.md` into the **Description** field
4. Save changes

## Workflow Behavior

### Triggers

The workflow runs automatically on:
- **Push to master branch**: Creates `latest` tag
- **Git tag push** (e.g., `v2.2.0`): Creates versioned tags
- **Manual dispatch**: Via Actions tab
- **PR merge** (automatic): Via auto-versioning workflow (see below)

### Automatic Versioning (New!)

When a PR is merged to master with appropriate labels (`major`, `minor`, or `patch`), the auto-versioning workflow:
1. Creates a new Git tag automatically
2. Triggers this Docker Hub workflow
3. Publishes versioned images

**See [AUTO_VERSIONING.md](AUTO_VERSIONING.md) for complete details.**

### Image Tags

For a tag like `v2.2.0`, the workflow creates:
- `k9barry/noaa-alerts-pushover:2.2.0` (full version)
- `k9barry/noaa-alerts-pushover:2.2` (major.minor)
- `k9barry/noaa-alerts-pushover:2` (major only)
- `k9barry/noaa-alerts-pushover:latest` (if on master branch)

### Multi-platform Builds

Images are built for:
- `linux/amd64` (Intel/AMD x86_64)
- `linux/arm64` (ARM 64-bit, e.g., Raspberry Pi 4/5, AWS Graviton)

## Troubleshooting

### Issue: Workflow fails with "unauthorized: authentication required"

**Solution:** Check that secrets are configured correctly:
1. Verify `DOCKERHUB_USERNAME` is set
2. Verify `DOCKERHUB_TOKEN` is set (not password)
3. Ensure token has Read & Write permissions
4. Try regenerating the Docker Hub token

### Issue: Workflow fails with "denied: requested access to the resource is denied"

**Solution:** Ensure the Docker Hub repository exists and the username in the workflow matches your Docker Hub account.

### Issue: Build fails on specific platform

**Solution:** Check the build logs for platform-specific errors. You may need to adjust the Dockerfile if there are architecture-specific dependencies.

### Issue: Tags not appearing on Docker Hub

**Solution:** Check the workflow logs to see which tags were created. Ensure the Git tag format matches `v*.*.*` pattern.

## Monitoring

### View Published Images

Visit: `https://hub.docker.com/r/YOUR_USERNAME/noaa-alerts-pushover/tags`

### Check Workflow Status

Go to **Actions** tab on GitHub to see:
- Workflow run history
- Build logs
- Success/failure status

### Docker Hub Analytics

Docker Hub provides:
- Pull statistics
- Popular tags
- Geographic distribution

## Security Best Practices

1. **Use Access Tokens**: Never use your Docker Hub password in secrets
2. **Minimum Permissions**: Create tokens with only required permissions (Read & Write)
3. **Rotate Tokens**: Periodically rotate access tokens
4. **Audit Access**: Review who has access to repository secrets
5. **Protected Branches**: Consider requiring reviews for master branch pushes

## Maintenance

### Updating the Workflow

If you need to modify the workflow:

1. Edit `.github/workflows/docker-publish.yml`
2. Test changes with manual trigger before merging
3. Document any changes in CHANGELOG.md

### Updating Docker Hub Description

Whenever you update `DOCKER_HUB_README.md`:
1. Copy the updated content to Docker Hub repository description
2. Or use Docker Hub's API to automate updates

### Revoking Access

If credentials are compromised:

1. **Immediately revoke** the Docker Hub access token
2. Delete the GitHub secrets
3. Generate new token and update secrets
4. Review recent workflow runs for suspicious activity

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Hub Access Tokens](https://docs.docker.com/docker-hub/access-tokens/)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Docker Metadata Action](https://github.com/docker/metadata-action)

## Support

For issues with the workflow, open an issue on GitHub with:
- Workflow run URL
- Error messages from logs
- Steps to reproduce

---

**Last Updated**: 2024
**Workflow File**: `.github/workflows/docker-publish.yml`

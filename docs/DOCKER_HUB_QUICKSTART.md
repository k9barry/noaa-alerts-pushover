# Docker Hub Quick Start for Maintainers

This file provides a quick reference for setting up and using the Docker Hub automated workflow.

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get Docker Hub Token
```bash
1. Go to hub.docker.com → Account Settings → Security → Access Tokens
2. Click "New Access Token"
3. Name: "github-actions-noaa-alerts"
4. Permissions: "Read & Write"
5. Copy the token (shown only once!)
```

### Step 2: Add GitHub Secrets
```bash
1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Add two secrets:
   - DOCKERHUB_USERNAME = your_dockerhub_username
   - DOCKERHUB_TOKEN = token_from_step_1
```

### Step 3: Test the Workflow
```bash
1. Go to Actions tab
2. Select "Build and Push to Docker Hub"
3. Click "Run workflow" → "Run workflow"
4. Wait 5-10 minutes for build
5. Check hub.docker.com for your image
```

## 📋 What Gets Published

### On Push to Master
- Image tag: `latest`
- Example: `k9barry/noaa-alerts-pushover:latest`

### On Tag Creation (e.g., v2.3.0)
- `k9barry/noaa-alerts-pushover:2.3.0` (full version)
- `k9barry/noaa-alerts-pushover:2.3` (minor version)
- `k9barry/noaa-alerts-pushover:2` (major version)
- `k9barry/noaa-alerts-pushover:latest` (if on main)

### Platforms
- `linux/amd64` (Intel/AMD)
- `linux/arm64` (ARM - Raspberry Pi, AWS Graviton)

## 🧪 Testing Published Image

```bash
# Pull and test
docker pull k9barry/noaa-alerts-pushover:latest
docker run --rm k9barry/noaa-alerts-pushover:latest python --version

# Pull specific version
docker pull k9barry/noaa-alerts-pushover:v2.2.0
```

## 📖 Full Documentation

- **Setup Guide**: [docs/DOCKER_HUB_SETUP.md](docs/DOCKER_HUB_SETUP.md) - Complete setup with troubleshooting
- **User Guide**: [DOCKER_HUB_README.md](DOCKER_HUB_README.md) - Copy this to Docker Hub description
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md#docker-hub-publishing) - Maintainer workflows

## 🔒 Security Notes

- ✅ Use access tokens, not passwords
- ✅ Set minimum required permissions (Read & Write)
- ✅ Rotate tokens periodically
- ✅ Review workflow runs regularly
- ✅ Never commit tokens to repository

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "authentication required" | Check secrets are set correctly |
| "access denied" | Verify token has Read & Write permissions |
| Build fails on platform | Check workflow logs for platform-specific errors |
| Tags not appearing | Ensure tag format is `v*.*.*` |

See [docs/DOCKER_HUB_SETUP.md](docs/DOCKER_HUB_SETUP.md) for detailed troubleshooting.

## 📝 Workflow File

Location: `.github/workflows/docker-publish.yml`

Key features:
- Multi-platform builds (amd64, arm64)
- Smart tagging based on git tags
- GitHub Actions cache for faster builds
- Automatic on push and tag creation
- Manual dispatch available

## ✅ Checklist After Setup

- [ ] Docker Hub token created
- [ ] GitHub secrets configured
- [ ] Workflow tested with manual trigger
- [ ] Image available on Docker Hub
- [ ] Docker Hub description updated with DOCKER_HUB_README.md
- [ ] Verified image pulls and runs correctly
- [ ] Updated team documentation if needed

---

**Need help?** See [docs/DOCKER_HUB_SETUP.md](docs/DOCKER_HUB_SETUP.md) for comprehensive guidance.

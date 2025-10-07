# GitHub Container Registry Quick Start

This file provides a quick reference for using the GitHub Container Registry (GHCR) automated workflow.

## 🚀 Quick Setup (2 Minutes)

### Step 1: Enable Workflow Permissions (First Time Only)

```bash
1. Go to GitHub repo → Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Click "Save"
```

### Step 2: Test the Workflow

```bash
1. Go to Actions tab
2. Select "Build and Push to GitHub Container Registry"
3. Click "Run workflow" → "Run workflow"
4. Wait 5-10 minutes for build
5. Check Packages tab for your image
```

That's it! No credentials or secrets needed - GHCR uses GitHub's built-in authentication.

## 📋 What Gets Published

When you push a tag like `v2.3.0`, the following images are created:

```bash
ghcr.io/k9barry/noaa-alerts-pushover:2.3.0   # Full version
ghcr.io/k9barry/noaa-alerts-pushover:2.3     # Major.minor
ghcr.io/k9barry/noaa-alerts-pushover:2       # Major only
ghcr.io/k9barry/noaa-alerts-pushover:latest  # Latest (main branch)
```

## 🧪 Using Published Images

### Pull the Image

```bash
# Pull latest version
docker pull ghcr.io/k9barry/noaa-alerts-pushover:latest

# Pull specific version
docker pull ghcr.io/k9barry/noaa-alerts-pushover:2.3.0
```

### Docker Compose

Update your `docker-compose.yml`:

```yaml
services:
  noaa-alerts:
    image: ghcr.io/k9barry/noaa-alerts-pushover:latest
    volumes:
      - ./data:/app/data
      - ./output:/app/output
      - ./config.txt:/app/config.txt
      - ./counties.json:/app/counties.json
```

## 📖 Full Documentation

See [docs/GHCR_SETUP.md](GHCR_SETUP.md) for:
- Detailed setup instructions
- Troubleshooting guide
- Security best practices
- Advanced configuration options
- Comparison with Docker Hub

## 🔒 Security Notes

- ✅ No external credentials required
- ✅ Uses GitHub's built-in authentication
- ✅ Automatic token management
- ✅ Token expires after workflow completes
- ✅ Images linked directly to repository

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Permission denied | Check workflow permissions in Settings → Actions |
| Package not visible | Check Packages tab or your profile packages |
| Cannot pull image | Ensure package is set to Public visibility |
| Build fails | Check Actions tab for detailed error logs |

See [docs/GHCR_SETUP.md](GHCR_SETUP.md) for detailed troubleshooting.

## 📝 Workflow File

Location: `.github/workflows/ghcr-publish.yml`

Key features:
- Multi-platform builds (amd64, arm64)
- Smart tagging based on git tags
- GitHub Actions cache for faster builds
- Automatic on push and tag creation
- Manual dispatch available
- Uses GitHub's built-in token (no secrets needed)

## ⚡ Integration with Auto-Versioning

The GHCR workflow automatically integrates with the versioning system:

1. **PR merged** with version label (major/minor/patch)
2. **auto-version.yml** creates Git tag (e.g., `v2.3.0`)
3. **ghcr-publish.yml** automatically triggered by tag
4. **Multi-platform images** built and pushed to GHCR
5. **Multiple tags** created (2.3.0, 2.3, 2, latest)

No manual intervention needed!

## ✅ Checklist After Setup

- [ ] Workflow permissions enabled (read and write)
- [ ] Workflow tested with manual trigger
- [ ] Image available in Packages tab
- [ ] Image pulls and runs correctly
- [ ] Package visibility set (Public/Private)
- [ ] Updated team documentation if needed

## 🆚 GHCR vs Docker Hub

| Feature | GHCR | Docker Hub |
|---------|------|------------|
| Setup | Automatic | Requires secrets |
| Authentication | Built-in | Manual token |
| Cost | Free (public) | Free with limits |
| Integration | Native GitHub | External |

Both registries work simultaneously - use whichever fits your needs!

---

**Need help?** See [docs/GHCR_SETUP.md](GHCR_SETUP.md) for comprehensive guidance.

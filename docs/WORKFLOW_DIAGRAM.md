# Automatic Versioning Workflow Diagram

## Visual Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AUTOMATIC VERSIONING                          │
│                    Complete Workflow Diagram                         │
└─────────────────────────────────────────────────────────────────────┘

Step 1: Create PR
┌─────────────────────┐
│  Developer creates  │
│   Pull Request on   │
│       GitHub        │
└──────────┬──────────┘
           │
           ▼
Step 2: Add Label
┌─────────────────────┐
│  Add version label: │
│  • major/breaking   │◄─── Breaking changes (X.0.0)
│  • minor/feature    │◄─── New features (0.X.0)
│  • patch/bugfix/fix │◄─── Bug fixes (0.0.X)
│  • (none - default) │◄─── Defaults to patch
└──────────┬──────────┘
           │
           ▼
Step 3: Review & Merge
┌─────────────────────┐
│   PR is reviewed    │
│    and approved     │
│                     │
│   PR is merged to   │
│    main branch    │
└──────────┬──────────┘
           │
           ▼
═══════════════════════════════════════════════════════════════════════
           AUTOMATIC WORKFLOW TRIGGERED
═══════════════════════════════════════════════════════════════════════
           │
           ▼
Step 4: Auto-Version Workflow
┌─────────────────────┐
│  auto-version.yml   │
│   workflow starts   │
└──────────┬──────────┘
           │
           ▼
Step 5: Check Conditions
┌─────────────────────┐
│ Is PR merged?       │──NO──► Workflow stops
│ (not just closed)   │
└──────────┬──────────┘
           │ YES
           ▼
Step 6: Read PR Label
┌─────────────────────┐
│  Parse PR labels    │
│  Determine bump:    │
│  • major            │
│  • minor            │
│  • patch (default)  │
└──────────┬──────────┘
           │
           ▼
Step 7: Get Current Version
┌─────────────────────┐
│  Check Git tags     │──► Look for v*.*.*
│  Fall back to       │
│  CHANGELOG.md       │
│  Default: 2.2.0     │
└──────────┬──────────┘
           │
           ▼
Step 8: Calculate New Version
┌─────────────────────────────────┐
│  Example: Current = 2.2.0       │
│                                 │
│  major bump → 3.0.0             │
│  minor bump → 2.3.0             │
│  patch bump → 2.2.1             │
└──────────┬──────────────────────┘
           │
           ▼
Step 9: Update CHANGELOG.md
┌─────────────────────┐
│  Insert new entry:  │
│  ## Version X.Y.Z   │
│                     │
│  ### Changes        │
│  - PR title (#123)  │
│    by @author       │
└──────────┬──────────┘
           │
           ▼
Step 10: Commit Changes
┌─────────────────────┐
│  git add CHANGELOG  │
│  git commit -m ...  │
└──────────┬──────────┘
           │
           ▼
Step 11: Create Git Tag
┌─────────────────────┐
│  git tag -a vX.Y.Z  │
│  -m "Release..."    │
└──────────┬──────────┘
           │
           ▼
Step 12: Push to GitHub
┌─────────────────────┐
│  git push origin    │
│     main          │
│  git push origin    │
│     vX.Y.Z          │
└──────────┬──────────┘
           │
           ▼
Step 13: Create GitHub Release
┌─────────────────────┐
│  Create Release:    │
│  • Tag: vX.Y.Z      │
│  • Title: Version   │
│  • Body: PR info    │
└──────────┬──────────┘
           │
           ▼
═══════════════════════════════════════════════════════════════════════
           TAG PUSH TRIGGERS DOCKER WORKFLOW
═══════════════════════════════════════════════════════════════════════
           │
           ▼
Step 14: Docker Publish Workflow
┌─────────────────────┐
│ docker-publish.yml  │
│   workflow starts   │
└──────────┬──────────┘
           │
           ▼
Step 15: Extract Metadata
┌─────────────────────┐
│  Generate tags:     │
│  • X.Y.Z (full)     │
│  • X.Y (major.minor)│
│  • X (major)        │
│  • latest           │
└──────────┬──────────┘
           │
           ▼
Step 16: Build Multi-Platform Images
┌─────────────────────┐
│  Build for:         │
│  • linux/amd64      │
│  • linux/arm64      │
└──────────┬──────────┘
           │
           ▼
Step 17: Push to Docker Hub
┌─────────────────────────────────┐
│  Push images:                   │
│  • k9barry/noaa-alerts:X.Y.Z    │
│  • k9barry/noaa-alerts:X.Y      │
│  • k9barry/noaa-alerts:X        │
│  • k9barry/noaa-alerts:latest   │
└──────────┬──────────────────────┘
           │
           ▼
═══════════════════════════════════════════════════════════════════════
           WORKFLOW COMPLETE
═══════════════════════════════════════════════════════════════════════
           │
           ▼
Results Available:
┌─────────────────────────────────┐
│  ✅ GitHub Release created      │
│  ✅ Git tag created              │
│  ✅ CHANGELOG.md updated         │
│  ✅ Docker images published      │
│  ✅ Version number incremented   │
└─────────────────────────────────┘
```

## Timeline Example

### Real-world Example: Adding Email Notifications

```
Time  | Event
------+----------------------------------------------------------
10:00 | Developer creates PR "Add email notification support"
10:05 | Developer adds label: "minor"
10:15 | Maintainer reviews PR
10:30 | Maintainer approves and merges PR
      |
10:31 | ⚡ auto-version.yml triggered automatically
      | • Reads label: "minor"
      | • Current version: 2.2.0
      | • Calculates: 2.3.0
      | • Updates CHANGELOG.md
      | • Creates tag v2.3.0
      | • Creates GitHub Release
      | • Pushes to repository
      | (Total time: ~30 seconds)
      |
10:32 | ⚡ docker-publish.yml triggered by tag push
      | • Builds linux/amd64 image
      | • Builds linux/arm64 image
      | • Pushes to Docker Hub
      | (Total time: ~5-10 minutes)
      |
10:42 | ✅ COMPLETE
      | • Version 2.3.0 released
      | • Docker images available
      | • Users can pull: docker pull k9barry/noaa-alerts:2.3.0
```

## Comparison: Before vs After

### Before (Manual Process)

```
Developer → Creates PR
            ↓
Maintainer → Reviews & Merges
            ↓
Maintainer → Manually updates CHANGELOG.md
            ↓
Maintainer → Manually creates Git tag
            ↓
Maintainer → Manually creates GitHub Release
            ↓
Maintainer → Waits for Docker build
            ↓
            ✅ Complete (30+ minutes of manual work)
```

### After (Automatic Process)

```
Developer → Creates PR + Adds Label
            ↓
Maintainer → Reviews & Merges
            ↓
            🤖 Everything else is automatic
            ↓
            ✅ Complete (0 minutes of manual work)
```

## Label Decision Tree

```
                    What changed?
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   Breaking API?     New Feature?      Bug Fix?
        │                 │                 │
      major             minor             patch
        │                 │                 │
    ┌───▼───┐         ┌───▼───┐        ┌───▼───┐
    │ 3.0.0 │         │ 2.3.0 │        │ 2.2.1 │
    └───────┘         └───────┘        └───────┘
```

## Integration Points

```
┌─────────────────────┐
│   GitHub Actions    │
│                     │
│  auto-version.yml   │◄──── Triggered by PR merge
└──────────┬──────────┘
           │ creates
           ▼
┌─────────────────────┐
│     Git Tag         │
│      vX.Y.Z         │
└──────────┬──────────┘
           │ triggers
           ▼
┌─────────────────────┐
│   GitHub Actions    │
│                     │
│ docker-publish.yml  │◄──── Triggered by tag push
└──────────┬──────────┘
           │ pushes to
           ▼
┌─────────────────────┐
│    Docker Hub       │
│                     │
│  noaa-alerts-       │
│    pushover         │
└─────────────────────┘
```

## Semantic Versioning Rules

```
Version: MAJOR . MINOR . PATCH
         ▲       ▲       ▲
         │       │       │
         │       │       └─ Bug fixes
         │       │          (backward compatible)
         │       │          Example: 2.2.0 → 2.2.1
         │       │
         │       └───────── New features
         │                  (backward compatible)
         │                  Example: 2.2.0 → 2.3.0
         │
         └─────────────────── Breaking changes
                             (incompatible changes)
                             Example: 2.2.0 → 3.0.0
```

## Error Handling

```
PR Merged with Label
        │
        ▼
┌────────────────┐
│ Workflow Fails?│──NO──► Continue normally
└────────┬───────┘
         │ YES
         ▼
┌────────────────┐
│  Check Logs    │
│  in Actions    │
└────────┬───────┘
         │
         ▼
┌────────────────────────────────┐
│ Common Issues:                 │
│ • Permission denied            │
│ • Version already exists       │
│ • CHANGELOG merge conflict     │
│ • Network timeout              │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────┐
│  Manual Fix    │
│  if needed     │
└────────────────┘
```

## Related Documentation

- [AUTO_VERSIONING.md](AUTO_VERSIONING.md) - Complete guide
- [VERSIONING_QUICK_REFERENCE.md](VERSIONING_QUICK_REFERENCE.md) - Quick reference
- [AUTOMATIC_VERSIONING_IMPLEMENTATION.md](AUTOMATIC_VERSIONING_IMPLEMENTATION.md) - Technical details

---

**Created:** 2024-10-06  
**Workflows:** `.github/workflows/auto-version.yml`, `.github/workflows/docker-publish.yml`

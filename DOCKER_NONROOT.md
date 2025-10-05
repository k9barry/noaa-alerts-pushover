# Running as Non-Root User

This Docker container now runs as a non-root user called `noaa` (UID 1000) for improved security.

## What Changed

### Security Improvements

- **Non-root execution**: The container now runs as user `noaa` (UID 1000) instead of root
- **Reduced attack surface**: Limits potential damage from container escape vulnerabilities
- **Best practices**: Follows Docker and Kubernetes security recommendations

### Technical Changes

1. **User Creation**: A user `noaa` with UID 1000 is created during build
2. **Ownership**: All files in `/app` are owned by `noaa:noaa`
3. **Database Init**: Database initialization now runs as the `noaa` user
4. **Scheduler**: The scheduler runs as the `noaa` user with logs in `/app/scheduler.log`

## Volume Mount Permissions

When using volume mounts, the host directories need appropriate permissions:

### Option 1: Set Host Directory Owner to UID 1000

```bash
# On the host system
sudo chown -R 1000:1000 ./output ./data
```

### Option 2: Use Permissive Permissions

```bash
# On the host system
chmod 777 ./output ./data
```

### Option 3: Match Host User to Container UID

If your host user already has UID 1000 (check with `id -u`), no changes are needed.

## Troubleshooting

### Permission Denied Errors

If you see permission errors when writing to volumes:

```bash
# Check the ownership of mounted directories
ls -la ./output ./data

# Fix permissions
sudo chown -R 1000:1000 ./output ./data
# Or
chmod 777 ./output ./data
```

### Database Permission Issues

If the database can't be created or accessed:

```bash
# Ensure data directory is writable
chmod 777 ./data

# Or set ownership
sudo chown -R 1000:1000 ./data
```

### Output Directory Errors

If HTML alert files can't be written:

```bash
# Ensure output directory is writable
chmod 777 ./output

# Or set ownership
sudo chown -R 1000:1000 ./output
```

## Docker Compose Example

Your existing docker-compose files will work, but ensure mounted directories have correct permissions:

```yaml
services:
  noaa-alerts:
    build: .
    volumes:
      - ./config.txt:/app/config.txt:ro
      - ./counties.json:/app/counties.json:ro
      - ./output:/app/output      # Must be writable by UID 1000
      - ./data:/app/data          # Must be writable by UID 1000
```

## Verifying Non-Root Execution

To verify the container runs as the `noaa` user:

```bash
# Check the user inside the running container
docker compose exec noaa-alerts whoami
# Should output: noaa

# Check the UID
docker compose exec noaa-alerts id
# Should output: uid=1000(noaa) gid=1000(noaa) groups=1000(noaa)
```

## Kubernetes Considerations

When deploying to Kubernetes, you may need to set the security context:

```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
  containers:
  - name: noaa-alerts
    image: your-image:latest
```

## Why UID 1000?

UID 1000 is commonly the first non-system user ID on most Linux systems. This makes it easier to match with host user permissions and is a common practice in Docker containers.

## Reverting to Root (Not Recommended)

If you need to run as root temporarily (not recommended):

```dockerfile
# Add this line before ENTRYPOINT
USER root
```

However, this defeats the security improvements and should only be used for debugging.

## Additional Security

Consider these additional security measures:

1. **Read-only root filesystem**: Add `--read-only` flag when running the container
2. **No new privileges**: Add `--security-opt=no-new-privileges` flag
3. **Drop capabilities**: Use `--cap-drop=ALL` to drop all Linux capabilities

Example:

```bash
docker run --read-only --security-opt=no-new-privileges --cap-drop=ALL \
  -v ./output:/app/output \
  -v ./data:/app/data \
  noaa-alerts
```

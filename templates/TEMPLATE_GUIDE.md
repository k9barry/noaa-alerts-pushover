# Detail Template Customization Guide

## Overview

The `templates/detail.html` file is a Jinja2 template used to generate HTML pages for individual weather alerts. These HTML pages are created in the `output/` directory and can be linked from push notifications.

## Quick Start: Configuration-Based Customization

**New!** The template now supports configuration-based feature toggling. Instead of creating multiple template files, you can enable or disable features by editing `config.txt`:

```ini
[template]
# Enable features you want (set to true or false)
show_event_info = true           # Display event type and issuing office
show_expiration = true            # Show expiration time
conditional_instructions = true   # Only show instructions if present
color_coding = true               # Color-code alerts by type
show_map_link = true              # Include Google Maps link
mobile_responsive = true          # Use mobile-friendly responsive design
show_social_sharing = true        # Add social sharing buttons
```

All options default to `false` if not specified, giving you the basic template layout.

### Available Features

1. **show_event_info** - Adds event type and issuing office information
2. **show_expiration** - Displays expiration time in a styled metadata section
3. **conditional_instructions** - Only shows instructions when they exist
4. **color_coding** - Applies color-coding based on event type (tornado, flood, wind)
5. **show_map_link** - Includes a Google Maps link for the affected area
6. **mobile_responsive** - Applies modern mobile-responsive design with better styling
7. **show_social_sharing** - Adds Twitter and Facebook sharing buttons

## Visual Examples with Sample Data

Below are examples showing how different configurations affect the rendered HTML output using sample data from a High Wind Warning.

**Sample Alert Data:**
- **Event**: High Wind Warning
- **Issued By**: NWS Boulder (Northeastern Colorado)
- **Headline**: "High Wind Warning issued December 21 at 2:49PM MST until December 22 at 6:00AM MST by NWS Boulder"
- **Area**: Jefferson and West Douglas Counties Above 6000 Feet, Gilpin, Clear Creek, Northeast Park Counties

### Example 1: Default Configuration (All Features Disabled)

**Configuration:**
```ini
[template]
# All options default to false - no configuration needed
```

**Rendered Output:**
```html
<body>
  <h1>High Wind Warning issued December 21 at 2:49PM MST until December 22 at 6:00AM MST by NWS Boulder</h1>

  <p><strong>Description:</strong></p>
  <p>...HIGH WIND WARNING IN EFFECT FROM 6 PM THIS EVENING TO 6 AM MST TUESDAY...</p>

  <p><strong>Instructions:</strong></p>
  <p>REMEMBER...A HIGH WIND WARNING MEANS THAT STRONG AND POTENTIALLY DAMAGING WINDS...</p>

  <p><strong>Area Affected:</strong></p>
  <p>Jefferson and West Douglas Counties Above 6000 Feet, Gilpin, Clear Creek...</p>
</body>
```

**Output Size:** ~1,776 bytes  
**Use Case:** Simple, minimal alert display

---

### Example 2: Informative Configuration

**Configuration:**
```ini
[template]
show_event_info = true
show_expiration = true
```

**Rendered Output:**
```html
<body>
  <h1>High Wind Warning issued December 21 at 2:49PM MST until December 22 at 6:00AM MST by NWS Boulder</h1>

  <!-- Event Type and Issuer Information -->
  <p><strong>Event Type:</strong> High Wind Warning</p>
  <p><strong>Issued By:</strong> NWS Boulder (Northeastern Colorado)</p>

  <!-- Expiration Time Display -->
  <div class="alert-meta">
    <p><strong>Expires:</strong> 2015-12-22T06:00:00-07:00</p>
  </div>

  <p><strong>Description:</strong></p>
  <p>...HIGH WIND WARNING IN EFFECT FROM 6 PM THIS EVENING TO 6 AM MST TUESDAY...</p>

  <p><strong>Instructions:</strong></p>
  <p>REMEMBER...A HIGH WIND WARNING MEANS THAT STRONG AND POTENTIALLY DAMAGING WINDS...</p>

  <p><strong>Area Affected:</strong></p>
  <p>Jefferson and West Douglas Counties Above 6000 Feet, Gilpin, Clear Creek...</p>
</body>
```

**Output Size:** ~2,230 bytes  
**Use Case:** More context with event details and expiration time

---

### Example 3: Mobile-Optimized Configuration

**Configuration:**
```ini
[template]
show_event_info = true
conditional_instructions = true
show_map_link = true
mobile_responsive = true
```

**Rendered Output:**
```html
<body>
  <h1>High Wind Warning issued December 21...</h1>

  <!-- Event information in styled section -->
  <div class="alert-section">
    <p><strong>Event Type:</strong> High Wind Warning</p>
    <p><strong>Issued By:</strong> NWS Boulder (Northeastern Colorado)</p>
  </div>

  <!-- Description in styled section -->
  <div class="alert-section">
    <strong>Description:</strong>
    <p>...HIGH WIND WARNING IN EFFECT FROM 6 PM THIS EVENING...</p>
  </div>

  <!-- Instructions (only shown if present) -->
  <div class="alert-section">
    <strong>Instructions:</strong>
    <p>REMEMBER...A HIGH WIND WARNING MEANS THAT STRONG AND POTENTIALLY DAMAGING WINDS...</p>
  </div>

  <!-- Area with map link -->
  <div class="alert-section">
    <strong>Area Affected:</strong>
    <p>Jefferson and West Douglas Counties Above 6000 Feet...</p>
    <p><a href="https://www.google.com/maps/search/Jefferson%20and%20West%20Douglas%20Counties...">View on Map</a></p>
  </div>
</body>
```

**Styling Applied:**
- Modern font family (system fonts)
- Responsive padding and max-width (800px)
- Styled alert sections with left border
- Mobile-optimized font sizes
- Responsive breakpoints for small screens

**Output Size:** ~2,784 bytes  
**Use Case:** Optimized for mobile devices with better touch targets and readability

---

### Example 4: Full Featured Configuration

**Configuration:**
```ini
[template]
show_event_info = true
show_expiration = true
conditional_instructions = true
color_coding = true
show_map_link = true
mobile_responsive = true
show_social_sharing = true
```

**Rendered Output:**
```html
<body class="high-wind-warning">
  <h1>High Wind Warning issued December 21 at 2:49PM MST until December 22 at 6:00AM MST by NWS Boulder</h1>

  <!-- Event information -->
  <div class="alert-section">
    <p><strong>Event Type:</strong> High Wind Warning</p>
    <p><strong>Issued By:</strong> NWS Boulder (Northeastern Colorado)</p>
  </div>

  <!-- Expiration -->
  <div class="alert-meta">
    <p><strong>Expires:</strong> 2015-12-22T06:00:00-07:00</p>
  </div>

  <!-- Description -->
  <div class="alert-section">
    <strong>Description:</strong>
    <p>...HIGH WIND WARNING IN EFFECT FROM 6 PM THIS EVENING TO 6 AM MST TUESDAY...</p>
  </div>

  <!-- Instructions (conditional) -->
  <div class="alert-section">
    <strong>Instructions:</strong>
    <p>REMEMBER...A HIGH WIND WARNING MEANS THAT STRONG AND POTENTIALLY DAMAGING WINDS...</p>
  </div>

  <!-- Area with map link -->
  <div class="alert-section">
    <strong>Area Affected:</strong>
    <p>Jefferson and West Douglas Counties Above 6000 Feet, Gilpin, Clear Creek...</p>
    <p><a href="https://www.google.com/maps/search/...">View on Map</a></p>
  </div>

  <!-- Social sharing buttons -->
  <div class="share-buttons">
    <p><strong>Share this alert:</strong></p>
    <a href="https://twitter.com/intent/tweet?text=High%20Wind%20Warning...&url=https%3A//www.weather.gov/alerts/CO-HW-W-0006" target="_blank">Share on Twitter</a>
    <a href="https://www.facebook.com/sharer/sharer.php?u=https%3A//www.weather.gov/alerts/CO-HW-W-0006" target="_blank">Share on Facebook</a>
  </div>
</body>
```

**All Features Applied:**
- Event type and issuer information
- Expiration time display
- Conditional rendering (only shows instructions if present)
- Color-coded background (amber for wind alerts)
- Google Maps link
- Mobile-responsive design
- Social sharing buttons with proper URLs

**Output Size:** ~4,207 bytes  
**Use Case:** Maximum information and interactivity for comprehensive alert display

---

### Feature Comparison Table

| Feature | Default | Informative | Mobile-Optimized | Full Featured |
|---------|---------|-------------|------------------|---------------|
| **show_event_info** | ❌ | ✅ | ✅ | ✅ |
| **show_expiration** | ❌ | ✅ | ❌ | ✅ |
| **conditional_instructions** | ❌ | ❌ | ✅ | ✅ |
| **color_coding** | ❌ | ❌ | ❌ | ✅ |
| **show_map_link** | ❌ | ❌ | ✅ | ✅ |
| **mobile_responsive** | ❌ | ❌ | ✅ | ✅ |
| **show_social_sharing** | ❌ | ❌ | ❌ | ✅ |
| **Output Size** | ~1,776 bytes | ~2,230 bytes | ~2,784 bytes | ~4,207 bytes |

## Template Location

- **File**: `templates/detail.html`
- **Output**: Generated HTML files are saved to `output/` directory with filenames like `<alert_id>.html`
- **Configuration**: Set features in `config.txt` under `[template]` section

## Available Variables

The template has access to the following variables:

### `alert` Dictionary

Contains detailed information about the weather alert:

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `alert['headline']` | string | The main alert headline | "High Wind Warning issued December 21..." |
| `alert['event']` | string | Event type | "High Wind Warning", "Tornado Warning" |
| `alert['issuer']` | string | Issuing office name | "NWS Boulder (Northeastern Colorado)" |
| `alert['description']` | string | Full alert description | Detailed conditions and impact information |
| `alert['instructions']` | string | Safety instructions | Actions to take in response to the alert |
| `alert['area']` | string | Affected geographic area | "Jefferson County; Boulder County" |

### `expires` Variable

- **Type**: string (ISO 8601 timestamp)
- **Description**: When the alert expires
- **Example**: "2015-12-22T06:00:00-07:00"

## Default Template Structure

The default template includes:

```html
<!DOCTYPE html>
<html>
<head>
  <meta name="expires" content="{{ expires }}" />
  <meta name="viewport" content="initial-scale=1.0" />
  <title>{{ alert['event'] }}</title>
  <style>
    /* Basic styling */
  </style>
</head>
<body>
  <h1>{{ alert['headline'] }}</h1>
  
  <p><strong>Description:</strong></p>
  <p>{{ alert['description'] }}</p>
  
  <p><strong>Instructions:</strong></p>
  <p>{{ alert['instructions'] }}</p>
  
  <p><strong>Area Affected:</strong></p>
  <p>{{ alert['area'] }}</p>
</body>
</html>
```

## Customization Examples

### Example 1: Add Event Type and Issuer

Add information about the event type and issuing office:

```html
<body>
  <h1>{{ alert['headline'] }}</h1>
  
  <p><strong>Event Type:</strong> {{ alert['event'] }}</p>
  <p><strong>Issued By:</strong> {{ alert['issuer'] }}</p>
  
  <p><strong>Description:</strong></p>
  <p>{{ alert['description'] }}</p>
  
  <!-- rest of template -->
</body>
```

### Example 2: Add Expiration Time Display

Show when the alert expires in a human-readable format:

```html
<body>
  <h1>{{ alert['headline'] }}</h1>
  
  <div class="alert-meta">
    <p><strong>Expires:</strong> {{ expires }}</p>
  </div>
  
  <!-- rest of template -->
</body>
```

### Example 3: Conditional Instructions

Only show instructions if they exist:

```html
{% if alert['instructions'] %}
<p><strong>Instructions:</strong></p>
<p>{{ alert['instructions'] }}</p>
{% endif %}
```

### Example 4: Custom Styling by Event Type

Add color-coding based on alert severity:

```html
<style>
body.tornado { background-color: #ffe6e6; }
body.flood { background-color: #e6f3ff; }
body.wind { background-color: #fff4e6; }
</style>

<body class="{{ alert['event']|lower|replace(' ', '-') }}">
  <!-- content -->
</body>
```

### Example 5: Add a Map Link

Include a link to view the affected area on a map:

```html
<p><strong>Area Affected:</strong></p>
<p>{{ alert['area'] }}</p>
<p><a href="https://www.google.com/maps/search/{{ alert['area']|urlencode }}">View on Map</a></p>
```

### Example 6: Mobile-Friendly Layout

Enhance the mobile experience with better styling:

```html
<style>
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  line-height: 1.6;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  font-size: 1.5em;
  color: #d32f2f;
  border-bottom: 3px solid #d32f2f;
  padding-bottom: 10px;
}

.alert-section {
  margin: 20px 0;
  padding: 15px;
  background-color: #f5f5f5;
  border-left: 4px solid #d32f2f;
}

@media (max-width: 600px) {
  body {
    padding: 10px;
  }
  h1 {
    font-size: 1.2em;
  }
}
</style>

<body>
  <h1>{{ alert['headline'] }}</h1>
  
  <div class="alert-section">
    <strong>Description:</strong>
    <p>{{ alert['description'] }}</p>
  </div>
  
  <div class="alert-section">
    <strong>Instructions:</strong>
    <p>{{ alert['instructions'] }}</p>
  </div>
  
  <div class="alert-section">
    <strong>Area Affected:</strong>
    <p>{{ alert['area'] }}</p>
  </div>
</body>
```

### Example 7: Add Social Sharing

Include buttons to share the alert:

```html
<div class="share-buttons">
  <p><strong>Share this alert:</strong></p>
  <a href="https://twitter.com/intent/tweet?text={{ alert['headline']|urlencode }}&url={{ request.url|urlencode }}">
    Share on Twitter
  </a>
  <a href="https://www.facebook.com/sharer/sharer.php?u={{ request.url|urlencode }}">
    Share on Facebook
  </a>
</div>
```

## Jinja2 Template Features

### Filters

Jinja2 provides useful filters for text manipulation:

- `{{ variable|upper }}` - Convert to uppercase
- `{{ variable|lower }}` - Convert to lowercase
- `{{ variable|title }}` - Title case
- `{{ variable|trim }}` - Remove whitespace
- `{{ variable|replace('old', 'new') }}` - Replace text
- `{{ variable|urlencode }}` - URL encode

### Control Structures

```jinja2
{% if condition %}
  <!-- content if true -->
{% elif other_condition %}
  <!-- content if other condition -->
{% else %}
  <!-- content if false -->
{% endif %}

{% for item in list %}
  <!-- repeated content -->
{% endfor %}
```

## Testing Your Template

1. **Edit the template**:
   ```bash
   nano templates/detail.html
   ```

2. **Run the application**:
   ```bash
   python fetch.py --nopush --debug
   ```

3. **Check generated HTML**:
   ```bash
   ls -la output/
   # Open generated HTML files in a browser to preview
   ```

4. **Validate HTML**:
   - Use online validators like [W3C Validator](https://validator.w3.org/)
   - Test on multiple devices and browsers

## Linking Templates to Pushover Notifications

By default, Pushover notifications link to NOAA's official alert page. To have notifications link to your customized HTML templates instead, you need to:

### 1. Configure Base URL

Add a `base_url` to your `config.txt`:

```ini
[pushover]
token = YOUR_PUSHOVER_TOKEN
user = YOUR_PUSHOVER_USER_KEY
base_url = https://example.com/alerts
```

### 2. Host Your HTML Files

You need to make your `output/` directory accessible via the web. Options include:

**Option A: Simple HTTP Server (Testing Only)**
```bash
cd output
python -m http.server 8080
# Access at http://localhost:8080
```

**Option B: Nginx (Production)**
```nginx
server {
    listen 80;
    server_name example.com;
    
    location /alerts {
        alias /path/to/noaa-alerts-pushover/output;
        autoindex off;
    }
}
```

**Option C: Apache (Production)**
```apache
<Directory "/path/to/noaa-alerts-pushover/output">
    Options -Indexes
    Require all granted
</Directory>

Alias /alerts "/path/to/noaa-alerts-pushover/output"
```

### 3. Test the Setup

1. Run the application: `python fetch.py --debug`
2. Check the logs for the URL being used:
   ```
   Using custom base URL: https://example.com/alerts/abc123def.html
   ```
3. Click the URL in a Pushover notification to verify it loads your custom template

**Note:** If `base_url` is not set, notifications will link to NOAA's page, and template customizations will only be visible when viewing HTML files directly from the `output/` directory.

## Best Practices

1. **Keep it Simple**: Alert details should be easy to read quickly
2. **Mobile First**: Many users will view on mobile devices
3. **Accessibility**: Use semantic HTML and proper contrast ratios
4. **Performance**: Keep CSS and HTML minimal for fast loading
5. **Test Thoroughly**: Test with different alert types and content lengths
6. **Preserve Information**: Don't hide critical safety information
7. **Escaping**: Jinja2 auto-escapes HTML by default for security

## Common Issues

### Issue: Variables Not Showing

**Problem**: `{{ alert['missing_field'] }}` shows nothing

**Solution**: Check if the field exists:
```jinja2
{% if alert.get('missing_field') %}
  {{ alert['missing_field'] }}
{% else %}
  No information available
{% endif %}
```

### Issue: HTML Not Updating

**Problem**: Changes to template don't appear in output

**Solution**: 
- Delete old HTML files: `rm output/*.html`
- Run fetch.py again to regenerate

### Issue: Broken Layout

**Problem**: Layout looks wrong on some devices

**Solution**: Add responsive meta tag and CSS:
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
```

## Additional Resources

- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [HTML5 Reference](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [CSS Tricks](https://css-tricks.com/)
- [NOAA CAP Documentation](http://docs.oasis-open.org/emergency/cap/v1.2/)

## Support

For questions or issues:
- Open an issue on GitHub
- Check existing documentation
- Review sample.json for available data structure

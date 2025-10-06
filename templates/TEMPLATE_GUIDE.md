# Detail Template Customization Guide

## Overview

The `templates/detail.html` file is a Jinja2 template used to generate HTML pages for individual weather alerts. These HTML pages are created in the `output/` directory and can be linked from push notifications.

## Quick Start: Pre-built Templates

**New!** This repository includes pre-built example templates you can use immediately:

- `example1_event_issuer.html` - Shows event type and issuing office
- `example2_expiration.html` - Displays expiration time
- `example3_conditional.html` - Conditional instructions display
- `example4_styling.html` - Color-coded by event type
- `example5_map.html` - Includes map link
- `example6_mobile.html` - Mobile-responsive design
- `example7_social.html` - Social sharing buttons
- `combined_all.html` - All features combined

To use a pre-built template, add this to your `config.txt`:

```ini
[template]
template_file = combined_all.html
```

See [README.md](README.md) in this directory for full template descriptions.

## Template Location

- **File**: `templates/detail.html` (default)
- **Output**: Generated HTML files are saved to `output/` directory with filenames like `<alert_id>.html`
- **Configuration**: Set in `config.txt` under `[template]` section

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

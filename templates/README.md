# Templates Directory

This directory contains templates and sample data for the NOAA Alerts Pushover application.

## Files

### detail.html
**Type**: Jinja2 HTML Template

**Purpose**: Generates individual HTML pages for weather alerts that are saved to the `output/` directory.

**Usage**: This template is automatically used by `fetch.py` to create alert detail pages. The generated HTML files can be linked from push notifications for users to view full alert details.

**Customization**: See [TEMPLATE_GUIDE.md](../TEMPLATE_GUIDE.md) in the root directory for detailed instructions on how to customize this template.

**Variables Available**:
- `alert['headline']` - Main alert headline
- `alert['event']` - Event type (e.g., "High Wind Warning")
- `alert['issuer']` - Issuing NWS office
- `alert['description']` - Full alert description
- `alert['instructions']` - Safety instructions
- `alert['area']` - Affected geographic area
- `expires` - Alert expiration timestamp

### sample.json
**Type**: JSON (GeoJSON with CAP properties)

**Purpose**: Sample NOAA weather alert data in the current GeoJSON format used by the NOAA Weather API.

**Usage**: This file serves as:
1. **Reference** - Example of the data structure returned by `https://api.weather.gov/alerts`
2. **Testing** - Can be used for testing template modifications
3. **Documentation** - Shows all available fields from the NOAA API

**Format**: GeoJSON FeatureCollection with CAP (Common Alerting Protocol) properties embedded in each feature.

**Key Structure**:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "properties": {
        "headline": "...",
        "event": "...",
        "description": "...",
        "instruction": "...",
        "areaDesc": "...",
        "geocode": {
          "FIPS6": ["..."],
          "UGC": ["..."]
        },
        "expires": "...",
        ...
      }
    }
  ]
}
```

**Historical Note**: This replaces the previous `sample.xml` file. The NOAA Weather API transitioned from XML to JSON/GeoJSON format. The application now exclusively uses the JSON API endpoint.

## Testing Templates

To test modifications to `detail.html`:

1. Make changes to the template
2. Run the application: `python fetch.py --nopush --debug`
3. Check generated HTML files in `output/` directory
4. Open HTML files in a browser to preview

## API Documentation

For complete documentation of the NOAA Weather API data format:
- [NOAA Weather API Documentation](https://www.weather.gov/documentation/services-web-api)
- [CAP v1.2 Standard](http://docs.oasis-open.org/emergency/cap/v1.2/)

## Support

For questions about template customization:
- See [TEMPLATE_GUIDE.md](../TEMPLATE_GUIDE.md)
- Check [CODE_EXPLANATION.md](../CODE_EXPLANATION.md) for architecture details
- Open an issue on GitHub

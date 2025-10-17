# NOAA User-Agent Requirement Compliance

The weather.gov API, provided by the National Weather Service (NWS), requires a User-Agent header in its requests. This header identifies the client making the request, allowing the NWS to understand the usage patterns and contact the user if necessary.

**Requirements for the User-Agent:**
- Format: The User-Agent should be a string containing a contact email address or a URL where the NWS can reach the user.
- Purpose: This contact information is crucial for the NWS to communicate any changes, issues, or important updates regarding the API.

**Example:**
- `MyApplicationName/1.0 (myemail@example.com)`
- `MyApplicationName/1.0 (https://www.example.com/contact)`

**Importance of a Proper User-Agent:**
- Compliance: Adhering to this requirement ensures compliance with the NWS API usage policies.
- Communication: It provides a channel for the NWS to contact you in case of API changes, outages, or potential abuse.
- Troubleshooting: It can assist in troubleshooting issues if the NWS needs to identify the source of specific requests.
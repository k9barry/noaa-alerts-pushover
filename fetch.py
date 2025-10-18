import argparse
import arrow
import configparser
import datetime
import hashlib
import jinja2
import json
import logging
import os
import requests
import sys
import urllib3

from models import Alert

# Disable SSL warnings (not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Parser(object):
    """ A convenience object to hold our functionality """


    def __init__(self, pushover_token, pushover_user, pushover_api_url, noaa_api_url, directory):
        self.pushover_token = pushover_token
        self.pushover_user = pushover_user
        self.pushover_api_url = pushover_api_url
        self.noaa_api_url = noaa_api_url
        self.current_dir = directory
        self.counties = None
        self.fips_watch_list = None
        self.ugc_watch_list = None


    def create_alert_title(self, p_alert):
        """ Formats the title for an alert message """
        # The push notification title should be like:
        # 'Arapahoe County (CO) Weather Alert'
        # The message is the title with the last characters
        # of the identifier added.
        msg_title = '%s (%s) Weather Alert' % (p_alert.county, p_alert.state)
        return msg_title


    def create_alert_message(self, p_alert):
        """ Creates the message body for the alert message """

        # If there are details, we append those into the title. This only
        # happens when it's a generic "Special Weather Statement" and helps
        # add context to the alert.
        if p_alert.details:
            title = p_alert.title.replace('issued', '(%s) issued' % p_alert.details)
        else:
            title = p_alert.title

        message = '%s (%s)' % (title, p_alert.alert_id[-5:])
        return message


    def send_pushover_alert(self, id, title, message, url):
        """ Sends an alert via Pushover API """
        request = requests.post(self.pushover_api_url, data={
            "title": title,
            "token": self.pushover_token,
            "user": self.pushover_user,
            "message": message,
            "sound": "falling",
            "url": url,
        }, timeout=30)

        if not request.ok:
            logger.error("Error sending push: %s\n" % request.text)
        else:
            logger.info("Sent push: %s" % title)


    def check_new_alerts(self, created_ts):
        """ Looks at the alerts created this run for ones we care about """

        # Keep track of alerts that match our watched counties
        matched_alerts = []

        # Iterate over the alerts in the latest run
        for alert_record in Alert.select().where(Alert.created == created_ts):

            # Get all the UGC codes for the alert
            if alert_record.ugc_codes:
                ugc_codes = alert_record.ugc_codes.split(',')
            else:
                ugc_codes = []

            # Get all the FIPS codes for the alert
            if alert_record.fips_codes:
                fips_codes = alert_record.fips_codes.split(',')
            else:
                fips_codes = []

            # Compare the fips and ugc codes to see if they overlap. If they
            # do, then we have a match
            ugc_match = set(ugc_codes).intersection(self.ugc_watch_list)
            fips_match = set(fips_codes).intersection(self.fips_watch_list)

            matched_counties = []

            # See if any of the UGC codes match our target counties
            for ugc_code in ugc_match:
                matched_counties = [county for county in self.counties if county['ugc'] == ugc_code]

            # See if any of the FIPS codes match our target counties
            for fips_code in fips_match:
                matched_counties = [county for county in self.counties if county['fips'] == fips_code]

            if len(matched_counties) > 0:
                # Because the counties we check are very far apart, the matched
                # counties should never be more than one. We only care about the
                # first, so just assign it.
                alert_record.county = matched_counties[0]['name']
                alert_record.state = matched_counties[0]['state']
                matched_alerts.append(alert_record)

        return matched_alerts


    def details_for_alert(self, alert):
        """ Fetches the NOAA detail JSON feed for an alert and returns the description """
        logger.info('Fetching Detail Link for Alert %s' % alert.alert_id)
        request = requests.get(alert.api_url)
        # Check for HTML or wrong content type
        if (
            'text/html' in request.headers.get('Content-Type', '')
            or request.text.strip().lower().startswith('<!doctype html')
            or request.text.strip().lower().startswith('<html')
        ):
            logger.error(f"Expected JSON but got HTML for alert {alert.alert_id}. Response was:\n{request.text[:1000]}")
            return None
        try:
            data = request.json()
        except Exception as e:
            logger.error(f"Failed to parse alert detail JSON: {e}\nResponse was:\n{request.text[:1000]}")
            return None

        # Extract properties from the GeoJSON feature response
        properties = data.get('properties', {})
        
        return {
            'headline': properties.get('headline', ''), 
            'event': properties.get('event', ''), 
            'issuer': properties.get('senderName', ''), 
            'description': properties.get('description', ''), 
            'instructions': properties.get('instruction', ''), 
            'area': properties.get('areaDesc', ''),
        }


    def fetch(self, run_timestamp):
        """ Fetches the NOAA alerts JSON feed and inserts into database """

        logger.info('Fetching Alerts Feed')
        request = requests.get(self.noaa_api_url)
        if request.status_code != 200:
            logger.error(f"Failed to fetch alerts feed: HTTP {request.status_code}")
            return
        # Check for HTML or wrong content type
        if (
            'text/html' in request.headers.get('Content-Type', '')
            or request.text.strip().lower().startswith('<!doctype html')
            or request.text.strip().lower().startswith('<html')
        ):
            logger.error(f"Expected JSON but got HTML. Response was:\n{request.text[:1000]}")
            return
        try:
            data = request.json()
        except Exception as e:
            logger.error(f"Failed to parse alerts feed JSON: {e}\nResponse was:\n{request.text[:1000]}")
            return

        total_count = 0
        insert_count = 0
        existing_count = 0

        for feature in data.get('features', []):
            total_count += 1
            properties = feature.get('properties', {})
            alert_id = hashlib.sha224(properties.get('id', '').encode('utf-8')).hexdigest()
            # Ensure title is never None or empty for DB NOT NULL constraint
            title = properties.get('headline')
            if not title:
                title = properties.get('event')
            if not title:
                title = properties.get('id')
            if not title:
                title = 'NO TITLE'
            event = properties.get('event', '')
            detail = ''
            description = properties.get('description', '')
            expires_str = properties.get('expires')
            try:
                expires_dt = arrow.get(expires_str) if expires_str else None
                expires = expires_dt.isoformat() if expires_dt else None
                expires_utc_ts = int(expires_dt.to('UTC').timestamp()) if expires_dt else 0
            except Exception:
                expires = None
                expires_utc_ts = 0
            url = properties.get('uri', '')
            api_url = properties.get('@id', '')
            fips_list = properties.get('geocode', {}).get('FIPS6', [])
            ugc_list = properties.get('geocode', {}).get('UGC', [])
            if isinstance(fips_list, str):
                fips_list = [fips_list]
            if isinstance(ugc_list, str):
                ugc_list = [ugc_list]

            # Optionally extract sub-events from description
            if event in ('Severe Weather Statement', 'Special Weather Statement') and description:
                summary = description.upper()
                sub_events = []
                for item in ('Thunderstorm', 'Strong Storm', 'Wind', 'Rain', 'Hail', 'Tornado', 'Flood'):
                    if item.upper() in summary:
                        sub_events.append(item)
                detail = ', '.join(sub_events)

            try:
                alert_record = Alert.get(Alert.alert_id == alert_id)
                existing_count += 1
            except Exception as _:
                insert_count += 1
                alert_record = Alert.create(
                    alert_id=alert_id,
                    title=title,
                    event=event,
                    details=detail,
                    description=description,
                    expires=expires,
                    expires_utc_ts=expires_utc_ts,
                    url=url,
                    api_url=api_url,
                    fips_codes=','.join(fips_list),
                    ugc_codes=','.join(ugc_list),
                    created=run_timestamp,
                )

        logger.debug("Found %d alerts in feed." % total_count)
        logger.info("Inserted %d new alerts." % insert_count)
        logger.debug("Matched %d existing alerts." % existing_count)


if __name__ == '__main__':

    # Parse the command-line arguments
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--purge', dest='purge', action='store_true')
    argparser.set_defaults(purge=False)
    argparser.add_argument('--nopush', dest='nopush', action='store_true')
    argparser.set_defaults(nopush=False)
    argparser.add_argument('--debug', dest='debug', action='store_true')
    argparser.set_defaults(debug=False)
    args = vars(argparser.parse_args())

    # Set up logger
    logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s  %(message)s')
    logging.Formatter(fmt='%(asctime)s', datefmt='%Y-%m-%d,%H:%M:%S')
    logger = logging.getLogger(__name__)

    # Make sure the requests library only logs errors
    logging.getLogger("requests").setLevel(logging.ERROR)

    # Log debug-level statements if we are in debugging mode
    if args['debug']:
        logger.level = logging.DEBUG

    # Make sure we can load our files regardless of where the script is called from
    CUR_DIR = os.path.dirname(os.path.realpath(__file__))

    # Set up the output directory
    OUTPUT_DIR = os.path.join(CUR_DIR, 'output')
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        logger.info('Created output directory: %s' % OUTPUT_DIR)

    # Load the configuration
    config = configparser.ConfigParser()
    config_filepath = os.path.join(CUR_DIR, 'config.txt')
    config.read(config_filepath)

    # Get template customization options from config
    template_options = {
        'show_event_info': False,
        'show_expiration': False,
        'conditional_instructions': False,
        'color_coding': False,
        'show_map_link': False,
        'mobile_responsive': False,
        'show_social_sharing': False
    }
    
    if config.has_section('template'):
        for option in template_options.keys():
            try:
                template_options[option] = config.getboolean('template', option)
            except (configparser.NoOptionError, ValueError):
                pass  # Keep default value
    
    # Set up the template engine
    template_loader = jinja2.FileSystemLoader('./templates')
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "detail.html"
    template = template_env.get_template(template_file)

    # Get the list of events that we don't want to be alerted about
    try:
        ignored_events = config.get('events', 'ignored').split(',')
    except configparser.NoSectionError:
        ignored_events = []

    # Instantiate our parser object
    PUSHOVER_TOKEN = config.get('pushover', 'token')
    PUSHOVER_USER = config.get('pushover', 'user')
    
    # Get optional Pushover API URL (defaults to standard endpoint)
    try:
        PUSHOVER_API_URL = config.get('pushover', 'api_url')
    except (configparser.NoSectionError, configparser.NoOptionError):
        PUSHOVER_API_URL = 'https://api.pushover.net/1/messages.json'
    
    # Get optional base URL for hosted HTML files
    try:
        BASE_URL = config.get('pushover', 'base_url')
        # Remove trailing slash if present
        if BASE_URL.endswith('/'):
            BASE_URL = BASE_URL[:-1]
    except (configparser.NoSectionError, configparser.NoOptionError):
        BASE_URL = None
    
    # Get NOAA API URL (defaults to standard endpoint)
    try:
        NOAA_API_URL = config.get('noaa', 'api_url')
    except (configparser.NoSectionError, configparser.NoOptionError):
        NOAA_API_URL = 'https://api.weather.gov/alerts'
    
    parser = Parser(PUSHOVER_TOKEN, PUSHOVER_USER, PUSHOVER_API_URL, NOAA_API_URL, CUR_DIR)

    # Load the counties we want to monitor
    counties_filepath = os.path.join(CUR_DIR, 'counties.json')
    with open(counties_filepath, 'r') as f:
        parser.counties = json.loads(f.read())
    
    # Check if test messages should be enabled
    try:
        test_message_enabled = config.getboolean('pushover', 'test_message', fallback=False)
    except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
        test_message_enabled = False
    
    # Add test message county if enabled
    if test_message_enabled:
        test_county = {
            "fips": "",
            "name": "TEST MESSAGES",
            "state": "NA",
            "ugc": "MDC031"
        }
        # Only add if not already present
        if not any(c.get('ugc') == 'MDC031' for c in parser.counties):
            parser.counties.append(test_county)
            logger.info("Test messages enabled - monitoring MDC031")

    # Assign the fips and ugc codes to watch for
    parser.fips_watch_list = [str(c['fips']) for c in parser.counties]
    parser.ugc_watch_list = [str(c['ugc']) for c in parser.counties]

    # If we got a command-line flag to purge the saved alerts, do
    # that before we fetch new alerts. If we didn't get the purge command,
    # delete any alerts that are now expired.
    if args['purge']:
        Alert.delete().execute()
    else:
        ago_ts = arrow.utcnow().shift(days=-1).timestamp()
        count = Alert.delete().where(Alert.expires_utc_ts < ago_ts).execute()
        logger.debug("Deleted %d expired alerts." % count)

    # Create a timestamp that will act as a numeric identifier for
    # this fetching run. We'll use this later to see if a record
    # has been added in this run
    run_ts = arrow.utcnow().timestamp()

    # Go grab the current alerts and process them
    parser.fetch(run_ts)

    # Find any new alerts that match our counties
    for alert in parser.check_new_alerts(run_ts):

        # See if they are in the list of alerts to ignore
        if alert.event not in ignored_events:

            # Get the details about the alert from the API
            details = parser.details_for_alert(alert)

            # Format expires timestamp as human-readable string for display
            expires_formatted = arrow.get(alert.expires_utc_ts).format('YYYY-MM-DD HH:mm:ss')

            # Render the detail page
            output = template.render({
                'alert': details,
                'expires': expires_formatted,
                'expires_timestamp': int(alert.expires_utc_ts),
                'alert_url': alert.url,
                'template_options': template_options
            })
            detail_filepath = os.path.join(OUTPUT_DIR, '%s.html' % alert.alert_id)
            with open(detail_filepath, 'w') as f:
                f.write(output)

            # Construct the title and message body for the alert
            alert_title = parser.create_alert_title(alert)
            alert_msg = parser.create_alert_message(alert)
            alert_id = alert.alert_id
            logger.info('Alert to send: %s' % alert_title)
            
            # Determine the URL to use in the push notification
            if BASE_URL:
                # Use custom base URL to link to locally hosted HTML
                push_url = '%s/%s.html' % (BASE_URL, alert_id)
                logger.debug('Using custom base URL: %s' % push_url)
            else:
                # Fall back to NOAA's official alert URL
                push_url = alert.url
                logger.debug('Using NOAA URL: %s' % push_url)

            # Check the argument to see if we should be sending the push
            if not args['nopush']:
                parser.send_pushover_alert(alert_id, alert_title, alert_msg, push_url)
            else:
                logger.info('Sending pushes disabled by argument')

        else:
            logger.info('Ignoring %s, %s alert for %s' % (alert.county, alert.state, alert.event))

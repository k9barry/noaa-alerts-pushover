#!/usr/bin/env python3
"""
Scheduler for NOAA Alerts Pushover
Uses Python schedule library to run fetch.py, cleanup.py, and vacuum.py on configurable schedules
"""

import argparse
import configparser
import logging
import os
import schedule
import subprocess
import sys
import time


# Set up logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def run_fetch(args_list):
    """Run fetch.py with optional arguments"""
    cmd = [sys.executable, 'fetch.py'] + args_list
    logger.info(f"Running fetch.py with args: {args_list}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            logger.info("fetch.py completed successfully")
            if result.stdout:
                logger.debug(f"Output: {result.stdout}")
        else:
            logger.error(f"fetch.py failed with return code {result.returncode}")
            if result.stderr:
                logger.error(f"Error: {result.stderr}")
    except subprocess.TimeoutExpired:
        logger.error("fetch.py timed out after 300 seconds")
    except Exception as e:
        logger.error(f"Error running fetch.py: {e}")


def run_cleanup():
    """Run cleanup.py to remove expired HTML files"""
    cmd = [sys.executable, 'cleanup.py']
    logger.info("Running cleanup.py")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            logger.info("cleanup.py completed successfully")
            if result.stdout:
                logger.info(f"Cleanup output: {result.stdout.strip()}")
        else:
            logger.error(f"cleanup.py failed with return code {result.returncode}")
            if result.stderr:
                logger.error(f"Error: {result.stderr}")
    except subprocess.TimeoutExpired:
        logger.error("cleanup.py timed out after 60 seconds")
    except Exception as e:
        logger.error(f"Error running cleanup.py: {e}")


def run_vacuum():
    """Run vacuum.py for database maintenance"""
    cmd = [sys.executable, 'vacuum.py']
    logger.info("Running vacuum.py")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            logger.info("vacuum.py completed successfully")
            if result.stdout:
                logger.info(f"Vacuum output: {result.stdout.strip()}")
        else:
            logger.error(f"vacuum.py failed with return code {result.returncode}")
            if result.stderr:
                logger.error(f"Error: {result.stderr}")
    except subprocess.TimeoutExpired:
        logger.error("vacuum.py timed out after 60 seconds")
    except Exception as e:
        logger.error(f"Error running vacuum.py: {e}")


def main():
    """Main scheduler loop"""
    parser = argparse.ArgumentParser(description='NOAA Alerts Pushover Scheduler')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--nopush', action='store_true', 
                       help='Disable push notifications (passed to fetch.py)')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    # Build args list to pass to fetch.py
    fetch_args = []
    if args.debug:
        fetch_args.append('--debug')
    if args.nopush:
        fetch_args.append('--nopush')

    # Load configuration
    CUR_DIR = os.path.dirname(os.path.realpath(__file__))
    config_filepath = os.path.join(CUR_DIR, 'config.txt')
    
    if not os.path.exists(config_filepath):
        logger.error(f"Configuration file not found: {config_filepath}")
        logger.error("Please create config.txt from config.txt.example")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(config_filepath)

    # Get schedule intervals from config with defaults
    try:
        fetch_interval = config.getint('schedule', 'fetch_interval', fallback=5)
        cleanup_interval = config.getint('schedule', 'cleanup_interval', fallback=24)
        vacuum_interval = config.getint('schedule', 'vacuum_interval', fallback=168)
    except (configparser.NoSectionError, ValueError) as e:
        logger.warning(f"Error reading schedule config, using defaults: {e}")
        fetch_interval = 5
        cleanup_interval = 24
        vacuum_interval = 168

    logger.info("=== NOAA Alerts Pushover Scheduler Started ===")
    logger.info(f"Fetch interval: {fetch_interval} minutes")
    logger.info(f"Cleanup interval: {cleanup_interval} hours")
    logger.info(f"Vacuum interval: {vacuum_interval} hours")

    # Schedule jobs
    schedule.every(fetch_interval).minutes.do(run_fetch, fetch_args)
    schedule.every(cleanup_interval).hours.do(run_cleanup)
    schedule.every(vacuum_interval).hours.do(run_vacuum)

    # Run fetch immediately on startup
    logger.info("Running initial fetch...")
    run_fetch(fetch_args)

    # Main scheduler loop
    logger.info("Scheduler running. Press Ctrl+C to exit.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Scheduler error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

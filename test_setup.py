#!/usr/bin/env python3
"""
Test script to validate the NOAA Alerts Pushover setup
Run this before starting the application to catch configuration issues
"""

import os
import sys
import json
import argparse
import subprocess
import shutil
import logging

def test_python_version():
    """Check Python version"""
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("  ❌ Python 3.8+ required, found:", sys.version)
        return False
    print(f"  ✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def test_imports():
    """Test that all required modules can be imported"""
    print("\nChecking required modules...")
    modules = ['arrow', 'beautifulsoup4', 'jinja2', 'peewee', 'requests']
    all_ok = True
    
    for module_name in modules:
        try:
            if module_name == 'beautifulsoup4':
                __import__('bs4')
            else:
                __import__(module_name)
            print(f"  ✓ {module_name}")
        except ImportError as e:
            print(f"  ❌ {module_name}: {e}")
            all_ok = False
    
    return all_ok

def test_config_file(auto_fix=False):
    """Check if config.txt exists and is readable"""
    print("\nChecking configuration file...")
    config_path = 'config.txt'
    
    if not os.path.exists(config_path):
        print(f"  ❌ {config_path} not found")
        if auto_fix:
            # In interactive mode, prompt first
            if '--interactive' in sys.argv or '-i' in sys.argv:
                response = input("  ❓ Create config.txt from config.txt.example? [y/N]: ")
                if response.lower() not in ['y', 'yes']:
                    print("     Skipped. Create it manually from config.txt.example")
                    return False
            return fix_config_file()
        else:
            print("     Create it from config.txt.example")
            print("     Or run: python test_setup.py --fix")
            return False
    
    try:
        import configparser
        config = configparser.ConfigParser()
        config.read(config_path)
        
        # Check required sections
        if not config.has_section('pushover'):
            print("  ❌ Missing [pushover] section")
            return False
        
        if not config.has_option('pushover', 'token'):
            print("  ❌ Missing pushover token")
            return False
        
        if not config.has_option('pushover', 'user'):
            print("  ❌ Missing pushover user")
            return False
        
        token = config.get('pushover', 'token')
        user = config.get('pushover', 'user')
        
        if 'YOUR_' in token or 'TEST_' in token:
            print("  ⚠️  Warning: Token looks like a placeholder")
        
        if 'YOUR_' in user or 'TEST_' in user:
            print("  ⚠️  Warning: User key looks like a placeholder")
        
        # Check schedule section (optional but recommended)
        if config.has_section('schedule'):
            try:
                fetch_interval = config.getint('schedule', 'fetch_interval', fallback=5)
                cleanup_interval = config.getint('schedule', 'cleanup_interval', fallback=24)
                vacuum_interval = config.getint('schedule', 'vacuum_interval', fallback=168)
                print(f"  ✓ Schedule config found: fetch={fetch_interval}m, cleanup={cleanup_interval}h, vacuum={vacuum_interval}h")
            except ValueError as e:
                print(f"  ⚠️  Warning: Invalid schedule values: {e}")
        else:
            print("  ℹ️  No [schedule] section found, using defaults (fetch=5m, cleanup=24h, vacuum=168h)")
        
        # Check test_message option (optional)
        try:
            test_message = config.getboolean('pushover', 'test_message', fallback=False)
            if test_message:
                print("  ℹ️  Test messages enabled - will monitor MDC031 for NOAA test alerts")
            else:
                print("  ✓ Test messages disabled (recommended for production)")
        except ValueError:
            print("  ⚠️  Warning: test_message should be 'true' or 'false'")
        
        # Check NOAA API URL (optional)
        if config.has_section('noaa'):
            try:
                noaa_api_url = config.get('noaa', 'api_url')
                print(f"  ✓ NOAA API URL: {noaa_api_url}")
            except configparser.NoOptionError:
                print("  ℹ️  [noaa] section exists but no api_url specified, using default (https://api.weather.gov/alerts)")
            except Exception as e:
                print(f"  ⚠️  Warning: Error reading NOAA API URL: {e}")
        else:
            print("  ℹ️  No [noaa] section found, using default API URL (https://api.weather.gov/alerts)")
        
        # Check User-Agent configuration (optional but recommended)
        if config.has_section('user_agent'):
            try:
                app_name = config.get('user_agent', 'app_name', fallback='')
                version = config.get('user_agent', 'version', fallback='')
                contact = config.get('user_agent', 'contact', fallback='')
                
                if app_name and version and contact:
                    user_agent = f"{app_name}/{version} ({contact})"
                    print(f"  ✓ User-Agent configured: {user_agent}")
                    
                    # Warn if contact looks like placeholder
                    if 'example.com' in contact or 'YOUR_' in contact.upper():
                        print("  ⚠️  Warning: Contact looks like a placeholder - please update with your actual contact info")
                else:
                    print("  ⚠️  Warning: [user_agent] section incomplete - missing app_name, version, or contact")
                    print("     NWS API requires User-Agent with contact information")
            except Exception as e:
                print(f"  ⚠️  Warning: Error reading User-Agent config: {e}")
        else:
            print("  ⚠️  Warning: No [user_agent] section found")
            print("     NWS API requires User-Agent with contact information")
            print("     Add [user_agent] section with app_name, version, and contact")
        
        # Check template configuration (optional)
        if config.has_section('template'):
            try:
                template_options = ['show_event_info', 'show_expiration', 'conditional_instructions', 
                                   'color_coding', 'show_map_link', 'mobile_responsive', 'show_social_sharing']
                enabled_count = 0
                for option in template_options:
                    if config.getboolean('template', option, fallback=False):
                        enabled_count += 1
                
                if enabled_count > 0:
                    print(f"  ✓ Template customization: {enabled_count} option(s) enabled")
                else:
                    print("  ℹ️  Template customization: all options disabled (using defaults)")
            except ValueError as e:
                print(f"  ⚠️  Warning: Invalid template option values: {e}")
                print("     Template options should be 'true' or 'false'")
            except Exception as e:
                print(f"  ⚠️  Warning: Error reading template config: {e}")
        else:
            print("  ℹ️  No [template] section found, using default HTML template")
        
        print(f"  ✓ config.txt found and readable")
        return True
        
    except Exception as e:
        print(f"  ❌ Error reading config: {e}")
        return False

def test_counties_file():
    """Check if counties.json exists and is valid"""
    print("\nChecking counties configuration...")
    counties_path = 'counties.json'
    
    if not os.path.exists(counties_path):
        print(f"  ❌ {counties_path} not found")
        return False
    
    try:
        with open(counties_path, 'r') as f:
            counties = json.load(f)
        
        if not isinstance(counties, list):
            print("  ❌ counties.json should be a JSON array")
            return False
        
        if len(counties) == 0:
            print("  ⚠️  Warning: No counties configured")
        
        # Validate structure
        for i, county in enumerate(counties):
            required = ['fips', 'name', 'state', 'ugc']
            for field in required:
                if field not in county:
                    print(f"  ❌ County {i}: missing '{field}' field")
                    return False
        
        print(f"  ✓ {len(counties)} county/counties configured")
        return True
        
    except json.JSONDecodeError as e:
        print(f"  ❌ Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error reading counties: {e}")
        return False

def test_directories():
    """Check required directories"""
    print("\nChecking directories...")
    dirs = ['templates', 'output', 'data']
    all_ok = True
    
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"  ✓ {dir_name}/")
        else:
            if dir_name in ['output', 'data']:
                print(f"  ℹ️  {dir_name}/ (will be created automatically)")
            else:
                print(f"  ❌ {dir_name}/ not found")
                all_ok = False
    
    return all_ok

def test_database(auto_fix=False):
    """Test database connection"""
    print("\nChecking database...")
    try:
        from models import db, Alert
        
        # Try to connect
        db.connect()
        
        # Check if table exists
        if not Alert.table_exists():
            print("  ℹ️  Database table not initialized")
            if auto_fix:
                # In interactive mode, prompt first
                if '--interactive' in sys.argv or '-i' in sys.argv:
                    response = input("  ❓ Initialize database now? [y/N]: ")
                    if response.lower() not in ['y', 'yes']:
                        print("     Skipped. Run: python models.py")
                        return True
                return fix_database()
            else:
                print("     Run: python models.py")
                print("     Or run: python test_setup.py --fix")
                return True  # Not a critical error
        
        print("  ✓ Database initialized")
        db.close()
        return True
        
    except Exception as e:
        print(f"  ⚠️  Database check: {e}")
        return True  # Not critical for initial setup

def fix_config_file():
    """Create config.txt from config.txt.example"""
    print("  🔧 Attempting to fix...")
    config_example = 'config.txt.example'
    config_path = 'config.txt'
    
    if not os.path.exists(config_example):
        print(f"  ❌ {config_example} not found, cannot auto-fix")
        return False
    
    try:
        shutil.copy(config_example, config_path)
        print(f"  ✓ Created {config_path} from {config_example}")
        print("  ⚠️  IMPORTANT: Edit config.txt and add your Pushover credentials!")
        print("     - Get your credentials from https://pushover.net")
        return True
    except Exception as e:
        print(f"  ❌ Failed to create config.txt: {e}")
        return False


def fix_database():
    """Initialize the database by running models.py"""
    print("  🔧 Attempting to initialize database...")
    
    try:
        # Import and run the database initialization
        import models
        if models.db.is_closed():
            models.db.connect()
        models.db.create_tables([models.Alert])
        print("  ✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"  ❌ Failed to initialize database: {e}")
        return False


def run_fetch_test(logger=None):
    """Run fetch.py --nopush --debug to test the application"""
    print("\nRunning test fetch (no push, debug mode)...")
    if logger:
        logger.info("Running test fetch with --nopush --debug flags")
    
    try:
        # Run fetch.py with --nopush and --debug flags
        result = subprocess.run(
            [sys.executable, 'fetch.py', '--nopush', '--debug'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Print output to console
        if result.stdout:
            print(result.stdout)
            if logger:
                for line in result.stdout.splitlines():
                    logger.info(f"FETCH: {line}")
        
        if result.stderr:
            print(result.stderr, file=sys.stderr)
            if logger:
                for line in result.stderr.splitlines():
                    logger.info(f"FETCH: {line}")
        
        if result.returncode == 0:
            print("  ✓ Test fetch completed successfully")
            if logger:
                logger.info("Test fetch completed successfully")
            return True
        else:
            print(f"  ⚠️  Test fetch exited with code {result.returncode}")
            if logger:
                logger.warning(f"Test fetch exited with code {result.returncode}")
            return True  # Not a critical failure for setup validation
            
    except subprocess.TimeoutExpired:
        print("  ⚠️  Test fetch timed out (60 seconds)")
        if logger:
            logger.warning("Test fetch timed out after 60 seconds")
        return True  # Not a critical failure
    except Exception as e:
        print(f"  ❌ Failed to run test fetch: {e}")
        if logger:
            logger.error(f"Failed to run test fetch: {e}")
        return False


def main():
    """Run all tests"""
    parser = argparse.ArgumentParser(
        description='Validate NOAA Alerts Pushover setup',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_setup.py              # Run validation checks
  python test_setup.py --fix        # Auto-fix common issues
  python test_setup.py --interactive # Interactive mode with prompts
        """
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Automatically fix common issues (create config.txt, initialize database)'
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Interactive mode: prompt before fixing each issue'
    )
    
    args = parser.parse_args()
    
    # Determine if we should auto-fix
    auto_fix = args.fix
    interactive = args.interactive
    
    # Set up logging to both file and console
    logger = None
    if interactive or auto_fix:
        # Configure logging for interactive/auto-fix mode
        log_filename = 'setup_validation.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s  %(message)s',
            handlers=[
                logging.FileHandler(log_filename)
            ]
        )
        logger = logging.getLogger(__name__)
        logger.info("=" * 60)
        logger.info("NOAA Alerts Pushover - Setup Validation")
        if auto_fix:
            logger.info("Mode: Auto-fix enabled")
        elif interactive:
            logger.info("Mode: Interactive")
        logger.info("=" * 60)
    
    print("=" * 60)
    print("NOAA Alerts Pushover - Setup Validation")
    if auto_fix:
        print("Mode: Auto-fix enabled")
    elif interactive:
        print("Mode: Interactive")
    print("=" * 60)
    
    results = []
    results.append(("Python Version", test_python_version()))
    results.append(("Required Modules", test_imports()))
    results.append(("Configuration File", test_config_file(auto_fix=auto_fix or interactive)))
    results.append(("Counties File", test_counties_file()))
    results.append(("Directories", test_directories()))
    results.append(("Database", test_database(auto_fix=auto_fix or interactive)))
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All checks passed! You're ready to run the application.")
        if logger:
            logger.info("All checks passed!")
        
        # Run test fetch if in interactive mode
        if interactive:
            print("\n" + "=" * 60)
            print("Running test fetch...")
            print("=" * 60)
            if logger:
                logger.info("=" * 60)
                logger.info("Running test fetch...")
                logger.info("=" * 60)
            run_fetch_test(logger)
        else:
            print("\nNext steps:")
            print("  1. Review your config.txt and counties.json")
            print("  2. Run: python fetch.py --nopush --debug")
            print("  3. If successful, run: python fetch.py")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        if logger:
            logger.error("Some checks failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())

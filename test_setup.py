#!/usr/bin/env python3
"""
Test script to validate the NOAA Alerts Pushover setup
Run this before starting the application to catch configuration issues
"""

import os
import sys
import json

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
    modules = ['arrow', 'beautifulsoup4', 'jinja2', 'lxml', 'peewee', 'requests']
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

def test_config_file():
    """Check if config.txt exists and is readable"""
    print("\nChecking configuration file...")
    config_path = 'config.txt'
    
    if not os.path.exists(config_path):
        print(f"  ❌ {config_path} not found")
        print("     Create it from config.txt.example")
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

def test_database():
    """Test database connection"""
    print("\nChecking database...")
    try:
        from models import db, Alert
        
        # Try to connect
        db.connect()
        
        # Check if table exists
        if not Alert.table_exists():
            print("  ℹ️  Database table not initialized")
            print("     Run: python models.py")
            return True  # Not a critical error
        
        print("  ✓ Database initialized")
        db.close()
        return True
        
    except Exception as e:
        print(f"  ⚠️  Database check: {e}")
        return True  # Not critical for initial setup

def main():
    """Run all tests"""
    print("=" * 60)
    print("NOAA Alerts Pushover - Setup Validation")
    print("=" * 60)
    
    results = []
    results.append(("Python Version", test_python_version()))
    results.append(("Required Modules", test_imports()))
    results.append(("Configuration File", test_config_file()))
    results.append(("Counties File", test_counties_file()))
    results.append(("Directories", test_directories()))
    results.append(("Database", test_database()))
    
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
        print("\nNext steps:")
        print("  1. Review your config.txt and counties.json")
        print("  2. Run: python fetch.py --nopush --debug")
        print("  3. If successful, run: python fetch.py")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

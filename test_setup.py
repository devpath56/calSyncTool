#!/usr/bin/env python3
"""
Test script to verify the calendar sync setup
"""

import sys
import os
from config import Config

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("Testing dependencies...")
    
    required_packages = [
        'icalendar',
        'google.oauth2.credentials',
        'googleapiclient.discovery',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    print("All dependencies are installed!")
    return True

def test_configuration():
    """Test configuration settings"""
    print("\nTesting configuration...")
    
    # Print configuration
    Config.print_config()
    
    # Validate required settings
    if Config.validate():
        print("\n✓ Configuration is valid!")
        return True
    else:
        print("\n✗ Configuration is invalid!")
        print("Please set the required environment variables:")
        print("  - GOOGLE_CLIENT_ID")
        print("  - GOOGLE_CLIENT_SECRET")
        print("  - GOOGLE_REFRESH_TOKEN")
        return False

def test_ics_url():
    """Test if the ICS URL is accessible"""
    print(f"\nTesting ICS URL accessibility...")
    
    try:
        import requests
        response = requests.get(Config.ICS_URL, timeout=10)
        response.raise_for_status()
        
        # Check if it looks like ICS data
        content = response.text
        if 'BEGIN:VCALENDAR' in content:
            print("✓ ICS URL is accessible and returns valid calendar data!")
            return True
        else:
            print("✗ ICS URL is accessible but doesn't return valid calendar data")
            return False
            
    except Exception as e:
        print(f"✗ Failed to access ICS URL: {e}")
        return False

def main():
    """Main test function"""
    print("Calendar Sync Setup Test")
    print("=" * 40)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Configuration", test_configuration),
        ("ICS URL", test_ics_url)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("Test Summary:")
    
    all_passed = True
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("You can now run: python sync.py")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

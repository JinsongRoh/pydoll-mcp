#!/usr/bin/env python3
"""Test script to debug ChromiumOptions error."""

import asyncio
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_chromium_options():
    """Test ChromiumOptions instantiation and usage."""
    try:
        from pydoll.browser import Chrome, Edge
        from pydoll.browser.options import ChromiumOptions
        
        logger.info("Successfully imported PyDoll components")
        
        # Test 1: Create ChromiumOptions instance
        logger.info("Test 1: Creating ChromiumOptions instance")
        options = ChromiumOptions()
        logger.info(f"ChromiumOptions created: {options}")
        logger.info(f"ChromiumOptions type: {type(options)}")
        logger.info(f"ChromiumOptions methods: {[m for m in dir(options) if not m.startswith('_')]}")
        
        # Test 2: Check for add_experimental_option method
        logger.info("\nTest 2: Checking for add_experimental_option method")
        has_method = hasattr(options, 'add_experimental_option')
        logger.info(f"Has add_experimental_option: {has_method}")
        
        # Test 3: Add basic arguments
        logger.info("\nTest 3: Adding basic arguments")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        logger.info("Arguments added successfully")
        
        # Test 4: Check options attributes
        logger.info("\nTest 4: Checking options attributes")
        if hasattr(options, 'arguments'):
            logger.info(f"Arguments: {options.arguments}")
        if hasattr(options, '_arguments'):
            logger.info(f"_arguments: {options._arguments}")
            
        # Test 5: Try creating a browser with options
        logger.info("\nTest 5: Creating Chrome browser with options")
        browser = Chrome(options=options)
        logger.info(f"Browser created: {browser}")
        logger.info(f"Browser type: {type(browser)}")
        
        # Test 6: Check browser attributes
        logger.info("\nTest 6: Checking browser attributes")
        browser_attrs = [attr for attr in dir(browser) if not attr.startswith('_')]
        logger.info(f"Browser attributes: {browser_attrs[:10]}...")  # First 10 attributes
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        traceback.print_exc()
    except Exception as e:
        logger.error(f"Error during test: {e}")
        traceback.print_exc()

async def test_browser_start():
    """Test actual browser start."""
    try:
        from pydoll.browser import Chrome
        from pydoll.browser.options import ChromiumOptions
        
        logger.info("\n=== Testing browser start ===")
        
        # Create simple options
        options = ChromiumOptions()
        options.add_argument("--headless=new")
        
        # Try to start browser
        logger.info("Creating Chrome instance...")
        browser = Chrome(options=options, start_timeout=30)
        
        logger.info("Starting browser...")
        await browser.start()
        
        logger.info("Browser started successfully!")
        
        # Clean up
        await browser.close()
        logger.info("Browser closed successfully!")
        
    except Exception as e:
        logger.error(f"Error starting browser: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    logger.info("Starting ChromiumOptions debug test...")
    asyncio.run(test_chromium_options())
    
    logger.info("\n" + "="*50 + "\n")
    
    logger.info("Starting browser start test...")
    asyncio.run(test_browser_start())
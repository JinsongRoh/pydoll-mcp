#!/usr/bin/env python3
"""Test script to validate the browser fix."""

import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_browser_creation():
    """Test browser creation after the fix."""
    try:
        from pydoll_mcp.browser_manager import get_browser_manager
        
        logger.info("Testing browser creation...")
        browser_manager = get_browser_manager()
        
        # Create browser without start_timeout
        browser_instance = await browser_manager.create_browser(
            browser_type="chrome",
            headless=True,
            window_width=1920,
            window_height=1080
        )
        
        logger.info(f"Browser created successfully: {browser_instance.instance_id}")
        
        # Clean up
        await browser_manager.destroy_browser(browser_instance.instance_id)
        logger.info("Browser destroyed successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_browser_creation())
    if success:
        logger.info("✓ Browser fix validated successfully!")
    else:
        logger.error("✗ Browser fix validation failed!")
#!/usr/bin/env python3
"""Test to discover PyDoll's default arguments."""

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_pydoll_defaults():
    """Check what default arguments PyDoll adds."""
    try:
        from pydoll.browser.options import ChromiumOptions
        
        # Create a fresh options instance
        options = ChromiumOptions()
        
        logger.info("Fresh ChromiumOptions created")
        
        # Check initial arguments
        if hasattr(options, 'arguments'):
            logger.info(f"Initial arguments: {options.arguments}")
        if hasattr(options, '_arguments'):
            logger.info(f"Initial _arguments: {options._arguments}")
            
        # Try to get browser manager defaults
        try:
            from pydoll.browser.managers import ChromiumOptionsManager
            
            # Create options manager
            manager = ChromiumOptionsManager(options)
            logger.info("ChromiumOptionsManager created")
            
            # Initialize options (this is what Chrome does internally)
            initialized_options = manager.initialize_options()
            logger.info(f"After initialization: {initialized_options._arguments}")
            
        except Exception as e:
            logger.error(f"Failed to test ChromiumOptionsManager: {e}")
            
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pydoll_defaults()
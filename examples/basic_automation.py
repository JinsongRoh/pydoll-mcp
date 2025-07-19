"""
Basic Browser Automation Example

This example demonstrates the fundamental capabilities of PyDoll MCP Server
including browser management, navigation, and element interaction.
"""

import asyncio
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def basic_automation_example():
    """Demonstrate basic browser automation capabilities."""
    
    print("🚀 PyDoll MCP Server - Basic Automation Example")
    print("=" * 50)
    
    try:
        # This example shows how PyDoll MCP Server would be used
        # Note: In actual usage, these commands would be sent via MCP protocol
        
        print("1. Starting browser...")
        # browser_id = await start_browser(browser_type="chrome", headless=False)
        browser_id = "example_browser_001"
        print(f"   ✅ Browser started: {browser_id}")
        
        print("\n2. Navigating to website...")
        # result = await navigate_to(browser_id, "https://example.com")
        print("   ✅ Navigated to: https://example.com")
        
        print("\n3. Taking screenshot...")
        # screenshot_path = await take_screenshot(browser_id, "basic_example.png")
        screenshot_path = "screenshots/basic_example.png"
        print(f"   ✅ Screenshot saved: {screenshot_path}")
        
        print("\n4. Getting page information...")
        # page_info = await get_page_info(browser_id)
        page_info = {
            "title": "Example Domain",
            "url": "https://example.com",
            "status": "loaded"
        }
        print(f"   ✅ Page title: {page_info['title']}")
        print(f"   ✅ Current URL: {page_info['url']}")
        
        print("\n5. Finding and interacting with elements...")
        # elements = await find_elements(browser_id, tag_name="p")
        print("   ✅ Found paragraph elements")
        
        # text_content = await get_element_text(browser_id, element_id)
        text_content = "This domain is for use in illustrative examples..."
        print(f"   ✅ Element text: {text_content[:50]}...")
        
        print("\n6. Testing form interaction...")
        print("   ℹ️  This example site doesn't have forms, but here's how it would work:")
        print("   - Find input field: await find_element(browser_id, id='username')")
        print("   - Type text: await type_text(browser_id, element_id, 'test@example.com')")
        print("   - Click button: await click_element(browser_id, button_id)")
        
        print("\n7. Demonstrating navigation...")
        # await navigate_to(browser_id, "https://httpbin.org/html")
        print("   ✅ Navigated to test site with more elements")
        
        print("\n8. Advanced element finding...")
        print("   ℹ️  Advanced element finding examples:")
        print("   - By class: await find_element(browser_id, class_name='submit-btn')")
        print("   - By text: await find_element(browser_id, text='Click Here')")
        print("   - By CSS: await find_element(browser_id, css_selector='#main .content')")
        print("   - By XPath: await find_element(browser_id, xpath='//div[@data-id=\"123\"]')")
        
        print("\n9. Network monitoring example...")
        print("   ℹ️  Network monitoring capabilities:")
        print("   - Enable monitoring: await enable_network_monitoring(browser_id)")
        print("   - Get requests: await get_network_requests(browser_id)")
        print("   - Block resources: await block_resources(browser_id, ['*.css', '*.png'])")
        
        print("\n10. JavaScript execution...")
        print("   ℹ️  JavaScript execution examples:")
        print("   - Simple script: await execute_script(browser_id, 'return document.title')")
        print("   - Complex operation: await execute_script(browser_id, custom_script)")
        
        print("\n✅ Basic automation example completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in basic automation: {e}")
        print(f"\n❌ Error: {e}")
    
    finally:
        print("\n🧹 Cleaning up...")
        # await stop_browser(browser_id)
        print("   ✅ Browser stopped and cleaned up")


async def demonstrate_error_handling():
    """Demonstrate error handling in automation."""
    
    print("\n" + "=" * 50)
    print("🛡️  Error Handling Demonstration")
    print("=" * 50)
    
    try:
        print("1. Handling navigation errors...")
        # This would fail in real usage
        print("   ℹ️  Trying to navigate to invalid URL...")
        print("   ✅ Error caught and handled gracefully")
        
        print("\n2. Handling element not found...")
        print("   ℹ️  Trying to find non-existent element...")
        print("   ✅ Fallback strategy implemented")
        
        print("\n3. Handling timeout scenarios...")
        print("   ℹ️  Setting reasonable timeouts for operations...")
        print("   ✅ Timeout handling prevents hanging")
        
        print("\n4. Browser crash recovery...")
        print("   ℹ️  Automatic browser restart on crash...")
        print("   ✅ Service continues uninterrupted")
        
    except Exception as e:
        logger.error(f"Error in error handling demo: {e}")


async def show_configuration_options():
    """Show various configuration options."""
    
    print("\n" + "=" * 50)
    print("⚙️  Configuration Options")
    print("=" * 50)
    
    configs = {
        "Basic Configuration": {
            "browser_type": "chrome",
            "headless": False,
            "window_width": 1920,
            "window_height": 1080
        },
        "Stealth Configuration": {
            "stealth_mode": True,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "disable_webgl": True,
            "randomize_viewport": True
        },
        "Performance Configuration": {
            "disable_images": True,
            "disable_css": False,
            "block_ads": True,
            "enable_cache": True
        },
        "Captcha Bypass Configuration": {
            "auto_solve_cloudflare": True,
            "auto_solve_recaptcha": True,
            "human_behavior_simulation": True,
            "solve_timeout": 30
        }
    }
    
    for config_name, config_options in configs.items():
        print(f"\n{config_name}:")
        for key, value in config_options.items():
            print(f"  {key}: {value}")


def main():
    """Main function to run all examples."""
    print("🤖 PyDoll MCP Server - Basic Examples")
    print("=" * 60)
    print("This file demonstrates basic PyDoll MCP Server capabilities.")
    print("In actual usage, these operations would be performed via MCP protocol.")
    print("=" * 60)
    
    try:
        # Run async examples
        asyncio.run(basic_automation_example())
        asyncio.run(demonstrate_error_handling())
        asyncio.run(show_configuration_options())
        
        print("\n" + "=" * 60)
        print("🎉 All examples completed successfully!")
        print("=" * 60)
        print("\n📚 Next Steps:")
        print("1. Install PyDoll MCP Server: pip install pydoll-mcp")
        print("2. Configure Claude Desktop (see INSTALLATION_GUIDE.md)")
        print("3. Start using with Claude: 'Open a browser and go to example.com'")
        print("4. Explore advanced examples in other files")
        print("\n🔗 Resources:")
        print("- GitHub: https://github.com/JinsongRoh/pydoll-mcp")
        print("- Documentation: See README.md and INSTALLATION_GUIDE.md")
        print("- Issues: https://github.com/JinsongRoh/pydoll-mcp/issues")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Example interrupted by user")
    except Exception as e:
        logger.error(f"Error running examples: {e}")
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()

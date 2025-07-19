"""Basic usage examples for PyDoll MCP Server.

This example demonstrates the fundamental operations you can perform
with PyDoll MCP Server through Claude or other MCP clients.
"""

import asyncio
import json
from pathlib import Path

# Example prompts you can use with Claude when PyDoll MCP Server is configured

EXAMPLE_PROMPTS = {
    "browser_management": [
        "Start a new Chrome browser instance in headless mode",
        "List all currently running browsers and their status",
        "Create a new tab in the browser",
        "Close the current tab and stop the browser"
    ],
    
    "navigation": [
        "Navigate to https://example.com",
        "Go to the GitHub homepage and wait for it to load completely",
        "Refresh the current page",
        "Go back to the previous page in browser history",
        "Get the current page URL and title"
    ],
    
    "element_interaction": [
        "Find the search box on the page and type 'PyDoll MCP'",
        "Click the submit button on the form",
        "Find all links on the page and show their text and URLs",
        "Scroll down to the bottom of the page",
        "Hover over the navigation menu"
    ],
    
    "data_extraction": [
        "Extract all the text content from the page",
        "Get all image URLs from the current page",
        "Find all form fields and their current values",
        "Extract the page metadata (title, description, keywords)",
        "Get all external links on the page"
    ],
    
    "screenshots": [
        "Take a screenshot of the entire page",
        "Capture a screenshot of just the header section",
        "Generate a PDF of the current page",
        "Save the page content as HTML file"
    ],
    
    "automation": [
        "Fill out the contact form with test data and submit it",
        "Perform a search on Google for 'browser automation'",
        "Navigate through a multi-step wizard form",
        "Test the login functionality with test credentials",
        "Monitor the page for 30 seconds and capture any changes"
    ],
    
    "advanced": [
        "Execute JavaScript to modify the page content",
        "Monitor all network requests while browsing",
        "Bypass any captcha challenges that appear",
        "Test the page performance and load times",
        "Extract data from a protected website"
    ]
}

# Step-by-step workflow examples
WORKFLOW_EXAMPLES = {
    "e_commerce_testing": """
    1. Start a browser and navigate to an e-commerce site
    2. Search for a specific product
    3. Add the product to cart
    4. Proceed to checkout (but don't complete purchase)
    5. Take screenshots of each step
    6. Verify all elements loaded correctly
    """,
    
    "form_automation": """
    1. Navigate to a contact form page
    2. Fill in all required fields with test data
    3. Upload a test file if file upload is available
    4. Submit the form
    5. Verify the success message appears
    6. Capture the confirmation page
    """,
    
    "data_scraping": """
    1. Navigate to a data-rich website
    2. Wait for dynamic content to load
    3. Extract structured data from tables or lists
    4. Handle pagination if present
    5. Export the collected data to JSON or CSV
    6. Generate a summary report
    """,
    
    "competitive_analysis": """
    1. Visit competitor websites
    2. Analyze their pricing pages
    3. Extract product features and descriptions
    4. Capture screenshots of key pages
    5. Monitor for any protection mechanisms
    6. Compile a comparison report
    """
}

def print_examples():
    """Print all available examples."""
    print("🤖 PyDoll MCP Server - Example Prompts")
    print("=" * 50)
    
    for category, prompts in EXAMPLE_PROMPTS.items():
        print(f"\n📂 {category.replace('_', ' ').title()}:")
        for i, prompt in enumerate(prompts, 1):
            print(f"  {i}. {prompt}")
    
    print("\n" + "=" * 50)
    print("📋 Workflow Examples:")
    
    for name, workflow in WORKFLOW_EXAMPLES.items():
        print(f"\n🔄 {name.replace('_', ' ').title()}:")
        print(workflow.strip())

# Direct API usage examples (for developers)
async def direct_api_example():
    """Example of using PyDoll MCP Server tools directly."""
    
    # This would be how you'd use the tools programmatically
    # In practice, you'd interact through Claude or another MCP client
    
    try:
        from pydoll_mcp.tools.browser_tools import handle_start_browser
        from pydoll_mcp.tools.navigation_tools import handle_navigate_to
        from pydoll_mcp.tools.screenshot_tools import handle_take_screenshot
        from pydoll_mcp.tools.browser_tools import handle_stop_browser
        
        print("🚀 Starting browser automation example...")
        
        # Start browser
        browser_result = await handle_start_browser({
            "browser_type": "chrome",
            "headless": True
        })
        
        browser_data = json.loads(browser_result[0].text)
        if not browser_data["success"]:
            print("❌ Failed to start browser")
            return
        
        browser_id = browser_data["data"]["browser_id"]
        print(f"✅ Browser started: {browser_id}")
        
        # Navigate to page
        nav_result = await handle_navigate_to({
            "browser_id": browser_id,
            "url": "https://example.com"
        })
        
        nav_data = json.loads(nav_result[0].text)
        if nav_data["success"]:
            print("✅ Navigation successful")
        else:
            print(f"❌ Navigation failed: {nav_data.get('error')}")
        
        # Take screenshot
        screenshot_result = await handle_take_screenshot({
            "browser_id": browser_id,
            "format": "png",
            "save_to_file": True
        })
        
        screenshot_data = json.loads(screenshot_result[0].text)
        if screenshot_data["success"]:
            print(f"✅ Screenshot saved: {screenshot_data['data'].get('file_path')}")
        
        # Stop browser
        stop_result = await handle_stop_browser({
            "browser_id": browser_id
        })
        
        stop_data = json.loads(stop_result[0].text)
        if stop_data["success"]:
            print("✅ Browser stopped successfully")
        
        print("🎉 Example completed successfully!")
        
    except ImportError:
        print("⚠️  PyDoll MCP Server not properly installed or configured")
    except Exception as e:
        print(f"❌ Error during example execution: {e}")

# Configuration examples
CONFIGURATION_EXAMPLES = {
    "claude_desktop": {
        "description": "Claude Desktop configuration for PyDoll MCP Server",
        "file_path": {
            "windows": "%APPDATA%\\Claude\\claude_desktop_config.json",
            "macos": "~/Library/Application Support/Claude/claude_desktop_config.json",
            "linux": "~/.config/Claude/claude_desktop_config.json"
        },
        "config": {
            "mcpServers": {
                "pydoll": {
                    "command": "python",
                    "args": ["-m", "pydoll_mcp.server"],
                    "env": {
                        "PYDOLL_LOG_LEVEL": "INFO",
                        "PYDOLL_DEBUG": "0"
                    }
                }
            }
        }
    },
    
    "advanced_config": {
        "description": "Advanced configuration with custom settings",
        "config": {
            "mcpServers": {
                "pydoll": {
                    "command": "pydoll-mcp",
                    "args": ["--log-level", "DEBUG"],
                    "env": {
                        "PYDOLL_LOG_LEVEL": "DEBUG",
                        "PYDOLL_DEBUG": "1",
                        "PYDOLL_BROWSER_TYPE": "chrome",
                        "PYDOLL_HEADLESS": "true",
                        "PYDOLL_STEALTH_MODE": "true"
                    }
                }
            }
        }
    }
}

def save_configuration_examples():
    """Save configuration examples to files."""
    examples_dir = Path(__file__).parent
    config_dir = examples_dir / "configurations"
    config_dir.mkdir(exist_ok=True)
    
    for name, config_info in CONFIGURATION_EXAMPLES.items():
        config_file = config_dir / f"{name}.json"
        
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config_info["config"], f, indent=2)
        
        print(f"💾 Saved {name} configuration to {config_file}")

if __name__ == "__main__":
    print_examples()
    print("\n" + "=" * 50)
    print("💡 To use these examples:")
    print("1. Ensure PyDoll MCP Server is installed: pip install pydoll-mcp")
    print("2. Configure Claude Desktop with the MCP server")
    print("3. Start a conversation with Claude and use the prompts above")
    print("4. For direct API usage, run: python -c 'import asyncio; from basic_usage import direct_api_example; asyncio.run(direct_api_example())'")
    
    # Save configuration examples
    print("\n📁 Saving configuration examples...")
    save_configuration_examples()
    
    # Run direct API example if requested
    import sys
    if "--run-example" in sys.argv:
        print("\n🔧 Running direct API example...")
        asyncio.run(direct_api_example())

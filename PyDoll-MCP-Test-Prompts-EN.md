# PyDoll MCP Server - Claude Desktop Testing Prompts Guide

## 📋 Overview

This document provides practical prompt examples for testing PyDoll MCP Server's 58 browser automation tools in Claude Desktop. Each category includes step-by-step testing scenarios and real-world use cases.

## 🚀 Quick Start

### 1. Installation Check
```
Please verify that the PyDoll MCP server is properly connected. List all available browser automation tools.
```

### 2. First Test
```
Start a new browser, navigate to Google.com, and search for "PyDoll MCP".
```

## 🗂️ Category-wise Test Prompts

## 1. Browser Management - 8 Tools

### Basic Browser Operations

#### 🆕 Browser Startup and Management
```
Start a new Chrome browser and check the status of all currently running browsers.
```

#### 🔗 Tab Management
```
Open 3 new tabs in the current browser, navigate each to different websites (YouTube, GitHub, Wikipedia), then show me the list of tabs.
```

#### 🔄 Tab Switching and Cleanup
```
Switch to the 2nd tab among the open tabs and clean up unused tabs.
```

#### 🛑 Browser Shutdown
```
Safely close the currently used browser.
```

## 2. Navigation Control - 7 Tools

### Web Page Navigation

#### 🧭 Basic Navigation
```
Start a browser and navigate in the following order:
1. Visit https://example.com
2. Check page title and current URL
3. Go back
4. Refresh the page
```

#### 📄 Page Information Collection
```
Navigate to https://github.com/JinsongRoh/pydoll-mcp and retrieve the page title, current URL, and the first 500 characters of the page source.
```

#### 🔍 Domain Commands Exploration
```
Query the available Chrome DevTools domain commands for the current page.
```

## 3. Element Interaction - 4 Tools

### Web Element Finding and Manipulation

#### 🔎 Basic Element Finding
```
Navigate to Google.com, find the search input field, type "PyDoll MCP Server", and click the search button.
```

#### 📝 Form Automation
```
Navigate to https://httpbin.org/forms/post and fill out the form as follows:
- Name: "Claude"
- Email: "claude@anthropic.com"
- Comment: "PyDoll MCP Server test"
Then submit the form.
```

#### 🎯 Advanced Element Selection
```
Navigate to Wikipedia main page, find the "Random article" link, click it, and retrieve the title of that page.
```

#### 👨‍👩‍👧‍👦 Parent Element Exploration
```
Find a button element on any website and retrieve information about its parent element.
```

## 4. Screenshot & Media - 3 Tools

### Screen Capture and Document Generation

#### 📸 Page Screenshot
```
Navigate to https://www.python.org and take a full page screenshot.
```

#### 🎯 Specific Element Capture
```
Take a screenshot of only the README section on a GitHub repository page.
```

#### 📄 PDF Generation
```
Convert the current page to PDF and save it. Include headers and footers in the generation.
```

## 5. Script Execution - 3 Tools

### JavaScript Execution and Automation

#### ⚡ Basic JavaScript Execution
```
Execute the following JavaScript on the current page:
- Count all links on the page
- Change the page title
- Scroll to the bottom of the page
```

#### 🔧 Library Injection and Usage
```
Inject the jQuery library into the current page and use jQuery to count all image elements.
```

#### 🤖 Automation Script Execution
```
If there are predefined automation scripts available, execute one and show the results.
```

## 6. Advanced Automation - 3 Tools

### Performance Analysis and AI-based Analysis

#### 📊 Performance Analysis
```
Navigate to a complex website (e.g., Amazon.com), analyze page loading performance, and provide optimization suggestions.
```

#### 🔍 AI Content Analysis
```
Navigate to a news website and perform sentiment analysis and keyword extraction on the main article.
```

#### 🌐 Network Request Analysis
```
Enable network monitoring and analyze API calls on a site with many AJAX requests.
```

## 7. Protection & Stealth - 11 Tools

### Captcha Bypass and Detection Evasion

#### 🛡️ Stealth Mode Activation
```
Activate stealth mode and visit a bot detection site to check if detection occurs.
```

#### 🔐 Cloudflare Bypass Test
```
Navigate to a site with Cloudflare protection and automatically bypass it.
```

#### 🤖 reCAPTCHA Bypass
```
Attempt to automatically bypass reCAPTCHA on a site that has it.
```

#### 👤 Human Behavior Simulation
```
Browse a website with human-like behavior patterns (random delays, mouse movements, etc.).
```

#### 🎭 User Agent Modification
```
Change user agents to various browsers and devices while browsing.
```

## 8. Network Monitoring - 10 Tools

### Network Traffic Analysis

#### 📡 Network Monitoring Start
```
Start network monitoring and record all requests on a website with many API calls.
```

#### 🚫 Request Blocking
```
Block advertising or tracking script requests while browsing a website.
```

#### 🔧 Request Header Modification
```
Modify headers of specific API requests to receive different results.
```

#### 🔌 WebSocket Monitoring
```
Monitor WebSocket connections on a site with real-time chat or updates.
```

#### 💾 HAR File Saving
```
Save all network activity of the session as a HAR file.
```

## 9. File Management - 8 Tools

### File Upload/Download and Data Processing

#### 📤 File Upload
```
Upload a test file on a site with file upload functionality.
```

#### 📥 File Download
```
Download an image or document file and check the download status.
```

#### 📊 Data Extraction and Conversion
```
Extract data from a webpage with table data and export it in CSV and JSON formats.
```

#### 💾 Session Save and Restore
```
Save the current browser session and restore it to the same state later.
```

## 🧪 Comprehensive Test Scenarios

### Real-world Automation Scenarios

#### 🛒 Online Shopping Automation
```
Automate the online shopping process in the following order:
1. Navigate to an e-commerce website
2. Search for a specific product
3. Collect information from the product detail page
4. Add to cart
5. Proceed to checkout page (don't actually make payment)
6. Record the entire process with screenshots
```

#### 📰 News Scraping Automation
```
Perform the following tasks on a news website:
1. Collect headline article list from main page
2. Extract title, summary, and link for each article
3. Scrape full content of top 3 articles
4. Organize data in JSON format
5. Perform sentiment analysis on articles using AI
```

#### 🔍 SEO Analysis Automation
```
Perform SEO analysis of a website:
1. Extract page title and meta tags
2. Analyze all heading tags (H1-H6)
3. Check image alt tags
4. Measure page loading performance
5. Test mobile friendliness
6. Generate comprehensive report
```

#### 🎯 A/B Testing Automation
```
Compare and analyze two different webpage versions:
1. Navigate to each page
2. Take screenshots of key elements
3. Compare loading performance
4. Analyze user experience elements
5. Generate difference report
```

## 🚨 Error Handling and Debugging

### Common Problem Resolution

#### 🔧 Browser Problem Resolution
```
If the browser becomes unresponsive or errors occur, try the following:
1. Check browser status
2. Check current tab information
3. Restart browser if necessary
4. Continue work after problem resolution
```

#### 🎯 Element Finding Failure Handling
```
When elements cannot be found:
1. Wait until page is fully loaded
2. Try different selector methods
3. Check element existence in page source
4. Suggest alternative approaches
```

## 📚 Advanced Usage

### Complex Feature Combinations

#### 🔄 Automation Workflow
```
Execute the following complex workflow:
1. Start browser in stealth mode
2. Apply proxy settings
3. Enable network monitoring
4. Navigate to target website
5. Automate login process
6. Collect and analyze data
7. Save results to file
8. Clean up and exit
```

#### 🎨 Scraping + AI Analysis
```
Combine web scraping with AI analysis:
1. Collect product information from e-commerce site
2. Download product images
3. Extract customer review text
4. Perform sentiment analysis on reviews using AI
5. Calculate product recommendation score
6. Organize results as structured data
```

## 🔍 Performance Optimization Testing

### Speed and Efficiency

#### ⚡ Speed Optimization
```
Work with optimized browser performance:
1. Block unnecessary resource loading
2. Optimize cache settings
3. Apply network throttling
4. Control number of concurrent tasks
5. Monitor memory usage
```

#### 📊 Benchmark Testing
```
Run performance benchmarks with various settings:
1. Measure processing time for 10 pages with default settings
2. Same test after enabling stealth mode
3. Test after enabling network monitoring
4. Compare results and generate report
```

## 📝 Conclusion

Through the prompts in this guide, you can systematically test all features of PyDoll MCP Server. Each prompt can be executed independently, and you can combine them as needed to create more complex automation scenarios.

### 💡 Additional Tips

- Break down complex tasks and execute them step by step
- Check intermediate results and debug when errors occur
- Adjust wait times considering website-specific characteristics
- Follow ethical web scraping principles

### 🚀 Next Steps

If you need help with more advanced features or specific use cases:
- Ask questions in the [GitHub Repository](https://github.com/JinsongRoh/pydoll-mcp) issues tab
- Refer to [PyDoll Documentation](https://pypi.org/project/pydoll-mcp/)
- Participate in community discussions

---

**PyDoll MCP Server v1.4.0** | 58 Browser Automation Tools | A New Dimension in AI-Powered Web Automation
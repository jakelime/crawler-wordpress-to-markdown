# Crawler: WordPress to Markdown

A Python script designed to scrape blog posts from a WordPress site (or similar structured blogs) and convert them into clean Markdown (`.md`) files. This tool is built specifically for extracting content from the `rockerfellasadventure.com` blog but can be easily adapted for other sites.

## Features

- **Automated Crawling:** Scans the blog, navigating through pagination to collect links to all individual posts.
- **HTML to Markdown Conversion:** Extracts the main content area and converts it to Markdown using `markdownify`.
- **Sanitized Filenames:** Automatically generates safe file names from the post titles.
- **Source Tracking:** Includes the original URL and title at the top of each generated Markdown file.
- **Respectful Scraping:** Implements pauses between requests to avoid overloading the target server.

## Prerequisites

- Python 3.x

## Installation

1. Clone this repository:

   ```bash
   git clone git@github.com:jakelime/crawler-wordpress-to-markdown.git
   cd crawler-wordpress-to-markdown
   ```

2. (Optional but recommended) Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script from your terminal:

```bash
python main.py
```

The script will:

1. Create a directory named `rockerfellas_posts` in the current working directory.
2. Crawl the base URL (`https://www.rockerfellasadventure.com/blog/`) to gather all post links.
3. Fetch each post, extract the core content, and save it as a Markdown file inside the `rockerfellas_posts` directory.

## Dependencies

- `requests`: Handles HTTP requests for fetching web pages.
- `beautifulsoup4`: Parses HTML and navigates the DOM to locate post links and content wrappers.
- `markdownify`: Converts HTML elements into Markdown format.

## Customization

To scrape a different website, modify the following within `main.py`:

- **`START_URL`**: Update this to the starting point of the target blog.
- **Content Wrapper**: The structure of websites vary. Adjust the `soup.find()` logic within the `extract_post()` function to match the target site's HTML classes (e.g., `article`, `<main>`, or specific `<div>` classes).

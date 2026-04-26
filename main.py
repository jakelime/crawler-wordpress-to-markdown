import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
import os
import time

# Target blog URL
START_URL = "https://www.rockerfellasadventure.com/blog/"

# Headers to mimic a standard browser visit
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


def get_filename_from_url(url, index):
    """Extracts the slug from the URL to be used as a valid file name."""
    if url.endswith("/"):
        url = url[:-1]
    clean_title = url.split("/")[-1]
    # Fallback if empty
    if not clean_title:
        clean_title = "untitled_post"
    return f"{index}_{clean_title}.md"


def extract_post(post_url, output_dir, index):
    """Fetches a single post, converts it to markdown, and saves it."""
    print(f"  -> Scraping: {post_url}")
    try:
        response = requests.get(post_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the title (usually the first <h1> tag on a blog post page)
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Untitled_Post"

        # Extract the main content.
        # Common WordPress classes are 'entry-content' or wrapped in an <article> tag.
        content_area = (
            soup.find("article")
            or soup.find("div", class_="entry-content")
            or soup.find("main")
        )

        if not content_area:
            print(
                f"     [!] Could not locate the main content wrapper for {post_url}. Skipping."
            )
            return

        # Convert the HTML block to Markdown
        md_content = markdownify(str(content_area), heading_style="ATX")

        # Prepare the file path and write the file
        filename = get_filename_from_url(post_url, index)
        filepath = os.path.join(output_dir, filename)

        # Check if file exists, if yes append number
        counter = 1
        name, ext = os.path.splitext(filename)
        while os.path.exists(filepath):
            filename = f"{name}_{counter}{ext}"
            filepath = os.path.join(output_dir, filename)
            counter += 1

        with open(filepath, "w", encoding="utf-8") as file:
            # Adding a title header at the top of the file
            file.write(f"# {title}\n\n")
            file.write(f"**Source:** {post_url}\n\n")
            file.write("---\n\n")
            file.write(md_content)

        print(f"     [✓] Saved to {filename}")

    except Exception as e:
        print(f"     [X] Error extracting {post_url}: {e}")


def get_all_post_links(base_url):
    """Crawls through the blog pages to collect all individual post links."""
    visited_pages = set()
    post_links = set()
    pages_to_visit = [base_url]

    print("Crawling for post links...")

    while pages_to_visit:
        current_page = pages_to_visit.pop(0)

        if current_page in visited_pages:
            continue

        print(f"Scanning page: {current_page}")
        visited_pages.add(current_page)

        try:
            response = requests.get(current_page, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all anchor tags
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]

                # Heuristic 1: If the link text is "Read more", it's usually pointing to a post
                if a_tag.get_text(strip=True).lower() == "read more":
                    post_links.add(href)

                # Heuristic 2: Handle Pagination. Look for page numbers (e.g., /blog/page/2/)
                if (
                    "/blog/page/" in href
                    and href not in visited_pages
                    and href not in pages_to_visit
                ):
                    pages_to_visit.append(href)

        except Exception as e:
            print(f"Error scanning {current_page}: {e}")

        # Brief pause to avoid hammering the server too quickly
        time.sleep(1)

    return list(post_links)


def main():
    output_directory = "rockerfellas_posts"

    # Create the directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    print(f"Output directory created: {output_directory}/\n")

    # 1. Get all the links
    links = get_all_post_links(START_URL)
    print(f"\nFound {len(links)} unique posts. Starting extraction...\n")

    # 2. Scrape each link and convert to Markdown
    for index, link in enumerate(links, start=1):
        extract_post(link, output_directory, index)
        # Sleep for a second between posts to respect the server
        time.sleep(1)

    print("\nScraping complete!")


if __name__ == "__main__":
    main()

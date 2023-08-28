import mechanicalsoup
import time
import json
import os
import threading
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re

def clean_title(title):
    # Remove numbers and hashtags from the title
    cleaned_title = re.sub(r'#\d+|\d+', '', title)
    # Remove extra spaces and dashes
    cleaned_title = cleaned_title.strip().rstrip('-').strip()
    # Remove " - (word)" pattern from titles
    cleaned_title = re.sub(r'\s*-\s*\w+', '', cleaned_title)
    # Remove "sözlük" from titles
    cleaned_title = cleaned_title.replace("sözlük", "")
    return cleaned_title

def extract_text_and_title(browser, link, headers):
    if not link.startswith("http"):
        link = "https://eksisozluk1923.com" + link  # Add the base URL
    
    response = browser.get(link, headers=headers)
    response.raise_for_status()
    soup = response.soup
    
    title_element = soup.find("title")
    title = clean_title(title_element.get_text()) if title_element else ""
    
    content_elements = soup.find_all("div", class_="content")
    content_texts = [clean_text(content_element.get_text()) for content_element in content_elements]
    
    return {
        "title": title,
        "content": content_texts
    }

def clean_text(text):
    # Clean up the text by removing extra whitespace
    cleaned_text = ' '.join(text.split())
    # Remove "(bkz:" prefix and following ")" from content texts
    cleaned_text = re.sub(r'\(bkz:(.*?)\)', r'\1', cleaned_text)
    # Remove leading spaces from each line of content
    cleaned_text = '\n'.join(line.lstrip() for line in cleaned_text.split('\n'))
    return cleaned_text

if __name__ == "__main__":
    # Initialize MechanicalSoup browser
    browser = mechanicalsoup.StatefulBrowser()

    discovered_links_filename = "discovered_links.json"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    }

    with open(discovered_links_filename, "r") as json_file:
        discovered_links = json.load(json_file)

    all_data = []

    # Loop through discovered links and scrape text and title sections
    for link in discovered_links:
        try:
            data = extract_text_and_title(browser, link, headers)
            
            # Clean the title by removing " - (word)" pattern and "sözlük"
            title = data["title"]
            
            # Remove "-" and surrounding spaces at the end of titles
            title = re.sub(r'\s*-\s*$', '', title)
            
            # Remove space at the end of the title
            title = title.rstrip()
            
            # Only add data if content is not empty
            if data["content"]:
                data["title"] = title
                all_data.append(data)
                time.sleep(1)  # Add a delay between requests
        except Exception as section_error:
            print(f"Error scraping link {link}: {section_error}")

        # Save the collected data to a JSON file after each scrape
        with open("eksi.json", "w", encoding="utf-8") as json_file:
            json.dump(all_data, json_file, ensure_ascii=False, indent=4)

            if data["content"]:
                print(f"Data for {title} saved to eksi.json")

    print("All data saved to eksi.json")

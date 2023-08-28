import mechanicalsoup
import time
import json
import random
import os

def clean_text(text):
    cleaned_text = text.strip()
    return cleaned_text

def extract_section_links(browser, initial_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    }
    
    browser.open(initial_url, headers=headers)
    
    section_links = []

    section_elements = browser.page.find_all("a", href=True)
    for section_element in section_elements:
        section_link = section_element.get("href")
        section_links.append(section_link)

    return section_links

def extract_data_from_section(browser, section_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    }
    
    browser.open(section_url, headers=headers)
    
    section_data = []

    data_elements = browser.page.find_all("div", class_="data")
    for data_element in data_elements:
        data_text = clean_text(data_element.get_text())
        section_data.append(data_text)

    return section_data

def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def load_links_from_json(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as json_file:
            links = json.load(json_file)
        return links
    else:
        return []

def main_loop():
    initial_url = "https://eksisozluk1923.com"
    section_links_filename = "section_links.json"
    
    browser = mechanicalsoup.StatefulBrowser()
    
    while True:
        print("Scraping cycle started...")
        
        try:
            discovered_sections = extract_section_links(browser, initial_url)
            
            stored_links = load_links_from_json(section_links_filename)
            
            # combine
            all_discovered_links = list(set(discovered_sections + stored_links))
            save_to_json(all_discovered_links, section_links_filename)
            
            for section_link in all_discovered_links:
                section_url = f"{initial_url}{section_link}"
                
                try:
                    section_data = extract_data_from_section(browser, section_url)
                    # process and save section_data 
                    
                    time.sleep(0.5)
                except Exception as section_error:
                    print(f"Error scraping section {section_url}: {section_error}")

            print("Data saved and updated.")
        
        except Exception as cycle_error:
            print(f"Scraping cycle error: {cycle_error}")
        
        print("Scraping cycle completed. Waiting before the next cycle...")
        time.sleep(0.5)  

if __name__ == "__main__":
    main_loop()

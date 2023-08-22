import requests
from bs4 import BeautifulSoup
import spacy
import yaml

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    cleaned_text = text.strip()
    return cleaned_text

def extract_qa_pairs(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    qa_pairs = []

    span_elements = soup.find_all("span", itemprop="name")
    div_elements = soup.find_all("div", class_="content")

    for span, div in zip(span_elements, div_elements):
        title = clean_text(span.get_text())
        content = clean_text(div.get_text())
        qa_pairs.append((title, content))  

    return qa_pairs

def save_to_yaml(data, filename):
    with open(filename, "w", encoding="utf-8") as yaml_file:
        yaml.dump(data, yaml_file, allow_unicode=True)

url = "https://eksisozluk1923.com/"  # Replace with the URL of the webpage
qa_pairs = extract_qa_pairs(url)

if qa_pairs:
    formatted_data = [{"question": title, "answer": content} for title, content in qa_pairs]  # Swap the places of title and content
    save_to_yaml(formatted_data, "scraped_data.yaml")
    print("Scraped data saved to scraped_data.yaml")
else:
    print("No question-answer pairs found on the page.")

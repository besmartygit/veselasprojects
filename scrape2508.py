import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
from PyPDF2 import PdfReader  # Correct import statement for PdfReader
from urllib.parse import urlparse  # Correct import for Python 3
from urllib.parse import urljoin  # Correct import for Python 3

# Function to scrape and extract emails from a webpage and its linked pages
def scrape_webpage(url, visited_urls=set(), max_links=100):
    try:
        # Mock the browser with headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Initialize an empty set to store unique emails
        unique_emails = set()

        # Fetch the page
        response = requests.get(url, headers=headers, verify=False)
        print(f"Scraping {url}: {response.status_code}")
        response.raise_for_status()

        # Parse the page content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Scrape emails from the page
        text = soup.get_text()
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        unique_emails.update(re.findall(email_pattern, text))

        # Mark this URL as visited
        visited_urls.add(url)
        link_count = 0  # Initialize a counter for the links

        # Find and follow all links on the page
        for link in soup.find_all('a', href=True):
            if link_count >= max_links:
             break
            next_url = urljoin(url, link['href'])
            # Parse the URL to ensure it's on the same domain and not previously visited
            if urlparse(next_url).netloc == urlparse(url).netloc and next_url not in visited_urls:
                # Recursively scrape the next URL
                unique_emails.update(scrape_webpage(next_url, visited_urls))

        return unique_emails

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return set()

# Function to scrape and extract emails from a PDF
def scrape_pdf(url):
    try:
        # Download the PDF
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        
        pdf_path = "downloaded_pdf.pdf"
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(response.content)
        
        # Extract text from the PDF (this part assumes you have a PDF text extraction library installed)
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Find and return all email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        unique_emails = list(set(re.findall(email_pattern, text)))
        return unique_emails
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while scraping the PDF: {e}")
        return []

# Main function to determine the type of URL and scrape accordingly
def scrape_and_extract_emails(url):
    if url.endswith(".pdf"):
        return scrape_pdf(url)
    else:
        return scrape_webpage(url)

# Function to save emails to a CSV file with a timestamp
def save_emails_to_csv(emails):
    if emails:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = f"extracted_emails_{timestamp}.csv"
        df = pd.DataFrame(emails, columns=["Email"])
        df.to_csv(csv_path, index=False)
        messagebox.showinfo("Success", f"Emails have been extracted and saved to {csv_path}")
    else:
        messagebox.showwarning("No Emails Found", "No emails were found during the scraping process.")

# Function to get URL from user input
def get_url_and_scrape():
    url = simpledialog.askstring("Input", "Please enter the URL to scrape (webpage or PDF):")
    if url:
        emails = scrape_and_extract_emails(url)
        save_emails_to_csv(emails)
    else:
        messagebox.showwarning("Input Required", "No URL provided. Please enter a valid URL.")

def on_closing():
        root.destroy()  # Close the window


# Setup the UI
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)

root.withdraw()  # Hide the root window


get_url_and_scrape()

### import package
import datetime
from time import sleep
import sys
import json
import requests
from bs4 import BeautifulSoup
### web crawling with Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

def fetch_job_links(key):
    """
    Fetch job listing URLs from 104.com.tw based on the provided keywords.

    This function iterates over a list of keywords, constructing a URL to fetch job listings for each keyword.
    It paginates through the search results, extracting job listing URLs until there are no more pages left.

    Parameters:
    - key: list of str
        A list of keywords to search for in job listings.

    Returns:
    - list of str
        A list of URLs, each pointing to a job listing on 104.com.tw.
    """
    jobs_url_list = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    }

    for keyword in key:
        current_page = 1  # Initialize the page counter for each keyword.
        while True:  # Loop through each page until there are no more job listings.
            # Construct the URL for the current page of job listings.
            first_page_url = f'https://www.104.com.tw/jobs/search/?ro=0&kwop=1&keyword={keyword}&expansionType=job&order=14&asc=0&page={current_page}&mode=s&langFlag=0'
            
            # Fetch the content of the page.
            response = requests.get(first_page_url, headers=headers)

            # If the request is successful, parse the HTML content.
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                job_list = soup.find_all('article', class_='js-job-item')

                # If no job listings are found on the current page, exit the loop.
                if not job_list:
                    break

                # Extract and store the URLs of each job listing.
                for job in job_list:
                    link = job.find('a', class_='js-job-link')
                    if link and 'href' in link.attrs:
                        job_url = f"https:{link['href']}"
                        jobs_url_list.append(job_url)

                # Move to the next page.
                current_page += 1
            else:
                # If the request fails, print the status code and exit the loop.
                print(f"Failed to connect to the website: {response.status_code}")
                break

    return jobs_url_list

def parse_job_listings(html):
    """
    Parse the HTML content to extract job listing information.

    Parameters:
    - html: str
        The HTML content of the job listings page.

    Returns:
    - list of dict
        A list of dictionaries, each containing the details of a job listing.
    """
    soup = BeautifulSoup(html, 'html.parser')
    jobs = []
    for listing in soup.find_all('a', class_='jjs-job-link'):
        # Extract necessary information (e.g., job title, company name, location, etc.)
        job_info = {
            'title': listing.find('a', class_='job-title').text.strip(),
            'company': listing.find('a', class_='company-name').text.strip(),
            # Add more fields as needed
        }
        jobs.append(job_info)
    return jobs

def save_jobs_to_csv(jobs, filename):
    """
    Save the extracted job listings to a CSV file.

    Parameters:
    - jobs: list of dict
        The list of job listing information to save.
    - filename: str
        The filename for the CSV file.
    """
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)

def open_selenium_remote_browser(url):
    """
    Initializes a remote Selenium WebDriver session and navigates to the specified URL.
    
    Args:
        url (str): The URL to be visited.
        
    Returns:
        webdriver.Remote: An instance of the remote WebDriver.
    """
    # Initialize the remote WebDriver with the specified Selenium Grid server address
    # and desired browser capabilities for Chrome.
    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',  # Using service name as hostname
        desired_capabilities=DesiredCapabilities.CHROME
    )
    
    # Navigate to the specified URL using the WebDriver.
    driver.get(url)
    
    return driver
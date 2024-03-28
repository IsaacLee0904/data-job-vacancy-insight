### import package
import datetime
from time import sleep
import sys
import json
### web crawling with Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

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
        command_executor='http://172.17.0.2:4444/wd/hub',  # Using service name as hostname
        desired_capabilities=DesiredCapabilities.CHROME
    )
    
    # Navigate to the specified URL using the WebDriver.
    driver.get(url)
    
    return driver

def fetch_job_links(url, params=None):
    """
    Fetch the HTML content from the given URL (104 job listings page) with the specified parameters.

    Parameters:
    - url: str
        The URL to fetch the job listings from.
    - params: dict, optional
        A dictionary of parameters to pass along with the request.

    Returns:
    - str
        The HTML content of the page.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
               "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

    job_links_list = []

    response = requests.get(url, headers=headers, params=None)
    soup = BeautifulSoup(response.text, "lxml")
    a_list = soup.find_all('a', 'js-job-link')
    for link in a_list:
        job_url = 'https:' + link['href']
        job_links_list.append(job_url)

    return job_links_list

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
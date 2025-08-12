### import package
import sys, os
import datetime
from time import sleep
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def setup_selenium_driver():
    """
    Setup and return a configured Chrome WebDriver for Selenium
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Use webdriver-manager to auto-download ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def fetch_job_links(search_keywords, logger):
    """
    Fetch job listing URLs from 104.com.tw using Selenium based on the provided keywords.

    This function uses Selenium WebDriver to handle JavaScript-rendered content.
    It iterates over keywords, paginates through search results, and extracts job URLs.

    Parameters:
    - search_keywords: list of str
        A list of keywords to search for in job listings.
    - logger: logging.Logger
        A Logger object used for logging information and errors.

    Returns:
    - list of str
        A list of URLs, each pointing to a job listing on 104.com.tw.
    """
    jobs_url_list = []
    driver = None
    
    try:
        driver = setup_selenium_driver()
        logger.info("Selenium WebDriver initialized successfully")
        
        for keyword in search_keywords:
            current_page = 1
            logger.info(f"Fetching job listings for keyword: {keyword}")
            
            while current_page <= 20:  # Limit pagination to 20 pages
                logger.info(f"Processing page {current_page} for keyword: {keyword}")
                url = f'https://www.104.com.tw/jobs/search/?ro=0&kwop=1&keyword={keyword}&expansionType=job&order=14&asc=0&page={current_page}&mode=s&langFlag=0'
                
                try:
                    driver.get(url)
                    
                    # Wait for job listings to load
                    wait = WebDriverWait(driver, 10)
                    
                    # Try multiple possible selectors for job items
                    job_selectors = [
                        'article[data-job-id]',
                        'div[data-job-id]', 
                        'article.js-job-item',
                        'a[href*="/job/"]',
                        '.job-item',
                        '[data-jobno]'
                    ]
                    
                    job_elements = None
                    for selector in job_selectors:
                        try:
                            job_elements = wait.until(
                                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                            )
                            if job_elements:
                                logger.info(f"Found {len(job_elements)} jobs using selector: {selector}")
                                break
                        except TimeoutException:
                            continue
                    
                    if not job_elements:
                        logger.info(f"No job listings found for keyword: {keyword} on page {current_page}")
                        break
                    
                    # Extract job URLs
                    page_job_count = 0
                    for element in job_elements:
                        try:
                            # Try to find job link within the element
                            job_link = None
                            if element.tag_name == 'a':
                                job_link = element
                            else:
                                job_link = element.find_element(By.CSS_SELECTOR, 'a[href*="/job/"]')
                            
                            if job_link:
                                href = job_link.get_attribute('href')
                                if href and '/job/' in href:
                                    if not href.startswith('http'):
                                        href = f"https://www.104.com.tw{href}"
                                    jobs_url_list.append(href)
                                    page_job_count += 1
                        except NoSuchElementException:
                            continue
                    
                    logger.info(f"Extracted {page_job_count} job URLs from page {current_page}")
                    
                    if page_job_count == 0:
                        logger.info(f"No job URLs found on page {current_page}, stopping pagination")
                        break
                    
                    current_page += 1
                    sleep(2)  # Be respectful to the server
                    
                except TimeoutException:
                    logger.error(f"Timeout while loading page {current_page} for keyword: {keyword}")
                    break
                except Exception as e:
                    logger.error(f"Error processing page {current_page} for keyword {keyword}: {e}")
                    break
        
        logger.info(f"Finished fetching job listings. Total URLs collected: {len(jobs_url_list)}")
        
    except Exception as e:
        logger.error(f"Error initializing Selenium WebDriver: {e}")
    
    finally:
        if driver:
            driver.quit()
            logger.info("Selenium WebDriver closed")
    
    return jobs_url_list
    
def get_job_info(job_url, logger):
    """
    Fetch and parse job listing content using both Selenium and AJAX API.

    Parameters:
    - job_url (str): The URL of the job listing.
    - logger (logging.Logger): A Logger object used for logging information and errors.

    Returns:
    - dict: A dictionary containing details of a job listing.
    """
    # First try the AJAX API approach (faster if it works)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            'Referer': 'https://www.104.com.tw/job/'
        }

        # Extract job ID from URL and try AJAX endpoint
        job_id = job_url.split('/job/')[-1].split('?')[0]
        ajax_url = f'https://www.104.com.tw/job/ajax/content/{job_id}'

        response = requests.get(ajax_url, headers=headers)
        
        if response.status_code == 200:
            json_data = response.json()
            
            # Check if we have full job data
            if 'data' in json_data and 'jobDetail' in json_data['data']:
                job_details = {
                    'job_title': json_data['data']['header'].get('jobName', None),
                    'company_name': json_data['data']['header'].get('custName', None),
                    'salary': json_data['data']['jobDetail'].get('salary', None),
                    'location': json_data['data']['jobDetail'].get('addressRegion', None),
                    'job_description': json_data['data']['jobDetail'].get('jobDescription', None),
                    'job_type': '、'.join(i['description'] for i in json_data['data']['jobDetail'].get('jobCategory', [])),
                    'degree_required': json_data['data']['condition'].get('edu', None),
                    'major_required': '、'.join(json_data['data']['condition'].get('major', [])),
                    'experience': json_data['data']['condition'].get('workExp', None),
                    'skill': '、'.join(i['description'] for i in json_data['data']['condition'].get('skill', [])),
                    'tools': '、'.join(i['description'] for i in json_data['data']['condition'].get('specialty', [])),
                    'others': json_data['data']['condition'].get('other', None),
                    'url': job_url,
                    'crawl_date': datetime.datetime.today().strftime('%Y%m%d')
                }
                logger.info(f"Successfully fetched job details via AJAX for {job_id}")
                return job_details
    except Exception as e:
        logger.warning(f"AJAX approach failed for {job_url}: {e}, trying Selenium")
    
    # If AJAX fails, use Selenium to scrape the page
    driver = None
    try:
        driver = setup_selenium_driver()
        driver.get(job_url)
        
        wait = WebDriverWait(driver, 10)
        
        # Wait for page to load
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        sleep(3)  # Additional wait for dynamic content
        
        # Extract job information using Selenium
        job_details = {
            'job_title': _safe_get_text(driver, ['h1[data-qa="jobName"]', 'h1', '.job-title']),
            'company_name': _safe_get_text(driver, ['[data-qa="companyName"]', '.company-name']),
            'salary': _safe_get_text(driver, ['[data-qa="salary"]', '.salary']),
            'location': _safe_get_text(driver, ['[data-qa="jobAddress"]', '.location']),
            'job_description': _safe_get_text(driver, ['[data-qa="jobDescription"]', '.job-description']),
            'job_type': _safe_get_text(driver, ['[data-qa="jobCategory"]', '.job-category']),
            'degree_required': _safe_get_text(driver, ['[data-qa="education"]', '.education']),
            'major_required': _safe_get_text(driver, ['[data-qa="major"]', '.major']),
            'experience': _safe_get_text(driver, ['[data-qa="experience"]', '.experience']),
            'skill': _safe_get_text(driver, ['[data-qa="skill"]', '.skill']),
            'tools': _safe_get_text(driver, ['[data-qa="tools"]', '.tools']),
            'others': _safe_get_text(driver, ['[data-qa="others"]', '.others']),
            'url': job_url,
            'crawl_date': datetime.datetime.today().strftime('%Y%m%d')
        }
        
        logger.info(f"Successfully scraped job details via Selenium for {job_url}")
        
    except Exception as e:
        logger.error(f"Failed to fetch job details via Selenium for {job_url}: {e}")
        job_details = {}
    
    finally:
        if driver:
            driver.quit()
    
    return job_details

def _safe_get_text(driver, selectors):
    """
    Try multiple selectors to get text content safely
    """
    for selector in selectors:
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            return element.text.strip() if element.text else None
        except NoSuchElementException:
            continue
    return None

def save_jobs_to_json(job_info_dict, logger):
    """
    Save the job information to a JSON file named with the current date and time in the data/raw_data folder.

    Parameters:
    - job_info_dict (list of dict): A list of dictionaries, each containing the details of a job listing.
    - logger (logging.Logger): A Logger object used for logging information and errors.
    """
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    directory = "data/raw_data"
    file_name = f"{directory}/jobs_{current_time}.json"

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(job_info_dict, file, ensure_ascii=False, indent=4)
        logger.info(f"Job information saved to {file_name}")
    except Exception as e:
        logger.error(f"Failed to save job information to JSON: {str(e)}")
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
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from queue import Queue

def setup_selenium_driver():
    """
    Setup and return a configured Chrome WebDriver for Selenium with performance optimizations
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-images')  # Don't load images (faster)
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Performance optimizations
    chrome_options.add_argument('--disable-background-timer-throttling')
    chrome_options.add_argument('--disable-backgrounding-occluded-windows')
    chrome_options.add_argument('--disable-renderer-backgrounding')
    chrome_options.add_argument('--disable-features=TranslateUI')
    chrome_options.page_load_strategy = 'eager'
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Set timeouts for faster response
    driver.set_page_load_timeout(10)
    driver.implicitly_wait(2)
    
    return driver

def fetch_page_jobs(keyword, page_num, logger):
    """
    Fetch job URLs from a single page (thread-safe function)
    """
    driver = None
    try:
        driver = setup_selenium_driver()
        url = f'https://www.104.com.tw/jobs/search/?ro=0&kwop=1&keyword={keyword}&expansionType=job&order=14&asc=0&page={page_num}&mode=s&langFlag=0'
        
        driver.get(url)
        wait = WebDriverWait(driver, 5)
        
        # Try to find job elements
        job_selectors = [
            'a[href*="/job/"]',
            'article[data-job-id]',
            'div[data-job-id]'
        ]
        
        job_elements = None
        for selector in job_selectors:
            try:
                job_elements = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )
                if job_elements:
                    break
            except TimeoutException:
                continue
        
        if not job_elements:
            logger.warning(f"No jobs found for {keyword} page {page_num}")
            return []
        
        # Extract job URLs
        job_urls = []
        for element in job_elements:
            try:
                if element.tag_name == 'a':
                    job_link = element
                else:
                    job_link = element.find_element(By.CSS_SELECTOR, 'a[href*="/job/"]')
                
                if job_link:
                    href = job_link.get_attribute('href')
                    if href and '/job/' in href:
                        if not href.startswith('http'):
                            href = f"https://www.104.com.tw{href}"
                        job_urls.append(href)
            except NoSuchElementException:
                continue
        
        logger.info(f"Thread {threading.current_thread().name}: Found {len(job_urls)} jobs on {keyword} page {page_num}")
        return job_urls
        
    except Exception as e:
        logger.error(f"Error fetching {keyword} page {page_num}: {e}")
        return []
    
    finally:
        if driver:
            driver.quit()

def fetch_job_links(search_keywords, logger, max_pages=5, max_workers=4):
    """
    Fetch job listing URLs using multi-threading for better performance
    """
    jobs_url_list = []
    
    # Create tasks for thread pool
    tasks = []
    for keyword in search_keywords:
        for page_num in range(1, max_pages + 1):
            tasks.append((keyword, page_num))
    
    logger.info(f"Starting multi-threaded crawling with {max_workers} workers for {len(tasks)} tasks")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_task = {
            executor.submit(fetch_page_jobs, keyword, page_num, logger): (keyword, page_num)
            for keyword, page_num in tasks
        }
        
        # Collect results
        for future in as_completed(future_to_task):
            keyword, page_num = future_to_task[future]
            try:
                page_jobs = future.result()
                jobs_url_list.extend(page_jobs)
            except Exception as e:
                logger.error(f"Task {keyword} page {page_num} failed: {e}")
    
    # Remove duplicates
    jobs_url_list = list(set(jobs_url_list))
    logger.info(f"Multi-threaded crawling completed. Total unique job URLs: {len(jobs_url_list)}")
    
    return jobs_url_list

def get_job_info_thread_safe(job_url, logger):
    """
    Thread-safe version of job info extraction
    """
    # First try AJAX API (faster)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            'Referer': 'https://www.104.com.tw/job/'
        }

        job_id = job_url.split('/job/')[-1].split('?')[0]
        ajax_url = f'https://www.104.com.tw/job/ajax/content/{job_id}'

        response = requests.get(ajax_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            json_data = response.json()
            
            if 'data' in json_data and 'jobDetail' in json_data['data']:
                return {
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
    except Exception as e:
        logger.warning(f"AJAX failed for {job_url}: {e}")
    
    # Fallback to Selenium (if needed)
    driver = None
    try:
        driver = setup_selenium_driver()
        driver.get(job_url)
        
        wait = WebDriverWait(driver, 8)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
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
        
        return job_details
        
    except Exception as e:
        logger.error(f"Selenium failed for {job_url}: {e}")
        return {}
    
    finally:
        if driver:
            driver.quit()

def get_job_info(job_url, logger):
    """
    Wrapper for backward compatibility
    """
    return get_job_info_thread_safe(job_url, logger)

def get_all_job_details(job_urls, logger, max_workers=6):
    """
    Get all job details using multi-threading
    """
    all_job_details = []
    
    logger.info(f"Starting multi-threaded job detail extraction with {max_workers} workers for {len(job_urls)} jobs")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(get_job_info_thread_safe, job_url, logger): job_url
            for job_url in job_urls
        }
        
        for future in as_completed(future_to_url):
            job_url = future_to_url[future]
            try:
                job_details = future.result()
                if job_details:
                    all_job_details.append(job_details)
                    logger.info(f"Thread {threading.current_thread().name}: Extracted details for {job_details.get('job_title', 'Unknown')}")
            except Exception as e:
                logger.error(f"Failed to get details for {job_url}: {e}")
    
    logger.info(f"Multi-threaded job detail extraction completed. Total jobs: {len(all_job_details)}")
    return all_job_details

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
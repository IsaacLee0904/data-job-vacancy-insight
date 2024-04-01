### import package
import sys, os
import datetime
from time import sleep
import json
import requests
from bs4 import BeautifulSoup

def fetch_job_links(search_keywords, logger):
    """
    Fetch job listing URLs from 104.com.tw based on the provided keywords.

    This function iterates over a list of keywords, constructing a URL to fetch job listings for each keyword.
    It paginates through the search results, extracting job listing URLs until there are no more pages left or until reaching page 20.

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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    }

    for keyword in search_keywords:
        current_page = 1  # Initialize the page counter for each keyword.
        logger.info(f"Fetching job listings for keyword: {keyword}")
        
        while current_page <= 20:  # Limit the pagination to 20 pages
            logger.info(f"Processing page {current_page} for keyword: {keyword}")
            url = f'https://www.104.com.tw/jobs/search/?ro=0&kwop=1&keyword={keyword}&expansionType=job&order=14&asc=0&page={current_page}&mode=s&langFlag=0'
            
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                job_list = soup.find_all('article', class_='js-job-item')

                if not job_list:
                    logger.info(f"No more job listings found for keyword: {keyword} on page {current_page}")
                    break

                for job in job_list:
                    link = job.find('a', class_='js-job-link')
                    if link and 'href' in link.attrs:
                        job_url = f"https:{link['href']}"
                        jobs_url_list.append(job_url)

                current_page += 1
            else:
                logger.error(f"Failed to connect to the website: {response.status_code} while fetching {url}")
                break

    logger.info(f"Finished fetching job listings for keywords.")
    return jobs_url_list
    
def get_job_info(job_url, logger):
    """
    Fetch and parse the job listing AJAX content to extract job details.

    Parameters:
    - job_url (str): The URL of the job listing.
    - logger (logging.Logger): A Logger object used for logging information and errors.

    Returns:
    - dict: A dictionary containing details of a job listing.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        'Referer': 'https://www.104.com.tw/job/'  # Referer header is required
    }

    # Convert the job URL to an AJAX URL
    replace_text = 'jobsource=jolist_c_relevance'  # Assuming 'c' is the replace_word, this may need to be dynamic
    id = job_url.replace('https://www.104.com.tw/job/', '').replace(f'?{replace_text}', '')
    ajax_url = f'https://www.104.com.tw/job/ajax/content/{id}'

    response = requests.get(ajax_url, headers=headers)
    job_details = {}

    if response.status_code == 200:
        json_data = response.json()

        # Extract various details from the JSON data with safety checks
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
    else:
        logger.error(f"Failed to fetch the job details from {ajax_url}: {response.status_code}")

    return job_details

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
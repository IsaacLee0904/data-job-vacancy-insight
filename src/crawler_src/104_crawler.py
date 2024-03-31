import sys, os 
from bs4 import BeautifulSoup
import requests
import pandas as pd

# setup project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.log_utils import set_logger
from utils.crawler_utils import fetch_job_links, get_job_info, save_jobs_to_json

# setup logger 
logger = set_logger()

# vacancy keywords 
# search_keywords = [ 'Business Analyst', 'BI', 'BA' # BA
#                   , 'Data Analyst', '資料分析師', '數據分析師' # DA
#                   , 'Data Scientist', '資料科學家' # DS
#                   , 'Data Engineer', '資料工程師', '數據工程師', '大數據工程師' # DE
#                   , 'Machine Learning Engineer', 'Machine Learning', '機器學習工程師' # MLE
#                   ]

def main():

    # Vacancy keywords
    search_keywords = ['資料工程師']
    job_url_list = fetch_job_links(search_keywords, logger)

    # Initialize an empty list to store all job details
    all_job_details = []

    # Iterate over each job page URL, fetch the job info, and append it to the list
    for job_page in job_url_list:
        job_info_dict = get_job_info(job_page, logger)
        if job_info_dict:  # Ensure the dictionary is not empty
            all_job_details.append(job_info_dict)

    # Save all job details to a single JSON file
    if all_job_details:  # Ensure the list is not empty
        save_jobs_to_json(all_job_details, logger)
    else:
        logger.info("No job information was fetched.")

if __name__ == "__main__":
    main()  
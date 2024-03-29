import sys, os 
from bs4 import BeautifulSoup
import requests
import pandas as pd

# setup project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.log_utils import set_logger
from utils.crawler_utils import fetch_job_links, parse_job_listings, save_jobs_to_csv

# setup logger 
logger = set_logger()

# vacancy keywords 
search_keywords = [ 'Business Analyst', 'BI', 'BA' # BA
                  , 'Data Analyst', '資料分析師', '數據分析師' # DA
                  , 'Data Scientist', '資料科學家' # DS
                  , 'Data Engineer', '資料工程師', '數據工程師', '大數據工程師' # DE
                  , 'Machine Learning Engineer', 'Machine Learning', '機器學習工程師' # MLE
                  ]

def main():
    
    key = ['資料工程師']
    all_jobs = []

    for keyword in key:

        first_pag_url = f'https://www.104.com.tw/jobs/search/?ro=0&kwop=1&keyword={keyword}&expansionType=job&order=14&asc=0&page=1&mode=s&langFlag=0' # kwop=1 for exact search 

        # driver = open_selenium_remote_browser(first_pag_url)  # Initialize and open a remote browser 

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        
        response = requests.get(first_pag_url, headers=headers, params=None)
        soup = BeautifulSoup(response.text, 'html.parser')

        page_select_tag  = soup.find('select', class_='page-select')
        print(page_select_tag)
        # options_tag = page_select_tag.find_all('option')
        # last_option_text = options_tag[-1].text 


        jobs_url_list = []
            
        # response = requests.get(first_pag_url, headers=headers, params=None)
        # soup = BeautifulSoup(response.text, 'html.parser')

        # for listing in soup.find_all('a', 'js-job-link'):
        #     job_url = 'https:' + listing['href']
        #     jobs_url_list.append(job_url)
        
        # print(jobs_url_list)


    # for keyword in key:
    #     params = {'keyword': keyword}
    #     job_links_list = fetch_job_links(url, params)
    #     print(job_links_list)
        # jobs = parse_job_listings(html)
        # all_jobs.extend(jobs)
    
    # save_jobs_to_csv(all_jobs, 'job_listings.csv')

if __name__ == "__main__":
    main()  
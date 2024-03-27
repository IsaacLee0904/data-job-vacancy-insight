import sys, os 
from bs4 import BeautifulSoup
import requests
import pandas as pd

# setup project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.log_utils import set_logger
from utils.crawler_utils import get_job_link, get_job_info

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

    job_list = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
               "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

    job_keyword = '資料工程師'

    for i in range(1, 10):

        url = f'https://www.104.com.tw/jobs/search/?ro=0&kwop=1&keyword={job_keyword}&expansionType=job&order=14&asc=0&page={i}&mode=s&langFlag=0' #kwop=1/只抓包含關鍵字相同的工作
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        a_list = soup.find_all('a', 'js-job-link')
        for link in a_list:
            href = 'https:'+link['href']
            # print(href)
            if 'relevance' in href:
                job_list.append(href)

            print(job_list)

if __name__ == "__main__":
    main()  
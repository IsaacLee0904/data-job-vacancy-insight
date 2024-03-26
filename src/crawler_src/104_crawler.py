import sys, os 
from bs4 import BeautifulSoup
import requests
import pandas as pd

# setup project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.log_utils import set_logger

# setup logger 
logger = set_logger()

# vacancy keywords 
search_keywords = [ 'Busniess Analyst', 'BI' # BA
                  , 'Data Analyst', '資料分析師', '數據分析師' # DA
                  , 'Data Scientist', '資料科學家' # DS
                  , 'Data Engineer', '資料工程師', '數據工程師', '大數據工程師' # DE
                  , 'Machine Learning Engineer', '機器學習工程師' # MLE
                  ]
 
def main():
    pass

if __name__ == "__main__":
    main()  
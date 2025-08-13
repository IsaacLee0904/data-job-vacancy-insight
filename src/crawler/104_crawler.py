import sys, os 
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# setup project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.core.log_utils import set_logger
from src.core.crawler_utils import fetch_job_links, get_all_job_details, save_jobs_to_json

def main():
    start_time = time.time()
    
    # setup logger 
    logger = set_logger()
    logger.info("🚀 Starting Multi-threaded 104 Job Crawler")

    # vacancy keywords 
    search_keywords = ['Business Analyst', 'BI', 'BA', # BA
                  'Data Analyst', '資料分析師', '數據分析師', # DA
                  'Data Scientist', '資料科學家', # DS
                  'Data Engineer', '資料工程師', '數據工程師', '大數據工程師', # DE
                  'Machine Learning Engineer', 'Machine Learning', '機器學習工程師' # MLE
                  ]
    
    # Performance settings
    MAX_PAGES_PER_KEYWORD = 5  # Reduce for testing, increase for production
    MAX_WORKERS_PAGES = 4      # Number of threads for page crawling
    MAX_WORKERS_DETAILS = 8    # Number of threads for job details
    
    logger.info(f"📊 Configuration:")
    logger.info(f"   Keywords: {len(search_keywords)}")
    logger.info(f"   Max pages per keyword: {MAX_PAGES_PER_KEYWORD}")
    logger.info(f"   Page crawling threads: {MAX_WORKERS_PAGES}")
    logger.info(f"   Details extraction threads: {MAX_WORKERS_DETAILS}")
    
    # Step 1: Get job URLs with multi-threading
    logger.info("📋 Step 1: Fetching job URLs...")
    job_url_list = fetch_job_links(
        search_keywords, 
        logger, 
        max_pages=MAX_PAGES_PER_KEYWORD,
        max_workers=MAX_WORKERS_PAGES
    )
    
    if not job_url_list:
        logger.error("❌ No job URLs were fetched!")
        return
    
    logger.info(f"✅ Step 1 Complete: Found {len(job_url_list)} unique job URLs")
    
    # Step 2: Get job details with multi-threading
    logger.info("📝 Step 2: Extracting job details...")
    all_job_details = get_all_job_details(
        job_url_list,
        logger,
        max_workers=MAX_WORKERS_DETAILS
    )
    
    if not all_job_details:
        logger.error("❌ No job details were extracted!")
        return
    
    logger.info(f"✅ Step 2 Complete: Extracted details for {len(all_job_details)} jobs")
    
    # Step 3: Save results
    logger.info("💾 Step 3: Saving results...")
    save_jobs_to_json(all_job_details, logger)
    
    # Performance summary
    end_time = time.time()
    total_time = end_time - start_time
    
    logger.info("🎉 Multi-threaded Crawling Complete!")
    logger.info(f"⏱️  Total time: {total_time:.2f} seconds")
    logger.info(f"⚡ Average time per job: {total_time/len(all_job_details):.2f} seconds")
    logger.info(f"📊 Jobs per minute: {len(all_job_details)/(total_time/60):.1f}")
    
    # Quick stats
    job_titles = [job.get('job_title') for job in all_job_details if job.get('job_title')]
    companies = [job.get('company_name') for job in all_job_details if job.get('company_name')]
    
    logger.info(f"📈 Results Summary:")
    logger.info(f"   Jobs with titles: {len(job_titles)}")
    logger.info(f"   Jobs with company names: {len(companies)}")
    logger.info(f"   Unique companies: {len(set(companies))}")

if __name__ == "__main__":
    main()
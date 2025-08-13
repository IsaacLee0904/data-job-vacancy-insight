#!/usr/bin/env python3
"""
Performance comparison between single-thread and multi-thread crawlers
"""

import sys, os
import time
from threading import Thread

# setup project root
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from src.core.log_utils import set_logger
from src.core.crawler_utils import fetch_job_links as single_thread_fetch
from src.core.crawler_utils_multithread import fetch_job_links as multi_thread_fetch

def test_single_thread(keywords, logger):
    """Test single-thread performance"""
    logger.info("🐌 Testing Single-Thread Crawler...")
    start_time = time.time()
    
    job_urls = single_thread_fetch(keywords, logger)
    
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info(f"🐌 Single-Thread Results:")
    logger.info(f"   Time: {duration:.2f} seconds")
    logger.info(f"   URLs: {len(job_urls)}")
    logger.info(f"   URLs/minute: {len(job_urls)/(duration/60):.1f}")
    
    return duration, len(job_urls)

def test_multi_thread(keywords, logger):
    """Test multi-thread performance"""
    logger.info("🚀 Testing Multi-Thread Crawler...")
    start_time = time.time()
    
    job_urls = multi_thread_fetch(keywords, logger, max_pages=3, max_workers=4)
    
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info(f"🚀 Multi-Thread Results:")
    logger.info(f"   Time: {duration:.2f} seconds")
    logger.info(f"   URLs: {len(job_urls)}")
    logger.info(f"   URLs/minute: {len(job_urls)/(duration/60):.1f}")
    
    return duration, len(job_urls)

def main():
    logger = set_logger()
    logger.info("⚡ Performance Test: Single vs Multi-Thread")
    
    # Test with small subset for fair comparison
    test_keywords = ['Data Analyst', 'Data Engineer']
    
    print("\n" + "="*50)
    print("🔬 PERFORMANCE COMPARISON TEST")
    print("="*50)
    
    try:
        # Test single-thread
        single_time, single_urls = test_single_thread(test_keywords, logger)
        
        print("\n" + "-"*30)
        
        # Test multi-thread  
        multi_time, multi_urls = test_multi_thread(test_keywords, logger)
        
        # Calculate improvement
        if single_time > 0:
            speed_improvement = (single_time / multi_time) if multi_time > 0 else 0
            time_saved = single_time - multi_time
        
        print("\n" + "="*50)
        print("📊 PERFORMANCE SUMMARY")
        print("="*50)
        print(f"Single-Thread: {single_time:.1f}s ({single_urls} URLs)")
        print(f"Multi-Thread:  {multi_time:.1f}s ({multi_urls} URLs)")
        print(f"Speed Up:      {speed_improvement:.1f}x faster")
        print(f"Time Saved:    {time_saved:.1f} seconds")
        print(f"Efficiency:    {((single_time - multi_time) / single_time * 100):.1f}% faster")
        print("="*50)
        
        if speed_improvement > 2:
            print("🎉 Excellent! Multi-threading provides significant improvement!")
        elif speed_improvement > 1.5:
            print("✅ Good! Multi-threading provides decent improvement!")
        else:
            print("⚠️  Multi-threading improvement is limited. Consider adjusting thread count.")
            
    except Exception as e:
        logger.error(f"Performance test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
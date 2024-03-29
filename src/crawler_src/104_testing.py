import time
import random
import requests

class Job104Spider():
     
    def search(self, keyword, max_mun=10, filter_params=None, sort_type='符合度', is_sort_asc=False):
        """搜尋職缺"""
        jobs = []
        total_count = 0

        url = 'https://www.104.com.tw/jobs/search/list'
        query = f'ro=0&kwop=7&keyword={keyword}&expansionType=area,spec,com,job,wf,wktm&mode=s&jobsource=2018indexpoc'
        if filter_params:
            # 加上篩選參數，要先轉換為 URL 參數字串格式
            query += ''.join([f'&{key}={value}' for key, value, in filter_params.items()])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'Referer': 'https://www.104.com.tw/jobs/search/',
        }

        # 加上排序條件
        sort_dict = {
            '符合度': '1',
            '日期': '2',
            '經歷': '3',
            '學歷': '4',
            '應徵人數': '7',
            '待遇': '13',
        }
        sort_params = f"&order={sort_dict.get(sort_type, '1')}"
        sort_params += '&asc=1' if is_sort_asc else '&asc=0'
        query += sort_params

        page = 1
        while len(jobs) < max_mun:
            params = f'{query}&page={page}'
            r = requests.get(url, params=params, headers=headers)
            if r.status_code != requests.codes.ok:
                print('請求失敗', r.status_code)
                data = r.json()
                print(data['status'], data['statusMsg'], data['errorMsg'])
                break

            data = r.json()
            total_count = data['data']['totalCount']
            jobs.extend(data['data']['list'])

            if (page == data['data']['totalPage']) or (data['data']['totalPage'] == 0):
                break
            page += 1
            time.sleep(random.uniform(3, 5))

        return total_count, jobs[:max_mun]

    def get_job(self, job_id):
        """取得職缺詳細資料"""
        url = f'https://www.104.com.tw/job/ajax/content/{job_id}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'Referer': f'https://www.104.com.tw/job/{job_id}'
        }

        r = requests.get(url, headers=headers)
        if r.status_code != requests.codes.ok:
            print('請求失敗', r.status_code)
            return

        data = r.json()
        return data['data']

    def collect_job_urls(self, search_keywords, max_num_per_keyword=10):
        """收集指定關鍵字職缺的URL"""
        job_urls = []
        for keyword in search_keywords:
            _, jobs = self.search(keyword, max_mun=max_num_per_keyword)
            for job in jobs:
                job_urls.append(f"https:{job['link']['job']}")
        return job_urls

    def collect_job_details(self, job_urls):
        """收集職缺詳細資訊"""
        job_details = []
        for url in job_urls:
            job_id = url.split('/job/')[-1].split('?')[0]
            job_detail = self.get_job(job_id)
            job_details.append(job_detail)
        return job_details

if __name__ == "__main__":
    # vacancy keywords 
    search_keywords = [ 'Business Analyst', 'BI', 'BA' # BA
                    , 'Data Analyst', '資料分析師', '數據分析師' # DA
                    , 'Data Scientist', '資料科學家' # DS
                    , 'Data Engineer', '資料工程師', '數據工程師', '大數據工程師' # DE
                    , 'Machine Learning Engineer', 'Machine Learning', '機器學習工程師' # MLE
                    ]
    job104_spider = Job104Spider()
    job_urls = job104_spider.collect_job_urls(search_keywords)
    job_details = job104_spider.collect_job_details(job_urls)

    # 現在 job_details 中包含了所有職缺的詳細資訊
    print(job_details[0])  # 印出第一個職缺的詳細資訊作為示例

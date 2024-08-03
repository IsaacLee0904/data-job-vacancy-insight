import pandas as pd
import numpy as np
import openai
import toml
# LangChain Models
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
# Kor!
from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number
import os, sys

api_config = toml.load('config/api_config.toml')['OPENAI']
openai_api_key = api_config['API_KEY']    # Set the API key

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo", # Cheaper but less reliable
    # model_name="gpt-4",
    temperature=0,
    max_tokens=2000,
    openai_api_key=openai_api_key
)

df = pd.read_csv('data/job_description.csv')

df['full_info'] = df.apply(lambda row: f"公司名稱：{row['company_name']}。\n職缺名稱：{row['job_title']}。\n需求年資:{row['experience']}。\n職務描述：{row['job_description']}，\n其他要求：{row['others']}。", axis=1)

job_description = """
    1.建置與優化巨量結構化資料、半結構、非結構化資料的資料管線
    2.建置不同類型的 data infra/pipeline，並設計部署策略、監控機制，以確保服務穩定性
    3.評估與導入 modern data stack，用以解決以下問題：data governance, data quality, MLOps
    4.優化開發者體驗，解決資料科學家開發與部署會遇到的問題

    104僅供職缺參考，若您對此職缺有興趣，請至本行「玉山菁英甄選網站」投遞履歷，如書審通過，後續將邀請您參加面談。謝謝！
    【網址：https://esnhr.pse.is/394b2n 】 

    【必備條件】
    1.熟悉 Linux、Python 程式開發、Git版本控制
    2.熟悉軟體開發流程實務，包含但不限於開發滿足可讀性、可維護性、可擴充性之應用程式
    3.精通開發與維護 ETL、資料管線，並具有處理每日 100GB 以上資料的經驗，熟悉 Apache Airflow 佳
    4.具備以下任一系統建置、監控機制、效能調校與維護實務經驗尤佳：PostgreSQL, ElasticSearch, Apache Kafka, Minio
    5.熟悉 SQL，有效能調教經驗佳

    【加分條件】
    1.具備 Kubernetes 基本概念
    2.具備 CI/CD pipeline基本概念
    3.具備 Infrastructure as Code(IaC) 基本概念
    4.具備 Apache Spark 基本概念
    5.具備 Data Streaming 基本概念
    """
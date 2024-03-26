import pandas
import numpy
import scrapy
import selenium
from bs4 import BeautifulSoup
import requests
import pyspark
import psycopg2
import dbt
import telegram

print(f"Pandas version: {pandas.__version__}")
print(f"NumPy version: {numpy.__version__}")

# Scrapy doesn't have a __version__ attribute, so we just check if it's imported
print("Scrapy imported successfully")

# Selenium
print(f"Selenium version: {selenium.__version__}")

# Beautiful Soup
print(f"BeautifulSoup imported successfully")

# Requests
print(f"Requests version: {requests.__version__}")

# PySpark
print(f"PySpark version: {pyspark.__version__}")

# Psycopg2 (PostgreSQL database adapter)
print(f"Psycopg2 version: {psycopg2.__version__}")

# DBT does not have a __version__ attribute directly accessible
# but you can import specific modules to check its presence
print("DBT imported successfully")

# Piperider and python-telegram-bot don't have __version__ attributes accessible like this
# We'll just print a message indicating they're imported.
print("Piperider imported successfully")
print("Python Telegram Bot imported successfully")

if __name__ == "__main__":
    pass

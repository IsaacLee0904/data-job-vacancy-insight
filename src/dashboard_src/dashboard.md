# dashboard Doc.
## Overview
A Data-Job-Vacancy-Insight dashboard designed with Figma and implemented with Plotly and Dash.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Pages](#pages)
- [References](#references)

## Installation

### Step 1: Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/Data-Job-Vacancy-Insight.git
cd Data-Job-Vacancy-Insight
```

### Step 2: Set Up Virtual Environment
Set up a virtual environment and install required packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Step 3: Configure Database and Settings
Ensure your database and any necessary environment variables are correctly configured. Modify any configuration files as needed.

## Usage

### Run the Dashboard

To start the dashboard application, run the following command:

```bash
python python src/dashboard_src/dashboard_app.py
```
Access the dashboard by visiting http://localhost:9100 in your web browser.

## Project Structure

The project structure is as follows:
```
├── assets
│   ├── geo_data
│   ├── globals.css
│   ├── icons
│   ├── img
│   └── styles.css
├── dashboard_app.py
├── dashboard_index.py
└── pages
        ├── __init__.py
        ├── education_pages.py
        ├── geography_pages.py
        ├── home_pages.py
        └── stack_pages.py
```

## Pages

### Home
The home page provides an overview of the dashboard's functionalities and highlights key metrics and insights.

### Stack
The stack page displays data regarding the technological stack and tools required for various job roles.

### Education
The education page visualizes data related to educational requirements and qualifications mentioned in job listings.

### Geography
The geography page presents geographical distribution and analysis of job vacancies.

## References
- [Dashboard Design 必讀的六篇文章](https://yvonne-chiu.medium.com/%E6%96%B0%E6%89%8B%E4%B8%8A%E8%B7%AF-dashboard-design-%E5%BF%85%E8%AE%80%E7%9A%84%E5%85%AD%E7%AF%87%E6%96%87%E7%AB%A0-c2c4f8e82179) - A medium article of dashboard design guideline.

- [Data Visualization資料視覺化- Python -Plotly進階視覺化 — Dash教學(一)](https://chwang12341.medium.com/data-visualization%E8%B3%87%E6%96%99%E8%A6%96%E8%A6%BA%E5%8C%96-python-plotly%E9%80%B2%E9%9A%8E%E8%A6%96%E8%A6%BA%E5%8C%96-dash%E6%95%99%E5%AD%B8-%E4%B8%80-c087c0008b78) - A medium article of basic plotly and dash concept.

- [Python Dash 實踐（上）——草圖設計與CSS｜教學](https://www.bianalyst-gt.com/post/python-dash-%E5%AF%A6%E8%B8%90%EF%BC%88%E4%B8%8A%EF%BC%89-%E8%8D%89%E5%9C%96%E8%A8%AD%E8%A8%88%E8%88%87css-%E6%95%99%E5%AD%B8) - A blog article introduce usage of CSS in a dash app.

- [玩玩看地理空間資料!(1)— 用Geopandas資料視覺化](https://medium.com/@fearless_fusion_snake_755/%E7%8E%A9%E7%8E%A9%E7%9C%8B%E5%9C%B0%E7%90%86%E7%A9%BA%E9%96%93%E8%B3%87%E6%96%99-1-%E7%94%A8geopandas%E8%B3%87%E6%96%99%E8%A6%96%E8%A6%BA%E5%8C%96-017c56e94730) - A medium article introduce plot with geo data.

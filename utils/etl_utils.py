import re
import os
import pandas as pd
import shutil

class GeneralDataProcessor:
    def __init__(self, logger):
        self.logger = logger

    def read_json_to_df(directory_path, logger):
        """
        Read the latest JSON file from a specified directory and convert it to a pandas DataFrame.

        Parameters:
        - directory_path (str): The path to the directory containing JSON files.
        - logger (logging.Logger): A Logger object used for logging information and errors.

        Returns:
        - tuple: A tuple containing the DataFrame and the file path. The DataFrame contains the contents of the latest JSON file,
                and the file path is the path to this JSON file. Returns (None, None) if no JSON files are found.
        """
        logger.info(f"Reading the latest JSON file from {directory_path}")

        # Get all files in the directory
        files = os.listdir(directory_path)

        # Filter out JSON files
        json_files = [file for file in files if file.endswith('.json')]

        # If no JSON files are found, log a warning and return None, None
        if not json_files:
            logger.warning("No JSON files found in the directory.")
            return None, None

        # Sort the files to find the latest one
        json_files.sort(reverse=True)
        latest_json_file = json_files[0]

        # Read the JSON file into a DataFrame
        file_path = os.path.join(directory_path, latest_json_file)
        df = pd.read_json(file_path)

        logger.info(f"Successfully read {latest_json_file}")

        # Return the DataFrame and the path to the JSON file
        return df, file_path

    def move_to_backup_folder(file_path, backup_folder):
        
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)
        
        shutil.move(file_path, os.path.join(backup_folder, os.path.basename(file_path)))

    def convert_column_type(df, column_name, target_type, format=None):
        """
        Convert the data type of a specific column in the DataFrame.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the data.
        - column_name (str): The name of the column to convert.
        - target_type (type): The target data type.
        - format (str, optional): The format string if converting to datetime.

        Returns:
        - pd.DataFrame: The DataFrame with the converted column.
        """
        if target_type == 'datetime':
            df[column_name] = pd.to_datetime(df[column_name], format=format)
        else:
            df[column_name] = df[column_name].astype(target_type)
        
        return df

class RawDataProcessor:
    def __init__(self, logger):
        self.logger = logger

    def filter_jobs_by_title_and_type(self, df):
        """
        Filter the DataFrame to include only jobs that match specified keywords in both job title and job type.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing job data.
        - title_keywords (list): Keywords to filter on the job title.
        - type_keywords (list): Keywords to filter on the job type.

        Returns:
        - pd.DataFrame: A DataFrame containing filtered job data.
        """
        # set up a job title keywords for data cleaning            
        title_keywords = ['數據', '資料', '機器學習', 'Data', 'AI', 
                            'Machine Learning', '演算法', '分析', 'NLP',
                            'BI', 'Business Analyst']
        # set up a job type keywords for data cleaning 
        type_keywords = ['軟體工程師', '演算法工程師', '系統分析師', '資料庫管理人員', '其他資訊專業人員', 
                    '數據分析師', '資料工程師', '市場調查／市場分析', 'Internet程式設計師', '系統工程師', 
                    '資料科學家', '其他專案管理師', '軟體專案管理師', '統計學研究員', 'AI工程師',
                    '統計精算人員', '網路管理工程師', '營運管理師／系統整合／ERP專案師', '網站行銷企劃'
                    '專案經理', '雲端工程師', '軟體工程研發高階主管', '顧問師']

        # Create a regex pattern to match any of the keywords, case insensitive
        title_pattern = '|'.join([f"(?i){re.escape(keyword)}" for keyword in title_keywords])
        type_pattern = '|'.join([f"(?i){re.escape(keyword)}" for keyword in type_keywords])

        # Filter df where 'job_titel' and 'job_type' matches the regex pattern
        filtered_df = df[
            df['job_title'].str.contains(title_pattern, regex=True) & 
            df['job_type'].str.contains(type_pattern, regex=True)
        ]

        return filtered_df

    def classify_data_role(self, df):
        """
        Assign a data role based on the job title.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing job data.

        Returns:
        - pd.DataFrame: The DataFrame with the new 'data_role' column added.
        """
        def determine_role(title):
            original_title = title
            title = title.lower()
            if 'AI' in original_title:
                return 'Machine Learning Engineer'
            elif any(keyword in title for keyword in ['business analyst', 'business strategy analyst', '商業分析師']):
                return 'Business Analyst'
            elif any(keyword in title for keyword in ['data analyst', '資料分析師', '數據分析師', '數據分析', '資料分析']):
                return 'Data Analyst'
            elif any(keyword in title for keyword in ['data scientist', 'data science', '資料科學家', '資料科學工程師', '資料科學']):
                return 'Data Scientist'
            elif any(keyword in title for keyword in ['data engineer', 'etl', '資料工程師', '數據工程師', '大數據工程師', '資料處理', '數據處理', '倉儲', '整合', '串流']):
                return 'Data Engineer'
            elif any(keyword in title for keyword in ['machine learning engineer', 'machine learning', 'deep learning', 'llm', '機器學習工程師', '機器學習', '深度學習', '演算法']):
                return 'Machine Learning Engineer'
            elif any(keyword in title for keyword in ['bi', '視覺化', '可視化']):
                return 'BI Engineer'
            elif any(keyword in title for keyword in ['pm', '專案', '資料庫']):
                return 'Project Manager'
            elif any(keyword in title for keyword in ['data architect', 'infrastructure', '架構師', '平台', '中台']):
                return 'Data Architect'
            elif any(keyword in title for keyword in ['dba', 'project manager', '資料庫管理']):
                return 'Database Administrator'
            elif any(keyword in title for keyword in ['mis']):
                return 'MIS'
            elif any(keyword in title for keyword in ['se', '系統']):
                return 'System Engineer'
            else:
                return 'Others'
        
        df['data_role'] = df['job_title'].apply(determine_role)
        return df
    
    def integrate_skills_into_tools(self, df):
        """
        Check 'job_description' and 'others' fields for specific keywords and add the relevant tools to the 'tools' field in a string format, separated by '、'.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing job data.

        Returns:
        - pd.DataFrame: The updated DataFrame with skills added to the 'tools' field.
        """
        # Dictionary for skills and tools mapping, in order to have a correct naming
        keywords_skills = {
            # Cloud Platforms
            'aws': 'AWS', 'gcp': 'GCP', 'google cloud storage': 'Google Cloud Storage', 
            'google cloud pub/sub': 'Google Cloud Pub/Sub', 

            # Big Data Technologies
            'hadoop': 'Hadoop', 'spark': 'Spark', 'flume': 'Flume', 'storm': 'Storm', 
            'zookeeper': 'Zookeeper', 'hbase': 'HBase', 'kafka': 'Kafka', 'rabbitMQ': 'RabbitMQ',

            # Database & Storage
            'redshift': 'Redshift', 'snowflake': 'Snowflake', 'qlik': 'Qlik', 'cognos': 'Cognos', 
            'bigQuery': 'BigQuery', 'bigTable': 'BigTable', 'bigQueryML': 'BigQueryML', 
            'bigQuerySQL': 'BigQuerySQL', 'hive': 'Hive', 'pig': 'Pig', 'sql server': 'SQL Server',

            # Data Science & Machine Learning
            'tensorFlow': 'TensorFlow', 'keras': 'Keras', 'scikit-learn': 'Scikit-learn', 
            'pyTorch': 'PyTorch', 'pandas': 'Pandas', 'numpy': 'Numpy', 'scipy': 'Scipy', 
            'matplotlib': 'Matplotlib', 'databricsk': 'Databricks', 'seaborn': 'Seaborn',

            # Business Intelligence
            'power bi': 'Power BI', 'tableau': 'Tableau', 'google looker studio': 'Google Looker Studio', 
            'google data studio': 'Google Data Studio',

            # Monitoring & Visualization
            'grafana': 'Grafana', 'kibana': 'Kibana',

            # DevOps & Version Control
            'docker': 'Docker', 'kubernetes': 'Kubernetes', 'jenkins': 'Jenkins', 'git': 'Git', 
            'gitHub': 'GitHub', 'gitLab': 'GitLab', 'bitbucket': 'Bitbucket',

            # General Software & Tools
            'excel': 'Excel', 'word': 'Word', 'powerpoint': 'PowerPoint', 'sharepoint': 'SharePoint', 
            'outlook': 'Outlook', 'visio': 'Visio', 'spreadsheet': 'Spreadsheet',

            # Programming & Scripting Environments
            'airflow': 'Airflow', 'alteryx': 'Alteryx', 'asp.net': 'ASP.NET', 'atlassian': 'Atlassian', 
            'srss': 'SRSS', 'ssrs': 'SSRS', 'ssis': 'SSIS',

            # Operating Systems & Platforms
            'unix': 'Unix', 'linux/unix': 'Linux / Unix', 'linux': 'Linux', 'windows': 'Windows', 'mac os': 'Mac OS',
            'ubnutu': 'Ubuntu', 'centos': 'CentOS', 'redhat': 'RedHat', 'fedora': 'Fedora', 'suse': 'SUSE',

            # Web Development
            'vue': 'Vue', 'jquery': 'jQuery',

            # Compliance & Security
            'gdpr': 'GDPR',

            # Statistical Software
            'spss': 'SPSS', 'microstrategy': 'MicroStrategy',
        }

        keywords_programming = {
            # High-level General Purpose Languages
            'python': 'Python', 'java': 'Java', 'c#': 'C#', 'javascript': 'JavaScript', 'php': 'PHP',
            'ruby': 'Ruby', 'go': 'Go', 'kotlin': 'Kotlin', 'swift': 'Swift', 'dart': 'Dart', 
            'r': 'R', 'golang': 'Golang',

            # Low-level & Systems Programming Languages
            'c': 'C', 'c++': 'C++', 'c/c++': 'C / C++', 'rust': 'Rust', 'assembly': 'Assembly',

            # Functional & Other Languages
            'scala': 'Scala', 'f#': 'F#', 'haskell': 'Haskell', 'elixir': 'Elixir', 'clojure': 'Clojure',
            'lisp': 'Lisp', 'ocaml': 'OCaml', 'erlang': 'Erlang', 'fortran': 'Fortran', 'apl': 'APL',
            'cobol': 'COBOL', 'delphi': 'Delphi', 'groovy': 'Groovy', 'lua': 'Lua', 'pascal': 'Pascal',

            # Web & Markup Languages
            'html': 'HTML', 'css': 'CSS', 'sass': 'Sass', 'typescript': 'TypeScript', 'javascript/typescript': 'JavaScript / TypeScript',

            # Scripting & Automation
            'bash': 'Bash', 'shell': 'Shell', 'shell script': 'Shell Script', 'powershell': 'Powershell',

            # Database Query Languages
            'sql': 'SQL', 't-sql': 'Transact-SQL', 'pl/sql': 'PL/SQL', 'nosql': 'NoSQL', 'no-sql': 'No-SQL', 
            'mongodb': 'MongoDB', 'mongo': 'Mongo', 'mysql': 'MySQL', 'postgresql': 'PostgreSQL', 'sqlite': 'SQLite',
            'oracle': 'Oracle', 'duckdb': 'DuckDB', 

            # Specialized & Miscellaneous
            'vba': 'VBA', 'matlab': 'MATLAB', 'sas': 'SAS', 'visual_basic': 'Visual Basic', 'vb.net': 'VB.NET', 'mssql': 'MSSQL',
            'perl': 'Perl', 'solidity': 'Solidity', 'crystal': 'Crystal', 'julia': 'Julia', 'd3.js': 'D3.js',
        }
        def find_skills(text):
            found_skills = []
            # Combine both skills and programming keywords into one dictionary
            all_keywords = {**keywords_skills, **keywords_programming}
            for keyword, formal_name in all_keywords.items():
                # Check if the keyword is in text, case insensitive
                if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
                    found_skills.append(formal_name)
            return found_skills

        # Apply find_skills function to 'job_description' and 'others', and add found skills to 'tools'
        df['tools'] = df.apply(
            lambda x: '、'.join(sorted(set((x['tools'].split('、') if x['tools'] else []) + find_skills(x['job_description']) + find_skills(x['others'])))),
            axis=1
        )

        return df

    def process_location(self, df):
        """
        Process the location column to extract county information or mark as overseas.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing job data.

        Returns:
        - pd.DataFrame: The DataFrame with the new 'County' column added.
        """
        def extract_county(location):
            # if info include "縣"
            if '縣' in location:
                return location[:location.index('縣') + 1]
            # else if info include "市"
            elif '市' in location:
                return location[:location.index('市') + 1]
            # if non "市" or "縣"
            return '海外'

        df.loc[:, 'county'] = df['location'].apply(extract_county)
        return df

    def convert_to_list(self, df, column_names):
        """
        Convert the string values in specified columns to lists, splitting by a specific character.
        Empty strings are converted to None.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the data.
        - column_names (list): A list of column names to be converted.

        Returns:
        - pd.DataFrame: The DataFrame with the updated columns.
        """
        for column in column_names:
            if column in df.columns:
                df[column] = df[column].apply(lambda x: x.split('、') if isinstance(x, str) and x != '' else None)
            else:
                self.logger.warning(f"Column {column} does not exist in DataFrame")
        return df
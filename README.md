<p align="left">
   <img src="https://user-images.githubusercontent.com/65984000/144644627-131d98b6-19ea-4fc6-a67a-a36d959a191a.png" width=200 height=200>
</p>
  <h3 align="left">Ingestion Rerport Tool</h3>
  <p align="left">
    This tool help you to created reports and extract data from Connect and LCT sistems. Moreover, you can see this data in a Dashboard and make you analysis easier and faster. 
</p>


## Table of contents

- [Quick start](#quick-start)
- [Installation](#installation)
- [Run](#run)
- [Run Report](#run-report)
- [View Report](#view-report)
- [Architecture](#architecture)



## Quick start

Requierments

- [Python](https://www.python.org/downloads/)
- [IDE](https://www.jetbrains.com/pycharm/download/#section=windows)
- [Clone repo](https://github.com/aldair-leon-by/IngestionReport)

## Installation

#### Step #1:
<br>
Select your location where you want to store this tool, then run this command.

`git clone https://github.com/aldair-leon-by/IngestionReport.git`

#### Step #2
After you clone the repo, some folder and files will download, and you wil get something simillar as this: 
```
IngestionReport/
└── .streamlit/
    │   ├── config.toml
    ├── ExcelMacros/
    │   ├── macros_format.xlsm
    ├── resources/
    │    ├── customers.json
    │    ├── data_base_credentials.json
    │    ├── ingestion_id.json
    │    ├── macro.json
    │    └── performance_header.json
    ├── scripts/
    |   ├── __init__.py
    |   ├── db_connection.py
    |   ├── env_config.py
    |   ├── excel_format.py
    |   ├── folder_file_name.py
    |   ├── init_logger.py
    |   ├── join_files.py
    |   ├── mysql_query.py
    |   ├── report_creation.py
    |   ├── run_report.py
    |   ├── sql_query.py
    |   ├── time_calculation.py
    │   └── view_report.py
    ├── .gitignore
    ├── README.md
    ├── app.py
    └── multiapp.py
```

#### Step #3

If you want to change, data base credentials of some config you have to edit, data_base_credentials.json.
```
  "SW": {
    "sql_db_sit": [
      {
        "sql_server": "****",
        "sql_username": "****",
        "sql_password": "****",
        "sql_database": "****"
      }
    ],
    "sql_db_uat": [
      {
        "sql_server": "****",
        "sql_username": "****",
        "sql_password": "****",
        "sql_database_adapter": "****",
        "sql_database_message_store": "****"
      }
    ],
    "sql_db_prod": [
      {
        "sql_server": "****",
        "sql_username": "****",
        "sql_password": "****",
        "sql_database_adapter": "****",
        "sql_database_message_store": "****"
      }
    ],
    "mysql_db_uat": [
      {
        "mysql_server": "****",
        "mysql_username": "****",
        "mysql_password": "****",
        "mysql_database": "****"
      }
    ],
    "mysql_db_prod": [
      {
        "mysql_server": "****",
        "mysql_username": "****",
        "mysql_password": "****",
        "mysql_database": "****"
      }
    ]
  }
```

In case that you need to add a new customer you have to edit customers.json 
```
{
  "customer": {
    "0": "Select customer",
    "1": "SW",
    "2": "Loblaw",
    "3": "GSK"
  },
    "env": {
    "0": "Select env",
    "1": "sit",
    "2": "uat",
    "3": "prod"
  }
}
```
After this, add this new customer DataBase credentials in data_base_credentials.json.

## Run
Open a command prompt located in **C:\your-path\IngestionReport** folder, then run following command:

`streamlit run .\app.py`

Then a window will diplay. 

![image](https://user-images.githubusercontent.com/65984000/144652308-683a9702-4990-4f08-a1ea-7dc2d522e869.png)


## Run Report

Please, fill the following information to run yout report. After you finish, click in the Run button. Then an Excel file will be created and store in your local. 


![image](https://user-images.githubusercontent.com/65984000/144652921-1a1bf9ba-7eab-4705-9697-ac5ae18d57b8.png)
![image](https://user-images.githubusercontent.com/65984000/144652969-7e76ea82-475b-4ddb-9170-9e79603b00f3.png)

After you run your report, you will see a message like this:
![image](https://user-images.githubusercontent.com/65984000/144653621-27959353-bd6e-4278-b28e-613270cf066f.png)

**NOTE: IF YOU GET THIS ERROR, IS BECAUSE IN THAT INTERVAL OF TIME THE SISTEM DIDNT MAKE ANY INGESTION PLEASE SELECT OTHER INTERVAL OF TIME**

**I will fix this and add a better exception**
![image](https://user-images.githubusercontent.com/65984000/144654035-6c1d23b2-4db9-48df-a4c7-d948441f43c9.png)




## View Report
Please select you excel file, that we created before

![image](https://user-images.githubusercontent.com/65984000/144654549-61db13a0-45ad-455b-99f0-e4f243eaf31d.png)

After you select your file, data will display in a dashboard:
![image](https://user-images.githubusercontent.com/65984000/144654692-b2e829a8-0943-49c2-8d08-29fb3cf979a7.png)



## Architecture








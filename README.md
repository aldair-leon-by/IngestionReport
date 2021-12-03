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
- [Bugs and feature requests](#bugs-and-feature-requests)
- [Contributing](#contributing)
- [Creators](#creators)
- [Thanks](#thanks)
- [Copyright and license](#copyright-and-license)


## Quick start

Requierments

- [Python](https://www.python.org/downloads/)
- [IDE](https://www.jetbrains.com/pycharm/download/#section=windows)
- [Clone repo](https://github.com/aldair-leon-by/IngestionReport)

## Installation

#### Step #1:
<br>
Select your location where you want to store this tool, then run this command.
<br>
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

Some text

```text
folder1/
└── folder2/
    ├── folder3/
    │   ├── file1
    │   └── file2
    └── folder4/
        ├── file3
        └── file4
```

## Bugs and feature requests

Have a bug or a feature request? Please first read the [issue guidelines](https://reponame/blob/master/CONTRIBUTING.md) and search for existing and closed issues. If your problem or idea is not addressed yet, [please open a new issue](https://reponame/issues/new).

## Contributing

Please read through our [contributing guidelines](https://reponame/blob/master/CONTRIBUTING.md). Included are directions for opening issues, coding standards, and notes on development.

Moreover, all HTML and CSS should conform to the [Code Guide](https://github.com/mdo/code-guide), maintained by [Main author](https://github.com/usernamemainauthor).

Editor preferences are available in the [editor config](https://reponame/blob/master/.editorconfig) for easy use in common text editors. Read more and download plugins at <https://editorconfig.org/>.

## Creators

**Creator 1**

- <https://github.com/usernamecreator1>

## Thanks

Some Text

## Copyright and license

Code and documentation copyright 2011-2018 the authors. Code released under the [MIT License](https://reponame/blob/master/LICENSE).

Enjoy :metal:







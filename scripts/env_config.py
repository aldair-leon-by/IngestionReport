import json
import os
from init_logger import log

"""
Env configurations and folders path
"""

# Logger
logger = log('ENV SETUP')


# Report folder absolut path
def abs_path_Report_folder() -> str:
    verify_path = os.path.exists(os.path.abspath("../Report"))
    if verify_path:
        report_path = os.path.abspath("../Report")
        logger.info('Report folder found ...')
    else:
        logger.error('Report folder doesnt found!')
    return report_path


# Resources folder absolut path
def abs_path_resources() -> str:
    verify_path = os.path.exists(os.path.abspath("../resources"))
    if verify_path:
        resource_path = os.path.abspath("../resources")
        logger.info('Resources folder found ...')
    else:
        logger.error('Resources folder doesnt found!')
    return resource_path


# Return json with all the db credentials sql and my sql
def abs_data_base_credentials() -> json:
    folder_path = abs_path_resources()
    verify_path = os.path.exists(os.path.abspath(folder_path + '/data_base_credentials.json'))
    if verify_path:
        credentials_file = os.path.abspath(folder_path + '/data_base_credentials.json')
        with open(credentials_file) as f:
            db_credentials = json.load(f)
        logger.info('Load db_credentials ...')
    else:
        logger.error('db_credentials doesnt found!')
    return db_credentials

import json
import os
from scripts.init_logger import log

"""
Env configurations and folders path
"""

# Logger
logger = log('ENV SETUP')


# Report folder absolut path
def abs_path_Report_folder() -> str:
    verify_path = os.path.exists(os.path.abspath("Report"))
    if verify_path:
        report_path = os.path.abspath("Report")
        logger.info('Report folder found ...')
    else:
        logger.error('Report folder doesnt found!')
    return report_path


# Macro folder absolut path
def abs_path_Macro_folder() -> str:
    verify_path = os.path.exists(os.path.abspath("ExcelMacros/macros_format.xlsm"))
    if verify_path:
        macro_path = os.path.abspath("ExcelMacros/macros_format.xlsm")
        logger.info('ExcelMacros folder found ...')
    else:
        logger.error('ExcelMacros folder doesnt found!')
    return macro_path


# Resources folder absolut path
def abs_path_resources() -> str:
    verify_path = os.path.exists(os.path.abspath("resources"))
    if verify_path:
        resource_path = os.path.abspath("resources")
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
        return db_credentials
        logger.info('Load db_credentials ...')
    else:
        logger.error('db_credentials doesnt found!')


# Return json with excel macros name
def abs_excel_macros() -> json:
    folder_path = abs_path_resources()
    verify_path = os.path.exists(os.path.abspath(folder_path + '/macro.json'))
    if verify_path:
        macro_name = os.path.abspath(folder_path + '/macro.json')
        with open(macro_name) as f:
            macro = json.load(f)
        return macro
        logger.info('Excel Macro format start ...')
    else:
        logger.error('Error Macros Name!')


"""
Author: Aldair Leon
Date: Dec 3rd, 2021
"""
import os
from datetime import datetime
from scripts.env_config import abs_path_Report_folder
from scripts.init_logger import log

# Logger
logger = log('FILE NAME')


# Return folder name with the interval of Data in the report (Ingestion start to Ingestion finish)
def folder_name_date(report) -> tuple:
    format_time_start = report['INGESTION_SERVICE_MESSAGE_STARTED'][0]
    format_time_finish = report['INGESTION_SERVICE_MESSAGE_STARTED'].iloc[-1]
    directory_FileName_start = format_time_start.to_pydatetime()
    directory_FileName_finish = format_time_finish.to_pydatetime()
    folder_name_start = datetime.strptime(str(directory_FileName_start), '%Y-%m-%d %H:%M:%S.%f').strftime(
        '%B-%d-%Y')
    folder_name_finish = datetime.strptime(str(directory_FileName_finish), '%Y-%m-%d %H:%M:%S.%f').strftime(
        '%B-%d-%Y')
    return folder_name_start, folder_name_finish


# Return file name with the interval of Time in the report (Ingestion start to Ingestion finish)
def file_name_date(report) -> tuple:
    format_time_start = report['INGESTION_SERVICE_MESSAGE_STARTED'][0]
    format_time_finish = report['INGESTION_SERVICE_MESSAGE_STARTED'].iloc[-1]
    directory_FileName_start = format_time_start.to_pydatetime()
    directory_FileName_finish = format_time_finish.to_pydatetime()
    file_name_start = datetime.strptime(str(directory_FileName_start), '%Y-%m-%d %H:%M:%S.%f').strftime(
        'h%Hm%Ms%Sms%f')
    file_name_finish = datetime.strptime(str(directory_FileName_finish), '%Y-%m-%d %H:%M:%S.%f').strftime(
        'h%Hm%Ms%Sms%f')
    return file_name_start, file_name_finish


# Create folder and return path of this folder
def folder_IngestionReport(report) -> str:
    folder = folder_name_date(report)
    report_folder = abs_path_Report_folder()
    folder_name_details = 'From- ' + folder[0] + ' To- ' + folder[1]
    path = os.path.join(report_folder, folder_name_details)
    path_detail = os.path.join(path, 'IngestionReport')
    if not os.path.exists(path):
        os.mkdir(path, 0o666)
        logger.info('Successfully creation of folder')
    if not os.path.exists(path_detail):
        os.mkdir(path_detail, 0o666)
        logger.info('Successfully creation of folder')
    return path_detail


# Create and return excel file name
def file_IngestionReport(report) -> str:
    file = file_name_date(report)
    exel_file_name_details = 'IngestionReport From- ' + file[0] + ' To- ' + \
                             file[1] + '.xlsx'
    return exel_file_name_details

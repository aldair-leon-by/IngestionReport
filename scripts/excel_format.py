import os
import win32com.client
from env_config import abs_path_Macro_folder, abs_excel_macros
from init_logger import log

# Logger
logger = log('ENV SETUP')


def excel_Report_format(path_report_name):
    macros = abs_excel_macros()
    detail = macros['excel_macros'][0]['detail_report']
    summary = macros['excel_macros'][0]['summary_report']
    path = abs_path_Macro_folder()
    if os.path.exists(path):
        xl = win32com.client.Dispatch("Excel.Application")
        wb = xl.Workbooks.Open(os.path.abspath(path))
        wb1 = xl.Workbooks.Open(os.path.abspath(path_report_name))
        wb1.Worksheets('DetailReport').Activate()
        wb1.Application.Run(detail)
        wb1.Worksheets('SummaryReport').Activate()
        wb1.Application.Run(summary)
        xl.Visible = True
        wb.Close(SaveChanges=1)
        wb1.Close(SaveChanges=1)
        xl.Application.Quit()
        logger.info('Excel format file Finish..')
        del xl


"""
Author: Aldair Leon
Date: Dec 3rd, 2021
"""

import pandas as pd
from scripts.folder_file_name import folder_IngestionReport, file_IngestionReport
from scripts.join_files import JoinFail
from scripts.init_logger import log
from scripts.excel_format import excel_Report_format

# Logger
logger = log('Ingestion Report')


class IngestionReport:
    # Constructor
    def __init__(self, start, finish, env, customer):
        self.start = start
        self.finish = finish
        self.env = env
        self.customer = customer

    # Customer Data Frame
    def customer_name(self):
        customer_name = {'Customer Name': [self.customer]}
        self.df_customer_name = pd.DataFrame(customer_name)

    # Run Ingestion Report and store in your local PC, return path where you file is located
    def ingestion_report(self) -> str:
        ingestion_Report = JoinFail(self.start, self.finish, self.env, self.customer)  # JoinFail object creation
        e2eIngestionReportDetails = ingestion_Report.DetailReport()  # Created Detail Report
        e2eIngestionReportSummary = ingestion_Report.SummaryReport()  # Created Summary Report
        customer_name = ingestion_Report.customer_name()
        # Performance Metrics
        e2eIngestionReportDetailsPerformanceMetrics = ingestion_Report.DetailReportPerformanceMetrics()
        folder_path = folder_IngestionReport(e2eIngestionReportDetails)
        file_name = file_IngestionReport(e2eIngestionReportDetails)
        with pd.ExcelWriter(folder_path + '\\' + file_name) as write:  # Excel is created with two different pandas DF
            e2eIngestionReportDetails[
                ['INGESTION_ID', 'TYPE_OF_MESSAGE', 'CRNT_STATUS', 'INGESTION_SERVICE_MESSAGE_STARTED',
                 'INGESTION_SERVICE_MESSAGE_FINISHED', 'INGESTION SERVICE TOTAL TIME',
                 'MESSAGE_BROKER_STARTED', 'MESSAGE_BROKER_FINISHED', 'MESSAGE BROKER TOTAL TIME',
                 'LCT_ADAPTER_STARTED', 'LCT_ADAPTER_FINISHED', 'LCT ADAPTER TOTAL TIME',
                 'MSG_STATUS', 'COMPUTATION_STARTED', 'COMPUTATION_FINISHED', 'COMPUTATION_STATUS',
                 'COMPUTATION TOTAL TIME',
                 'totalSourcingObjectCount', 'TOTAL TIME INGESTION']].to_excel(
                write, index=False, sheet_name='DetailReport')
            e2eIngestionReportSummary.to_excel(write, index=False, sheet_name='SummaryReport')
            e2eIngestionReportDetailsPerformanceMetrics[0].to_excel(write, index=False, sheet_name='OrderMetrics')
            e2eIngestionReportDetailsPerformanceMetrics[1].to_excel(write, index=False,
                                                                    sheet_name='TransportationMetrics')
            customer_name.to_excel(write, index=False, sheet_name='CustomerName')
            logger.info('INGESTION REPORT CREATED SUCCESSFULLY ! .. path -> ' + folder_path + '\\' + file_name)
        abs_path_report = folder_path + '\\' + file_name
        excel_Report_format(abs_path_report)
        return abs_path_report

import pandas as pd
from folder_file_name import folder_IngestionReport, file_IngestionReport
from join_files import JoinFail
from init_logger import log
from excel_format import excel_Report_format

# Logger
logger = log('Ingestion Report')


class IngestionReport:
    def __init__(self, start, finish, env):
        self.start = start
        self.finish = finish
        self.env = env

    def ingestion_report(self):
        ingestion_Report = JoinFail(self.start, self.finish, self.env)  # JoinFail object creation
        e2eIngestionReportDetails = ingestion_Report.DetailReport()  # Created Detail Report
        e2eIngestionReportSummary = ingestion_Report.SummaryReport()  # Created Summary Report
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
                 'totalSourcingObjectCount', 'TimeDiff']].to_excel(
                write, index=False, sheet_name='DetailReport')
            e2eIngestionReportSummary.to_excel(write, index=False, sheet_name='SummaryReport')
            e2eIngestionReportDetailsPerformanceMetrics[0].to_excel(write, index=False, sheet_name='OrderMetrics')
            e2eIngestionReportDetailsPerformanceMetrics[1].to_excel(write, index=False,
                                                                    sheet_name='TransportationMetrics')
            logger.info('INGESTION REPORT CREATED SUCCESSFULLY ! .. path -> ' + folder_path + '\\' + file_name)
        abs_path_report = folder_path + '\\' + file_name
        excel_Report_format(abs_path_report)

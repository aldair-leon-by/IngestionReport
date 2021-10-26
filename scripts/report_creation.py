import pandas as pd
from folder_file_name import folder_Details, folder_Summary, file_Summary, file_Details
from join_files import JoinFail
from init_logger import log

# Logger
logger = log('Ingestion Report')


class IngestionReport:
    def __init__(self, start, finish, env):
        self.start = start
        self.finish = finish
        self.env = env

    def detail_report(self):
        self.detailReport = JoinFail(self.start, self.finish, self.env)
        self.e2eIngestionDetails = self.detailReport.DetailReport()
        folder_path = folder_Details(self.e2eIngestionDetails)
        file_name = file_Details(self.e2eIngestionDetails)
        with pd.ExcelWriter(folder_path + '\\' + file_name) as write:
            self.e2eIngestionDetails[
                ['INGESTION_ID', 'TYPE_OF_MESSAGE', 'CRNT_STATUS', 'INGESTION_SERVICE_MESSAGE_STARTED',
                 'INGESTION_SERVICE_MESSAGE_FINISHED', 'INGESTION SERVICE TOTAL TIME',
                 'MESSAGE_BROKER_STARTED', 'MESSAGE_BROKER_FINISHED', 'MESSAGE BROKER TOTAL TIME',
                 'LCT_ADAPTER_STARTED', 'LCT_ADAPTER_FINISHED', 'LCT ADAPTER TOTAL TIME',
                 'MSG_STATUS', 'COMPUTATION_STARTED', 'COMPUTATION_FINISHED', 'COMPUTATION_STATUS',
                 'COMPUTATION TOTAL TIME',
                 'totalSourcingObjectCount', 'TimeDiff']].to_excel(
                write, index=False, sheet_name='DetailReport')
            self.e2eIngestionDetails[
                ['INGESTION_ID', 'totalCpuTimeMs',
                 'averageCpuTimeMs',
                 'performanceStatus',
                 'totalInvocationCount',
                 'currentInvocationCount',
                 'invocationPerObjectRatio',
                 'totalSourcingObjectCount',
                 'totalProcessedObjectCount'
                 ]].to_excel(
                write, index=False, sheet_name='DetailReportComputation')
            logger.info('EXCEL FILE DETAILS REPORT path -> ' + folder_path + '\\' + file_name)

    def summary_report(self):
        e2eIngestionSummary = self.detailReport.SummaryReport()
        folder_path = folder_Summary(self.e2eIngestionDetails)
        file_name = file_Summary(self.e2eIngestionDetails)
        with pd.ExcelWriter(folder_path + '\\' + file_name) as write:
            e2eIngestionSummary.to_excel(write, index=False, sheet_name='SummaryReport')
        logger.info('EXCEL FILE SUMMARY REPORT path -> ' + folder_path + '\\' + file_name)

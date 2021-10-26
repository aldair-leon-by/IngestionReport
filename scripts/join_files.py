from sql_query import sql_query_message_Detail, sql_query_adapter_Detail
from init_logger import log
from mysql_query import mysql_query_computation_time
from time_calculation import ave_time_execution

# Logger
logger = log('JOIN REPORTS')


class JoinFail:

    def __init__(self, start_time, finish_time, env):
        self.start_time = start_time
        self.finish_time = finish_time
        self.env = env

    def DetailReport(self):
        message_store = sql_query_message_Detail(self.start_time, self.finish_time, self.env)
        lct_adapter = sql_query_adapter_Detail(self.start_time, self.finish_time, self.env)
        computation = mysql_query_computation_time(self.env)
        e2eIngestionDetails = message_store[
            ['TYPE_OF_MESSAGE', 'CRNT_STATUS', 'MESSAGE_BROKER_BLK_ID', 'INGESTION_SERVICE_MESSAGE_STARTED',
             'INGESTION_SERVICE_MESSAGE_FINISHED', 'MESSAGE_BROKER_STARTED', 'MESSAGE_BROKER_FINISHED']].merge(
            lct_adapter[['LCT_ADAPTER_STARTED', 'LCT_ADAPTER_FINISHED', 'MSG_STATUS', 'INGESTION_ID'
                , 'MESSAGE_BROKER_BLK_ID']],
            on="MESSAGE_BROKER_BLK_ID",
            how="left")
        self.e2eIngestionComputation = e2eIngestionDetails[
            ['TYPE_OF_MESSAGE', 'CRNT_STATUS', 'INGESTION_SERVICE_MESSAGE_STARTED',
             'INGESTION_SERVICE_MESSAGE_FINISHED', 'MESSAGE_BROKER_STARTED', 'MESSAGE_BROKER_FINISHED',
             'LCT_ADAPTER_STARTED', 'LCT_ADAPTER_FINISHED', 'MSG_STATUS', 'INGESTION_ID']].merge(
            computation[['INGESTION_ID', 'COMPUTATION_STARTED', 'COMPUTATION_FINISHED',
                         'COMPUTATION_STATUS', 'totalCpuTimeMs',
                         'averageCpuTimeMs',
                         'performanceStatus',
                         'totalInvocationCount',
                         'currentInvocationCount',
                         'invocationPerObjectRatio',
                         'totalSourcingObjectCount',
                         'totalProcessedObjectCount'
                         ]],
            on=['INGESTION_ID'],
            how="left")
        self.e2eIngestionComputation = ave_time_execution(self.e2eIngestionComputation)
        logger.info('DETAIL REPORT CREATED!')
        return self.e2eIngestionComputation

    def SummaryReport(self):
        self.e2eIngestionComputation = self.e2eIngestionComputation.astype({"totalSourcingObjectCount": int})
        self.e2eIngestionComputationSummary = self.e2eIngestionComputation.groupby(
                ['TYPE_OF_MESSAGE', 'MSG_STATUS', 'COMPUTATION_STATUS']) \
            .agg(AVE_TIMEINGESTIONsec=('TimeDiff', 'mean'),
                 TOTAL_OBJECT_COUNT=('totalSourcingObjectCount', sum),
                 TOTAL_OF_MESSAGE=('COMPUTATION_STATUS', 'count'),
                 INGESTION_SERVICE_MESSAGE_STARTED=('INGESTION_SERVICE_MESSAGE_STARTED', 'min'),
                 INGESTION_SERVICE_MESSAGE_FINISHED=('INGESTION_SERVICE_MESSAGE_FINISHED', 'max'),
                 MESSAGE_BROKER_STARTED=('MESSAGE_BROKER_STARTED', 'min'),
                 MESSAGE_BROKER_FINISHED=('MESSAGE_BROKER_FINISHED', 'max'),
                 LCT_ADAPTER_STARTED=('LCT_ADAPTER_STARTED', 'min'),
                 LCT_ADAPTER_FINISHED=('LCT_ADAPTER_FINISHED', 'max'),
                 COMPUTATION_STARTED=('COMPUTATION_STARTED', 'min'),
                 COMPUTATION_FINISHED=('COMPUTATION_FINISHED', 'max')).reset_index().round(2)
        logger.info('JOIN SUMMARY INGESTION TO COMPUTATION !!')
        return self.e2eIngestionComputationSummary


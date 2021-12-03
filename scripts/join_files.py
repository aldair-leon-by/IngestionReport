"""
Author: Aldair Leon
Date: Dec 3rd, 2021
"""
import json
from scripts.sql_query import sql_query_message_Detail, sql_query_adapter_Detail
from scripts.init_logger import log
from scripts.mysql_query import mysql_query_computation_time
from scripts.time_calculation import ave_time_execution
import pandas as pd

# Logger
logger = log('JOIN REPORTS')


class JoinFail:

    # Constructor
    def __init__(self, start_time, finish_time, env, customer):
        self.start_time = start_time
        self.finish_time = finish_time
        self.env = env
        self.customer = customer

    # Query and join data and return pandas data frame (Detail Report)
    def DetailReport(self) -> pd.DataFrame:
        message_store = sql_query_message_Detail(self.start_time, self.finish_time, self.env, self.customer)
        lct_adapter = sql_query_adapter_Detail(self.start_time, self.finish_time, self.env, self.customer)
        computation = mysql_query_computation_time(self.env, self.customer)
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
            computation,
            on=['INGESTION_ID'],
            how="left")
        self.e2eIngestionComputation = ave_time_execution(self.e2eIngestionComputation)
        logger.info('DETAIL REPORT CREATED!')
        return self.e2eIngestionComputation

    # Query and group by, using Detail Report data frame (self.e2eIngestionComputation)
    def SummaryReport(self) -> pd.DataFrame:
        self.e2eIngestionComputation = self.e2eIngestionComputation.astype({"totalSourcingObjectCount": int})
        self.e2eIngestionComputationSummary = self.e2eIngestionComputation.groupby(
            ['TYPE_OF_MESSAGE', 'MSG_STATUS', 'COMPUTATION_STATUS']) \
            .agg(AVE_TIMEINGESTIONsec=('TOTAL TIME INGESTION', 'mean'),
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

    # Using performs metrics (json format) from stack_db, convert this data into excel file
    # Return tuple with DataFrame
    # Pending add the rest of services, now only works with Order, Transport, Computation Frontend and Backend service.
    def DetailReportPerformanceMetrics(self) -> tuple:
        with open('resources/performance_header.json') as f:
            performance2 = json.load(f)
        orderMetrics = self.e2eIngestionComputation[
            self.e2eIngestionComputation['TYPE_OF_MESSAGE'].str.contains("Order")]
        transportMetrics = self.e2eIngestionComputation[
            self.e2eIngestionComputation['TYPE_OF_MESSAGE'].str.contains("transport")]
        orderMetrics = orderMetrics[list(performance2['order'][0].values())]
        transportMetrics = transportMetrics[list(performance2['transport'][0].values())]
        return orderMetrics, transportMetrics

    # Return data frame with customer name and environment
    def customer_name(self) -> pd.DataFrame:
        customer_name = {'Customer Name': [self.customer],
                         'Environment': [self.env]}
        df_customer_name = pd.DataFrame(customer_name)
        return df_customer_name

from datetime import datetime
import pyodbc
from scripts.db_connection import sql_connection_message_storage, sql_connection_adapter
import pandas as pd
from scripts.init_logger import log
from scripts.env_config import abs_path_resources

# Logger
logger = log('SQL Query execution')


# SQL Query Ingest Service to Message Broker line by line
def sql_query_message_Detail(start_time, finish_time, env,customer):
    connection_message = sql_connection_message_storage(env,customer)
    start_time = datetime.strptime(start_time, '%y/%m/%d %H:%M:%S.%f')
    finish_time = datetime.strptime(finish_time, '%y/%m/%d %H:%M:%S.%f')
    # Query to execute
    query = 'WITH ingestService_to_MessageBroker AS(SELECT MSG_HDR.MSG_TYPE AS TYPE_OF_MESSAGE,' \
            'MSG_EVNT.CRTD_AT AS INGESTION_SERVICE_MESSAGE_STARTED,' \
            'MSG_HDR.LST_UPDT_AT AS INGESTION_SERVICE_MESSAGE_FINISHED,' \
            'BLK_HDR.BLK_HDR_ID,' \
            'MSG_HDR.MSG_ID,' \
            'BLK_HDR.BLK_ID,' \
            'BLK_HDR.CRNT_STATUS ' \
            'FROM CONNECT_MS.MS_MSG_EVNT AS MSG_EVNT ' \
            'JOIN CONNECT_MS.MS_MSG_HDR AS MSG_HDR ' \
            'ON MSG_EVNT.MSG_HDR_ID = MSG_HDR.MSG_HDR_ID ' \
            'JOIN CONNECT_MS.MS_BLK_HDR AS BLK_HDR ' \
            'ON BLK_HDR.BLK_ID LIKE CONCAT(?, MSG_HDR.MSG_ID,?) ' \
            'AND MSG_EVNT .STATUS = ? ' \
            'AND MSG_HDR.MDL_TYPE LIKE ? WHERE MSG_EVNT.CRTD_AT > ? and MSG_EVNT.CRTD_AT <  ? ' \
            ')' \
            'SELECT ingestService_to_MessageBroker.BLK_HDR_ID,' \
            'ingestService_to_MessageBroker.TYPE_OF_MESSAGE,' \
            'ingestService_to_MessageBroker.CRNT_STATUS, ' \
            'ingestService_to_MessageBroker.MSG_ID AS INGEST_SERVICE_MSG_ID, ' \
            'ingestService_to_MessageBroker.INGESTION_SERVICE_MESSAGE_STARTED,' \
            'ingestService_to_MessageBroker.INGESTION_SERVICE_MESSAGE_FINISHED,' \
            'ingestService_to_MessageBroker.BLK_ID AS MESSAGE_BROKER_BLK_ID,' \
            'MIN(BULK_EVENT.CRTD_AT) AS MESSAGE_BROKER_STARTED,' \
            'MAX(BULK_EVENT.CRTD_AT) AS MESSAGE_BROKER_FINISHED ' \
            'FROM ingestService_to_MessageBroker JOIN CONNECT_MS.MS_BLK_EVNT AS BULK_EVENT ' \
            'ON ingestService_to_MessageBroker.BLK_HDR_ID = BULK_EVENT.BLK_HDR_ID ' \
            'WHERE  BULK_EVENT.STATUS != ? ' \
            'GROUP BY BULK_EVENT.BLK_HDR_ID, ' \
            'ingestService_to_MessageBroker.BLK_HDR_ID,' \
            'ingestService_to_MessageBroker.TYPE_OF_MESSAGE,' \
            'ingestService_to_MessageBroker.INGESTION_SERVICE_MESSAGE_STARTED, ' \
            'ingestService_to_MessageBroker.INGESTION_SERVICE_MESSAGE_FINISHED,' \
            'ingestService_to_MessageBroker.MSG_ID,' \
            'ingestService_to_MessageBroker.BLK_ID, ' \
            'ingestService_to_MessageBroker.CRNT_STATUS ' \
            'ORDER BY ingestService_to_MessageBroker.INGESTION_SERVICE_MESSAGE_STARTED'
    try:
        logger.info('Executing query... Message Store DB')
        sql_query = pd.read_sql_query(query, params=(
            '%', '%', 'Received', '%BYDM%', start_time, finish_time, 'Processed'),
                                      con=connection_message)
        logger.info('Message store query execution completed!')
        return sql_query
    except pyodbc.Error as ex:
        logger.error(ex)


# SQL Query LCT Adapter line by line
def sql_query_adapter_Detail(start_time, finish_time, env,customer):
    resources_path = abs_path_resources()
    connection_adapter = sql_connection_adapter(env,customer)
    start_time = datetime.strptime(start_time, '%y/%m/%d %H:%M:%S.%f')
    finish_time = datetime.strptime(finish_time, '%y/%m/%d %H:%M:%S.%f')
    query = 'SELECT AUDIT_TBL.MSG_TYPE,' \
            'AUDIT_TBL.MSG_INGEST_PARAM,' \
            'AUDIT_TBL.INGEST_STATUS_MSG,' \
            'AUDIT_TBL.INGESTION_ID,' \
            'AUDIT_TBL.MSG_STATUS,' \
            'AUDIT_TBL.CREATED_DATETIME AS LCT_ADAPTER_STARTED,' \
            'AUDIT_TBL.MODIFIED_DATETIME AS LCT_ADAPTER_FINISHED,' \
            'JSON_Value(DATA_TBL.GS1_header, ?) AS MESSAGE_BROKER_BLK_ID ' \
            'FROM dbo.LCTA_INBOUND_DATA_TBL AS DATA_TBL ' \
            'JOIN dbo.LCTA_MSG_AUDIT_TBL AS AUDIT_TBL ON AUDIT_TBL.MSG_HDR_REF_ID = DATA_TBL.MSG_HDR_ID ' \
            'AND JSON_Value(GS1_header, ?) != ? WHERE DATA_TBL.CREATED_DATETIME  > ? ' \
            'AND DATA_TBL.CREATED_DATETIME <  ? ORDER BY AUDIT_TBL.MODIFIED_DATETIME ASC;'
    try:
        logger.info('Executing query... LCT Adapter DB')
        sql_query = pd.read_sql_query(query, params=(
            '$.messageId', '$.messageId', 'NULL', start_time, finish_time),
                                      con=connection_adapter)
        logger.info('LCT Adapter query execution completed!')
        sql_query['INGESTION_ID'].to_json(resources_path + '//ingestion_id.json')
        return sql_query
    except pyodbc.Error as ex:
        logger.error(ex)

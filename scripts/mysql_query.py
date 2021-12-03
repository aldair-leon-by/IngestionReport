"""
Author: Aldair Leon
Date: Dec 3rd, 2021
"""

import json
from errno import errorcode
import mysql
from scripts.db_connection import mysql_connection
import pandas as pd
from scripts.init_logger import log
from scripts.env_config import abs_path_resources

# Logger
logger = log('ENV SETUP')


# Read json file with ingestion_id that we extract from Connect
def get_ingestion_id() -> list:
    ingestion_id_list = []
    path = abs_path_resources()
    ingestion_id = open(path + '//ingestion_id.json')
    data = json.load(ingestion_id)
    for i in data:
        ingestion_id_list.append(data[i])
    return ingestion_id_list


# Query LCT DB and joind data in one Data frame
def mysql_query_computation_time(env, customer) -> pd.DataFrame:
    cnx = mysql_connection(env, customer)
    ingestion_id = get_ingestion_id()
    format_strings = ",".join(['%s'] * len(ingestion_id))
    # Run query when computation service start Status Accepting
    query_start = "SELECT ingestion_id as INGESTION_ID, min(event_time) AS COMPUTATION_STARTED " \
                  "FROM stack_db.event WHERE ingestion_id IN (%s) " \
                  "AND status IN ('ACCEPTING') " \
                  "AND service IN ('computation') " \
                  "GROUP BY ingestion_id " % format_strings

    try:
        mysql_query_start = pd.read_sql(query_start, con=cnx, params=tuple(ingestion_id))
        logger.info('Executing query COMPUTATION START... MySQL stack DB')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    # Run query when computation service finish Status COMPLETED or COMPLETED_WITH_TIMEOUT
    query_finish = "SELECT ingestion_id as INGESTION_ID, max(event_time) AS COMPUTATION_FINISHED " \
                   "FROM stack_db.event WHERE ingestion_id IN (%s) " \
                   "AND status IN ('COMPLETED','COMPLETED_WITH_TIMEOUT') " \
                   "AND service IN ('computation') " \
                   "AND performance_metrics != 'NULL' " \
                   "GROUP BY ingestion_id" % format_strings

    try:
        mysql_query_finish = pd.read_sql(query_finish, con=cnx, params=tuple(ingestion_id))
        logger.info('Executing query COMPUTATION FINISH... MySQL stack DB')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    # Run query, performance metrics
    query = "SELECT max(event_time) AS COMPUTATION_FINISHED, ingestion_id as INGESTION_ID, status AS COMPUTATION_STATUS, " \
            "json_extract(performance_metrics,'$.summary.overall.totalCpuTimeMs') AS totalCpuTimeMs, " \
            "json_extract(performance_metrics,'$.summary.overall.averageCpuTimeMs') AS averageCpuTimeMs, " \
            "json_extract(performance_metrics,'$.summary.overall.performanceStatus') AS performanceStatus, " \
            "json_extract(performance_metrics,'$.summary.overall.totalInvocationCount') AS totalInvocationCount, " \
            "json_extract(performance_metrics,'$.summary.overall.currentInvocationCount') AS currentInvocationCount, " \
            "json_extract(performance_metrics,'$.summary.overall.invocationPerObjectRatio') AS invocationPerObjectRatio, " \
            "json_extract(performance_metrics,'$.summary.overall.totalSourcingObjectCount') AS totalSourcingObjectCount, " \
            "json_extract(performance_metrics,'$.summary.overall.totalProcessedObjectCount') AS totalProcessedObjectCount, " \
            "json_extract(performance_metrics,'$.summary.Order.totalCpuTimeMs') AS ORDER_totalCpuTimeMs, " \
            "json_extract(performance_metrics,'$.summary.Order.averageCpuTimeMs') AS Order_averageCpuTimeMs, " \
            "json_extract(performance_metrics,'$.summary.Order.performanceStatus') AS Order_performanceStatus, " \
            "json_extract(performance_metrics,'$.summary.Order.totalInvocationCount') AS ORDER_totalInvocationCount, " \
            "json_extract(performance_metrics,'$.summary.Order.currentInvocationCount') AS ORDER_currentInvocationCount, " \
            "json_extract(performance_metrics,'$.summary.Order.invocationPerObjectRatio') AS ORDER_invocationPerObjectRatio, " \
            "json_extract(performance_metrics,'$.summary.Order.totalSourcingObjectCount') AS ORDER_totalSourcingObjectCount, " \
            "json_extract(performance_metrics,'$.summary.Order.totalProcessedObjectCount') AS ORDER_totalProcessedObjectCount, " \
            "json_extract(performance_metrics,'$.summary.transportation.totalCpuTimeMs') AS TRANSPORTATION_totalCpuTimeMs, " \
            "json_extract(performance_metrics,'$.summary.transportation.averageCpuTimeMs') AS TRANSPORTATION_averageCpuTimeMs, " \
            "json_extract(performance_metrics,'$.summary.transportation.performanceStatus') AS TRANSPORTATION_performanceStatus, " \
            "json_extract(performance_metrics,'$.summary.transportation.totalInvocationCount') AS TRANSPORTATION_totalInvocationCount, " \
            "json_extract(performance_metrics,'$.summary.transportation.currentInvocationCount') AS TRANSPORTATION_currentInvocationCount, " \
            "json_extract(performance_metrics,'$.summary.transportation.invocationPerObjectRatio') AS TRANSPORTATION_invocationPerObjectRatio, " \
            "json_extract(performance_metrics,'$.summary.transportation.totalSourcingObjectCount') AS TRANSPORTATION_totalSourcingObjectCount, " \
            "json_extract(performance_metrics,'$.summary.transportation.totalProcessedObjectCount') AS TRANSPORTATION_totalProcessedObjectCount, " \
            "json_extract(performance_metrics,'$.summary.\"computation-backend\".totalCpuTimeMs') AS computation_backend_totalCpuTimeMs, " \
            "json_extract(performance_metrics,'$.summary.\"computation-backend\".averageCpuTimeMs') AS computation_backend_averageCpuTimeMs, " \
            "json_extract(performance_metrics,'$.summary.\"computation-backend\".performanceStatus') AS computation_backend_performanceStatus, " \
            "json_extract(performance_metrics,'$.summary.\"computation-backend\".totalInvocationCount') AS computation_backend_totalInvocationCount, " \
            "json_extract(performance_metrics,'$.summary.\"computation-backend\".currentInvocationCount') AS computation_backend_currentInvocationCount, " \
            "json_extract(performance_metrics,'$.summary.\"computation-backend\".invocationPerObjectRatio') AS computation_backend_invocationPerObjectRatio, " \
            "json_extract(performance_metrics,'$.summary.\"computation-backend\".totalSourcingObjectCount') AS computation_backend_totalSourcingObjectCount, " \
            "json_extract(performance_metrics,'$.summary.\"computation-backend\".totalProcessedObjectCount') AS computation_backend_totalProcessedObjectCount, " \
            "json_extract(performance_metrics,'$.summary.\"computation-frontend\".totalCpuTimeMs') AS computation_frontend_totalCpuTimeMs, " \
            "json_extract(performance_metrics,'$.summary.\"computation-frontend\".averageCpuTimeMs') AS computation_frontend_averageCpuTimeMs, " \
            "json_extract(performance_metrics,'$.summary.\"computation-frontend\".performanceStatus') AS computation_frontend_performanceStatus, " \
            "json_extract(performance_metrics,'$.summary.\"computation-frontend\".totalInvocationCount') AS computation_frontend_totalInvocationCount, " \
            "json_extract(performance_metrics,'$.summary.\"computation-frontend\".currentInvocationCount') AS computation_frontend_currentInvocationCount, " \
            "json_extract(performance_metrics,'$.summary.\"computation-frontend\".invocationPerObjectRatio') AS computation_frontend_invocationPerObjectRatio, " \
            "json_extract(performance_metrics,'$.summary.\"computation-frontend\".totalSourcingObjectCount') AS computation_frontend_totalSourcingObjectCount, " \
            "json_extract(performance_metrics,'$.summary.\"computation-frontend\".totalProcessedObjectCount') AS computation_frontend_totalProcessedObjectCount " \
            "FROM stack_db.event " \
            "WHERE ingestion_id IN (%s)  and status in ('COMPLETED','COMPLETED_WITH_TIMEOUT')  " \
            "AND service in ('COMPUTATION') " \
            "AND performance_metrics != 'NULL' " \
            "group by ingestion_id,performance_metrics,status;" % format_strings
    try:
        logger.info('Executing query PERFORMANCE METRICS... MySQL stack DB')
        computation_performance = pd.read_sql(query, con=cnx, params=tuple(ingestion_id))
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    computation_time = mysql_query_start[['INGESTION_ID', 'COMPUTATION_STARTED']].merge(
        mysql_query_finish[['INGESTION_ID', 'COMPUTATION_FINISHED']],
        on="INGESTION_ID",
        how="left")
    e2eComputationDetails = computation_time[
        ['INGESTION_ID', 'COMPUTATION_STARTED', 'COMPUTATION_FINISHED']].merge(
        computation_performance,
        on=["INGESTION_ID", "COMPUTATION_FINISHED"],
        how="left")
    logger.info('JOIN DETAILS COMPUTATION METRICS REPORT !!')
    return e2eComputationDetails

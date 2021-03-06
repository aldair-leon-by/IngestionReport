"""
Author: Aldair Leon
Date: Dec 3rd, 2021
"""

import mysql.connector
import pyodbc
from mysql.connector import errorcode
from scripts.env_config import abs_data_base_credentials
from scripts.init_logger import log


# Logger
logger = log('DB CONNECTION')


# MYSQL connection STACK_DB
def mysql_connection(env, customer):
    db = abs_data_base_credentials()
    mysql_server = db[customer]['mysql_db_' + env][0]['mysql_server']
    mysql_username = db[customer]['mysql_db_' + env][0]['mysql_username']
    mysql_password = db[customer]['mysql_db_' + env][0]['mysql_password']
    mysql_db = db[customer]['mysql_db_' + env][0]['mysql_database']
    try:
        cnx = mysql.connector.connect(user=mysql_username, password=mysql_password,
                                      host=mysql_server,
                                      database=mysql_db)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        logger.info('Successfully connection MYSQL stack_db ' + env + '!')
        return cnx


# SQL connection message_store db
def sql_connection_message_storage(env, customer):
    db = abs_data_base_credentials()
    sql_server = db[customer]['sql_db_' + env][0]['sql_server']
    sql_username = db[customer]['sql_db_' + env][0]['sql_username']
    sql_password = db[customer]['sql_db_' + env][0]['sql_password']
    sql_db = db[customer]['sql_db_' + env][0]['sql_database_message_store']
    try:
        connection_message = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + sql_server + ';DATABASE=' + sql_db + ';UID=' +
            sql_username + ';PWD=' + sql_password)
        logger.info('Successfully connection SQL sql_database_message_store ' + env + '!')
        return connection_message
    except pyodbc.Error as ex:
        logger.error(ex)


# SQL connection LCT_adapter db
def sql_connection_adapter(env, customer):
    db = abs_data_base_credentials()
    sql_server = db[customer]['sql_db_' + env][0]['sql_server']
    sql_username = db[customer]['sql_db_' + env][0]['sql_username']
    sql_password = db[customer]['sql_db_' + env][0]['sql_password']
    sql_db = db[customer]['sql_db_' + env][0]['sql_database_adapter']
    try:
        connection_adapter = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + sql_server + ';DATABASE=' + sql_db + ';UID=' +
            sql_username + ';PWD=' + sql_password)
        logger.info('Successfully connection SQL sql_database_adapter ' + env + '!')
        return connection_adapter
    except pyodbc.Error as ex:
        logger.error(ex)

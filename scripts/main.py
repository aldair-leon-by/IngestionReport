from report_creation import IngestionReport
"""
Author: Aldair Leon
Date: Oct 26th, 2021
"""

# This class request of date_start and date_finish in this format YY/MM/DD HH:MM:SS.FFF and
# env "sql_db_uat or sql_db_sit"


date_start = '21/10/25 11:00:00.000'
date_finish = '21/10/25 12:00:00.000'
env = 'sql_db_prod'
report = IngestionReport(date_start, date_finish, env)
report.detail_report()
report.summary_report()

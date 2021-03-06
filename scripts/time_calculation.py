"""
Author: Aldair Leon
Date: Dec 3rd, 2021
"""

from datetime import datetime
from scripts.init_logger import log

# Logger
logger = log('TIME CALCULATIONS')


# Note: This functions are not correct, works but is not the better way. I need to check and optimize this code lol.

# Calculate line by line  complete time in every service, and  complete time of ingestion.
def ave_time_execution(e2eIngestionComputation):
    total_time = []
    for i in range(len(e2eIngestionComputation)):
        try:
            adapter = datetime.strptime(str(e2eIngestionComputation.iloc[i, 7]), '%Y-%m-%d %H:%M:%S.%f').strftime(
                '%H:%M:%S.%f')
            computation = datetime.strptime(str(e2eIngestionComputation.iloc[i, 11]),
                                            '%Y-%m-%d %H:%M:%S.%f').strftime(
                '%H:%M:%S.%f')
        except ValueError:
            pass
        try:
            adapter = datetime.strptime(str(e2eIngestionComputation.iloc[i, 7]), '%Y-%m-%d %H:%M:%S').strftime(
                '%H:%M:%S.%f')
            computation = datetime.strptime(str(e2eIngestionComputation.iloc[i, 11]),
                                            '%Y-%m-%d %H:%M:%S').strftime(
                '%H:%M:%S.%f')
        except ValueError:
            pass
        if adapter > computation:
            timeDiff = e2eIngestionComputation.iloc[i, 8] - e2eIngestionComputation.iloc[i, 3]
            td = str(timeDiff).split(' ')[-1:][0]
            try:
                timeDiff_calculation = datetime.strptime(str(td), '%H:%M:%S.%f').strftime(
                    '%H:%M:%S.%f')
            except ValueError:
                pass
            try:
                timeDiff_calculation = datetime.strptime(str(td), '%H:%M:%S').strftime(
                    '%H:%M:%S.%f')
            except ValueError:
                pass
            ftr = [3600, 60, 1]
            u = sum([a * b for a, b in zip(ftr, map(float, timeDiff_calculation.split(':')))])
            u = round(u, 2)
            total_time.append(u)
        else:
            timeDiff = e2eIngestionComputation.iloc[i, 11] - e2eIngestionComputation.iloc[i, 3]
            td = str(timeDiff).split(' ')[-1:][0]
            try:
                timeDiff_calculation = datetime.strptime(str(td), '%H:%M:%S.%f').strftime(
                    '%H:%M:%S.%f')
            except ValueError:
                pass
            try:
                timeDiff_calculation = datetime.strptime(str(td), '%H:%M:%S').strftime(
                    '%H:%M:%S.%f')
            except ValueError:
                pass
            ftr = [3600, 60, 1]
            u = sum([a * b for a, b in zip(ftr, map(float, timeDiff_calculation.split(':')))])
            u = round(u, 2)
            total_time.append(u)
    e2eIngestionComputation.insert(14, 'TOTAL TIME INGESTION', total_time)  # e2eIngestion
    total_time.clear()
    for i in range(len(e2eIngestionComputation)):
        timeDiff = e2eIngestionComputation.iloc[i, 3] - e2eIngestionComputation.iloc[i, 2]
        td = str(timeDiff).split(' ')[-1:][0]
        try:
            timeDiff_calculation = datetime.strptime(str(td), '%H:%M:%S.%f').strftime(
                '%H:%M:%S.%f')
        except ValueError:
            pass
        try:
            timeDiff_calculation = datetime.strptime(str(td), '%H:%M:%S').strftime(
                '%H:%M:%S.%f')
        except ValueError:
            pass
        ftr = [3600, 60, 1]
        u = sum([a * b for a, b in zip(ftr, map(float, timeDiff_calculation.split(':')))])
        u = round(u, 2)
        total_time.append(u)
    e2eIngestionComputation.insert(15, 'INGESTION SERVICE TOTAL TIME', total_time)  # Ingestion service
    total_time.clear()
    for i in range(len(e2eIngestionComputation)):
        timeDiff = e2eIngestionComputation.iloc[i, 5] - e2eIngestionComputation.iloc[i, 4]
        td = str(timeDiff).split(' ')[-1:][0]
        try:
            timeDiff_calculation = datetime.strptime(str(td), '%H:%M:%S.%f').strftime(
                '%H:%M:%S.%f')
        except ValueError:
            pass
        try:
            timeDiff_calculation = datetime.strptime(str(td), '%H:%M:%S').strftime(
                '%H:%M:%S.%f')
        except ValueError:
            pass
        ftr = [3600, 60, 1]
        u = sum([a * b for a, b in zip(ftr, map(float, timeDiff_calculation.split(':')))])
        u = round(u, 2)
        total_time.append(u)
    e2eIngestionComputation.insert(16, 'MESSAGE BROKER TOTAL TIME', total_time)  # Message broker
    total_time.clear()
    for i in range(len(e2eIngestionComputation)):
        timeDiff = e2eIngestionComputation.iloc[i, 7] - e2eIngestionComputation.iloc[i, 6]
        td = str(timeDiff).split(' ')[-1:][0]
        try:
            timeDiff_calculation = datetime.strptime(str(td), '%H:%M:%S.%f').strftime(
                '%H:%M:%S.%f')
        except ValueError:
            pass
        try:
            timeDiff_calculation = datetime.strptime(str(td), '%H:%M:%S').strftime(
                '%H:%M:%S.%f')
        except ValueError:
            pass
        ftr = [3600, 60, 1]
        u = sum([a * b for a, b in zip(ftr, map(float, timeDiff_calculation.split(':')))])
        u = round(u, 2)
        total_time.append(u)
    e2eIngestionComputation.insert(17, 'LCT ADAPTER TOTAL TIME', total_time)  # LCT Adapter
    total_time.clear()
    for i in range(len(e2eIngestionComputation)):
        timeDiff = e2eIngestionComputation.iloc[i, 11] - e2eIngestionComputation.iloc[i, 10]
        td = str(timeDiff).split(' ')[-1:][0]
        try:
            timeDiff_calculation = datetime.strptime(str(td), '%H:%M:%S.%f').strftime(
                '%H:%M:%S.%f')
        except ValueError:
            pass
        try:
            timeDiff_calculation = datetime.strptime(str(td), '%H:%M:%S').strftime(
                '%H:%M:%S.%f')
        except ValueError:
            pass
        ftr = [3600, 60, 1]
        u = sum([a * b for a, b in zip(ftr, map(float, timeDiff_calculation.split(':')))])
        u = round(u, 2)
        total_time.append(u)
    e2eIngestionComputation.insert(18, 'COMPUTATION TOTAL TIME', total_time)  # Computation service
    logger.info('CALCULATION TIME FINISHED !')
    return e2eIngestionComputation


# Format time values
def format_time_dashboard(time):
    td = str(time).split(' ')[-1:][0]
    try:
        timeDiff = datetime.strptime(str(td), '%H:%M:%S.%f').strftime('%H:%M:%S.%f')
    except ValueError:
        pass
    try:
        timeDiff = datetime.strptime(str(td), '%H:%M:%S').strftime('%H:%M:%S.%f')
    except ValueError:
        pass
    ftr = [3600, 60, 1]
    u = sum([a * b for a, b in zip(ftr, map(float, timeDiff.split(':')))])
    u = round(u, 2)
    return u

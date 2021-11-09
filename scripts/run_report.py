import datetime

import streamlit as st
from scripts.report_creation import IngestionReport

"""
Author: Aldair Leon
Date: Oct 26th, 2021
"""


def app():
    st.title('Run Report')
    env = st.selectbox('Select environment', ('Choose env', 'sql_db_uat', 'sql_db_prod'))
    col1, col2 = st.columns(2)
    with col1:
        date_start = st.date_input("Date Start", datetime.date(2021, 1, 1))
        time_start = st.text_input('Time Start HH:MM:SS.fff', '00:00:00.000')
    with col2:
        date_finish = st.date_input("Date Finish", datetime.date(2021, 1, 1), key=1)
        time_finish = st.text_input('Time Finish HH:MM:SS.fff', '00:00:00.000', key=2)

    if st.button('Run Report'):
        if env == 'Choose env':
            st.warning('Please select environment!')
        else:
            date_time_start = date_start.strftime("%y/%m/%d" + " " + time_start)
            date_time_finish = date_finish.strftime("%y/%m/%d" + " " + time_finish)
            report = IngestionReport(date_time_start, date_time_finish, env)
            with st.spinner('Running...'):
                path = report.ingestion_report()
            st.success('Done!')
            st.success('File download in this location: ')
            st.success(path)
            return path

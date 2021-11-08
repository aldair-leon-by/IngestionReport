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
        date_start = st.date_input("Select Date Start")
        time_start = st.time_input('Select Time start')
    with col2:
        date_finish = st.date_input("Select Date Finish", key=1)
        time_finish = st.time_input('Select Time finish', key=1)

    if st.button('Run Report'):
        if env == 'Choose env':
            st.warning('Please select environment!')
        else:
            date_time_start = date_start.strftime("%y/%m/%d" + " " + time_start.strftime("%I:%M:%S.%f")[:-3])
            date_time_finish = date_finish.strftime("%y/%m/%d" + " " + time_finish.strftime("%I:%M:%S.%f")[:-3])
            report = IngestionReport(date_time_start, date_time_finish, env)
            with st.spinner('Running...'):
                path = report.ingestion_report()
            st.success('Done!')
            st.success('File download in this location: ')
            st.success(path)
            return path

from io import StringIO

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go


def format_time(time):
    td = str(time).split(' ')[-1:][0]
    try:
        timeDiff2 = datetime.strptime(str(td), '%H:%M:%S.%f').strftime('%H:%M:%S.%f')
    except ValueError:
        pass
    try:
        timeDiff2 = datetime.strptime(str(td), '%H:%M:%S').strftime('%H:%M:%S.%f')

    except ValueError:
        pass
    ftr = [3600, 60, 1]
    u = sum([a * b for a, b in zip(ftr, map(float, timeDiff2.split(':')))])
    u = round(u, 2)
    return u


class DashboardIngestion:

    def __init__(self, data):
        self.data = data

    def dash_board_top(self):
        self.detail_report = pd.read_excel(self.data, sheet_name='DetailReport')
        self.summary_report = pd.read_excel(self.data, sheet_name='SummaryReport')
        with st.container():  # Container Header
            st.title(":bar_chart: Ingestion Report")
            st.markdown("###")
        with st.container():  # Container Ingestion interval
            col1, col2 = st.columns(2)
            with col1:
                time_start = self.detail_report['INGESTION SERVICE MESSAGE STARTED'].sort_values()
                option = st.selectbox('Ingestion Start', time_start)
            with col2:
                time_finish = self.detail_report['COMPUTATION FINISHED'].sort_values(ascending=False)
                option2 = st.selectbox('Ingestion Finish', time_finish)
            st.write('Ingestion time:', option, 'To ', option2)
        with st.container():  # Container Filters
            st.sidebar.header(":mag: Please Filter Here")
            st.sidebar.subheader("Service parameters")
            type_of_message = st.sidebar.multiselect(
                "Select type of Message:",
                options=self.detail_report["TYPE OF MESSAGE"].unique(),
                default=self.detail_report["TYPE OF MESSAGE"].unique()
            )

            message_status = st.sidebar.multiselect(
                "Select Message Status:",
                options=self.detail_report["MSG STATUS"].unique(),
                default=self.detail_report["MSG STATUS"].unique()
            )
            computation_status = st.sidebar.multiselect(
                "Select Computation Status:",
                options=self.detail_report["COMPUTATION STATUS"].unique(),
                default=self.detail_report["COMPUTATION STATUS"].unique()
            )
            ingestion_status = st.sidebar.multiselect(
                "Select Ingestion Status:",
                options=self.detail_report["CRNT STATUS"].unique(),
                default=self.detail_report["CRNT STATUS"].unique()
            )

            self.df_selection = self.detail_report.query(
                "`TYPE OF MESSAGE` == @type_of_message & `MSG STATUS` == @message_status "
                "& `INGESTION SERVICE MESSAGE STARTED` >= @option & `COMPUTATION FINISHED` <= @option2 "
                "& `COMPUTATION STATUS` == @computation_status & `CRNT STATUS` == @ingestion_status  "

            )

        with st.container():
            total_count_object = self.df_selection['TOTAL COUNT OBJECT'].sum()
            if total_count_object > 0:

                total_time_ingestion = max(self.df_selection['COMPUTATION FINISHED']) - \
                                       min(self.df_selection['INGESTION SERVICE MESSAGE STARTED'])

                total_time_ingestion = format_time(total_time_ingestion)

                total_of_messages = sum(self.summary_report['TOTAL OF MESSAGE'])
                total_of_objects = sum(self.summary_report['TOTAL OBJECT COUNT'])

                min_time_ingestion = min(self.df_selection['TOTAL TIME INGESTION(sec)'])
                max_time_ingestion = max(self.df_selection['TOTAL TIME INGESTION(sec)'])

                col1, col2, col3 = st.columns(3)
                count_ingest_total = go.Figure(go.Indicator(
                    domain={'x': [0, 1], 'y': [0, 1]},
                    value=len(self.df_selection),
                    mode="gauge+number",
                    title={'text': "Total of messages"},
                    gauge={'axis': {'range': [None, total_of_messages]},
                           'steps': [
                               {'range': [0, total_of_messages / 2], 'color': "lightgray"},
                               {'range': [total_of_messages + 1 / 2, total_of_messages], 'color': "gray"}],
                           'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75,
                                         'value': total_of_messages + 1}
                           }))
                count_total_objects = go.Figure(go.Indicator(
                    domain={'x': [0, 1], 'y': [0, 1]},
                    value=total_count_object,
                    mode="gauge+number",
                    title={'text': "Total count objects"},
                    gauge={'axis': {'range': [None, total_of_objects]},
                           'steps': [
                               {'range': [0, total_of_objects / 2], 'color': "lightgray"},
                               {'range': [total_of_objects + 1 / 2, total_of_objects], 'color': "gray"}],
                           'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75,
                                         'value': total_of_objects}
                           }))

                col1.plotly_chart(count_ingest_total, use_container_width=True)
                col2.plotly_chart(count_total_objects, use_container_width=True)
                col3.metric(label="e2e Total time Ingestion", value=str(total_time_ingestion) + " sec")
                col3.metric(label="min Total time Ingestion", value=str(min_time_ingestion) + " sec")
                col3.metric(label="max Total time Ingestion", value=str(max_time_ingestion) + " sec")
            else:
                st.warning('No data to display..')

    def dash_board_service(self):
        with st.container():  # Container Services Report
            st.subheader(":chart_with_downwards_trend: Services")
            st.markdown("###")
            if len(self.df_selection) > 0:
                total_ingest_service = max(self.df_selection['INGESTION SERVICE MESSAGE FINISHED']) - min(
                    self.df_selection['INGESTION SERVICE MESSAGE STARTED'])
                timeDiff_calculation_ingestion_service = format_time(total_ingest_service)
                execution_time_total_ingestion_service = round(self.df_selection['INGESTION SERVICE TOTAL TIME'].sum(),
                                                               2)
                average_total_ingestion_service = round(self.df_selection['INGESTION SERVICE TOTAL TIME'].mean(), 2)
                max_time_ingestion_service = self.df_selection['INGESTION SERVICE TOTAL TIME'].max()
                min_time_ingestion_service = self.df_selection['INGESTION SERVICE TOTAL TIME'].min()

                total_message_broker = max(self.df_selection["MESSAGE BROKER FINISHED"]) - min(
                    self.df_selection["MESSAGE BROKER STARTED"])
                timeDiff_calculation_message_broker_service = format_time(total_message_broker)
                execution_time_total_message_broker_service = round(
                    self.df_selection['MESSAGE BROKER TOTAL TIME'].sum(), 2)
                average_total_message_broker = round(self.df_selection['MESSAGE BROKER TOTAL TIME'].mean(), 2)
                max_time_message_broker_service = self.df_selection['MESSAGE BROKER TOTAL TIME'].max()
                min_time_message_broker_service = self.df_selection['MESSAGE BROKER TOTAL TIME'].min()

                total_lct_adapter = max(self.df_selection['LCT ADAPTER FINISHED']) - min(
                    self.df_selection['LCT ADAPTER STARTED'])
                timeDiff_calculation_lct_adapter_service = format_time(total_lct_adapter)
                execution_time_total_lct_adapter_service = round(self.df_selection['LCT ADAPTER TOTAL TIME'].sum(), 2)
                average_total_lct_adapter = round(self.df_selection['LCT ADAPTER TOTAL TIME'].mean(), 2)
                max_time_lct_adapter_service = self.df_selection['LCT ADAPTER TOTAL TIME'].max()
                min_time_lct_adapter_service = self.df_selection['LCT ADAPTER TOTAL TIME'].min()

                total_computation = max(self.df_selection['COMPUTATION FINISHED']) - min(
                    self.df_selection['COMPUTATION STARTED'])
                timeDiff_calculation_time_computation_service = format_time(total_computation)
                execution_time_total_computation_service = round(self.df_selection['COMPUTATION TOTAL TIME'].sum(), 2)
                average_total_computation_service = round(self.df_selection['COMPUTATION TOTAL TIME'].mean(), 2)
                max_time_lct_computation_service = self.df_selection['COMPUTATION TOTAL TIME'].max()
                min_time_lct_computation_service = self.df_selection['COMPUTATION TOTAL TIME'].min()

                total_ingestion_time = max(self.df_selection["COMPUTATION FINISHED"]) - min(
                    self.df_selection["INGESTION SERVICE MESSAGE STARTED"])
                timeDiff_calculation_total_ingestion = format_time(total_ingestion_time)
                execution_time_total_ingestion = round(execution_time_total_ingestion_service + \
                                                       execution_time_total_message_broker_service + \
                                                       execution_time_total_lct_adapter_service + \
                                                       execution_time_total_computation_service, 2)
                average_total_ingestion = round(self.df_selection['TOTAL TIME INGESTION(sec)'].mean(), 2)
                max_total_ingestion = self.df_selection['TOTAL TIME INGESTION(sec)'].max()
                min_total_ingestion = self.df_selection['TOTAL TIME INGESTION(sec)'].min()

                left_column, middle_column, middle_column2, right_column, right_column2 = st.columns(5)
                with left_column:
                    st.markdown('#### Ingestion Service')
                    st.text(f"Elapsed Time: {timeDiff_calculation_ingestion_service} sec")
                    st.text(f"Execution Time: {execution_time_total_ingestion_service} sec")
                    st.text(f"Average Time: {average_total_ingestion_service} sec")
                    st.text(f"Max Time: {max_time_ingestion_service} sec")
                    st.text(f"Min Time: {min_time_ingestion_service} sec")
                with middle_column:
                    st.markdown('#### Message Broker')
                    st.text(f"Elapsed Time: {timeDiff_calculation_message_broker_service} sec")
                    st.text(f"Execution Time: {execution_time_total_message_broker_service} sec")
                    st.text(f"Average Time: {average_total_message_broker} sec")
                    st.text(f"Max Time: {max_time_message_broker_service} sec")
                    st.text(f"Min Time: {min_time_message_broker_service} sec")
                with middle_column2:
                    st.markdown('#### LCT Adapter')
                    st.text(f"Elapsed Time: {timeDiff_calculation_lct_adapter_service} sec")
                    st.text(f"Execution Time: {execution_time_total_lct_adapter_service} sec")
                    st.text(f"Average Time: {average_total_lct_adapter} sec")
                    st.text(f"Max Time: {max_time_lct_adapter_service} sec")
                    st.text(f"Min Time: {min_time_lct_adapter_service} sec")
                with right_column:
                    st.markdown('#### Computation')
                    st.text(f"Elapsed Time: {timeDiff_calculation_time_computation_service} sec")
                    st.text(f"Execution Time: {execution_time_total_computation_service} sec")
                    st.text(f"Average Time: {average_total_computation_service} sec")
                    st.text(f"Max Time: {max_time_lct_computation_service} sec")
                    st.text(f"Min Time: {min_time_lct_computation_service} sec")
                with right_column2:
                    st.markdown('#### Total Ingestion')
                    st.text(f"Elapsed Time: {timeDiff_calculation_total_ingestion} sec")
                    st.text(f"Execution Time: {execution_time_total_ingestion} sec")
                    st.text(f"Average Time: {average_total_ingestion} sec")
                    st.text(f"Max Time: {max_total_ingestion} sec")
                    st.text(f"Min Time: {min_total_ingestion} sec")
                with st.expander('Services Charts'):
                    header = ['Ingest Service', 'Message Broker', 'LCT Adapter', 'Computation']
                    time_elapsed = [timeDiff_calculation_ingestion_service, timeDiff_calculation_message_broker_service,
                                    timeDiff_calculation_lct_adapter_service,
                                    timeDiff_calculation_time_computation_service]
                    time_average = [average_total_ingestion_service, average_total_message_broker,
                                    average_total_lct_adapter, average_total_computation_service]

                    df_chart = pd.DataFrame(list(zip(header, time_elapsed, time_average)),
                                            columns=['Service', 'Time (sec)', 'Average Time (sec)'])
                    header_df = list(df_chart['Service'])
                    data_elapsed_time = list(df_chart['Time (sec)'])
                    data_average_time = list(df_chart['Average Time (sec)'])

                    services_chart = px.bar(df_chart,
                                            x='Service',
                                            y='Time (sec)',
                                            title="<b>Service Elapsed Time (sec)</b>",
                                            color_discrete_sequence=["#0083B8"] * len(df_chart),
                                            template="plotly_white",
                                            )
                    services_chart.update_layout(
                        xaxis=dict(tickmode="linear"),
                        plot_bgcolor="rgba(0,0,0,0)",
                        yaxis=(dict(showgrid=False)), )

                    service_chart_pay = go.Figure(data=[go.Pie(labels=header_df, values=data_elapsed_time)])
                    service_chart_pay.update_layout(title='<b>Service Elapsed Time (%)</b>')

                    service_chart_line = go.Figure(data=go.Scatter(x=header_df, y=data_average_time))
                    service_chart_line.update_layout(title='<b>Average Time (sec)</b>',
                                                     xaxis_title='<b>Service</b>',
                                                     yaxis_title='<b>Average Time (sec)</b>',
                                                     plot_bgcolor="rgba(0,0,0,0)", yaxis=(dict(showgrid=False)),
                                                     xaxis=(dict(showgrid=True)), )

                    left_column, center_column, right_column = st.columns(3)
                    left_column.plotly_chart(services_chart, use_container_width=True)
                    center_column.plotly_chart(service_chart_pay, use_container_width=True)
                    right_column.plotly_chart(service_chart_line, use_container_width=True)
            else:
                st.warning('No data to display..')

    def dash_boar_message_type(self):
        with st.container():
            st.subheader(":chart_with_downwards_trend: Message Type")
            st.markdown("###")
            if len(self.df_selection) > 0:
                summary = self.df_selection.groupby(
                    ['TYPE OF MESSAGE', 'MSG STATUS', 'COMPUTATION STATUS']) \
                    .agg({'TOTAL TIME INGESTION(sec)': ['mean', 'max', 'min'],
                          'TOTAL COUNT OBJECT': 'sum',
                          'COMPUTATION STATUS': [('count', 'count')],
                          'INGESTION SERVICE MESSAGE STARTED': 'min',
                          'INGESTION SERVICE MESSAGE FINISHED': 'max',
                          'MESSAGE BROKER STARTED': 'min',
                          'MESSAGE BROKER FINISHED': 'max',
                          'LCT ADAPTER STARTED': 'min',
                          'LCT ADAPTER FINISHED': 'max',
                          'COMPUTATION STARTED': 'min',
                          'COMPUTATION FINISHED': 'max'}).reset_index().round(3)
                message_type_ = list(summary['TYPE OF MESSAGE'])
                message_type = st.columns(len(message_type_))
                elapsed_time_pay_chart = []
                total_messages = []
                total_object = []
                average_time = []
                for i in range(0, len(message_type)):
                    with message_type[i]:
                        st.markdown(f'##### {message_type_[i]}')
                        x = summary['COMPUTATION STATUS'].values[i][0]
                        st.text(f'Status: {x}')

                        x = summary['TOTAL COUNT OBJECT'].values[i][0]
                        st.text(f'Total count objects: {x}')
                        total_object.append(x)

                        x = summary['TOTAL TIME INGESTION(sec)'].values[i][0]
                        max_time = summary['TOTAL TIME INGESTION(sec)'].values[i][1]
                        min_time = summary['TOTAL TIME INGESTION(sec)'].values[i][2]
                        average_time.append(x)
                        st.text(f'Average time ingestion: {x} sec')
                        st.text(f'Max Time: {max_time} sec')
                        st.text(f'Min Time: {min_time} sec')

                        x = summary['COMPUTATION STATUS'].values[i][1]
                        st.text(f'Total of messages: {x}')
                        total_messages.append(x)

                        time = np.datetime64(summary['COMPUTATION FINISHED'].values[i][0]) - \
                               np.datetime64(summary['INGESTION SERVICE MESSAGE STARTED'].values[i][0])
                        seconds = time / np.timedelta64(1, 's')
                        st.text(f' Elapsed time ingestion: {seconds} sec')
                        elapsed_time_pay_chart.append(seconds)

                with st.expander('Message Type Charts'):
                    total_message_chart = go.Figure(
                        data=[go.Bar(y=total_messages, x=message_type_)],
                        layout_title_text="A Figure Displayed with fig.show()")
                    total_message_chart.update_layout(title='<b>Total of Messages</b>', yaxis=(dict(showgrid=False)),
                                                      xaxis_title='<b>Service</b>',
                                                      yaxis_title='<b>Count messages</b>',
                                                      plot_bgcolor="rgba(0,0,0,0)",
                                                      )

                    total_object_chart = go.Figure(
                        data=[go.Bar(y=total_object, x=message_type_)],
                        layout_title_text="A Figure Displayed with fig.show()")
                    total_object_chart.update_layout(title='<b>Total object count</b>', yaxis=(dict(showgrid=False)),
                                                     xaxis_title='<b>Service</b>',
                                                     yaxis_title='<b>Count objects</b>',
                                                     plot_bgcolor="rgba(0,0,0,0)",

                                                     )

                    message_type_chart_pay = go.Figure(
                        data=[go.Pie(labels=message_type_, values=elapsed_time_pay_chart)])
                    message_type_chart_pay.update_layout(title='<b>Message Type Elapsed Time (%)</b>')

                    average_chart_line = go.Figure(data=go.Scatter(x=message_type_, y=average_time))
                    average_chart_line.update_layout(title='<b>Average Time (sec)</b>',
                                                     xaxis_title='<b>Service</b>',
                                                     yaxis_title='<b>Average Time (sec)</b>',
                                                     plot_bgcolor="rgba(0,0,0,0)", yaxis=(dict(showgrid=False)),
                                                     xaxis=(dict(showgrid=True)), )

                    col1, col2, col3, col4 = st.columns(4)
                    col1.plotly_chart(message_type_chart_pay, use_container_width=True)
                    col2.plotly_chart(total_message_chart, use_container_width=True)
                    col3.plotly_chart(total_object_chart, use_container_width=True)
                    col4.plotly_chart(average_chart_line, use_container_width=True)
            else:
                st.warning('No data to display..')


def app():
    st.title('View Report')
    uploaded_file = st.file_uploader("Select report")
    if uploaded_file is not None:
        view_report = DashboardIngestion(uploaded_file)
        view_report.dash_board_top()
        view_report.dash_board_service()
        view_report.dash_boar_message_type()

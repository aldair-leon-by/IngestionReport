import streamlit as st
from multiapp import MultiApp
from scripts import view_report, run_report

st.set_page_config(page_title="Ingestion Report",
                   page_icon=":bar_chart:", layout="wide")
app = MultiApp()

st.markdown("""
# Ingestion Report Generator
""")

app.add_app("Run Report", run_report.app)
app.add_app("View Report", view_report.app)

# The main app
app.run()

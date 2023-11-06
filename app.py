from datetime import datetime
from datetime import timedelta
from typing import List
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from lib.logger import logger
from scripts.system import BareSystem, PvSystem, RawFullSystem, SmartSystem


@st.cache_data
def interactive_plot(df: pd.DataFrame):
    x_value = df.pop("Date")
    fig = make_subplots(rows=len(df.columns), cols=1)
    for idx, y_col in enumerate(df.columns):
        fig.add_trace(go.Scatter(x=x_value, y=df[y_col], name=y_col), row=idx + 1, col=1)
    fig.update_layout(title="System", autosize=False, width=2000, height=1350)
    st.plotly_chart(fig, use_container_width=True)


def plot_total(df_list: List[pd.DataFrame]):
    x_value = list(df_list[0]["Date"])
    y_values = [list(val["Total price [zl]"]) for val in df_list]
    columns = ["Date", "Bare", "Pv", "Raw", "Smart"]
    chart_data = pd.DataFrame({k: v for k, v in zip(columns, [x_value]+y_values)})
    print(chart_data)
    st.line_chart(chart_data, x="Date", y=columns[1:])


st.set_page_config(page_title="RES", page_icon=":bar_chart:")
st.title("Energy Management System")

with st.form("my_form"):
    date_start = datetime.strptime("04.09.2020 05:00:00", "%d.%m.%Y %H:%M:%S")
    date_end = datetime.strptime("04.09.2020 12:00:00", "%d.%m.%Y %H:%M:%S")
    date_earliest = datetime.strptime("01.09.2020 05:00:00", "%d.%m.%Y %H:%M:%S")
    date_oldest = datetime.strptime("10.09.2020 12:00:00", "%d.%m.%Y %H:%M:%S")
    date_start, date_end = st.slider("Date range",
                                     min_value=date_earliest,
                                     max_value=date_oldest,
                                     value=[date_start, date_end])
    energy_bank_capacity = st.number_input("Energy bank max lvl:", min_value=0.0, max_value=5.0, value=3.0)
    day_algorithm_choice = st.selectbox("Chose a day algorithm", ("full_bank", "interval"))
    with st.expander("Info about day algorithms"):
        st.markdown("""##### *full_bank* \n\n _The priority of this algorithm is to ensure the maximum energy bank level
                    during the day. If consumption exceeds production, and there's a need to source additional energy, 
                    the system will prefer to purchase it. It will only use the energy bank when it is certain that it 
                    will be fully charged by the end of the day.This algorithm works best when prices fluctuate 
                    unpredictably._""")
        st.markdown("""##### *interval* \n\n _The goal of the algorithm is to utilize the time between the appearance of 
                    energy prices for a new day and sunset (the moment when photovoltaic production stops). During this 
                    period, system calculates the optimal plan for using energy from the energy bank until the next 
                    morning. This algorithm is particularly effective during the summer when sunset occurs later._""")

    submitted = st.form_submit_button("Run!")
    if submitted:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Bare", "pv", "full_raw", "smart", "summary"])
        bare_system = BareSystem()
        pv_system = PvSystem()
        raw_full_system = RawFullSystem(energy_bank_capacity=energy_bank_capacity)
        smart_system = SmartSystem(energy_bank_capacity=energy_bank_capacity)
        for current_date in pd.date_range(start=date_start, end=date_end, freq=timedelta(hours=1)):
            logger.info(f"CURRENT DATE: {current_date}")
            bare_system.feed_consumption(current_date)
            pv_system.feed_consumption(current_date)
            raw_full_system.feed_consumption(current_date)
            smart_system.feed_consumption(current_date)

with st.container():
    try:
        systems = [bare_system, pv_system, raw_full_system, smart_system]
        tabs = [tab1, tab2, tab3, tab4]
        for system, tab in zip(systems, tabs):
            with tab:
                st.write(f"TOTAL: {system.summed_cost:.2}")
                df_to_plot = system.plotter.df
                interactive_plot(df_to_plot)
        with tab5:
            st.write(f"Summary of total costs")
            dfs_to_plot = [s.plotter.df for s in systems]
            plot_total(dfs_to_plot)
    except:
        st.info('Click "Run!" button to run the system!')
        st.stop()

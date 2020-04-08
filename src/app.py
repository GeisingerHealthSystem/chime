"""App."""

import altair as alt  # type: ignore
import streamlit as st  # type: ignore
import pandas as pd
import xlwt,xlsxwriter
import io
from penn_chime.presentation import (
    display_download_link,
    display_header,
    display_more_info,
    display_sidebar,
    hide_menu_style,
    write_definitions,
    write_footer,
    getParamFromFile,
    display_batch_download_link,
    display_sample_download_link
)
from penn_chime.settings import get_defaults
from penn_chime.models import SimSirModel
from penn_chime.charts import (
    build_admits_chart,
    build_census_chart,
    build_descriptions,
    build_sim_sir_w_date_chart,
    build_table,
)

# This is somewhat dangerous:
# Hide the main menu with "Rerun", "run on Save", "clear cache", and "record a screencast"
# This should not be hidden in prod, but removed
# In dev, this should be shown
st.markdown(hide_menu_style, unsafe_allow_html=True)

d = get_defaults()
p = display_sidebar(st, d)
m = SimSirModel(p)

display_header(st, m, p)

#Upload file
uploaded_file = st.file_uploader("Choose a XLSX file", type="xlsx")
if uploaded_file:
    result=[]
    df=pd.read_excel(uploaded_file)
    excel_filename=f"{p.current_date}_projected_census.xlsx"
    xlsx_io = io.BytesIO()
    writer = pd.ExcelWriter(xlsx_io, engine='xlsxwriter')
    # book = xlwt.Workbook()
    # excelWriter = pd.ExcelWriter(excel_filename)
    for index, row in df.iterrows():
        batch_param=getParamFromFile(row,d)
        batch_model=SimSirModel(batch_param)
        file_name_hosp=row["HOSPITAL_NAME"]
        scenario=row["SCENARIO_LABEL"]
        sheet_name=f"{file_name_hosp}_{scenario}_projected_admits"
        modified_census_df = batch_model.census_df
        modified_census_df["non-icu"] = batch_model.census_df.hospitalized - batch_model.census_df.icu
        modified_census_df.to_excel(excel_writer=writer,sheet_name=sheet_name)
        writer.save()
    display_batch_download_link(
        st,
        filenameStr=excel_filename,
        xlsx_io=xlsx_io,
        )
else:
    if st.checkbox("Show more info about this tool"):
        notes = "The total size of the susceptible population will be the entire catchment area for our hospitals."
        display_more_info(st=st, model=m, parameters=p, defaults=d, notes=notes)
    # st.subheader("New Admissions")
    # st.markdown("Projected number of **daily** COVID-19 admissions. \n\n _NOTE: Now including estimates of prior admissions for comparison._")
    # admits_chart = build_admits_chart(alt=alt, admits_floor_df=m.admits_floor_df, max_y_axis=p.max_y_axis)
    # st.altair_chart(admits_chart, use_container_width=True)
    # st.markdown(build_descriptions(chart=admits_chart, labels=p.labels, suffix=" Admissions"))
    # display_download_link(
    #     st,
    #     filename=f"{p.current_date}_projected_admits.csv",
    #     df=m.admits_df,
    # )
    # if st.checkbox("Show Projected Admissions in tabular form"):
    #     admits_modulo = 1
    #     if not st.checkbox("Show Daily Counts"):
    #         admits_modulo = 7
    #     table_df = build_table(
    #         df=m.admits_floor_df,
    #         labels=p.labels,
    #         modulo=admits_modulo)
    #     st.table(table_df)
    # st.subheader("Admitted Patients (Census)")
    # st.markdown("Projected **census** of COVID-19 patients, accounting for arrivals and discharges \n\n _NOTE: Now including estimates of prior census for comparison._")
    # census_chart = build_census_chart(alt=alt, census_floor_df=m.census_floor_df, max_y_axis=p.max_y_axis)
    # st.altair_chart(census_chart, use_container_width=True)
    # st.markdown(build_descriptions(chart=census_chart, labels=p.labels, suffix=" Census"))
    # display_download_link(
    #     st,
    #     filename=f"{p.current_date}_projected_census.csv",
    #     df=m.census_df,
    # )
    # if st.checkbox("Show Projected Census in tabular form"):
    #     census_modulo = 1
    #     if not st.checkbox("Show Daily Census Counts"):
    #         census_modulo = 7
    #     table_df = build_table(
    #         df=m.census_floor_df,
    #         labels=p.labels,
    #         modulo=census_modulo)
    #     st.table(table_df)
    # st.subheader("Susceptible, Infected, and Recovered")
    # st.markdown("The number of susceptible, infected, and recovered individuals in the hospital catchment region at any given moment")
    # sim_sir_w_date_chart = build_sim_sir_w_date_chart(alt=alt, sim_sir_w_date_floor_df=m.sim_sir_w_date_floor_df)
    # st.altair_chart(sim_sir_w_date_chart, use_container_width=True)
    # display_download_link(
    #     st,
    #     filename=f"{p.current_date}_sim_sir_w_date.csv",
    #     df=m.sim_sir_w_date_df,
    # )
    # if st.checkbox("Show SIR Simulation in tabular form"):
    #     table_df = build_table(
    #         df=m.sim_sir_w_date_floor_df,
    #         labels=p.labels)
    #     st.table(table_df)

display_sample_download_link(st)
write_definitions(st)
write_footer(st)

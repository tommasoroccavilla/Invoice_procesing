import streamlit as st
import pandas as pd

COLUMNS = [
    "file_name",
    "invoice_number",
    "invoice_date",
    "issuer_name",
    "issuer_office",
    "receiver_name",
    "receiver_office",
    "line_items",
    "line_item_amounts",
    "vat",
    "total_amount",
    "due_date",
    "period_start",
    "period_end",
    "custom_field_1",
    "custom_field_2",
]

csv_path = "app/data/annotated_data/csvs/extracted_data.csv"


def csv_creation(columns, csv_path):
    empty_csv = pd.DataFrame(columns=columns)
    empty_csv.to_csv(csv_path)


def reading_csv():
    st.session_state.past_data_csv = pd.read_csv(csv_path)
    columns = st.session_state.past_data_csv.columns.to_list()
    columns.remove("file_name")
    for col in columns:
        if col.startswith("Unnamed"):
            columns.remove(col)
    return st.session_state.past_data_csv, columns


def is_file_uploaded_already(file_name: str):
    try:
        df = reading_csv(csv_path)
        return df["file_name"].eq(file_name).any()
    except Exception as e:
        print(f"Error checking file duplicates: {e}")
        return False


def initialize_new_file_entry(df):
    if any(df[0]) == st.session_state.uploaded_file_name:
        st.warning("file already uploaded")


def extracting_csv(csv_path):
    st.session_state.new_data = st.session_state.past_data_csv.copy()
    # HOW IS IT BEST FOR CSV_ENTRIES TO BE MODIFIED (REMOVE DUPLICATES, TYPE?, etc)
    st.session_state.new_data.loc[-1] = st.session_state.csv_entries
    st.session_state.new_data.to_csv(csv_path, index=False)

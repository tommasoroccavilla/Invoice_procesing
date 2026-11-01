import streamlit as st
import random
from PIL import Image, ImageDraw

from state.session_manager import init_state
from invoice_processing.processing.pdf_handling import (
    pdf_uploader,
    aggregate_page_data,
    image_of_selected_page,
)
from invoice_processing.processing.pdf_handling import page_selection
from invoice_processing.components.annotation_ui import (
    image_of_selected_page_with_boxes,
    column_setup,
    selection_mode_ui,
)
from invoice_processing.processing.coordinate_mapper import (
    word_selection,
    find_clicked_word,
)

from invoice_processing.processing.data_extraction import filling_csv

from invoice_processing.user_data_handling.csv_handling import (
    reading_csv,
    initialize_new_file_entry,
)


st.set_page_config(layout="wide")
st.title("Invoice Data Extractor")

init_state()

st.subheader("Current Entries")
st.session_state.past_data_csv, columns = reading_csv()
st.dataframe(st.session_state.past_data_csv)

uploaded_file = pdf_uploader()

if st.session_state.uploaded_file_object:
    # if is_file_uploaded_already(st.session_state.uploaded_file_name):
    #     st.warning("file already uploaded")
    # LOGIC HERE IN CASE DUPLICATE - SECONDARY

    if st.session_state.uploaded_file_name != st.session_state.get(
        "last_uploaded_name"
    ):
        st.info(f"Processing new file: {st.session_state.uploaded_file_name}...")
        initialize_new_file_entry(st.session_state.uploaded_file_name)
        st.session_state.current_file_data = aggregate_page_data(
            st.session_state.uploaded_file_object
        )
        st.session_state.last_uploaded_name = st.session_state.uploaded_file_name
        st.session_state.page_count = len(
            st.session_state.current_file_data.get("pages", {})
        )
        st.session_state.current_page = 1
        st.session_state.click_count = 0

    if st.session_state.current_file_data.get("pages"):
        if st.session_state.page_count > 1:
            st.session_state.current_page = page_selection()
        else:
            st.session_state.current_page = 1
        page_num = st.session_state.current_page
        page_index = page_num - 1
        DISPLAY_WIDTH = 800

        page_data = st.session_state.current_file_data["pages"][page_num]
        raw_words_data = page_data["words_data"]
        pdf_width = page_data["pdf_width"]

        st.session_state.page_image = image_of_selected_page(
            page_index, uploaded_file, dpi=300
        )

        col1, col2 = st.columns([1, 1])

        with col1:
            boxed_image = image_of_selected_page_with_boxes(
                st.session_state.page_image, raw_words_data, pdf_width
            )

            clicked_data = word_selection(boxed_image)

            if clicked_data and "x" in clicked_data:
                selected_word_text, selected_word_box = find_clicked_word(
                    click_x=clicked_data["x"],
                    click_y=clicked_data["y"],
                    display_width=DISPLAY_WIDTH,
                    pdf_width=pdf_width,
                    raw_words_data=raw_words_data,
                )

        with col2:
            st.session_state.selection_mode = selection_mode_ui()
            column_setup(columns)
            try:
                if selected_word_text == None:
                    st.write("Invalid Selection, please select again")
                else:
                    st.write("Selected word: ", selected_word_text)
                filling_csv(selected_word_text, selected_word_box)
            except NameError as e:
                st.warning("Please Select a Word to Start")
            # except ValueError as v:
            #     st.warning("Please Select a column to fill")


def clear_cache():
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)


if st.button("Clear Cache"):
    clear_cache()
    st.rerun()

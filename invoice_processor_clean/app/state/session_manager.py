import streamlit as st


def init_state():
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    if "uploaded_file_object" not in st.session_state:
        st.session_state.uploaded_file_object = None

    if "uploaded_file_name" not in st.session_state:
        st.session_state.uploaded_file_name = None

    if "last_uploaded_name" not in st.session_state:
        st.session_state.last_uploaded_name = None

    if "past_data_csv" not in st.session_state:
        st.session_state.past_data_csv = None

    if "new_row_data" not in st.session_state:
        st.session_state.new_row_data = None

    if "new_row_df" not in st.session_state:
        st.session_state.new_row_df = None

    if "selection_mode" not in st.session_state:
        st.session_state.selection_mode = "Single Entry"

    if "changing_word" not in st.session_state:
        st.session_state.changing_word = False

    if "editing_mode" not in st.session_state:
        st.session_state.editing_mode = False

    if "current_column" not in st.session_state:
        st.session_state.current_column = None

    if "extration" not in st.session_state:
        st.session_state.extration = None

    if "current_file_data" not in st.session_state:
        st.session_state.current_file_data = {}

    if "page_count" not in st.session_state:
        st.session_state.page_count = 1

    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    if "click_count" not in st.session_state:
        st.session_state.click_count = 0

    if "current_field" not in st.session_state:
        st.session_state.current_field = "invoice_id"

    if "selection_mode" not in st.session_state:
        st.session_state.selection_mode = "single_word"

    if "scaling_factor" not in st.session_state:
        st.session_state.scaling_factor = 1.0

    if "annotation_json_sep" not in st.session_state:
        st.session_state.annotation_json_sep = {
            "id": "",
            "tokens": [],
            "bboxes": [],
            "ner_tags": [],
            "page_numbers": [],
            "image": [],
        }

    if "annotation_json_uni" not in st.session_state:
        st.session_state.annotation_json_uni = {
            "id": "",
            "tokens": [],
            "bboxes": [],
            "ner_tags": [],
            "page_numbers": [],
            "image": [],
        }

    if "page_image" not in st.session_state:
        st.session_state.page_image = None

    if "current_sentence_json_united" not in st.session_state:
        st.session_state.current_sentence_json_united = ""
    if "current_bbox_json_united" not in st.session_state:
        st.session_state.current_bbox_json_united = []

    if "img_data" not in st.session_state:
        st.session_state.page_image = None

    if "img_bytes" not in st.session_state:
        st.session_state.img_bytes = None

    if "sentence_option_indexes" not in st.session_state:
        st.session_state.sentence_option_indexes = []

    if "sentence_options" not in st.session_state:
        st.session_state.sentence_options = []

    if "sentence_index" not in st.session_state:
        st.session_state.sentence_index = None

    if "current_sentence_csv" not in st.session_state:
        st.session_state.current_sentence_csv = ""

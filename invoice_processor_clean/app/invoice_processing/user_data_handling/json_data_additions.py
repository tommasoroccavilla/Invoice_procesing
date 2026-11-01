import streamlit as st
import base64
from io import BytesIO
from PIL import Image


def encoding_page_image(page_image):
    buffer = BytesIO()
    page_image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def adding_single_entry_json(selected_word_text, selected_word_box):
    # SEPARATED JSON
    st.session_state.annotation_json_sep["tokens"].append(selected_word_text)
    st.session_state.annotation_json_sep["bboxes"].append(selected_word_box)
    st.session_state.annotation_json_sep["ner_tags"].append(
        f"S-{st.session_state.current_column.upper()}"
    )
    st.session_state.annotation_json_sep["page_numbers"].append(
        st.session_state.current_page
    )

    st.session_state.annotation_json_sep["image"].append(
        encoding_page_image(st.session_state.page_image)
    )

    # UNITED JSON
    st.session_state.annotation_json_uni["tokens"].append(selected_word_text)
    st.session_state.annotation_json_uni["bboxes"].append(selected_word_box)
    st.session_state.annotation_json_uni["ner_tags"].append(
        f"S-{st.session_state.current_column.upper()}"
    )
    st.session_state.annotation_json_uni["page_numbers"].append(
        st.session_state.current_page
    )
    st.session_state.annotation_json_uni["image"].append(
        encoding_page_image(st.session_state.page_image)
    )


def single_selection_json(selected_word_text, selected_word_box):

    label = f"S-{st.session_state.current_column.upper()}"
    if label in (
        st.session_state.annotation_json_uni["ner_tags"]
        and st.session_state.annotation_json_uni["ner_tags"]
    ):
        index_sep = st.session_state.annotation_json_sep["ner_tags"].index(label)
        index_uni = st.session_state.annotation_json_uni["ner_tags"].index(label)

        # SEPARATED JSON
        st.session_state.annotation_json_sep["tokens"].pop(index_sep)
        st.session_state.annotation_json_sep["bboxes"].pop(index_sep)
        st.session_state.annotation_json_sep["ner_tags"].pop(index_sep)
        st.session_state.annotation_json_sep["page_numbers"].pop(index_sep)
        st.session_state.annotation_json_sep["image"].pop(index_sep)

        # UNITED JSON
        st.session_state.annotation_json_uni["tokens"].pop(index_uni)
        st.session_state.annotation_json_uni["bboxes"].pop(index_uni)
        st.session_state.annotation_json_uni["ner_tags"].pop(index_uni)
        st.session_state.annotation_json_uni["page_numbers"].pop(index_uni)
        st.session_state.annotation_json_uni["image"].pop(index_uni)

        adding_single_entry_json(selected_word_text, selected_word_box)

    else:
        adding_single_entry_json(selected_word_text, selected_word_box)


def single_multiple_selection_json(selected_word_text, selected_word_box):
    adding_single_entry_json(selected_word_text, selected_word_box)
    return None


def saving_to_current_sentence_json_separated(selected_word_text, selected_word_box):
    col = st.session_state.current_column.upper()
    items = st.session_state.annotation_json_sep["ner_tags"]
    if len(st.session_state.current_sentence_json_united) != 0:
        tag = "I-"
        st.session_state.annotation_json_sep["tokens"].append(selected_word_text)
        st.session_state.annotation_json_sep["bboxes"].append(selected_word_box)
        st.session_state.annotation_json_sep["ner_tags"].append(tag + col)
        st.session_state.annotation_json_sep["page_numbers"].append(
            st.session_state.current_page
        )
        st.session_state.annotation_json_sep["image"].append(
            encoding_page_image(st.session_state.page_image)
        )
    else:
        tag = "B-"
        st.session_state.annotation_json_sep["tokens"].append(selected_word_text)
        st.session_state.annotation_json_sep["bboxes"].append(selected_word_box)
        st.session_state.annotation_json_sep["ner_tags"].append(tag + col)
        st.session_state.annotation_json_sep["page_numbers"].append(
            st.session_state.current_page
        )
        st.session_state.annotation_json_sep["image"].append(
            encoding_page_image(st.session_state.page_image)
        )


def saving_to_current_sentence_json_united(selected_word_text, selected_word_box):
    st.session_state.current_sentence_json_united += selected_word_text + " "
    if len(st.session_state.current_bbox_json_united) == 0:
        st.session_state.current_bbox_json_united = selected_word_box
    else:
        st.session_state.current_bbox_json_united = [
            min(st.session_state.current_bbox_json_united[0], selected_word_box[0]),
            min(st.session_state.current_bbox_json_united[1], selected_word_box[1]),
            max(st.session_state.current_bbox_json_united[2], selected_word_box[2]),
            max(st.session_state.current_bbox_json_united[3], selected_word_box[3]),
        ]
    return (
        st.session_state.current_sentence_json_united,
        st.session_state.current_bbox_json_united,
    )


def finishing_selection_json_united():
    st.session_state.annotation_json_uni["tokens"].append(
        st.session_state.current_sentence_json_united
    )
    st.session_state.annotation_json_uni["bboxes"].append(
        st.session_state.current_bbox_json_united
    )
    st.session_state.annotation_json_uni["ner_tags"].append(
        f"U-{st.session_state.current_column.upper()}"
    )
    st.session_state.annotation_json_uni["page_numbers"].append(
        st.session_state.current_page
    )
    st.session_state.annotation_json_uni["image"].append(
        encoding_page_image(st.session_state.page_image)
    )


def resetting_json_united_vars():
    st.session_state.current_sentence_json_united = ""
    st.session_state.current_bbox_json_united = []

from PIL import Image, ImageDraw
import fitz  # Needed if you use fitz page objects, but better to pass data
import streamlit as st


def image_of_selected_page_with_boxes(image, raw_words_data, pdf_width):
    image_with_boxes = image.copy()
    draw = ImageDraw.Draw(image_with_boxes)
    img_width, _ = image.size
    scale_factor = img_width / pdf_width

    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 165, 0),
        (255, 0, 255),
        (0, 255, 255),
        (255, 255, 0),
        (128, 0, 128),
    ]
    i = 0

    for x0, y0, x1, y1, word, *rest in raw_words_data:
        left = int(x0 * scale_factor)
        top = int(y0 * scale_factor)
        right = int(x1 * scale_factor)
        bottom = int(y1 * scale_factor)

        color = colors[i % len(colors)]
        draw.rectangle((left, top, right, bottom), outline=color, width=2)
        i += 1

    return image_with_boxes


def selection_mode_ui():
    st.session_state.selection_mode = st.radio(
        "Selection Mode:",
        [
            "Single Entry",
            "Multiple Single Entries",
            "Entry to be Joined",
            "Multiple Entries to be Joined",
        ],
        horizontal=True,
    )
    return st.session_state.selection_mode


def column_setup(column_list):
    col1, col2 = st.columns(2)
    for i, col in enumerate(column_list):
        if i < len(column_list) / 2:
            with col1:
                is_current = st.session_state.current_column == col
                button_type = "primary" if is_current else "secondary"
                button_label = col.replace("_", " ").title()
                if st.button(
                    button_label,
                    key=f"nav_{col}",
                    type=button_type,
                    help=f"Select {button_label.lower()} field for annotation",
                ):
                    st.session_state.current_column = col
        else:
            with col2:
                is_current = st.session_state.current_column == col
                button_type = "primary" if is_current else "secondary"
                button_label = col.replace("_", " ").title()
                if st.button(
                    button_label,
                    key=f"nav_{col}",
                    type=button_type,
                    help=f"Select {button_label.lower()} field for annotation",
                ):
                    st.session_state.current_column = col

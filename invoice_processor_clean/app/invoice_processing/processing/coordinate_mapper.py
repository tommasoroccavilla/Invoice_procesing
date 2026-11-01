import math
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates as st_img_coor


def word_selection(image):
    value = st_img_coor(image, key=f"img_coord_", width=800)
    # image_width, image_height = image.size

    # x_position = value["x"] / 800 * image_width
    # y_position = value["y"] / 1130 * image_height

    # for i, box in enumerate(boxes):
    #     if box[0] <= x_position <= box[2] and box[1] <= y_position <= box[3]:
    #         word = texts[i]

    # click += 1
    return value


def find_clicked_word(click_x, click_y, display_width, pdf_width, raw_words_data):
    scale_to_pdf_point = pdf_width / display_width

    pdf_point_x = click_x * scale_to_pdf_point
    pdf_point_y = click_y * scale_to_pdf_point

    selected_word_text = None
    selected_word_bbox = None
    for x0, y0, x1, y1, word, *rest in raw_words_data:
        if (x0 <= pdf_point_x <= x1) and (y0 <= pdf_point_y <= y1):
            selected_word_text = word
            selected_word_bbox = [x0, y0, x1, y1]
            break

    if selected_word_text is None:
        st.warning("Click did not land on a word.")
        return None, None

    return selected_word_text, selected_word_bbox

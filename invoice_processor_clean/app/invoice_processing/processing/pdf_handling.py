import streamlit as st
import fitz
from PIL import Image, ImageDraw
import io


def pdf_uploader():
    st.subheader("Upload an invoice PDF")
    uploaded_file = st.file_uploader("Choose PDF file", type="pdf")

    if uploaded_file is not None:
        st.session_state.uploaded_file_name = uploaded_file.name
        st.session_state.uploaded_file_object = uploaded_file
        return st.session_state.uploaded_file
    else:
        st.session_state.uploaded_file_object = None
        st.session_state.uploaded_file_name = None
        return None


def aggregate_page_data(uploaded_file):
    pdf_bytes = uploaded_file.getvalue()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    total_pages = len(doc)

    file_data = {"file_name": uploaded_file.name, "csv_entry": {}, "pages": {}}

    for i in range(total_pages):
        page = doc.load_page(i)

        words_data = page.get_text("words")

        file_data["pages"][i + 1] = {
            "words_data": words_data,
            "annotations": {},
            "pdf_width": page.rect.width,
            "pdf_height": page.rect.height,
        }

    doc.close()
    return file_data


def page_selection():
    page_num = st.number_input(
        "Select Page",
        min_value=1,
        max_value=st.session_state.page_count,
        value=st.session_state.get("current_page", 1),
        key="page_select",
    )
    return page_num


def get_page_object(uploaded_file, page_index):
    pdf_bytes = st.session_state.uploaded_file_object
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc[page_index]
    return page


def image_of_selected_page(page_index, uploaded_file, dpi=300):
    page = get_page_object(uploaded_file, page_index)
    page_area = page.rect.width * page.rect.height
    adaptive_dpi = min(dpi, max(150, int(300000 / page_area * 72)))
    mat = fitz.Matrix(adaptive_dpi / 72, adaptive_dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    image = Image.open(io.BytesIO(img_data))
    return image

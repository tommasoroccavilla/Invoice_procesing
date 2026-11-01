import json
import streamlit as st
from invoice_processing.user_data_handling.json_data_additions import (
    encoding_page_image,
)

json_separated_path = "app/data/annotated_data/jsons/training_data_separated.json"
json_united_path = "app/data/annotated_data/jsons/training_data_united.json"


def json_creation():
    empty_data = [
        {
            "id": "",
            "tokens": [],
            "bboxes": [],
            "ner_tags": [],
            "page_numbers": [],
        }
    ]
    json_str = json.dumps(empty_data, indent=2)
    with open("app/data/annotated_data/jsons/training_data_separated.json", "w") as f:
        f.write(json_str)

    with open("app/data/annotated_data/jsons/training_data_united.json", "w") as f:
        f.write(json_str)


def appending_Os_jsons():
    # Cache already labeled (word + bbox) pairs for fast lookup
    labeled_pairs = set(
        zip(
            st.session_state.annotation_json_sep["tokens"],
            map(tuple, st.session_state.annotation_json_sep["bboxes"]),
        )
    )

    for i, page in st.session_state.current_file_data["pages"].items():
        raw_words = page["words_data"]
        encoded_img = encoding_page_image(
            st.session_state.page_image
        )  # Encode once per page

        for x0, y0, x1, y1, word, *rest in raw_words:
            bbox = [x0, y0, x1, y1]
            key = (word, tuple(bbox))

            # Add only if this exact word+bbox isn't already annotated
            if key not in labeled_pairs:
                for ann_json in [
                    st.session_state.annotation_json_sep,
                    st.session_state.annotation_json_uni,
                ]:
                    ann_json["tokens"].append(word)
                    ann_json["bboxes"].append(bbox)
                    ann_json["ner_tags"].append("O")
                    ann_json["page_numbers"].append(i)
                    ann_json["image"].append(encoded_img)

                labeled_pairs.add(key)


def json_data_cleaning(data):
    new_separated_data = []
    number_of_pages = set(data["page_numbers"])
    number_of_pages = list(number_of_pages)
    for p in number_of_pages:
        provisional_new_separated_data = {
            "id": "",
            "tokens": [],
            "bboxes": [],
            "ner_tags": [],
            "page_number": [],
            "image": "",
        }
        for e, page_data_point in enumerate(data["page_numbers"]):
            if data["page_numbers"][e] == p:
                provisional_new_separated_data["id"] = data["id"]
                provisional_new_separated_data["tokens"].append(data["tokens"][e])
                provisional_new_separated_data["bboxes"].append(data["bboxes"][e])
                provisional_new_separated_data["ner_tags"].append(data["ner_tags"][e])
                provisional_new_separated_data["page_number"] = p
                provisional_new_separated_data["image"] = data["image"][e]
            else:
                pass
        new_separated_data.append(provisional_new_separated_data)

    return new_separated_data


def appending_finished_jsons_separated(new_data_separated):
    json_separated_path = "app/data/annotated_data/jsons/training_data_separated.json"
    with open(json_separated_path, "r") as f:
        existing_separated_data = json.load(f)
    existing_separated_data.append(new_data_separated)
    with open(json_separated_path, "w") as f:
        json.dump(existing_separated_data, f, indent=4)


def appending_finished_jsons_united(new_data_united):
    json_united_path = "app/data/annotated_data/jsons/training_data_united.json"
    with open(json_united_path, "r") as f:
        existing_united_data = json.load(f)
    existing_united_data.append(new_data_united)
    with open(json_united_path, "w") as f:
        json.dump(existing_united_data, f, indent=4)

import streamlit as st
import pandas as pd

from invoice_processing.user_data_handling.csv_handling import extracting_csv

from invoice_processing.user_data_handling.csv_data_additions import (
    single_selection_csv,
    single_multiple_selection_csv,
    saving_to_current_sentence_csv,
    finishing_selection_csv,
)

from invoice_processing.user_data_handling.csv_data_removals import (
    single_multiple_selection_csv_removal,
    word_removal_csv,
)


from invoice_processing.user_data_handling.json_data_additions import (
    single_selection_json,
    single_multiple_selection_json,
    saving_to_current_sentence_json_separated,
    saving_to_current_sentence_json_united,
    finishing_selection_json_united,
    resetting_json_united_vars,
)

from invoice_processing.user_data_handling.json_data_removal import (
    single_multiple_selection_json_removal,
    sentence_selection,
    word_selection,
    word_removal_json_sep,
    word_removal_json_uni,
)

from invoice_processing.user_data_handling.json_handling import (
    appending_finished_jsons_separated,
    appending_finished_jsons_united,
    appending_Os_jsons,
    json_data_cleaning,
)

csv_path = "app/data/annotated_data/csvs/extracted_data.csv"


def filling_csv(selected_word_text, selected_word_box):
    if "csv_entries" not in st.session_state:
        cols = st.session_state.past_data_csv.columns.to_list()
        st.session_state.csv_entries = ["" for _ in cols]
        index_filename = cols.index("file_name")
        st.session_state.csv_entries[index_filename] = (
            st.session_state.uploaded_file_name
        )

    cols = st.session_state.past_data_csv.columns.to_list()
    index = cols.index(st.session_state.current_column)

    options = sentence_selection()

    if st.session_state.uploaded_file_object:
        if not st.session_state.annotation_json_sep["id"]:
            st.session_state.annotation_json_sep["id"] = (
                st.session_state.uploaded_file_name
            )
        if not st.session_state.annotation_json_uni["id"]:
            st.session_state.annotation_json_uni["id"] = (
                st.session_state.uploaded_file_name
            )
    col1, col2, col3, col4 = st.columns(4)

    if st.session_state.selection_mode == "Single Entry":
        if selected_word_text and col1.button("Finished Selection - single entry"):
            single_selection_csv(selected_word_text, index)
            single_selection_json(selected_word_text, selected_word_box)
        # REMOVING SHOULD BE DONE BY OVERWRITNG CURRENT SELECTION

    if st.session_state.selection_mode == "Multiple Single Entries":

        if selected_word_text and col1.button("Save New Word - MSE"):
            single_multiple_selection_csv(selected_word_text, index)
            single_multiple_selection_json(selected_word_text, selected_word_box)

        with col2:
            removal_entry = st.selectbox(
                "Select a Word to remove", options=st.session_state.csv_entries[index]
            )
            st.write(
                st.session_state.annotation_json_sep["tokens"].index(removal_entry)
            )

        if col3.button("Remove Word"):
            single_multiple_selection_csv_removal(removal_entry, index)
            single_multiple_selection_json_removal(removal_entry)

    if (
        st.session_state.selection_mode == "Entry to be Joined"
        or st.session_state.selection_mode == "Multiple Entries to be Joined"
    ):

        if selected_word_text and col1.button(
            "Save Word to Current Sentence", key="MultSavBut"
        ):
            saving_to_current_sentence_csv(selected_word_text, index)
            saving_to_current_sentence_json_separated(
                selected_word_text, selected_word_box
            )
            saving_to_current_sentence_json_united(
                selected_word_text, selected_word_box
            )

        if col1.button("Finish Sentence"):
            finishing_selection_json_united()
            resetting_json_united_vars()
            finishing_selection_csv(index)

        with col2:
            try:
                options = sentence_selection()
                sentence_to_remove_from = st.selectbox(
                    "Select a Sentence to Change", options=options
                )
            except TypeError:
                pass

        with col3:
            try:
                words_to_remove = st.selectbox(
                    "Select word to remove",
                    options=word_selection(sentence_to_remove_from),
                )
            except TypeError:
                pass

        if col4.button("Remove Word", key="MultRemBut"):
            word_removal_json_sep(sentence_to_remove_from, words_to_remove)
            word_removal_json_uni(sentence_to_remove_from, words_to_remove)
            word_removal_csv(sentence_to_remove_from, index, words_to_remove)

    current_df = pd.DataFrame(columns=cols)
    current_df.loc[len(current_df)] = st.session_state.csv_entries
    current_df = current_df.transpose()
    st.dataframe(current_df)

    if st.button("Finished with Invoice"):
        appending_Os_jsons()
        st.session_state.annotation_json_sep = json_data_cleaning(
            st.session_state.annotation_json_sep
        )
        st.session_state.annotation_json_uni = json_data_cleaning(
            st.session_state.annotation_json_uni
        )
        extracting_csv(csv_path)
        appending_finished_jsons_separated(st.session_state.annotation_json_sep)
        appending_finished_jsons_united(st.session_state.annotation_json_uni)

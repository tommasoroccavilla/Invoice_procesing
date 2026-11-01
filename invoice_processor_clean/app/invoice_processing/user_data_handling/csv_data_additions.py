import streamlit as st


def single_selection_csv(selected_word_text, index):
    st.session_state.csv_entries[index] = selected_word_text


def single_multiple_selection_csv(selected_word_text, index):

    if type(st.session_state.csv_entries[index]) == list:
        st.session_state.csv_entries[index].append(selected_word_text)

    else:
        st.session_state.csv_entries[index] = []
        st.session_state.csv_entries[index].append(selected_word_text)


def saving_to_current_sentence_csv(selected_word_text, index):
    st.session_state.current_sentence_csv += selected_word_text + " "
    st.write(st.session_state.current_sentence_csv)
    return st.session_state.current_sentence_csv


def finishing_selection_csv(index):
    if type(st.session_state.csv_entries[index]) == list:
        st.session_state.csv_entries[index].append(
            st.session_state.current_sentence_csv
        )

    else:
        st.session_state.csv_entries[index] = []
        st.session_state.csv_entries[index].append(
            st.session_state.current_sentence_csv
        )

    st.session_state.current_sentence_csv = ""

import streamlit as st


def single_multiple_selection_csv_removal(removal_entry, index):
    removal_entry_index = st.session_state.csv_entries[index].index(removal_entry)
    st.session_state.csv_entries[index].pop(removal_entry_index)


def word_removal_csv(sentence_to_remove, index, word): 
    current_entries = st.session_state.csv_entries[index]
    for sentence in current_entries:
        if sentence == sentence_to_remove:
            index_sentence = st.session_state.csv_entries[index].index(sentence)

    words = st.session_state.csv_entries[index][index_sentence].split()
    words.remove(word)
    words = " ".join(words)
    st.session_state.csv_entries[index][index_sentence] = words

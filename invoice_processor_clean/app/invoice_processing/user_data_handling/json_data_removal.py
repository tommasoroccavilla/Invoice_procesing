import streamlit as st


def sentence_selection():
    items = st.session_state.annotation_json_uni["ner_tags"]

    st.session_state.sentence_option_indexes = []

    for index, item in enumerate(items):
        if item.endswith(st.session_state.current_column.upper()):
            st.session_state.sentence_option_indexes.append(index)

    st.session_state.sentence_options = []

    for index in st.session_state.sentence_option_indexes:
        sentence = st.session_state.annotation_json_uni["tokens"][index]
        st.session_state.sentence_options.append(sentence)

    return st.session_state.sentence_options


def word_selection(sentence):
    sentences = st.session_state.annotation_json_uni["tokens"]
    for item in sentences:
        if item == sentence:
            st.session_state.sentence_index = sentences.index(sentence)
    split_sentence = sentences[st.session_state.sentence_index].split()
    return split_sentence


def word_removal_json_sep(sentence, word):
    split_sentence = word_selection(sentence)
    for parola in split_sentence:
        if parola == word:
            word_to_remove_index = st.session_state.annotation_json_sep["tokens"].index(
                parola
            )
    st.session_state.annotation_json_sep["tokens"].pop(word_to_remove_index)
    st.session_state.annotation_json_sep["bboxes"].pop(word_to_remove_index)
    st.session_state.annotation_json_sep["ner_tags"].pop(word_to_remove_index)
    st.session_state.annotation_json_sep["page_numbers"].pop(word_to_remove_index)
    st.session_state.annotation_json_sep["image"].pop(word_to_remove_index)


def word_removal_json_uni(sentence, word):
    split_sentence = word_selection(sentence)
    sentence_index = st.session_state.annotation_json_uni["tokens"].index(sentence)

    # LOGIC TO REMOVE THE WORD FROM SENTENCE
    word_to_remove_index = split_sentence.index(word)
    split_sentence.pop(word_to_remove_index)

    # IF EMPTY REMOVES THE WHOLE ENTRY
    if len(split_sentence) == 0:
        st.session_state.annotation_json_uni["tokens"].pop(sentence_index)
        st.session_state.annotation_json_uni["bboxes"].pop(sentence_index)
        st.session_state.annotation_json_uni["ner_tags"].pop(sentence_index)
        st.session_state.annotation_json_uni["page_numbers"].pop(sentence_index)
        st.session_state.annotation_json_uni["image"].pop(sentence_index)

    else:
        joined_sentence = " ".join(split_sentence)
        st.session_state.annotation_json_uni["tokens"][sentence_index] = joined_sentence

        # LOGIC FOR BBOX
        starting_point = 0
        sentence_index_test = sentence_index - 1
        while sentence_index_test >= 0:
            sent_prov = st.session_state.annotation_json_uni["tokens"][
                sentence_index_test
            ]

            split_sen_prov = sent_prov.split()

            starting_point += len(split_sen_prov)
            sentence_index_test -= 1

        ending_point = (
            starting_point + len(st.session_state.annotation_json_uni["tokens"]) - 1
        )

        x_min = []
        y_min = []
        x_max = []
        y_max = []
        try:
            for i in range(starting_point, ending_point):
                bbox = st.session_state.annotation_json_sep["bboxes"][i]
                x_min.append(bbox[0])
                y_min.append(bbox[1])
                x_max.append(bbox[2])
                y_max.append(bbox[3])
        except IndexError:
            st.write("Error in removal, check which word it removed")

        new_bbox = [min(x_min), min(y_min), max(x_max), max(y_max)]
        st.session_state.annotation_json_uni["bboxes"][sentence_index] = new_bbox


def single_multiple_selection_json_removal(removal_entry):
    index_for_removal_sep = st.session_state.annotation_json_sep["tokens"].index(
        removal_entry
    )

    index_for_removal_uni = st.session_state.annotation_json_uni["tokens"].index(
        removal_entry
    )

    st.session_state.annotation_json_sep["tokens"].pop(index_for_removal_sep)
    st.session_state.annotation_json_sep["bboxes"].pop(index_for_removal_sep)
    st.session_state.annotation_json_sep["ner_tags"].pop(index_for_removal_sep)
    st.session_state.annotation_json_sep["page_numbers"].pop(index_for_removal_sep)
    st.session_state.annotation_json_sep["image"].pop(index_for_removal_sep)

    # UNITED JSON
    st.session_state.annotation_json_uni["tokens"].pop(index_for_removal_uni)
    st.session_state.annotation_json_uni["bboxes"].pop(index_for_removal_uni)
    st.session_state.annotation_json_uni["ner_tags"].pop(index_for_removal_uni)
    st.session_state.annotation_json_uni["page_numbers"].pop(index_for_removal_uni)
    st.session_state.annotation_json_uni["image"].pop(index_for_removal_uni)

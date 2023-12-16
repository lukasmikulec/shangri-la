# import the library to create user interface of the quiz
import streamlit as st

# import the function to generate txt files with quiz sentences
from helpers_small_functions import create_sentences_txt_file

# define a function which will display the content of the quiz tab
def display_tab_content(number_of_question):
    # lower the input to this function by one because Python lists start at 0, not 1
    nr = number_of_question - 1

    # blank out the word to be guessed in the sentence
    sentence = st.session_state["quiz_sentences"][nr].replace(st.session_state["quiz_words"][nr], "___ ______")
    # write this blanked out sentence as a subheader
    st.subheader(sentence)
    # ask user for the answer with instructions
    word_guess = st.text_input("What is the word? Write both the definite article and the word.", key=f"input {nr}")

    # if the user answered already
    if len(word_guess) > 0:
        # lowercase both the user input and the correct answer to eliminate errors
        if word_guess.lower() == st.session_state["quiz_words"][nr].lower():
            # if the input is the same as the blanked out word, show success
            st.markdown("✔️ Correct!")
            # display the audio
            st.audio(st.session_state["quiz_audios"][nr])
            # if the list does not contain the value for this question (if this was not checked, user
            # could just enter the same correct value multiple times in one question and trick the system to
            # believe user already answered everything)
            if f"Correct {nr}" not in st.session_state["all_questions_answered"]:
                # write down an element to the list which is used to check if all answers were answered already
                st.session_state["all_questions_answered"].append(f"Correct {nr}")
        # if the answer is incorrect
        else:
            # tell user to try again
            st.markdown("❌ Try again.")

# define a function which will display the quiz in frontend
def display_quiz():
    # define a list which to which one element will be added after one correct answer and which will unlock the
    # last tab with summary when all questions have been answered
    # use the session state for this data to be available for management for the display_tab_content function too
    st.session_state["all_questions_answered"] = []

    # if the number of images uploaded was 3
    if st.session_state["number_of_items_quiz"] == 3:
        # create three tabs for each quiz question and the last tab for summary of results
        tab1, tab2, tab3, tab4 = st.tabs(["1st task", "2nd task", "3rd task", "Results"])

        # first tab
        with tab1:
            # put heading
            st.header("1st task")
            # display content for tab1
            display_tab_content(1)

        # second tab
        with tab2:
            # put heading
            st.header("2nd task")
            # display content for tab2
            display_tab_content(2)

        # third tab
        with tab3:
            # put heading
            st.header("3rd task")
            # display content for tab3
            display_tab_content(3)

        # summary tab
        with tab4:
            # put heading
            st.header("Results")

            # if all questions are correctly answered
            if len(st.session_state["all_questions_answered"]) == 3:
                # place text
                st.markdown("Here is a list of all sentences from this quiz:")
                # give a list of all sentences with the quiz words in bold
                for i in range(3):
                    # split each sentence into words (list of words)
                    sentence_split_into_words = st.session_state["quiz_sentences"][i].split()
                    # take the first two words (first two items in a list), the article and the word
                    first_two_words = sentence_split_into_words[:2]
                    # join them into one string
                    first_two_words = " ".join(first_two_words)
                    # take the rest of the words
                    rest_of_the_sentence = sentence_split_into_words[2:]
                    # join them into one string
                    rest_of_the_sentence = " ".join(rest_of_the_sentence)
                    # display the sentences with the first two (the quiz words) in bold
                    st.markdown(f'{i+1}. **{first_two_words}** {rest_of_the_sentence}')

                # assign the output of the txt generating function for sentences to this variable
                file = create_sentences_txt_file(st.session_state["quiz_sentences"])
                # open this file variable for interaction
                with open(file, "rb") as f:
                    # show download button for the user to download sentences
                    st.download_button("📥 Download sentences as a txt file", data=f, file_name="sentences.txt")

                # celebrate the successful quiz
                st.balloons()
            # if all questions are not yet (correctly) answered
            else:
                st.markdown("Answer all questions correctly first. 👀")



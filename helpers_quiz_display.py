# Import the library to create user interface of the quiz
import streamlit as st

# Import the function to generate txt files with quiz sentences
from helpers_small_functions import create_sentences_txt_file


# Define a function which will display the content of the quiz tab
def display_tab_content(number_of_question, total_questions):
    # Lower the input to this function by one because Python lists start at 0, not 1
    nr = number_of_question - 1

    # Ask user for the answer with instructions
    word_guess = st.text_input("What is the word? Write both the definite article and the word.", key=f"input {nr}")

    # Blank out the word to be guessed in the sentence
    sentence = st.session_state["quiz_sentences"][nr].replace(st.session_state["quiz_words"][nr], "___ ______")
    # Write this blanked out sentence as a subheader
    st.subheader(sentence)

    # Remind user of the generated words user can choose from in the quiz
    if total_questions == 3:
        # Display three hint words if the quiz has three questions
        st.markdown(f'*Possible answers: {st.session_state["quiz_help"][0]}, {st.session_state["quiz_help"][1]}, '
                    f'{st.session_state["quiz_help"][2]}*')
    elif total_questions == 4:
        # Display four hint words if the quiz has four questions
        st.markdown(f'*Possible answers: {st.session_state["quiz_help"][0]}, {st.session_state["quiz_help"][1]}, '
                    f'{st.session_state["quiz_help"][2]}, {st.session_state["quiz_help"][3]}*')
    elif total_questions == 5:
        # Display five hint words if the quiz has five questions
        st.markdown(f'*Possible answers: {st.session_state["quiz_help"][0]}, {st.session_state["quiz_help"][1]}, '
                    f'{st.session_state["quiz_help"][2]}, {st.session_state["quiz_help"][3]}, '
                    f'{st.session_state["quiz_help"][4]}*')

    # If the user answered already
    if len(word_guess) > 0:
        # Lowercase both the user input and the correct answer to eliminate errors
        if word_guess.lower() == st.session_state["quiz_words"][nr].lower():
            # If the input is the same as the blanked out word, show success
            st.markdown("✔️ Correct!")
            # Display the audio
            st.audio(st.session_state["quiz_audios"][nr])
            # If the list does not contain the value for this question (if this was not checked, user
            # could just enter the same correct value multiple times in one question and trick the system to
            # believe user already answered everything)
            if f"Correct {nr}" not in st.session_state["all_questions_answered"]:
                # Write down an element to the list which is used to check if all answers were answered already
                st.session_state["all_questions_answered"].append(f"Correct {nr}")
        # If the answer is incorrect
        else:
            # Tell user to try again
            st.markdown("❌ Try again.")


# Define a function which will display the results tab of the quiz
def display_results_tab(number_of_quiz_items):
    # If all questions are correctly answered
    if len(st.session_state["all_questions_answered"]) == number_of_quiz_items:
        # Place text
        st.markdown("Here is a list of all sentences from this quiz:")
        # Give a list of all sentences with the quiz words in bold
        for i in range(number_of_quiz_items):
            # Split each sentence into words (list of words)
            sentence_split_into_words = st.session_state["quiz_sentences"][i].split()
            # Take the first two words (first two items in a list), the article and the word
            first_two_words = sentence_split_into_words[:2]
            # Join them into one string
            first_two_words = " ".join(first_two_words)
            # Take the rest of the words
            rest_of_the_sentence = sentence_split_into_words[2:]
            # Join them into one string
            rest_of_the_sentence = " ".join(rest_of_the_sentence)
            # Display the sentences with the first two (the quiz words) in bold
            st.markdown(f'{i + 1}. **{first_two_words}** {rest_of_the_sentence}')

        # Assign the output of the txt generating function for sentences to this variable
        file = create_sentences_txt_file(st.session_state["quiz_sentences"])
        # Open this file variable for interaction
        with open(file, "rb") as f:
            # Show download button for the user to download sentences
            st.download_button("📥 Download sentences as a txt file",
                               data=f,
                               file_name="sentences.txt")

        # Celebrate the successful quiz
        st.balloons()
    # If all questions are not yet (correctly) answered
    else:
        # Inform the user they have to complete the quiz successfully first
        st.markdown("Answer all questions correctly first. 👀")


# Define a function which will display the quiz in frontend
def display_quiz():
    # Define a list which to which one element will be added after one correct answer and which will unlock the
    # last tab with summary when all questions have been answered
    # Use the session state for this data to be available for management for the display_tab_content function too
    st.session_state["all_questions_answered"] = []

    # If the number of images uploaded was 3
    if st.session_state["number_of_items_quiz"] == 3:
        # Create three tabs for each quiz question and the last tab for summary of results
        tab1, tab2, tab3, tab4 = st.tabs(["1st task", "2nd task", "3rd task", "Results"])

        # First tab
        with tab1:
            # Put heading
            st.header("1st task")
            # Display content for tab1
            display_tab_content(1, 3)

        # Second tab
        with tab2:
            # Put heading
            st.header("2nd task")
            # Display content for tab2
            display_tab_content(2, 3)

        # Third tab
        with tab3:
            # Put heading
            st.header("3rd task")
            # Display content for tab3
            display_tab_content(3, 3)

        # Results tab
        with tab4:
            # Put heading
            st.header("Results")
            # Display content for results tab
            display_results_tab(3)

    # If the number of images uploaded was 4
    elif st.session_state["number_of_items_quiz"] == 4:
        # Create three tabs for each quiz question and the last tab for summary of results
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["1st task", "2nd task", "3rd task", "4th task", "Results"])

        # First tab
        with tab1:
            # Put heading
            st.header("1st task")
            # Display content for tab1
            display_tab_content(1, 4)

        # Second tab
        with tab2:
            # Put heading
            st.header("2nd task")
            # Display content for tab2
            display_tab_content(2, 4)

        # Third tab
        with tab3:
            # Put heading
            st.header("3rd task")
            # Display content for tab3
            display_tab_content(3, 4)

        # Fourth tab
        with tab4:
            # Put heading
            st.header("4th task")
            # Display content for tab3
            display_tab_content(4, 4)

        # Results tab
        with tab5:
            # Put heading
            st.header("Results")
            # Display content for results tab
            display_results_tab(4)

    # If the number of images uploaded was 5
    elif st.session_state["number_of_items_quiz"] == 5:
        # Create three tabs for each quiz question and the last tab for summary of results
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["1st task", "2nd task", "3rd task", "4th task", "5th task",
                                                      "Results"])

        # First tab
        with tab1:
            # Put heading
            st.header("1st task")
            # Display content for tab1
            display_tab_content(1, 5)

        # Second tab
        with tab2:
            # Put heading
            st.header("2nd task")
            # Display content for tab2
            display_tab_content(2, 5)

        # Third tab
        with tab3:
            # Put heading
            st.header("3rd task")
            # Display content for tab3
            display_tab_content(3, 5)

        # Fourth tab
        with tab4:
            # Put heading
            st.header("4th task")
            # Display content for tab3
            display_tab_content(4, 5)

        # Fifth tab
        with tab5:
            # Put heading
            st.header("5th task")
            # Display content for tab3
            display_tab_content(5, 5)

        # Results tab
        with tab6:
            # Put heading
            st.header("Results")
            # Display content for results tab
            display_results_tab(5)

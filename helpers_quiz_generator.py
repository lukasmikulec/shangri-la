# Import library time to give time for retrying to connect to the API
import time
# Import library to reshuffle quiz items randomly
import random

# Import the library for handling API
import requests
# Import streamlit to create widgets
import streamlit as st

# Import library for saving audio files with unique, timestamped names
from datetime import datetime

# Load the API KEY from st.secrets (used to authenticate API requests)
api_key = st.secrets["API_KEY"]


# Define a function to generate a sentence based on the first word
def generate_sentence(word):
    # Define the API url
    url = "https://api-inference.huggingface.co/models/stefan-it/german-gpt2-larger"
    # Define the headers for authorization of access to the API
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'identity, deflate, compress, gzip',
               'Authorization': f"Bearer {api_key}",
               'User-Agent': 'python-requests/0.12.1'}
    # Set this variable as empty string which will later receive the status message from API
    api_status_sentence_generation = ""
    # Set this variable as 0 (no request to API made yet)
    api_sentence_generation_try = 0

    # While API won't return a successful response and the number of retries does not reach 10, keep retrying
    while api_status_sentence_generation != "<Response [200]>" and api_sentence_generation_try != 10:
        api_status_sentence_generation = requests.post(url,
                                                       headers=headers,
                                                       json=word)
        # Make the format as string, so it can be noticed by the while loop condition
        api_status_sentence_generation = str(api_status_sentence_generation)
        # In case the API request failed, wait for two seconds before retrying
        if api_status_sentence_generation != "<Response [200]>":
            time.sleep(2)
        # Increase the number of attempts to reach API by 1
        api_sentence_generation_try += 1

    # If the API connection was successful, do the actual job and get the sentence from a working API
    if api_sentence_generation_try != 10:
        # Get the response using the URL, headers, and image data; convert the response into a readable format
        sentence = requests.post(url,
                                 headers=headers,
                                 json=word).json()
        # Get the sentence from the response
        sentence = sentence[0]["generated_text"]
        # Only keep the first generated sentence (discard everything after the first dot)
        sentence = sentence[:sentence.find(".")]
        # Since the previous step removes the dot as well, add the dot at the end of the sentence
        sentence = sentence + "."
        # Return the sentence
        return sentence
    # If the API connection failed
    else:
        # Return error to the process function
        return "ERROR"


# Define a text-to-speech function (in German)
def generate_audio(sentence):
    # Define the API url
    url = "https://api-inference.huggingface.co/models/facebook/mms-tts-deu"
    # Define the headers for authorization of access to the API
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'identity, deflate, compress, gzip',
               'Authorization': f"Bearer {api_key}",
               'User-Agent': 'python-requests/0.12.1'}
    # Set this variable as empty string which will later receive the status message from API
    api_status_audio_generation = ""
    # Set this variable as 0 (no request to API made yet)
    api_audio_generation_try = 0

    # While API won't return a successful response and the number of retries does not reach 10, keep retrying
    while api_status_audio_generation != "<Response [200]>" and api_audio_generation_try != 10:
        api_status_audio_generation = requests.post(url,
                                                    headers=headers,
                                                    json=sentence)
        # Make the format as string, so it can be noticed by the while loop condition
        api_status_audio_generation = str(api_status_audio_generation)
        # In case the API request failed, wait for two seconds before retrying
        if api_status_audio_generation != "<Response [200]>":
            time.sleep(2)
        # Increase the number of attempts to reach API by 1
        api_audio_generation_try += 1

    # If the API connection was successful, do the actual job and get the audio from a working API
    if api_audio_generation_try != 10:
        # Get the audio file from the API
        audio = requests.post(url,
                              headers=headers,
                              json=sentence)
        # Get the current date and time
        now = datetime.now()
        # Format this current date and time into a string suitable for a filename
        formatted_now = now.strftime("%Y-%m-%d-%H-%M-%S")
        # Create the filename
        filename = f"data/audio_{formatted_now}.wav"
        # Save the audio received from the API under the filename just defined
        with open(filename, "wb") as file:
            file.write(audio.content)
        # Return the filename
        return filename
    # If the API connection failed
    else:
        # Return error to the process function
        return "ERROR"


# Put the functions for writing sentences and generating speech from them together
def generate_quiz(word_list):
    # Define a variable which will store the list of sentences
    list_of_sentences = []
    # Define a variable which will store the number of sentences
    number_of_items = None
    # Define a variable which will store the list of audios
    list_of_audios = []

    # Define a list in which quiz words will be stored (plural has to go away)
    quiz_words = []

    # Define a list in which quiz words in the original order will be stored to display as help for the user
    # to know which words to choose from when answering the question
    quiz_help = []

    # If there are more than 5 words that were generated
    if len(word_list) > 5:
        # Choose 5 words out of them randomly for the quiz
        word_list = random.sample(word_list, 5)

    # Remove the plurals from the generated words and put them into the quiz_words list
    for i in range(len(word_list)):
        # Take the German words from the original word list
        word = word_list[i][0]
        # Remove the plural form after the comma (removes comma and space too)
        word = word[:word.find(",")]

        # Take the value of "word" variable and assign it to quiz helper word (before formatting it for other purposes)
        quiz_helper_word = word

        # Take the first letter of the word and capitalize it
        first_letter = word[0].upper()
        # Recreate the word with capitalized first letter by putting the capitalized letter and the rest of the
        # word apart from the first letter together
        word = first_letter + word[1:]
        # Add the word to the quiz words list to be used in the sentence writing function
        quiz_words.append(word)

        # Add the helper word to quiz help list
        quiz_help.append(quiz_helper_word)

    # Store the quiz helper words as session state to be accessed later
    st.session_state["quiz_help"] = quiz_help

    # Reshuffle the words in list randomly so the user does not know which word is where
    random.shuffle(quiz_words)

    # Define percentage as 0 (will be used to display the progress of the function in st.status)
    percentage = 0
    # Do everything within a with st.status function to enable display the progress of function to the user
    with st.status(f"Generating the quiz ({percentage}% completed)", expanded=True) as status:
        # Define percentage increase as 100 divided by the number of words and this divided by two
        # (each word has two steps - sentence writing and audio generation)
        percentage_increase = round((100 / len(word_list)) / 2)
        # For as many words as there are
        for i in range(len(word_list)):
            # Check if there are no errors in the list of sentences yet. If not, continue.
            if "ERROR" not in list_of_sentences:
                # Get the word you are processing from the list of quiz words
                quiz_word = quiz_words[i]
                # Add another percentage increase
                percentage = percentage + percentage_increase
                # Display the current percentage state in st.status (after successful step)
                status.update(label=f"Generating the quiz ({percentage - percentage_increase}% completed)")
                # Write to the status that a sentence including the word is generated (first part)
                st.write(f"✍️ Writing sentence with the word number {i + 1}")
                # Get the sentence which includes the word and assign it to a variable sentence
                sentence = generate_sentence(quiz_word)
                # If the API works correctly and does not return an error
                if sentence != "ERROR":
                    # Add another percentage increase (after successful step)
                    percentage = percentage + percentage_increase
                    # Display the current percentage state in st.status
                    status.update(label=f"Generating the quiz ({percentage - percentage_increase}% completed)")
                    # Write to the status that the audio is being created (second part)
                    st.write(f"🎤 Narrating the audio for the sentence number {i + 1}")
                    # Add the sentence to the list
                    list_of_sentences.append(sentence)
                    # Pass audio to the generate audio function
                    audio = generate_audio(sentence)
                    # If the API works and does not return an error
                    if audio != "ERROR":
                        # Assign the audio to the list of audios
                        list_of_audios.append(audio)
                    else:
                        # Otherwise say this item returned an error (due to API error)
                        list_of_audios.append("ERROR")
                # Otherwise say this item returned an error (due to API error)
                else:
                    list_of_sentences.append("ERROR")

        # If there was no error in the process
        if "ERROR" not in list_of_sentences and "ERROR" not in list_of_audios:
            # set the number of items to the actual number of quiz items
            number_of_items = len(word_list)
        # If there was an error in the process
        else:
            # Set the number of items to 0, so the display quiz function does not display errors
            number_of_items = 0
            # Display an error for 7 seconds informing the user that API connection failed
            with st.empty():
                for i in range(7):
                    st.error(
                        "The connection to the API which generates the quiz content failed. \
                        Please refresh and try again.",
                        icon="🚨")
                    time.sleep(1)
                st.empty()
        # Change the status information to complete
        status.update(label="Images processed!", state="complete", expanded=False)

    # Return the list of sentences, list of audios, list of quiz words, and number of items as session states
    # as they are not rewritten once the app code reruns like variables
    # (for example after an interaction with a widget) and are valid for the whole session
    st.session_state["quiz_sentences"] = list_of_sentences
    st.session_state["quiz_audios"] = list_of_audios
    st.session_state["quiz_words"] = quiz_words
    st.session_state["number_of_items_quiz"] = number_of_items

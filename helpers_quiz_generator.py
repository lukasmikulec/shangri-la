# import the library for handling API
import requests

# import streamlit to create widgets
import streamlit as st

# import library time to give time for retrying to connect to the API
import time

# import library for saving audio files with unique, timestamped names
from datetime import datetime

# import library to reshuffle quiz items randomly
import random

# load the API KEY from st.secrets (used to authenticate API requests)
api_key = st.secrets["API_KEY"]

# define a function to generate a sentence based on the first word
def generate_sentence(word):
	# define the API url
	url = "https://api-inference.huggingface.co/models/stefan-it/german-gpt2-larger"
	# define the headers for authorization of access to the API
	headers = {'Accept': '*/*',
 'Accept-Encoding': 'identity, deflate, compress, gzip',
 'Authorization': f"Bearer {api_key}",
 'User-Agent': 'python-requests/0.12.1'}
	# set this variable as empty string which will later receive the status message from API
	api_status_sentence_generation = ""
	# set this variable as 0 (no request to API made yet)
	api_sentence_generation_try = 0

	# while API won't return a successful response and the number of retries does not reach 10, keep retrying
	while api_status_sentence_generation != "<Response [200]>" and api_sentence_generation_try != 10:
		api_status_sentence_generation = requests.post(url, headers=headers, json=word)
		# make the format as string, so it can be noticed by the while loop condition
		api_status_sentence_generation = str(api_status_sentence_generation)
		print(api_status_sentence_generation)
		# in case the API request failed, wait for two seconds before retrying
		if api_status_sentence_generation != "<Response [200]>":
			time.sleep(2)
		# increase the number of attempts to reach API by 1
		api_sentence_generation_try += 1

	# if the API connection was successful, do the actual job and get the sentence from a working API
	if api_sentence_generation_try != 10:
		# get the response using the URL, headers, and image data; convert the response into a readable format
		sentence = requests.post(url, headers=headers, json=word).json()
		# get the sentence from the response
		sentence = sentence[0]["generated_text"]
		# only keep the first generated sentence (discard everything after the first dot)
		sentence = sentence[:sentence.find(".")]
		# since the previous step removes the dot as well, add the dot at the end of the sentence
		sentence = sentence + "."
		print(sentence)
		# return the sentence
		return sentence
	# # if the API connection failed, return error to the process function
	else:
		return "ERROR"

# define a text-to-speech function (in German)
def generate_audio(sentence):
	# define the API url
	url = "https://api-inference.huggingface.co/models/facebook/mms-tts-deu"
	# define the headers for authorization of access to the API
	headers = {'Accept': '*/*',
 'Accept-Encoding': 'identity, deflate, compress, gzip',
 'Authorization': f"Bearer {api_key}",
 'User-Agent': 'python-requests/0.12.1'}
	# set this variable as empty string which will later receive the status message from API
	api_status_audio_generation = ""
	# set this variable as 0 (no request to API made yet)
	api_audio_generation_try = 0

	# while API won't return a successful response and the number of retries does not reach 10, keep retrying
	while api_status_audio_generation != "<Response [200]>" and api_audio_generation_try != 10:
		api_status_audio_generation = requests.post(url, headers=headers, json=sentence)
		# make the format as string, so it can be noticed by the while loop condition
		api_status_audio_generation = str(api_status_audio_generation)
		print(api_status_audio_generation)
		# in case the API request failed, wait for two seconds before retrying
		if api_status_audio_generation != "<Response [200]>":
			time.sleep(2)
		# increase the number of attempts to reach API by 1
		api_audio_generation_try += 1

	# if the API connection was successful, do the actual job and get the audio from a working API
	if api_audio_generation_try != 10:
		# get the audio file from the API
		audio = requests.post(url, headers=headers, json=sentence)
		# get the current date and time
		now = datetime.now()
		# format this current date and time into a string suitable for a filename
		formatted_now = now.strftime("%Y-%m-%d-%H-%M-%S")
		# create the filename
		filename = f"data/audio_{formatted_now}.wav"
		# save the audio received from the API under the filename just defined
		with open(filename, "wb") as file:
			file.write(audio.content)
		# return the filename
		return filename
	# # if the API connection failed, return error to the process function
	else:
		return "ERROR"

# put the functions for writing sentences and generating speech from them together
def generate_quiz(word_list):
	# define a variable which will store the list of sentences
	list_of_sentences = []
	# define a variable which will store the number of sentences
	number_of_items = None
	# define a variable which will store the list of audios
	list_of_audios = []

	# define a list in which quiz words will be stored (plural has to go away)
	quiz_words = []

	# define a list in which quiz words in the original order will be stored to display as help for the user
	# to know which words to choose from when answering the question
	quiz_help = []

	# remove the plurals from the generated words and put them into the quiz_words list
	for i in range(len(word_list)):
		# take the German words from the original word list
		word = word_list[i][0]
		# remove the plural form after the comma (removes comma and space too)
		word = word[:word.find(",")]

		# take the value of "word" variable and assign it to quiz helper word (before formatting it for other purposes)
		quiz_helper_word = word

		# take the first letter of the word and capitalize it
		first_letter = word[0].upper()
		# recreate the word with capitalized first letter by putting the capitalized letter and the rest of the
		# word apart from the first letter together
		word = first_letter + word[1:]
		# add the word to the quiz words list to be used in the sentence writing function
		quiz_words.append(word)

		# add the helper word to quiz help list
		quiz_help.append(quiz_helper_word)

	# store the quiz helper words as session state to be accessed later
	st.session_state["quiz_help"] = quiz_help

	# reshuffle the words in list randomly so the user does not know which word is where
	random.shuffle(quiz_words)

	# define percentage as 0 (will be used to display the progress of the function in st.status)
	percentage = 0
	# do everything within a with st.status function to enable display the progress of function to the user
	with st.status(f"Generating the quiz ({percentage}% completed)", expanded=True) as status:
		# define percentage increase as 100 divided by the number of words and this divided by two
		# (each word has two steps - sentence writing and audio generation)
		percentage_increase = round((100 / len(word_list))/2)
		# for as many words as there are
		for i in range(len(word_list)):
			# Check if there are no errors in the list of sentences yet. If not, continue.
			if "ERROR" not in list_of_sentences:
				# get the word you are processing from the list of quiz words
				quiz_word = quiz_words[i]
				# add another percentage increase
				percentage = percentage + percentage_increase
				# display the current percentage state in st.status (after successful step)
				status.update(label=f"Generating the quiz ({percentage-percentage_increase}% completed)")
				# write to the status that a sentence including the word is generated (first part)
				st.write(f"✍️ Writing sentence with the word number {i+1}")
				# get the sentence which includes the word and assign it to a variable sentence
				sentence = generate_sentence(quiz_word)
				# if the API works correctly and does not return an error
				if sentence != "ERROR":
					# add another percentage increase (after successful step)
					percentage = percentage + percentage_increase
					# display the current percentage state in st.status
					status.update(label=f"Generating the quiz ({percentage-percentage_increase}% completed)")
					# write to the status that the audio is being created (second part)
					st.write(f"🎤 Narrating the audio for the sentence number {i+1}")
					# add the sentence to the list
					list_of_sentences.append(sentence)
					# pass audio to the generate audio function
					audio = generate_audio(sentence)
					# if the API works and does not return an error
					if audio != "ERROR":
						# assign the audio to the list of audios
						list_of_audios.append(audio)
					else:
						# otherwise say this item returned an error (due to API error)
						list_of_audios.append("ERROR")
				# otherwise say this item returned an error (due to API error)
				else:
					list_of_sentences.append("ERROR")

		# if there was no error in the process
		if "ERROR" not in list_of_sentences and "ERROR" not in list_of_audios:
			# set the number of items to the actual number of quiz items
			number_of_items = len(word_list)
		# if there was an error in the process
		else:
			# set the number of items to 0, so the display quiz function does not display errors
			number_of_items = 0
			# display an error for 7 seconds informing the user that API connection failed
			with st.empty():
				for i in range(7):
					st.error('The connection to the API which generates the quiz content failed. Please refresh and try again.',
							 icon="🚨")
					time.sleep(1)
				st.empty()
		# change the status information to complete
		status.update(label="Images processed!", state="complete", expanded=False)

	# return the list of sentences, list of audios, list of quiz words, and number of items as session states
	# as they are not rewritten once the app code reruns like variables
	# (for example after an interaction with a widget) and are valid for the whole session
	st.session_state["quiz_sentences"] = list_of_sentences
	st.session_state["quiz_audios"] = list_of_audios
	st.session_state["quiz_words"] = quiz_words
	st.session_state["number_of_items_quiz"] = number_of_items
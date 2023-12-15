# import the library for getting API
import requests

# import the library for accessing environment variables
import os

# import streamlit to create widgets to be displayed in the main app
import streamlit as st

# import library time to give time for retrying to connect to the API
import time

# import library for saving audio files with unique names
from datetime import datetime

# import library to reshuffle quiz items randomly
import random

# load the PONS API KEY from the keys.env to a string variable used for calling the API
api_key = api_key = st.secrets["API_KEY"]

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
		# make the format as string so it can be noticed by the while loop condition
		api_status_sentence_generation = str(api_status_sentence_generation)
		print(api_status_sentence_generation)
		time.sleep(2)
		# increase the number of attempts to reach API by 1
		api_sentence_generation_try += 1

	# if the API connection was successful, do the actual job and get the translation from a working API
	if api_sentence_generation_try != 10:
		# get the response using the URL, headers, and image data; convert the response into a readable format
		sentence = requests.post(url, headers=headers, json=word).json()
		# get the most probable object on the photo according to the model and the label of it
		sentence = sentence[0]["generated_text"]
		# only keep the first generated sentence
		sentence = sentence[:sentence.find(".")]
		sentence = sentence + "."
		print(sentence)
		return sentence
	# # if the API connection failed, return error to the process function
	else:
		return "ERROR"

def generate_audio(sentence):
	# define the API url
	url = "https://api-inference.huggingface.co/models/facebook/mms-tts-deu"
	# define the headers for authorization of access to the API
	headers = {"Authorization": f"Bearer {api_key}"}
	# set this variable as empty string which will later receive the status message from API
	api_status_audio_generation = ""
	# set this variable as 0 (no request to API made yet)
	api_audio_generation_try = 0

	# while API won't return a successful response and the number of retries does not reach 10, keep retrying
	while api_status_audio_generation != "<Response [200]>" and api_audio_generation_try != 10:
		api_status_audio_generation = requests.post(url, headers=headers, json=sentence)
		# make the format as string so it can be noticed by the while loop condition
		api_status_audio_generation = str(api_status_audio_generation)
		print(api_status_audio_generation)
		time.sleep(2)
		# increase the number of attempts to reach API by 1
		api_audio_generation_try += 1

	# if the API connection was successful, do the actual job and get the translation from a working API
	if api_audio_generation_try != 10:
		# get the response using the URL, headers, and image data; convert the response into a readable format
		audio = requests.post(url, headers=headers, json=sentence)
		# get the current date and time
		now = datetime.now()
		# format this current date and time into a string good for the file name
		formatted_now = now.strftime("%Y-%m-%d-%H-%M-%S")
		# create the filename
		filename = f"data/audio_{formatted_now}.wav"
		# save the audio received from the API
		with open(filename, "wb") as file:
			file.write(audio.content)
		# return the filename
		return filename
	# # if the API connection failed, return error to the process function
	else:
		return "ERROR"


# define a variable which will store the list of sentence for each word
list_of_sentences = []
# define a variable which stores the number of sentences
number_of_items = None
# define a variable which will store the list of audios
list_of_audios = []

def generate_quiz(word_list):
	# define a list in which quiz words will be stored (plural has to go away)
	quiz_words = []
	# remove the plurals from the generated words and put them into the quiz_words list
	for i in range(len(word_list)):
		# take the first word from the original word list
		word = word_list[i]
		# remove the plural form after the comma (removes comma and space too)
		word = word[:word.find(",")]
		# take the first letter of the word and capitalize it
		first_letter = word[0].upper()
		# recreate the word with capitalized first letter by putting the capitalized letter and the rest of the
		# word apart from the first letter together
		word = first_letter + word[1:]
		# add the word to the quiz words list to be used in the sentence writing function
		quiz_words.append(word)

	# reshuffle the words in list randomly so the user does not know which word is where
	random.shuffle(quiz_words)


	# define percentage as 0 (will be used to display the progress of the function in st.status)
	percentage = 0
	# do everything within a with st.status function to enable display the progress of function to the user
	with st.status(f"Generating the quiz ({percentage}% completed)", expanded=True) as status:
		# define percentage increase as 100 divided by the number of words and this divided by two
		# (each word has two steps - sentence and audio)
		percentage_increase = round((100 / len(word_list))/2)
		# for as many words as there are
		for i in range(len(word_list)):
			# Check if there are no errors in the list of translations yet. If not, continue.
			if "ERROR" not in list_of_sentences:
				# get the word you are processing from the list of quiz words
				quiz_word = quiz_words[i]
				# add another percentage increase
				percentage = percentage + percentage_increase
				# display the current percentage state in st.status (after successful step)
				status.update(label=f"Generating the quiz ({percentage-percentage_increase}% completed)")
				# write to the status that a sentence including the word is generated (first part)
				st.write(f"Generating sentence with the word number {i+1}")
				# get the sentence which includes the word and assign it to a variable sentence
				sentence = generate_sentence(quiz_word)
				# if the API works correctly and does not return an error
				if sentence != "ERROR":
					# add another percentage increase (after successful step)
					percentage = percentage + percentage_increase
					# display the current percentage state in st.status
					status.update(label=f"Generating the quiz ({percentage-percentage_increase}% completed)")
					# write to the status that the audio is being created (second part)
					st.write(f"Creating audio for the sentence number {i+1}")
					# add the sentence to the list
					list_of_sentences.append(sentence)
					# pass audio to the generate audio function#
					audio = generate_audio(sentence)
					# if the API works and does not return an error
					if audio != "ERROR":
						# assign the translation to the list of translations to be used in the main app
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
		else:
			# set the number of items to 0 so the main app does not show incomplete and error-containing result
			number_of_items = 0
			# display an error for 7 seconds informing the user that API connection failed
			with st.empty():
				for i in range(7):
					st.error('The connection to the API which processes your image failed. Please refresh and try again.',
							 icon="🚨")
					time.sleep(1)
				st.empty()
		# change the status information to complete
		status.update(label="Images processed!", state="complete", expanded=False)

	st.session_state["quiz_sentences"] = list_of_sentences
	st.session_state["quiz_words"] = quiz_words
	st.session_state["number_of_items_quiz"] = number_of_items
	st.session_state["quiz_audios"] = list_of_audios

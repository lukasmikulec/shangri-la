# Import library time to measure time for retrying to connect to the API
import time

# Import the library for handling API
import requests
# Import streamlit to create widgets to be displayed in the main app
import streamlit as st

# Load the API KEY from st.secrets (used to authenticate API requests)
api_key = st.secrets["API_KEY"]


# Define a function to identify the object on an image through AI model
def get_the_object_name(image):
    # Define the API url
    url = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
    # Define the headers for authorization of access to the API
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'identity, deflate, compress, gzip',
               'Authorization': f"Bearer {api_key}",
               'User-Agent': 'python-requests/0.12.1'}
    # Prepare the image to the format readable by API
    image = image.read()
    # Set this variable as empty string which will later receive the status message from API
    api_status_object_analysis = ""
    # Set this variable as 0 (no request to API made yet)
    api_object_analysis_try = 0

    # While API won't return a successful response and the number of retries does not reach 10, keep retrying
    while api_status_object_analysis != "<Response [200]>" and api_object_analysis_try != 10:
        api_status_object_analysis = requests.post(url,
                                                   headers=headers,
                                                   data=image)
        # Make the format as string, so it can be noticed by the while loop condition
        api_status_object_analysis = str(api_status_object_analysis)
        # In case the API request failed, wait for two seconds before retrying
        if api_status_object_analysis != "<Response [200]>":
            time.sleep(2)
        # Increase the number of attempts to reach API by 1
        api_object_analysis_try += 1

    # If the API connection was successful, do the actual job and get the object name from a working API
    if api_object_analysis_try != 10:
        # Get the response using the URL, headers, and image data; convert the response into a readable format (JSON)
        word = requests.post(url,
                             headers=headers,
                             data=image).json()
        # Get the most probable object on the photo according to the model and the label of it
        word = word[0]["label"]
        # If there are multiple words identified on the picture (indicated by comma)
        if "," in word:
            # Split the words and create a list
            word = word.split(",")
            # Take the first item of the list (first word)
            word = word[0]
        # If there is only one word
        else:
            # Nothing else needs to happen
            pass
        # Return the identified object
        return word
    # If the API connection failed
    else:
        # Return error to the process function
        return "ERROR"


# Define a function to translate the object name into German
def get_the_translation(text):
    # Prepare the translation text using the input from the object identifier
    translation_input = f"the {text}, the {text}s"

    # Define the API url
    url = "https://api-inference.huggingface.co/models/facebook/wmt19-en-de"
    # Define the headers for authorization of access to the API
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'identity, deflate, compress, gzip',
               'Authorization': f"Bearer {api_key}",
               'User-Agent': 'python-requests/0.12.1'}

    # Set this variable as empty string which will later receive the status message from API
    api_status_translation = ""
    # Set this variable as 0 (no request to API made yet)
    api_status_translation_try = 0

    # While API won't return a successful response and the number of retries does not reach 10, keep retrying
    while api_status_translation != "<Response [200]>" and api_status_translation_try != 10:
        api_status_translation = requests.post(url, headers=headers, json={
            "inputs": translation_input,
        })
        # Make the format as string, so it can be noticed by the while loop condition
        api_status_translation = str(api_status_translation)
        # In case the API request failed, wait for two seconds before retrying
        if api_status_translation != "<Response [200]>":
            time.sleep(2)
        # Increase the number of attempts to reach API by 1
        api_status_translation_try += 1

    # If the API connection was successful, do the actual job and get the translation from a working API
    if api_status_translation_try != 10:
        # Load the response from the translation model and convert it into a readable format (JSON)
        translation = requests.post(url, headers=headers, json={
            "inputs": translation_input,
        }).json()
        # Get the dictionary item from the list generated by the API
        translation = translation[0]
        # Get the string value from the generated_text parameter
        translation = translation["generated_text"]
        # Return the translation and also the original input
        return translation, translation_input
    # If the API connection failed
    else:
        # Return error to the process function
        return "ERROR"


# Put the functions for analysing objects and then translating them into German together
def process(images):
    # Define a variable which will store the list of translations (pair: English word, German word)
    # for each image uploaded
    list_of_translations = []
    # Define a variable which will store the number of images for main app to know how many items to display
    number_of_items = None

    # Define percentage as 0 (will be used to display the progress of the function in st.status)
    percentage = 0
    # Do everything within a with st.status to enable display of the progress of the function to the user
    with st.status(f"Processing your images ({percentage}% completed)", expanded=True) as status:
        # Define percentage increase as 100 divided by the number of uploaded images and this divided by two
        # (each image has two steps - object identification and translation to German)
        percentage_increase = round((100 / len(images)) / 2)
        # For as many images as the user uploaded
        for i in range(len(images)):
            # Check if there are no errors in the list of translations yet. If not, continue.
            if "ERROR" not in list_of_translations:
                # Get the image you are processing from the list of uploaded images
                image = images[i]
                # Add another percentage increase
                percentage = percentage + percentage_increase
                # Display the current percentage state in st.status (after successful previous step)
                status.update(label=f"Processing your images ({percentage - percentage_increase}% completed)")
                # Write to the status that the object is being identified on the image (first part)
                st.write(f"🔎 Identifying the object on the image *{image.name}*")
                # Get the object name from the picture and assign it to a variable object_name
                object_name = get_the_object_name(image)
                # If the API works correctly and does not return an error
                if object_name != "ERROR":
                    # Add another percentage increase (after successful previous step)
                    percentage = percentage + percentage_increase
                    # Display the current percentage state in st.status
                    status.update(label=f"Processing your images ({percentage - percentage_increase}% completed)")
                    # Write to the status that the translation is being received (second part)
                    st.write(f"📰 Fetching the German name of the object on the image *{image.name}*")
                    # Pass object_name to the translation function and also get the original value
                    translation, original_input = get_the_translation(object_name)
                    # If the API works and does not return an error
                    if translation != "ERROR":
                        # Assign the translation and the original input to the list of translations
                        # to be used in the main app
                        list_of_translations.append([translation, original_input])
                    else:
                        # Otherwise say this item returned an error (due to API error)
                        list_of_translations.append("ERROR")
                # Otherwise say this item returned an error (due to API error)
                else:
                    list_of_translations.append("ERROR")

        # If there was no error in the process
        if "ERROR" not in list_of_translations:
            # Set the number of items to the actual number of images
            number_of_items = len(images)
        # If there was an error in the process
        else:
            # Set the number of items to 0 so the main app does not show incomplete and error-containing result
            number_of_items = 0
            # Display an error message for 7 seconds informing the user that API connection failed
            with st.empty():
                for i in range(7):
                    st.error(
                        'The connection to the API which processes your image failed. Please refresh and try again.',
                        icon="🚨")
                    time.sleep(1)
                st.empty()
        # Change the status information to complete
        status.update(label="Images processed!",
                      state="complete",
                      expanded=False)

    # Return the list of translations and number of items to the main app as session states
    # as they are not rewritten once the app code reruns like variables
    # (for example after an interaction with a widget) and are valid for the whole session
    st.session_state["result"] = list_of_translations
    st.session_state["number_of_items"] = number_of_items

    # This will enable the user to change pages in menu again after this German words generation has finished
    st.session_state["no_menu_changing"] = False

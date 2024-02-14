# Import the library to create the app
import streamlit as st
# Import the library to embed animations
import streamlit.components.v1 as com

# Import the function to generate German words from images
from helpers_process import process
# Import the function to generate txt files, display share and wiktionary buttons
from helpers_small_functions import create_words_txt_file, display_share_button, display_wiktionary_link
# Import the function to generate the quiz
from helpers_quiz_generator import generate_quiz
# Import the function to display quiz
from helpers_quiz_display import display_quiz


# Define a function which will be called after the user submits images (Submit button)
# and which will enable the process of generating German words from images to start
def enable_process():
    # Allow the processing of the images to run
    st.session_state["run_process"] = True
    # Disable the upload and submit button after user clicks Submit
    st.session_state["input_disabled"] = True
    # Disable menu changing by user during the German words generation process to prevent errors
    st.session_state["no_menu_changing"] = True


# Configure the web app
st.set_page_config(page_title="Streetschatz",
                   page_icon="🧭")

# Create keys in session state when the user starts a new user session
if "process_finished" not in st.session_state:
    # This key will track if the process of generating translations finished or not
    st.session_state["process_finished"] = False  # False means it has not run yet

    # This key will disable the upload and submit button once the user clicks the submit button
    st.session_state["input_disabled"] = False  # False means upload and submit button are active

    # This key will enable the German word generation function to run. For now, process function cannot run
    # (user has not uploaded images yet, so we are missing input for the function)
    st.session_state["run_process"] = False

    # User can freely use the menu to change pages because no process is running
    st.session_state["no_menu_changing"] = False

    # No German words were generated (if user goes to quiz page, quiz won't show until at least 3 words
    # were generated)
    st.session_state["number_of_items"] = 0

# Define menu options
menu = ["Identify German words", "Take a quiz", "About"]

# Create a dropdown menu for the sidebar
choice = st.sidebar.selectbox("Mode",
                              menu,
                              disabled=st.session_state["no_menu_changing"])

# Place an image of a treasure box
st.image("images/treasure_box.png",
         width=200)

# If the user chooses the main page for identifying German words (is also the default to display)
if choice == "Identify German words":

    # Place the heading
    st.header("Welcome to Streetschatz",
              divider="blue")

    # Create a column structure for the instructions
    col_1, col_2, col_3 = st.columns(3)

    # Left column (step: upload pictures)
    with col_1:
        # Place an animation through iframe
        com.iframe("https://lottie.host/embed/3aa490a0-3ce7-4bf1-b351-b9012e3d45c6/f4vXV46B9x.json")
        # Place text
        st.markdown("1. Upload pictures of objects from your everyday life to Streetschatz.")

    # Middle column (step: generate German words)
    with col_2:
        # Place an animation through iframe
        com.iframe("https://lottie.host/embed/bd0c1bf9-fd98-4e3e-b274-b2c46d713249/Mq1sACVbDe.json")
        # Place text
        st.markdown("2. Get their German names automatically.")

    # Right column (step: use quiz)
    with col_3:
        # Place an animation through iframe
        com.iframe("https://lottie.host/embed/bdf526e9-4daa-4b7c-a996-e3c2c3e9d5c3/Z6Ak0D0AMw.json")
        # Place text
        st.markdown("3. Upload 3 or more images to take a quiz after upload (left sidebar).")

    # Let user upload images to get the German names of objects on them at the end
    uploaded_photos = st.file_uploader("Upload your photos",
                                       type=["jpg", "png", "jpeg"],
                                       help="Make sure your photos are in jpg, png, or jpeg format.",
                                       accept_multiple_files=True,
                                       # This is dynamically managed based on whether the user clicked on submit images
                                       # or not yet. If they did, button will be disabled.
                                       disabled=st.session_state.input_disabled)

    # When the user uploaded photos
    if len(uploaded_photos) != 0:
        # Offer them a button to start the process and end the ability to change the files to uploaded
        st.button("Submit",
                  on_click=enable_process,
                  disabled=st.session_state.input_disabled)

    # If the user clicked on the Submit button
    if st.session_state["run_process"] == True:

        # If the content was not yet processed, run the process function
        if "result" not in st.session_state:
            process(uploaded_photos)
            # Save the uploaded photos as a session state key to display images after user returns from other pages too
            st.session_state["uploaded_photos"] = uploaded_photos
        # If the process function already processed the content (if the result of it is saved in session state)
        else:
            # Do nothing (this prevents the process function from being rerun when user clicks on the
            # download txt button - this has to do with the fact that after each widget interaction, Streamlit
            # reruns the whole code from the top to bottom again)
            pass

        # Add a divider
        st.divider()

        # This part of the code will display the results of the process function

        # For as many images as the user uploaded, display that many items
        for i in range(st.session_state["number_of_items"]):
            # Create a column structure
            c1, c2 = st.columns(2)

            # Left column
            with c1:
                # Display the original word
                st.markdown(st.session_state["result"][i][1])
                # Display the output of the process function (the German name of the object on the picture)
                st.header(st.session_state["result"][i][0])
                # Display Share on X button
                display_share_button(st.session_state["result"][i][0])
                # Display the link to Wiktionary
                display_wiktionary_link(st.session_state["result"][i][0])

            # Right column
            with c2:
                # Display the image from the user for that word
                st.image(st.session_state["uploaded_photos"][i])
            # Add a divider
            st.divider()

        # This is where the display code ends

        # If this is after running the process function
        if st.session_state["process_finished"] == False:
            # After the process of generating translations finishes, set the key in session state to True
            st.session_state["process_finished"] = True
            # Rerun the whole script to update the status of the selectbox (unlock it after the process run)
            # based on the new value of st.session_state["no_menu_changing"]
            st.rerun()

        # If the process of generating translations finished already, show the download txt file button
        if st.session_state["process_finished"] == True:
            # Assign the output of the txt generating function to this variable
            file = create_words_txt_file(st.session_state["result"])
            # Open this file variable for interaction
            with open(file, "rb") as f:
                # Show download button for the user
                st.download_button("📥 Download words as a txt file",
                                   data=f,
                                   file_name="words.txt")
        # If translations were not yet generated
        else:
            # Do not display the txt download button
            pass

        # If 3 or more images were uploaded, inform the user that they can use the quiz functionality
        if st.session_state["number_of_items"] >= 3 and "turn_toast_off" not in st.session_state:
            # Display the pop-up notification
            st.toast("3 or more images! Take a quiz in the left menu!",
                     icon="🎉")
            # Highlight the place in sidebar where user can go to quiz
            # Show the highlighting only until the next interaction with the page
            with st.empty():
                st.sidebar.markdown("⬆️ Take the quiz here! ⬆️")
                st.sidebar.empty()
            # Even if user comes back to the page from other pages or interacts with a widget, do not show
            # the quiz notification after it was once displayed again
            st.session_state["turn_toast_off"] = True
        # If less than 3 images were uploaded
        else:
            # Do not notify about the quiz
            pass
    # If fewer than 3 images were uploaded
    else:
        # Wait for the user to upload the images
        pass

# If the user chooses the quiz page
elif choice == "Take a quiz":
    # Place the heading
    st.header("Welcome to Streetschatz Quiz",
              divider="blue")

    # If less than 3 images are uploaded, show that at least 3 are required for quiz to be generated
    if st.session_state["number_of_items"] < 3:
        st.info("To use the quiz function, please upload at least 3 images.",
                icon="ℹ️")
    # If 3 or more images are uploaded and German words generated
    else:
        # If the quiz was not yet generated, run the generate quiz function
        if "quiz_sentences" not in st.session_state:
            generate_quiz(st.session_state["result"])

        # Run the function which displays the quiz
        display_quiz()

# If the user chooses the about page
elif choice == "About":
    # Place the heading
    st.header("About Streetschatz",
              divider="blue")

    # Place subheader
    st.subheader("What is Streetschatz about?")
    # Place text
    st.markdown("""
        Have you ever wanted to call an object by its German name among
        your German friends but couldn't? Streetschatz is an app which
        allows you to upload 📤 pictures of everyday projects and instantly
        get their German 🥨 names. In addition, you can use the Quiz function
        to better learn 📖 those new words for your everyday conversations.
        You can also download 📥 the words or sentences with those words as
        a txt file for future reference.
        """)

    # Place subheader
    st.subheader("Why the name Streetschatz?")
    # Place text
    st.markdown("""
            Schatz means treasure in German, so Streetschatz means finding
            treasures (new German words) on the street.
            """)

    # Place subheader
    st.subheader("Who created Streetschatz?")
    # Place text
    st.markdown("""
                Streetschatz was created by <a href="https://github.com/lukasmikulec">Lukas Mikulec</a> as part of his
                Practical experience in Digital Media II course at Leuphana
                University of Lüneburg in Major Digital Media.
                
                View the <a href="https://github.com/lukasmikulec/shangri-la">code on Github</a>.
                """,
                unsafe_allow_html=True)

    # Place subheader
    st.subheader("What powers Streetschatz?")
    # Place text
    st.markdown("""
                    Streetschatz runs on <a href="https://streamlit.io/cloud">Streamlit Cloud</a>, \
                    uses <a href="https://streamlit.io">Streamlit Python library</a> for its UI and is powered \
                    by four AI models on <a href="https://huggingface.co/">Hugging Face</a>. Namely:
* <a href="https://huggingface.co/google/vit-base-patch16-224">google/vit-base-patch16-224</a> for object \
identification on uploaded pictures
* <a href="https://huggingface.co/facebook/wmt19-en-de">facebook/wmt19-en-de</a> for translating English \
words into German
* <a href="https://huggingface.co/stefan-it/german-gpt2-larger">stefan-it/german-gpt2-larger</a> for writing \
German sentences
* <a href="https://huggingface.co/facebook/mms-tts-deu">facebook/mms-tts-deu</a> for creating audios of \
German sentences in the quiz
                    """,
                unsafe_allow_html=True)

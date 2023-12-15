# import the library to create the app
import streamlit as st

# import library to embed animations
import streamlit.components.v1 as com

# import the function to get the translation
from helpers_process import process

# import the function to display quiz
from helpers_quiz_display import display_quiz

# import the function to generate txt files, display share and wiktionary buttons
from helpers_small_functions import create_words_txt_file, display_share_button, display_wiktionary_link

# import the function to generate the quiz
from helpers_quiz_generator import generate_quiz


# define a function which will be called after the user submits images (Submit button)
def enable_process():
    # this session state key change will allow the processing of the images to run
    st.session_state["run_process"] = True
    # this session state key change will disable the upload and submit button after user clicks Submit
    st.session_state["input_disabled"] = True
    # disable menu changing during the translation generation process to prevent errors
    st.session_state["no_menu_changing"] = True


# configure the web app
st.set_page_config(page_title="Streetschatz", page_icon="🧭")

# create keys in session state
# when the user starts a new user session
if "process_finished" not in st.session_state:
    # this key will track if the process of generating translations finished or not
    # False means it has not run yet
    st.session_state["process_finished"] = False

    # this key will disable the upload and submit button once the user clicks the submit button.
    # False means upload and submit button are active.
    st.session_state["input_disabled"] = False

    # this key will enable the process function to be run. For now, process function cannot run (user has not
    # no uploaded images yet so we are missing input for the function.
    st.session_state["run_process"] = False

    # the user can freely use the menu
    st.session_state["no_menu_changing"] = False

    st.session_state["number_of_items"] = 0

# define menu options
menu = ["Identify German words", "Take a quiz", "About"]

# create a dropdown menu for the sidebar
choice = st.sidebar.selectbox("Mode", menu, disabled=st.session_state["no_menu_changing"])

# place an image of a treasure box
st.image("images/treasure_box.png", width=200)

# if the user chooses the main page for identifying German words (is also the default to display)
if choice == "Identify German words":

    # place the heading
    st.header("Welcome to Streetschatz", divider="blue")

    # create a column structure
    col_1, col_2, col_3 = st.columns(3)

    with col_1:
        com.iframe("https://lottie.host/embed/3aa490a0-3ce7-4bf1-b351-b9012e3d45c6/f4vXV46B9x.json")
        st.markdown("1. Upload pictures of objects from your everyday life to Streetschatz.")

    with col_2:
        com.iframe("https://lottie.host/embed/bd0c1bf9-fd98-4e3e-b274-b2c46d713249/Mq1sACVbDe.json")
        st.markdown("2. Get their German names automatically.")

    with col_3:
        com.iframe("https://lottie.host/embed/bdf526e9-4daa-4b7c-a996-e3c2c3e9d5c3/Z6Ak0D0AMw.json")
        st.markdown("3. Upload 3 or more images to take a quiz after upload (left sidebar).")

    # let user upload images to get the German names of objects on them at the end
    uploaded_photos = st.file_uploader("Upload your photos", type=["jpg", "png", "jpeg"],
                                       help="Make sure your photos are in jpg, png, or jpeg format.",
                                       accept_multiple_files=True,
                                       disabled=st.session_state.input_disabled) # this is dynamically managed based on
                                        # whether the user clicked on submit images or not yet. If they did, button
                                        # will be disabled

    # when the user uploaded photos
    if len(uploaded_photos) != 0:
        # offering them a button to start the process and end the ability to change the files to uploaded
        st.button("Submit",on_click=enable_process,disabled=st.session_state.input_disabled)

    # if the user clicked on the Submit button
    if st.session_state["run_process"] == True:

        # if the content was not yet processed, run the process function
        if "result" not in st.session_state:
            process(uploaded_photos)
            # save the uploaded photos as a session state key to display images after user returns from other pages
            st.session_state["uploaded_photos"] = uploaded_photos
        # if the process function already processed the content (if the result of it is saved in session states)
        else:
            # do nothing (this prevents the process function from being rerun when a user clicks on the
            # download txt button - this has to do with the fact that after each widget interaction, Streamlit
            # reruns the whole code from the top to bottom again)
            pass

        # add a divider
        st.divider()

        # this part of the code will display the results of the process function

        # for as many images as the user uploaded, display that many items
        for i in range(st.session_state["number_of_items"]):
            # create a column structure
            c1, c2 = st.columns(2)

            with c1:
                # display the output of the process function (the German name of the object on the picture)
                st.markdown(st.session_state["result"][i][1])
                st.header(st.session_state["result"][i][0])
                display_share_button(st.session_state["result"][i][0])
                display_wiktionary_link(st.session_state["result"][i][0])

            with c2:
                # display the image from the user
                st.image(st.session_state["uploaded_photos"][i])
            # add a divider
            st.divider()

        # this is where the display code ends

        # if this is the first time running the process
        if st.session_state["process_finished"] == False:
            # after the process of generating translations finishes, set the key in session state to True
            st.session_state["process_finished"] = True
            # rerun the whole script to update the status of the selectbox (unlock it after the process run)
            # based on the new value of st.session_state["no_menu_changing"]
            st.rerun()

        # if the process of generating translations finished already, show the download txt file button
        if st.session_state["process_finished"] == True:
            # assign the output of the txt generating function to this variable
            file = create_words_txt_file(st.session_state["result"])
            # open this file variable for interaction
            with open(file, "rb") as f:
                # show download button for the user
                st.download_button("📥 Download words as a txt file", data=f, file_name="words.txt")
        # if translations were not yet generated, do not display the txt download button
        else:
            pass


        # if 3 or more images were uploaded, inform the user they can use the Quiz functionality
        if st.session_state["number_of_items"] >= 3 and "turn_toast_off" not in st.session_state:
            # display the pop-up notification
            st.toast("3 or more images! Take a quiz in the left menu!", icon="🎉")
            with st.empty():
                st.sidebar.markdown("⬆️ Take the quiz here! ⬆️")
                st.sidebar.empty()
            st.session_state["turn_toast_off"] = True
        else:
            pass
    else:
        # wait for the user to upload the images
        pass

# if the user chooses the quiz page
elif choice == "Take a quiz":
    # place the heading
    st.header("Welcome to Streetschatz Quiz", divider="blue")

    if st.session_state["number_of_items"] < 3:
        st.info("To use the quiz function, upload at least 3 images.", icon="ℹ️")
    else:
        # if the quiz was not yet generated, run the generate quiz
        if "quiz_sentences" not in st.session_state:
            generate_quiz(st.session_state["result"])

        display_quiz()

# if the user chooses the about page
elif choice == "About":
    # place the heading
    st.header("About Streetschatz", divider="blue")
    # place the about text
    st.markdown("This is the about page.")

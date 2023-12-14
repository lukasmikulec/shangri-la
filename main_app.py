# import the library to create the app
import streamlit as st

# import the function to get the translation
from helpers_process import process

# import the function to generate txt files out of the result
from helpers_small_functions_and_quiz_display import write_into_a_txt_file, display_share_button, display_quiz

from helpers_quiz_generator import generate_quiz

# define a function which will be called after the user submits images (Submit button)
def enable_process():
    # this session state key change will allow the processing of the images to run
    st.session_state["run_process"] = True
    # this session state key change will disable the upload and submit button after user clicks Submit
    st.session_state["input_disabled"] = True

# function that will unlock the select box in the sidebar
def unlock_quiz():
    st.session_state["no_menu_changing"] = False

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

    # this key disables the quiz functionality until at least 3 images have been uploaded and processed
    # do not allow user to change the mode to quiz until user uploads 3 or more images
    st.session_state["no_menu_changing"] = True

# define menu options
menu = ["Streetschatz", "Streetschatz Quiz"]

# create a dropdown menu for the sidebar
choice = st.sidebar.selectbox("Mode", menu, disabled=st.session_state["no_menu_changing"])
st.sidebar.markdown("To change mode to Streetschatz Quiz, upload at least 3 images.")

# place an image of a treasure box
st.image("images/treasure_box.png", width=200)

# if the user chooses Streetschatz page (is also the default to display)
if choice == "Streetschatz":

    # place the heading
    st.header("Welcome to Streetschatz", divider="blue")

    # display text
    st.markdown("Let's get the names of those treasures of Alltag!")

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
                st.header(st.session_state["result"][i])
                display_share_button(i)

            with c2:
                # display the image from the user
                st.image(st.session_state["uploaded_photos"][i])
            # add a divider
            st.divider()

        # this is where the display code ends

        # after the process of generating translations finishes, set the key in session state to True
        st.session_state["process_finished"] = True

        # if the process of generating translations finished already, show the download txt file button
        if st.session_state["process_finished"] == True:
            # assign the output of the txt generating function to this variable
            file = write_into_a_txt_file(st.session_state["result"])
            # open this file variable for interaction
            with open(file, "rb") as f:
                # show download button for the user
                st.download_button("Download words as a txt file", data=f, file_name="words.txt")
        # if translations were not yet generated, do not display the txt download button
        else:
            pass

        # if 3 or more images were uploaded, inform the user they can use the Quiz functionality
        if st.session_state["number_of_items"] >= 3:
            # display the pop-up notification
            st.toast("3 or more images! You can take a quiz by changing the mode in menu on left!", icon="🎉")
            st.button("Unlock quiz feature", on_click=unlock_quiz)
        else:
            pass
    else:
        # wait for the user to upload the images
        pass

# if the user chooses Streetschatz Quiz page
elif choice == "Streetschatz Quiz":
    # place the heading
    st.header("Welcome to Streetschatz Quiz", divider="blue")

    # if the quiz was not yet generated, run the generate quiz
    if "quiz_sentences" not in st.session_state:
        generate_quiz(st.session_state["result"])

    display_quiz()

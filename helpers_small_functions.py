# Import the library to interact with the GUI
import streamlit as st
# Import module which enables working with HTMl that will display X share button
import streamlit.components.v1 as components


# Define a function which will create a txt file with the German object words that user can download
def create_words_txt_file(list_of_translations):
    # Open a new txt file in a variable and allow for writing
    file = open("words.txt", "w")
    # Write a German-English pair, leave space, and repeat until all word-pairs have been written
    for i in range(len(list_of_translations)):
        file.write(f"DE: {list_of_translations[i][0]}\nEN: {list_of_translations[i][1]}\n\n")
    # Close the file so it can be downloaded
    file.close()
    # Return the name of the file to the download button in the main app
    return "words.txt"


# Define a function which will show the X share button
def display_share_button(word):
    # Use the components module to be able to embed X HTML code for X sharing button
    components.html(
        f"""
            <a href="https://twitter.com/share?ref_src=twsrc%5Etfw"
            class="twitter-share-button"
            data-text="Did you know the German name of this everyday object?

{word}

"
            data-url="streetschatz.streamlit.app"
            data-hashtags="Streamschatz"
            data-lang="en"
            data-show-count="false">Tweet</a><script
            async src="https://platform.twitter.com/widgets.js"
            charset="utf-8"></script>
        """
    )


# Define a function which will display a link to Wiktionary
def display_wiktionary_link(word):
    # Split the whole string into a list of words
    words = word.split()
    # Select the second word (the actual term in singular which comes after the article)
    term = words[1]
    # Remove the comma at the end
    term = term[:-1]
    # Display the button with dynamically created URL
    st.link_button("🔗 View more on Wikitionary", f"https://en.wiktionary.org/wiki/{term}#German")


# Define a function which will create a txt file with the quiz sentences
def create_sentences_txt_file(list_of_sentences):
    # Open a new txt file in a variable and allow for writing
    file = open("sentences.txt", "w")
    # Write one sentence on one line, leave space, and repeat until all sentences have been written
    for i in range(len(list_of_sentences)):
        file.write(f"{i+1}. {list_of_sentences[i]}\n\n")
    # Close the file so it can be downloaded
    file.close()
    # Return the name of the file to the download button in the quiz summary tab
    return "sentences.txt"

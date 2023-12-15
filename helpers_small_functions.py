import streamlit as st

# import module which enables working with HTMl that will display X share button
import streamlit.components.v1 as components

# define a function which will create a txt file with the German object words that user can download
def create_words_txt_file(list_of_translations):
    # open a new txt file in a variable and allow for writing
    file = open("words.txt", "w")
    # write one object on one line and repeat until all words have been written
    for i in range(len(list_of_translations)):
        file.write(f"DE: {list_of_translations[i][0]}\nEN: {list_of_translations[i][1]}\n\n")
    # close the file so it can be downloaded
    file.close()
    # return the name of the file to the download button in the main app
    return "words.txt"

# define a function which will show the X share button
def display_share_button(word):
    # use the components module to be able to embed X HTML code for X sharing button
    components.html(
        f"""
            <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-text="Did you know the German name of this everyday object? {word}" data-url="https://www.leuphana.de/" data-hashtags="Streamschatz" data-lang="en" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        """
    )

# define a function which will display a link to Wikitonary
def display_wiktionary_link(word):
    # split the whole string into a list of words
    words = word.split()
    # select the second word (the actual term which comes after the article)
    term = words[1]
    # remove the comma at the end
    term = term[:-1]
    # display the button
    st.link_button("🔗 View more on Wikitionary", f"https://en.wiktionary.org/wiki/{term}#German")


# define a function which will create a txt file with the quiz sentences
def create_sentences_txt_file(list_of_sentences):
    # open a new txt file in a variable and allow for writing
    file = open("sentences.txt", "w")
    # write one object on one line and repeat until all words have been written
    for i in range(len(list_of_sentences)):
        file.write(f"{i+1}. {list_of_sentences[i]}\n\n")
    # close the file so it can be downloaded
    file.close()
    # return the name of the file to the download button in the main app
    return "sentences.txt"
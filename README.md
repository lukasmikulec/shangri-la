# shangri-la

## What is Streetschatz about?
Have you ever wanted to call an object by its German name among your German friends but couldn't? <a href="https://streetschatz.streamlit.app/">Streetschatz</a> is an app which allows you to upload 📤 pictures of everyday projects and instantly get their German 🥨 names. In addition, you can use the Quiz function to better learn 📖 those new words for your everyday conversations. You can also download 📥 the words or sentences with those words as a txt file for future reference.

## Why the name Streetschatz?
Schatz means treasure in German, so Streetschatz means finding treasures (new German words) on the street.


## Who created Streetschatz?
Streetschatz was created by <a href="https://github.com/lukasmikulec">Lukas Mikulec</a> as part of his Practical experience in Digital Media II course at Leuphana University of Lüneburg in Major Digital Media.
                
The full code is available here on GitHub.

## What powers Streetschatz?
Streetschatz runs on <a href="https://streamlit.io/cloud">Streamlit Cloud</a>, uses <a href="https://streamlit.io">Streamlit Python library</a> for its UI and is powered by four AI models on <a href="https://huggingface.co/">Hugging Face</a>. Namely:
* <a href="https://huggingface.co/google/vit-base-patch16-224">google/vit-base-patch16-224</a> for object identification on uploaded pictures
* <a href="https://huggingface.co/facebook/wmt19-en-de">facebook/wmt19-en-de</a> for translating English words into German
* <a href="https://huggingface.co/stefan-it/german-gpt2-larger">stefan-it/german-gpt2-larger</a> for writing German sentences
* <a href="https://huggingface.co/facebook/mms-tts-deu">facebook/mms-tts-deu</a> for creating audios of German sentences in the quiz

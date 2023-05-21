from flask import Flask, request, render_template
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

app = Flask(__name__)

#I Load the Spacy model and stop words
nlp = spacy.load('en_core_web_sm')
stopwords = list(STOP_WORDS)
punctuation = punctuation + '\n'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    #text = request.form['text']
    text = request.form.get('text')
    #if text is None:
    #    return "Invalid request"

    percentage = int(request.form['percentage'])
    # Process the text
    doc = nlp(text)
    tokens = [token.text for token in doc]
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    select_length = int(len(sentence_tokens)*percentage/100)
    #if select_length < 1:
    #    return "You can't summarize up to this percentage. Please change your percentage."

    summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    # Calculate word count for input and output text
    input_word_count = len(text.split())
    output_word_count = len(summary.split())

    #if output_word_count == 1:
    #    return "You can't summarize up to this percentage. Please change your percentage."

    return summary



if __name__ == '__main__':
    app.run(debug=True)


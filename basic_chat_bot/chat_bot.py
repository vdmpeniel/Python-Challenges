import numpy
import nltk
import string
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

lemmer = nltk.stem.WordNetLemmatizer()
greeting_inputs = ('hello', 'hi', 'greetings', 'sup', 'what\'s up', 'hey', 'hi there')
greeting_responses = ['hi', 'hey', '*nods*', 'hi there', 'hello', 'I am glad you are talking to me!']
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
sent_tokens = None
word_tokens = None


# Defining the greeting function
def greet(sentence):
    if sentence.lower() in greeting_inputs:
        return random.choice(greeting_responses)


# Text preprocessing
# Wordnet is a semantically-oriented dictionary of English included in NLTK
def lem_tokens(tokens):
    global lemmer
    return [lemmer.lemmatize(token) for token in tokens]


def lem_normalize(text):
    return lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Response generation
def get_response(user_response):
    global sent_tokens, word_tokens
    vectorizer = TfidfVectorizer(tokenizer=lem_normalize, stop_words='english')
    fit_transform = vectorizer.fit_transform(sent_tokens)
    values = cosine_similarity(fit_transform[-1], fit_transform)
    index = values.argsort()[0][-2]
    flat = values.flatten()
    flat.sort()
    required_tfidf = flat[-2]
    return "I am sorry! I didn't get that." if required_tfidf == 0 else sent_tokens[index]


def import_and_read_corpus():
    global sent_tokens, word_tokens
    # Importing and reading the corpus
    file = open('chatbot.txt', 'r', errors='ignore')
    raw_doc = file.read()
    raw_doc = raw_doc.lower()  # converts text to lowercase
    nltk.download('omw-1.4')
    nltk.download('punkt')  # Using the Punk tokenizer
    nltk.download('wordnet')  # Using the Wordnet dictionary
    sent_tokens = nltk.sent_tokenize(raw_doc)  # Converts document to list of sentences
    word_tokens = nltk.word_tokenize(raw_doc)  # Converts document to list of words

    print(sent_tokens[:2])
    print(word_tokens[:2])


def say(message):
    print(f'Bot: {message}')


def define_conversation_protocol():
    global sent_tokens, word_tokens
    print("Bot: My name is Stark. Let's have a conversation!")
    print('You can exit at any time just by saying "Bye"')

    while True:
        message = ''
        user_response = input()
        user_response = user_response.lower()
        if user_response == 'bye':
            break

        elif user_response in {'thanks', 'thank you'}:
            message = 'You are welcome'

        elif greet(user_response) is not None:
            message = greet(user_response)

        else:
            sent_tokens.append(user_response)
            word_tokens += nltk.word_tokenize(user_response)
            final_words = list(set(word_tokens))
            message = get_response(user_response)
            sent_tokens.remove(user_response)

        say(message)

    say('Good bye! Take care.')


def main():
    import_and_read_corpus()
    define_conversation_protocol()








            


if __name__ == '__main__':
    main()
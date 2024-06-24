import datetime
from flask import Flask, render_template, request, redirect, url_for, make_response, Response, stream_with_context, jsonify
from google.cloud import firestore
from prompts import special_prompt
import uuid
from bot import ChatBot
import time
import os



# Ensure environmental variables are set
if not os.getenv("GCP_PROJECT_ID"):
    raise ValueError("GCP project not found. Please set the GCP_PROJECT_ID environment variable in app.yaml.")
if not os.getenv("FIRESTORE_DB"):
    raise ValueError("Firestore database not found. Please set the FIRESTORE_DB environment variable in app.yaml.")

# create Flask app
app = Flask(__name__)

# create Firestore client
db = firestore.Client(project=os.getenv("GCP_PROJECT_ID"), database=os.getenv("FIRESTORE_DB"))

# create a reference to the Firestore collection
sessions = db.collection('sessions')

@firestore.transactional
def get_session_data(transaction, session_id):
    """ Looks up (or creates) the session with the given session_id."""

    print("session_id before test", session_id)
    if session_id in (None, ""):
        session_id = str(uuid.uuid4())   # Random, unique identifier

    doc_ref = sessions.document(document_id=session_id)
    doc = doc_ref.get(transaction=transaction)
    if doc.exists:
        session = doc.to_dict()
    else:
        session = {
            'messages': 0
        }

    session['messages'] += 1
    transaction.set(doc_ref, session)
    session['session_id'] = session_id
    return session

def store_data(session_id, user_id, message, sender, history):
    """Stores message in Firestore."""

    # create a reference to the Firestore collection
    collection_ref = db.collection('messages')

    # prepare data to store in Firestore
    data = {
        'session_id': session_id,
        'user_id': user_id,
        'timestamp': datetime.datetime.now(),
        'message': message,
        'sender': sender,
        'history': history
    }

    # add the data to the Firestore collection
    collection_ref.add(data)

def fetch_data(limit, session_id):
    """Fetches recent messages from Firestore."""

    # get messages from Firestore
    collection_ref = db.collection('messages')

    # reverse order and get newest messages
    query = collection_ref.where(
        "session_id", "==", session_id).order_by(
        'timestamp', direction=firestore.Query.DESCENDING).limit(limit)
    messages = query.stream()

    return messages

def proportional_sleep(message, sleep_per_char=0.1):
    """"Sleeps for a time proportional to the length of the message."""
    message_length = len(message)
    sleep_time = message_length * sleep_per_char
    time.sleep(sleep_time)


@app.route('/', methods=['GET'])
def root():
    """Shows the main page."""
    response = make_response(render_template('index.html'))
    response.headers['Set-Cookie'] = 'session_id=""; HttpOnly; expires=Thu, 01 Jan 1970 00:00:00 UTC'
    return response

@app.route('/process_message', methods=['GET', 'POST'])
def process_message():

    # get user id
    user_id = request.form['user_id']
    print("user_id", user_id)

    # get session data
    transaction = db.transaction()
    session = get_session_data(transaction, request.cookies.get('session_id'))
    print(session)


    # instantiate ChatBot
    bot = ChatBot()

    # Store the current access time in Datastore.
    if request.method == 'POST':

        # get user input from chat window
        chat_content = request.form['chat_window']
        print("chat_content", chat_content)

        # swap in special prompt
        if chat_content == "#special":
            bot.user_input(special_prompt)
            bot_response = bot.run_bot()

        # this is what usually happens
        else:
            try:
                messages = fetch_data(1, session['session_id'])
                history = next(messages).to_dict()["history"]
                bot = ChatBot()
                bot.set_messages(history)
                print("history retrieved...")
            except Exception as e:
                print(e)

            # feed user input to bot
            bot.user_input(chat_content)

            # store user input in Datastore
            store_data(session_id=session['session_id'], user_id=user_id, message=chat_content, sender="user",
                       history=bot.messages)

            # this can be used to keep the bot on track
            bot.reminder("Remember to keep the conversation going.")

            # run on new user input and get response
            bot_response = bot.run_bot()

            # end concersation after a specified number of turns
            try:
                if len(history) >= 50:
                    bot_response = "Thank you for the conversation. Please return to the survey. Your confirmation code is 12345."
            except Exception as e:
                print(e)

            # store bot response input in Datastore
            store_data(session_id=session['session_id'], user_id=user_id, message=bot_response, sender="gpt",
                       history=bot.messages)

        # delay response to simulate thinking
        # proportional_sleep(bot_response, sleep_per_char=0.01)

        # print for app logs
        print(bot.messages[2:])
        print("session_id", session['session_id'])
        print("from cookie", request.cookies.get('session_id'))

        # prepare response to send back to chat window
        response = make_response(jsonify({'bot_response': bot_response}))
        response.headers['Set-Cookie'] = 'session_id=' + session['session_id'] + '; HttpOnly'
        return response



if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)
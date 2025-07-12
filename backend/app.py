from rag_pipeline import generate_answer
from flask import Flask, request, jsonify, send_from_directory, session
from datetime import datetime, timezone
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
import os
from uuid import uuid4

app = Flask(__name__, static_folder='../frontend', static_url_path='/frontend')
app.secret_key = 'sakhi123!@#'
CORS(app)



# Serve index.html (login page)
@app.route('/')
def serve_index():
    return send_from_directory('../frontend/pages', 'landing.html')

# Connect to MongoDB
client = MongoClient('MONGO_URI') #here replace your mongodb_uri
db = client['mentalhealth']
users_collection = db['users']

# Login POST Route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')

    user = users_collection.find_one({'username': username})
    if user:
        if bcrypt.checkpw(password, user['password']):
            session['username'] = username 
            return '''
              <script>
                alert("Login Successful!");
                window.location.href = "/frontend/pages/choose.html";
              </script>
            '''
        else:
            return '''
              <script>
                alert("Incorrect password!");
                window.location.href = "/";
              </script>
            '''
    else:
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
        users_collection.insert_one({'username': username, 'password': hashed_pw})
        session['username'] = username 
        return '''
          <script>
            alert("User registered and logged in!");
            window.location.href = "/frontend/pages/choose.html";
          </script>
        '''

# Serve choose.html, chat.html, mood.html
@app.route('/<page>')
def serve_pages(page):
    valid_pages = ['landing.html', 'index.html', 'choose.html', 'chatbot.html', 'moodtracker.html']
    if page in valid_pages:
        return send_from_directory('../frontend/pages', page)
    return "Page Not Found", 404

# Serve static assets (JS, images, etc.)
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('../frontend/assets', filename)

@app.route('/styles/<path:filename>')
def serve_styles(filename):
    return send_from_directory('../frontend/styles', filename)

# Chatbot API (same as before)
@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '').strip()

    username = session.get('username')
    if not username:
        return jsonify({'error': 'User not logged in'}), 401

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    answer = generate_answer(question)

    # Get or generate session ID
    session_id = data.get('session_id')
    if not session_id:
        session_id = str(datetime.now(timezone.utc).timestamp())
    session['current_session_id'] = session_id

    timestamp = datetime.now(timezone.utc)

    # Save chat messages
    db['chats'].insert_many([
        {
            'username': username,
            'session_id': session_id,
            'sender': 'user',
            'message': question,
            'timestamp': timestamp
        },
        {
            'username': username,
            'session_id': session_id,
            'sender': 'bot',
            'message': answer,
            'timestamp': timestamp
        }
    ])

    # 💡 Save session info (needed for Recent Chats!)
    db['chat_sessions'].update_one(
        {'session_id': session_id, 'username': username},
        {'$set': {'last_activity': timestamp}},
        upsert=True
    )

    return jsonify({'answer': answer})

@app.route('/api/new_session', methods=['POST'])
def new_session():
    session_id = str(datetime.now(timezone.utc).timestamp())
    session['current_session_id'] = session_id
    return jsonify({'session_id': session_id})

@app.route('/api/get_sessions', methods=['GET'])
def get_sessions():
    username = session.get('username')
    if not username:
        return jsonify({'error': 'User not logged in'}), 401

    sessions = db['chats'].aggregate([
        {'$match': {'username': username}},
        {'$sort': {'timestamp': 1}},  # oldest message first
        {'$group': {
            '_id': '$session_id',
            'first_message': {'$first': '$message'},
            'last_activity': {'$max': '$timestamp'}
        }},
        {'$sort': {'last_activity': -1}}
    ])

    sessions_list = [{
        'session_id': s['_id'],
        'preview': s['first_message'][:30] if s['first_message'] else 'New Chat',
        'last_activity': s['last_activity'].strftime('%Y-%m-%d %H:%M:%S')
    } for s in sessions]

    return jsonify(sessions_list)


@app.route('/api/get_chats', methods=['GET'])
def get_chats():
    username = session.get('username')
    session_id = request.args.get('session_id')

    if not username:
        return jsonify({'error': 'User not logged in'}), 401
    if not session_id:
        return jsonify({'error': 'Session ID missing'}), 400

    chats = list(db['chats'].find({
        'username': username,
        'session_id': session_id
    }).sort('timestamp', 1))

    for chat in chats:
        chat['_id'] = str(chat['_id'])
        chat['timestamp'] = chat['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

    return jsonify(chats)

@app.route('/api/delete_session', methods=['DELETE'])
def delete_session():
    username = session.get('username')
    session_id = request.args.get('session_id') 

    if not username:
        return jsonify({'error': 'User not logged in'}), 401
    if not session_id:
        return jsonify({'error': 'Session ID is required'}), 400

    db['chats'].delete_many({'username': username, 'session_id': session_id})
    db['chat_sessions'].delete_one({'username': username, 'session_id': session_id})

    return jsonify({'message': 'Session deleted successfully.'})




@app.route('/api/delete_chats', methods=['DELETE'])
def delete_chats():
    username = session.get('username')
    if not username:
        return jsonify({'error': 'User not logged in'}), 401

    result = db['chats'].delete_many({'username': username})
    return jsonify({'message': f'{result.deleted_count} messages deleted.'})


@app.route('/api/log_mood', methods=['POST'])
def log_mood():
    username = session.get('username')  
    if not username:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.get_json()
    mood = data.get('mood')

    if not mood:
        return jsonify({'error': 'Mood not provided'}), 400

    
    db['moods'].insert_one({
        'username': username,
        'mood': mood,
        'timestamp': datetime.now(timezone.utc)
    })

    return jsonify({'message': f"Your mood '{mood}' has been logged. Thank you, {username}!"}), 200

@app.route('/api/get_moods', methods=['GET'])
def get_moods():
    username = session.get('username')
    if not username:
        return jsonify({'error': 'User not logged in'}), 401

    moods = list(db['moods'].find({'username': username}).sort('timestamp', -1))

    for m in moods:
        m['_id'] = str(m['_id'])  
        m['timestamp'] = m['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

    return jsonify(moods)


@app.route('/get_user')
def get_user():
    username = session.get('username')
    return jsonify({'username': username})


if __name__ == '__main__':
    app.run(debug=True)

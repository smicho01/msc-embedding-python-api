from flask import Flask, request, jsonify
from functools import wraps
from utils import generate_embedding  # Import the function from utils.py
import os
from mongo_utils import *

app = Flask(__name__)

# In-memory storage for simplicity
data_storage = []

# Set a simple auth token (in a real app, store securely)
API_TOKEN = os.getenv('API_TOKEN', 'my_secure_api_token')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-tokens')
        if not token or token != API_TOKEN:
            return jsonify({"message": "Token is missing or invalid"}), 401
        return f(*args, **kwargs)

    return decorated


def convert_object_id(document):
    """ Convert Mongo ObjectId to string for JSON serialization [fixes serialization error] """
    document['_id'] = str(document['_id'])
    return {'questionId': document['questionId'], 'question': document['question']}


#-------------------------------------- API -------------------------------------#
@app.route('/embedding', methods=['POST'])
@token_required
def create_embedding():
    data = request.json
    embedding = generate_embedding(data['text'])
    return jsonify(embedding), 201


@app.route('/embedding/mongostore', methods=['POST'])
@token_required
def create_embedding_mongo_store():
    """
    It is used to create an embedding mongo store by generating an embedding for a given question
    and storing it in the database [here MongoDb Atlas]

    :return: JSON response containing the Mongo ID, question ID, question text, and question embedding.
    """
    data = request.json
    questionId = data['questionId']
    question = data['question']
    question_embedding = generate_embedding(question)  # create the embeddings
    record = {
        'questionId': questionId,
        'question': question,
        'question_embedding': question_embedding
    }
    insertId = mongo_insert_record(record)
    return jsonify({'mongoId': str(insertId), 'questionId': questionId, 'question': question,
                    'question_embedding': question_embedding}), 201


@app.route('/embedding/search', methods=['GET'])
@token_required
def search_embedding_mongo_store():
    """
    Returns the similar questions from the MongoDB store based on the provided question.
    It compares vectors when doing the search.

    :return: A dictionary containing the similar questions.
    """
    data = request.json
    question = data['question']
    question_embedding = generate_embedding(question)
    results = mongo_search_similar_questions(question_embedding)
    data = [convert_object_id(doc) for doc in results]

    return jsonify(data), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9050, debug=True)

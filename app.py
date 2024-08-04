# Install:
# pip3 install tensorflow
# pip3 install python-dotenv
# pip3 install torch torchvision
# pip3 install flask-cors

from flask import Flask, request, jsonify
from functools import wraps
import os
import logging
import apputils as au
from flask_cors import CORS

# Create app
app = Flask(__name__)
CORS(app)

# Create a StreamHandler for logging
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
app.logger.addHandler(stream_handler)

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


# -------------------------------------- API ------------------------------------- #
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    app.logger.info('Called /healthcheck')
    print('Called /healthcheck')
    mongoCollectionName = os.environ.get('MONGO_COLLECTION', "can't get cool name form env variable")
    response = {
        "status": "HEALTHY",
        "mongoCollection": mongoCollectionName
    }
    return jsonify(response), 200


@app.route('/embedding', methods=['POST'])
@token_required
def create_embedding():
    app.logger.info('Called /embedding')
    print('Called /embedding')
    data = request.json
    embedding = au.generate_embedding(data['text'])
    return jsonify(embedding), 201


@app.route('/embedding/mongostore', methods=['POST'])
@token_required
def create_embedding_mongo_store():
    app.logger.info('Called /embedding/mongostore')
    print('Called /embedding/mongostore')
    """
    It is used to create an embedding mongo store by generating an embedding for a given question
    and storing it in the database [here MongoDb Atlas]

    :return: JSON response containing the Mongo ID, question ID, question text, and question embedding.
    """
    data = request.json
    questionId = data['questionId']
    question = data['question']
    question_embedding = au.generate_embedding(question)  # create the embeddings
    record = {
        'questionId': questionId,
        'question': question,
        'question_embedding': question_embedding
    }
    insertId = au.mongo_insert_record(record)
    return jsonify({'mongoId': str(insertId), 'questionId': questionId, 'question': question,
                    'question_embedding': question_embedding}), 201


@app.route('/embedding/search', methods=['POST'])
@token_required
def search_embedding_mongo_store():
    app.logger.info('Called /embedding/search')
    print('Called /embedding/search')
    """
    Returns the similar questions from the MongoDB store based on the provided question.
    It compares vectors when doing the search.

    :return: A dictionary containing the similar questions.
    """
    data = request.json
    question = data['question']
    limit = request.args.get('limit', default=5, type=int)
    question_embedding = au.generate_embedding(question)
    results = au.mongo_search_similar_questions(question_embedding, limit)
    data = [convert_object_id(doc) for doc in results]

    return jsonify(data), 200


@app.route('/validatetext', methods=['POST'])
@token_required
def check_if_text_is_english():
    app.logger.info('Called /valudatetext')
    print('Called /validatetext')
    data = request.json
    text = data['text']
    isValid = au.check_text(text)
    return jsonify({'valid': isValid}), 200


@app.route('/toxicity', methods=['POST'])
@token_required
def check_text_toxicity():
    app.logger.info('Called /toxicity')
    print('Called /toxicity')
    data = request.json
    toxicity_score = au.get_text_toxicity_score(data['text'])
    return jsonify({'score': toxicity_score}), 201


@app.route('/validate/question', methods=['POST'])
@token_required
def validate_question():
    app.logger.info('Called /validate/question')
    print('Called /validate/question')
    data = request.json
    title = data['title']
    body = data['body']

    is_valid_english_title = au.check_text(title)
    is_valid_english_body = au.check_text(body)

    toxicity_score_title = au.get_text_toxicity_score(title)
    toxicity_score_body = au.get_text_toxicity_score(body)

    return jsonify(
        {
            'valid_english_title': is_valid_english_title,
            'valid_english_body': is_valid_english_body,
            'toxicity_score_title': toxicity_score_title,
            'toxicity_score_body': toxicity_score_body
        }
    ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9050, debug=True)

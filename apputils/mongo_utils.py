import pymongo
import os

mongo_connection_string = os.getenv('MONGO_CONN_STRING', 'mongodb://localhost:27017/')
search_limits_count = int(os.getenv('SEARCH_LIMITS_COUNT', 5))

client = pymongo.MongoClient(mongo_connection_string)
db = client.mscstudents
collection = db.questions


def mongo_insert_record(record):
    result = collection.insert_one(record)
    return result.inserted_id


def mongo_search_similar_questions(queryEmbedding):
    results = collection.aggregate([
        {"$vectorSearch": {
            "queryVector": queryEmbedding,
            "path": "question_embedding",
            "numCandidates": 100,
            "limit": search_limits_count,
            "index": "QuestionSematicSearchIndex",
        }}
    ])
    return results

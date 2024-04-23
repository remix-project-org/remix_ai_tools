import requests
import pandas as pd
from sentence_transformers import SentenceTransformer
import pymongo
from tqdm import tqdm 
tqdm.pandas()

embedding_model = SentenceTransformer("thenlper/gte-large")
mongo_uri = "mongodb://127.0.0.1:27017/?directConnection=true"

def get_embedding(text: str) -> list[float]:
    if not text.strip():
        print("Attempted to get embedding for empty text.")
        return []

    embedding = embedding_model.encode(text)

    return embedding.tolist()

def get_mongo_client(mongo_uri):
    """Establish connection to the MongoDB."""
    try:
        client = pymongo.MongoClient(mongo_uri)
        print("Connection to MongoDB successful")
        return client
    except pymongo.errors.ConnectionFailure as e:
        print(f"Connection failed: {e}")
        return None
    
def vector_search(user_query, collection, limit=4, vector_name="vector_index_cos"):
    """
    Perform a vector search in the MongoDB collection based on the user query.

    Args:
    user_query (str): The user's query string.
    collection (MongoCollection): The MongoDB collection to search.

    Returns:
    list: A list of matching documents.
    """

    # Generate embedding for the user query
    query_embedding = get_embedding(user_query)

    if query_embedding is None:
        return "Invalid query or embedding generation failed."

    # Define the vector search pipeline
    pipeline = [
        {
            "$vectorSearch": {
                "index": vector_name, # vector_index_cos
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 300,  # Number of candidate matches to consider
                "limit": limit,  # Return top 4 matches
            }
        },
        {
            "$project": {
                "_id": 0,  # Exclude the _id field
                "content": 1,  # Include the plot field
                "filename": 1,  # Include the title field
                "contractName": 1,  # Include the genres field
                "score": {"$meta": "vectorSearchScore"},  # Include the search score
            }
        },
    ]

    # Execute the search
    results = collection.aggregate(pipeline)
    return list(results)

def get_search_result(query, collection, limit=4, vector_name="vector_index_cos"):

    get_knowledge = vector_search(query, collection, limit, vector_name)

    search_result = ""
    for result in get_knowledge:
        search_result += f"#{result.get('filename', 'N/A')}\n{result.get('content', 'N/A')}\n"

    return search_result


def main():
    try:
        data = pd.read_csv('/cookbook/cookbook_audited_data.csv')

        if "embedding" not in data.columns:
            data["embedding"] = data["content"].progress_apply(get_embedding)

        data = data.drop(columns=["details", "sources", "_id", "createdAt", "updatedAt", "__v"])

        mongo_client = get_mongo_client(mongo_uri)

        # Ingest data into MongoDB
        db = mongo_client["Audited_contracts"]
        collection = db["contracts"]
        
        # Delete any existing records in the collection
        collection.delete_many({})
        documents = data.to_dict("records")
        collection.insert_many(documents)

    except Exception as ex: 
        print('Error:', ex)
        raise ex
    
if __name__=='main':
    main()
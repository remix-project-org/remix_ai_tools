import os, requests, json
from dotenv import load_dotenv

load_dotenv()
elastic_endpoint = os.environ["ELASTIC_HOSTNAME"]
elastic_apikey = os.environ["ELASTI_API_KEY"]

#print(elastic_apikey, elastic_endpoint)

def get_relevant_solidity_topics(user_prompt, k=3):
    x = requests.post(elastic_endpoint + "/_search",
        json={  "query" : {
    "query_string" : {
      "query" : user_prompt,
      "fields": ["body_content", "url"],
    }
  }, 
  "sort":["_score"],
  "size" : 10
        }, headers={"Content-Type": "application/json", "Authorization": "ApiKey " + elastic_apikey}).json()
    
    # with open('data.json', 'w') as f:
    #     json.dump(x, f)

    matching_url = []
    max_k = k if x["hits"]["total"]["value"]>=k else x["hits"]["total"]["value"]
    for d in range(max_k):
        matching_url.append([[x["hits"]["hits"][d]["_source"]["url"], x["hits"]["hits"][d]["_source"]["title"]], x["hits"]["hits"][d]["_source"]["body_content"]])
        print('INFO: found URL - ', x["hits"]["hits"][d]["_source"]["url"])

    return matching_url

if __name__=="__main__":
    get_relevant_solidity_topics('test')
import os, requests, json
from dotenv import load_dotenv
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('-c', '--search_index', type=str, default=None, help='The elastic search index name')
parser.add_argument('-a', '--get_all', action='store_true', default=False, help='Whether to grap al the data')
parser.add_argument('-f', '--fname', type=str, default='./data_ES.json', help='Where to save the result as json file')

load_dotenv()
elastic_endpoint = os.environ["ELASTIC_HOSTNAME"]
elastic_apikey = os.environ["ELASTI_API_KEY"]

#print(elastic_apikey, elastic_endpoint)

def get_ES_all(fname):
    x = requests.post(elastic_endpoint + "/search*/_search",
            json={  "query" : {
                "match_all" : {}
                }, 
                "size" : 10000
                },
            headers={"Content-Type": "application/json", "Authorization": "ApiKey " + elastic_apikey}
        ).json()
    
    with open(fname, 'w') as f:
        json.dump(x, f)

def main():
    args=parser.parse_args()

    if args.get_all:
        get_ES_all(args.fname)


if __name__=='__main__':
    main()
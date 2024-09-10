import sys
sys.path.append('./')
import json 
import pandas as pd
from utils.utils import conn, elastic_vector_store, get_embedding, TextNode, VectorDBRetriever
from utils.utils import soldoc_db_name

file_to_process = "./solidity_doc/data_ES.json"
def main():
    try:
        print('INFO: Ingesting data ...')
        with conn.cursor() as c:
            print('INFO creating database ...')
            c.execute(f"DROP DATABASE IF EXISTS {soldoc_db_name}")
            c.execute("DROP EXTENSION IF EXISTS vector")
            c.execute(f"CREATE DATABASE {soldoc_db_name}")
            c.execute("CREATE EXTENSION vector")

        # read data in 
        with open(file_to_process, 'r') as f:
            rd = json.load(f)['hits']['hits']
        entries = []
        for e in rd:
            entries.append(e['_source'])
        data = pd.DataFrame(entries)
        data = data[data['url_path_dir1'] != 'tr'] # remove turkish language
        data = data[data['url_path_dir1'] != 'zh'] # remove chinese language

        data['embedding'] = data["body_content"].progress_apply(get_embedding)

        nodes = []
        for _, row in data.iterrows():
            node = TextNode(text=row.body_content, metadata={'url':row.url, 'title':row.title})
            node.embedding=row.embedding
            nodes.append(node)

        elastic_vector_store.add(nodes)

    except Exception as ex:
        raise ex

def test():
    query_str = "Explaining the modifiers in solidity"
    retriever = VectorDBRetriever(elastic_vector_store, query_mode="default", similarity_top_k=2)
    results = retriever.retrieve(query_str)
    idx = 0
    print(results[idx].node.get_content())
    print(results[idx].score, results[idx].score)

if __name__=='__main__':
    main()
    test()

    
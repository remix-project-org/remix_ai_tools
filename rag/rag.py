import json
import pandas as pd
from tqdm import tqdm
from rag.utils.utils import conn, cookbook_db_name, get_embedding, TextNode, VectorDBRetriever, rag_vector_store


def main():
    try:
        print('INFO: Ingesting data ...')
        with conn.cursor() as c:
            print('INFO creating database ...')
            c.execute(f"DROP DATABASE IF EXISTS {cookbook_db_name}")
            c.execute("DROP EXTENSION IF EXISTS vector")
            c.execute(f"CREATE DATABASE {cookbook_db_name}")
            c.execute("CREATE EXTENSION vector")

        data = pd.read_csv('./cookbook/cookbook_audited_data.csv')
        nodes = []
        for _, row in tqdm(data.iterrows(), total=len(data), desc='getting nodes'):
            node = TextNode(text=row.content)
            node.embedding=json.loads(row.embedding)
            nodes.append(node)
        
        rag_vector_store.add(nodes)
        print('INFO: Added vectors to DB')

    except Exception as ex: 
        print('Error:', ex)
        raise ex
    
def test():
    query_str = "Write a SimpleERC20 contract"
    query_embedding = get_embedding(query_str)

    query_mode = "default"
    # query_mode = "sparse"
    # query_mode = "hybrid"

    retr = VectorDBRetriever(rag_vector_store, query_mode, similarity_top_k=5)
    query_result = retr.retrieve(query_str)

    #query_result = rag_vector_store.query(rag_vector_store_query)
    print(query_result[0].node.get_content())
          
    
if __name__=='__main__':
    main()
    test()
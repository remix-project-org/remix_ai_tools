import json
import psycopg2, json
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores import VectorStoreQuery
import psycopg2
from llama_index.vector_stores.postgres import PGVectorStore

from llama_index.core.schema import NodeWithScore
from typing import Optional
from tqdm import tqdm 
tqdm.pandas()
from sentence_transformers import SentenceTransformer

from llama_index.core import QueryBundle
from llama_index.core.retrievers import BaseRetriever
from typing import Any, List

embedding_model = SentenceTransformer("thenlper/gte-large")
query_mode = "default"

soldoc_db_name = "remix_soldoc_vector_db"
cookbook_db_name = "remix_vector_db"
host = "localhost"
password = "remix"
port = "5432"
user = "remix"

conn = psycopg2.connect(
    dbname="postgres",
    host=host,
    password=password,
    port=port,
    user=user,
)
conn.autocommit = True

rag_vector_store = PGVectorStore.from_params(
    database=cookbook_db_name,
    host=host,
    password=password,
    port=port,
    user=user,
    table_name="cookbook_idx",
    embed_dim=1024
)

elastic_vector_store = PGVectorStore.from_params(
    database=soldoc_db_name,
    host=host,
    password=password,
    port=port,
    user=user,
    table_name="solidity_doc",
    embed_dim=1024
)

def is_rag_initialized(db_name):
    with conn.cursor() as c:
        c.execute(f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        result = c.fetchone()
        return False if result is None else True
    
def get_embedding(text: str) -> list[float]:
    if not text.strip():
        print("Attempted to get embedding for empty text.")
        return []

    embedding = embedding_model.encode(text)
    return embedding.tolist()

class VectorDBRetriever(BaseRetriever):
    """Retriever over a postgres vector store."""

    def __init__(
        self,
        vector_store: PGVectorStore,
        query_mode: str = "default",
        similarity_top_k: int = 2,
    ) -> None:
        """Init params."""
        self._vector_store = vector_store
        self._query_mode = query_mode
        self._similarity_top_k = similarity_top_k
        super().__init__()

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Retrieve."""
        query_embedding = get_embedding(
            query_bundle.query_str
        )
        vector_store_query = VectorStoreQuery(
            query_embedding=query_embedding,
            similarity_top_k=self._similarity_top_k,
            mode=self._query_mode,
        )
        query_result = self._vector_store.query(vector_store_query)

        nodes_with_scores = []
        for index, node in enumerate(query_result.nodes):
            score: Optional[float] = None
            if query_result.similarities is not None:
                score = query_result.similarities[index]
            nodes_with_scores.append(NodeWithScore(node=node, score=score))

        return nodes_with_scores

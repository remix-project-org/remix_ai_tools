# RAG for code completion and further tasks
The RAG is meant for enhancing the LLM outputs. 


## Setup local Postgres Database
```bash
sudo apt install postgresql-client postgresql postgresql-contrib
sudo apt install -y postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
sudo apt install postgresql-14-pgvector
service postgresql start

psql postgres  # or su postgres
CREATE ROLE remix WITH LOGIN PASSWORD 'remix';
ALTER ROLE remix SUPERUSER;
ALTER ROLE remix CREATEDB;

```


## Populating the Database
First download the data freeze located [here](https://drive.google.com/file/d/1IS2vf6rAyaXNnjNZi3Z_Vjc1wpiK7Gyt/view?usp=share_link) to the *cookbook* folder and run 

```bash 
mkdir cookbook
cd cookbook
gdown <link>
cd ..
python rag.py
```

Or simply create other data sources and use the `rag.py` script to populate the database with latest informations.

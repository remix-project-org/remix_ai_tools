# RAG for code completion and further tasks


## Setup local Postgres Database
```bash
psql postgres 
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

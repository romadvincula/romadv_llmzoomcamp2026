uv init
uv add requests minsearch openai jupyter python-dotenv
uv add sentence-transformers
uv add sqlitesearch

Section: Vector Search with PGVector

docker run -it \
    --name pgvector \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=pswd \
    -e POSTGRES_DB=faq \
    -v pgvector_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    pgvector/pgvector:pg17
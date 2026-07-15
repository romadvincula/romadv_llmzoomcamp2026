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

## Week 5: Monitoring

- Setup docker network for postgres and grafana
docker network create monitoring

- Start PostgreSQL with a volume for data persistence and connect it to the network:

docker run -it \
    --name course-assistant-pg \
    --network monitoring \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=course_assistant \
    -p 5432:5432 \
    -v pgdata:/var/lib/postgresql/data \
    postgres:17

- To reach Postgres from Python, we install the psycopg driver:

uv add "psycopg[binary]"


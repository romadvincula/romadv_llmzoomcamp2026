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

- run sql query to the course_assistant db
docker exec -it course-assistant-pg psql -U user -d course_assistant \
    -c "SELECT id, question, response_time, cost FROM conversations ORDER BY timestamp DESC LIMIT 5;"

- run script to generate fake data
uv run python generate_data.


- Grafana Response Time Panel query:
SELECT
  timestamp AS time,
  response_time
FROM conversations
WHERE timestamp BETWEEN $__timeFrom() AND $__timeTo()
ORDER BY timestamp

- Grafana Token Usage Panel query:
SELECT
  $__timeGroup(timestamp, $__interval) AS time,
  AVG(total_tokens) AS avg_tokens
FROM conversations
WHERE timestamp BETWEEN $__timeFrom() AND $__timeTo()
GROUP BY 1
ORDER BY 1

- Grafana Cost Panel query:
SELECT
  $__timeGroup(timestamp, $__interval) AS time,
  SUM(cost) AS total_cost
FROM conversations
WHERE timestamp BETWEEN $__timeFrom() AND $__timeTo()
  AND cost > 0
GROUP BY 1
ORDER BY 1

- Grafana Model Usage Panel query:
SELECT
  model,
  COUNT(*) as count
FROM conversations
WHERE timestamp BETWEEN $__timeFrom() AND $__timeTo()
GROUP BY model

- Grafana Relevance Usage Panel query:
SELECT
  relevance,
  COUNT(*) as count
FROM feedback
WHERE source = 'judge'
  AND timestamp BETWEEN $__timeFrom() AND $__timeTo()
GROUP BY relevance

- Grafana User Feedback Panel query:
SELECT
  SUM(CASE WHEN score > 0 THEN 1 ELSE 0 END) as thumbs_up,
  SUM(CASE WHEN score < 0 THEN 1 ELSE 0 END) as thumbs_down
FROM feedback
WHERE source = 'user'
  AND timestamp BETWEEN $__timeFrom() AND $__timeTo()

- Grafana Recent Conversations Panel query:
SELECT
  timestamp AS time,
  question,
  answer,
  response_time,
  cost
FROM conversations
WHERE timestamp BETWEEN $__timeFrom() AND $__timeTo()
ORDER BY timestamp DESC
LIMIT 5


- project layout
code/
├── docker-compose.yaml
├── Dockerfile
├── .env
├── pyproject.toml
├── uv.lock
├── .python-version
├── app.py           # Streamlit app
├── assistant.py     # RAG pipeline + LLM
├── db_init.py       # Database init
├── db_save.py       # Save conversations
└── dashboard.py     # Streamlit dashboard


- start everything using docker-compose
docker-compose up

- initialize db
docker-compose up

- stop services
docker-compose down
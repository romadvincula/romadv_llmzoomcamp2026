
run:
	uv run python assistant.py

chat:
	uv run streamlit run app.py

network:
	docker network create monitoring

postgres: network
	docker run -it \
		--name course-assistant-pg \
		--network monitoring \
		-e POSTGRES_USER=user \
		-e POSTGRES_PASSWORD=password \
		-e POSTGRES_DB=course_assistant \
		-p 5432:5432 \
		-v pgdata:/var/lib/postgresql/data \
		postgres:17

cleanup-docker:
	docker rm grafana
	docker rm course-assistant-pg
	docker network rm monitoring

db-init:
	uv run python db_init.py

dashboard:
	uv run streamlit run dashboard.py --server.port 8502

grafana:
	docker run -it \
		--name grafana \
		--network monitoring \
		-p 3000:3000 \
		-v grafana_data:/var/lib/grafana \
		grafana/grafana
docker compose exec asset-service alembic upgrade head
docker compose exec forecast-service alembic upgrade head
docker compose exec trading-service alembic upgrade head

python dev/import_fixtures.py fixtures/assets

bash dev/update_forecasts.sh

python dev/export_static_api.py

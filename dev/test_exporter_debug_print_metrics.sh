cd observability
docker compose exec test-exporter \
  python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/metrics').read().decode())"
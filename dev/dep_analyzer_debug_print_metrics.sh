cd observability
docker compose exec dependency-analyzer \
  python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/health').read().decode())"
docker compose exec dependency-analyzer \
  python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/api/dependencies/asset-service').read().decode())"

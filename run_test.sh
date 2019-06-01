pipenv install ./
docker pull redis
docker run --name some-redis -p 6379:6379 -d redis redis-server --appendonly yes 

pipenv run python pytest

# Ensure Webserver is killed
kill $(pgrep python)
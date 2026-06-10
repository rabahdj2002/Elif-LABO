release: bash railway-deploy.sh
web: cd elif_universe && gunicorn elif_platform.wsgi --log-file -
worker: cd elif_universe && celery -A elif_platform worker -l info
beat: cd elif_universe && celery -A elif_platform beat -l info

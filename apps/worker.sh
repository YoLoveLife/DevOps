export C_FORCE_ROOT="true"
python manage.py celery worker --broker='django://' --loglevel=info &

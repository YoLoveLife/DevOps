export C_FORCE_ROOT="true"
celery -A deveops worker --loglevel=debug -B
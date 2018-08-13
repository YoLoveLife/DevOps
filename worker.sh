export C_FORCE_ROOT="true"
export PYTHONOPTIMIZE=1
celery -A deveops worker --loglevel=debug -B
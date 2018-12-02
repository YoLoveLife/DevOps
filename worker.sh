export C_FORCE_ROOT="true"
export PYTHONOPTIMIZE=1
/storage02/python-deveops/bin/celery -A deveops worker --loglevel=debug -B
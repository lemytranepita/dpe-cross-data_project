all:
	( \
	. venv/bin/activate; 					\
	python main_batch.py;				\
	)

install:
	( \
	python -m venv venv; 					\
	. venv/bin/activate; 					\
	python -m pip install --upgrade pip;	\
	pip install psycopg2;				\
	)
all:
	( \
	. venv/bin/activate; 					\
	python main_batch.py;					\
	deactivate;								\
	)

install:
	( \
	python -m venv venv; 					\
	. venv/bin/activate; 					\
	python -m pip install --upgrade pip;	\
	pip install psycopg2;					\
	deactivate;								\
	)

clean:
	rm -rf venv
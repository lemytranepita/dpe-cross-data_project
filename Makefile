all:
	( \
	. venv/bin/activate; 					\
	./dl_dvf.sh;							\
	python clean_dvf_csv.py;				\
	python dpe_sql_to_csv.py;				\
	python clean_dpe_csv.py;				\
	python correlation_sans_id.py;		    \
	python analyse_fichier_merge.py;		\
	python modelisation_predictive.py;		\
	deactivate;								\
	)

install:
	( \
	python -m venv venv; 					\
	. venv/bin/activate; 					\
	python -m pip install --upgrade pip;	\
	pip install psycopg2 pandas unidecode scipy seaborn matplotlib catboost scikit-learn;					\
	deactivate;								\
	)

clean:
	rm -rf venv files correlation nettoyage catboost_info correlation
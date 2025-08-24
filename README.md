# DPE Cross Data Project

## Summary

This project aims at unifying DPE (Diagnostic de Performance Energetique) and DVF (Demande de Valeur Fonciere) in order to provide data about how DPE influences the real estate prices.

## Program steps

- dl_dvf.sh: Download DVF data from the official website, extract it and put it in a single CSV file
- clean_dvf_csv.py: Clean the previous DVF file
- dpe_sql_to_csv.py: Extract a CSV file with all DPE records in the database
- clean_dpe_csv.py: Clean the previous DPE file
- correlation_sans_id.py: Will correlate DPE and DVF datasets based on address recognition, create barplot and boxplot graphs
- modelisation_predictive.py: Create a CatBoost model and computes MAE, RMSE and R2

## Prerequisites

In order to import one of the sources that is available as a Postgres dump, you need to have Postgres installed on your machine.

You will also need about 400GB of available space on your hard drive to be able to download, decompress and import one of the sources.

You can delete the dump as well as its decompressed version afterwards, thus needing only about 200GB.

We suppose PostgreSQL is running on the same machine as the main program, using localhost port 5432 and user 'postgres'.

Feel free to enter your own PostgreSQL remote server in the 'dpe_sql_to_csv.py' file, default is localhost.

## Commands

### DPE source aquisition

```sh
# Download the PostgreSQL dump from the official website
wget https://opendata.ademe.fr/dump_dpev2_prod_fdld.sql.gz

# Decompress the dump
gunzip dump_dpev2_prod_fdld.sql.gz

# Import the dump into your PostgreSQL instance
psql -U postgres -d dpe -f dump_dpev2_prod_fdld.sql # This might take up to a few hours, depending on your machine.
```

### Installing the virtual environment

This command installs the required dependencies for Python in a virtual environment:

```sh
make install
```

### Launch program

This command will launch the entire program (download, extract, cross sources, etc.):

```sh
make
```

### Clean virtual environment files

This command removes all temporary, downloaded or generated files from the folder:

```sh
make clean
```

### Disclaimer

You might need to modify the Makefile to use 'python3' instead of 'python', depending on your operating system.
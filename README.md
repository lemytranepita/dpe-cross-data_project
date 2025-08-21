# DPE Cross Data Project

## Summary

This project aims at unifying DPE (Diagnostic de Performance Energetique) and DVF (Demande de Valeur Fonciere) in order to provide data about how DPE influences the real estate prices.

## Prerequisites

In order to import one of the sources that is available as a Postgres dump, you need to have Postgres installed on your machine.

You will also need about 400GB of available space on your hard drive to be able to download, decompress and import one of the sources.

You can delete the dump as well as its decompressed version afterwards, thus needing only about 200GB.

## Commands

### DPE source aquisition

```sh
# Download the PostgreSQL dump from the official website
wget https://opendata.ademe.fr/dump_dpev2_prod_fdld.sql.gz

# Decompress the dump
gunzip dump_dpev2_prod_fdld.sql.gz

# Import the dump into your PostgreSQL instance
psql -U postgres -d dpe -f dump_dpev2_prod_fdld.sql # This will take up to a few hours, depending on your machine.
```

### Installing the virtual environment

```sh
make install
```

### Launch program

```sh
make
```

### Other...


# Steps to launch the virtual environment:
1) Create a new virtual environment with Python 3.8.5
`python -m venv venv`
2) Activate the virtual environment
`source venv/bin/activate`
3) Upgrade pip and install Jupyter
`python -m pip install --upgrade pip`
`python -m pip install notebook`
4) Start Jupyter Notebook
`jupyter notebook`
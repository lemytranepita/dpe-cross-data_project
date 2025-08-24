# DPE Cross Data Project

## Summary

This project aims at unifying DPE (Diagnostic de Performance Energetique) and DVF (Demande de Valeur Fonciere) in order to provide data about how DPE influences the real estate prices.

## Prerequisites

In order to import one of the sources that is available as a Postgres dump, you need to have Postgres installed on your machine.

You will also need about 400GB of available space on your hard drive to be able to download, decompress and import one of the sources.

You can delete the dump as well as its decompressed version afterwards, thus needing only about 200GB.

We suppose PostgreSQL is running on the same machine as the main program, using localhost port 5432 and user 'postgres'.

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

This command installs 

```sh
make install
```

### Launch program

This command will launch 

```sh
make
```

### Clean virtual environment files

```sh
make clean
```
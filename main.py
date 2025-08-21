import csv
import psycopg2
import time

# Connection to the Postgres DB
conn = psycopg2.connect(
    dbname="dpe",
    user="postgres",
    password="your_password",
    host="localhost",  # or your DB host
    port="5432"        # default PostgreSQL port
)

cur = conn.cursor()
i = 0
with open('DVF_maison_vente.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')  # Specify semicolon as separator
    for row in reader:
        # Remove Bis, Ter, etc. that would be hard to identify in the DPE file.
        if row['B/T/Q']:
            continue

        # Get all needed fields from DVF file
        code_postal = (5-len(row['Code postal'])) * '0' + row['Code postal']
        ville = row['Commune']
        code_departement = row['Code departement']
        numero_de_voie = row['No voie']
        type_de_voie = row['Type de voie']
        nom_de_voie = row['Voie'].replace('\'', '')

        #print(code_postal, ville, code_departement, numero_de_voie, type_de_voie, nom_de_voie)

        # Your SQL query
        sql = f"""
        SELECT 
            d.identifiant_dpe AS numero_dpe,
            d.date_etablissement_dpe,
            a.ban_label AS adresse_complete,
            a.ban_postcode AS code_postal,
            a.ban_city AS ville,
            bc.classe_conso_energie AS score_dpe,
            bc.classe_emission_ges AS score_ges
        FROM dpe d
        JOIN dpe_administratif da ON da.dpe_id = d.id
        JOIN dpe_geolocalisation g ON administratif_id = da.dpe_id
        JOIN dpe_t_adresse a ON a.id = g.adresse_bien_id
        JOIN dpe_bilan_consommation bc ON bc.dpe_id = d.id
        WHERE a.ban_postcode = '{code_postal}'
        AND a.ban_label ILIKE '{numero_de_voie}%{nom_de_voie}%'
        ORDER BY d.date_etablissement_dpe DESC
        LIMIT 1;
        """

        cur.execute(sql)

        # Fetch the first row
        row = cur.fetchone()

        if row:
            i += 1
            numero_dpe, date_etablissement_dpe, adresse_complete, code_postal, ville, score_dpe, score_ges = row
            print(i)
            print("DVF=", code_postal, ville, code_departement, numero_de_voie, type_de_voie, nom_de_voie)
            print("DPE=", numero_dpe, date_etablissement_dpe, adresse_complete, code_postal, ville, score_dpe, score_ges)
        else:
            print("No results found.", i)
            print("DVF=", code_postal, ville, code_departement, numero_de_voie, type_de_voie, nom_de_voie)

        if i == 10:
            exit(0)


cur.close()
conn.close()
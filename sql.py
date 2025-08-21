import psycopg2

# Connect to your database
conn = psycopg2.connect(
    dbname="dpe",
    user="postgres",
    password="your_password",
    host="localhost",  # or your DB host
    port="5432"        # default PostgreSQL port
)

cur = conn.cursor()

# Your SQL query
sql = """
SELECT 
    d.identifiant_dpe AS numero_dpe,
    d.date_etablissement_dpe,
    a.ban_label AS adresse_complete,
    a.label_brut_avec_complement AS adresse_brute,
    a.ban_postcode AS code_postal,
    a.ban_city AS ville,
    bc.classe_conso_energie AS score_dpe,
    bc.classe_emission_ges AS score_ges
FROM dpe d
JOIN dpe_administratif da ON da.dpe_id = d.id
JOIN dpe_geolocalisation g ON administratif_id = da.dpe_id
JOIN dpe_t_adresse a ON a.id = g.adresse_bien_id
JOIN dpe_bilan_consommation bc ON bc.dpe_id = d.id
WHERE a.ban_postcode = '89500'
ORDER BY d.date_etablissement_dpe DESC
LIMIT 50;
"""

cur.execute(sql)

# Fetch the first row
row = cur.fetchone()

if row:
    numero_dpe, date_etablissement_dpe, adresse_complete, adresse_brute, code_postal, ville, score_dpe, score_ges = row
    print(numero_dpe, date_etablissement_dpe, adresse_complete, adresse_brute, code_postal, ville, score_dpe, score_ges)
else:
    print("No results found.")

cur.close()
conn.close()

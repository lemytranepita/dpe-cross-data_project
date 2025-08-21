import csv
import psycopg2

BATCH_SIZE = 1000

# Connect to Postgres
conn = psycopg2.connect(
    dbname="dpe",
    user="postgres",
    password="your_password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def format_postcode(code_postal):
    return code_postal.zfill(5)

# This will store all matched rows
all_matches = []

# -------------------------
# Function to execute batch
# -------------------------
def execute_batch(cur, batch, total_matches_so_far, lines_processed):
    # Build parameterized query with multiple OR conditions
    sql_conditions = []
    params = []

    for entry in batch:
        sql_conditions.append("(a.ban_postcode = %s AND a.ban_label ILIKE %s)")
        params.append(entry['code_postal'])
        params.append(f"{entry['numero_de_voie']} %{entry['nom_de_voie']}%")

    sql_where = " OR ".join(sql_conditions)

    sql = f"""
    SELECT DISTINCT ON (a.id)
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
    WHERE {sql_where}
    ORDER BY a.id, d.date_etablissement_dpe DESC;
    """

    cur.execute(sql, params)
    results = cur.fetchall()

    # Map results to the batch entries
    for entry in batch:
        matched = None
        for row in results:
            numero_dpe, date_etablissement_dpe, adresse_complete, code_postal, ville, score_dpe, score_ges = row
            if code_postal == entry['code_postal'] and adresse_complete.startswith(entry['numero_de_voie']):
                matched = row
                break

        if matched:
            total_matches_so_far += 1
            print(f"Total matches so far: {total_matches_so_far}")
            print("DVF=", entry['code_postal'], entry['ville'], entry['code_departement'],
                  entry['numero_de_voie'], entry['type_de_voie'], entry['nom_de_voie'], entry['valeur_fonciere'])
            numero_dpe, date_etablissement_dpe, adresse_complete, code_postal, ville, score_dpe, score_ges = matched
            print("DPE=", numero_dpe, date_etablissement_dpe, adresse_complete, code_postal, ville, score_dpe, score_ges)

            # Append to all_matches
            all_matches.append({
                'DVF_code_postal': entry['code_postal'],
                'DVF_ville': entry['ville'],
                'DVF_code_departement': entry['code_departement'],
                'DVF_numero_de_voie': entry['numero_de_voie'],
                'DVF_type_de_voie': entry['type_de_voie'],
                'DVF_nom_de_voie': entry['nom_de_voie'],
                'DVF_valeur_fonciere': entry['valeur_fonciere'],
                'DPE_numero_dpe': numero_dpe,
                'DPE_date_etablissement_dpe': date_etablissement_dpe,
                'DPE_adresse_complete': adresse_complete,
                'DPE_code_postal': code_postal,
                'DPE_ville': ville,
                'DPE_score_dpe': score_dpe,
                'DPE_score_ges': score_ges
            })

    print(f"Processed {lines_processed} lines from DVF so far.")
    return total_matches_so_far


# -------------------------
# Read CSV and prepare batches
# -------------------------
i = 0
batch = []
lines_processed = 0

with open('DVF_maison_vente.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    
    for row in reader:
        if row['B/T/Q']:
            continue

        code_postal = format_postcode(row['Code postal'])
        numero_de_voie = row['No voie']
        nom_de_voie = row['Voie'].replace("'", "")
        ville = row['Commune']
        code_departement = row['Code departement']
        type_de_voie = row['Type de voie']
        valeur_fonciere = row['Valeur fonciere']

        batch.append({
            'code_postal': code_postal,
            'numero_de_voie': numero_de_voie,
            'nom_de_voie': nom_de_voie,
            'ville': ville,
            'code_departement': code_departement,
            'type_de_voie': type_de_voie,
            'valeur_fonciere': valeur_fonciere
        })

        lines_processed += 1  # Count every row processed

        if len(batch) >= BATCH_SIZE:
            i = execute_batch(cur, batch, i, lines_processed)
            batch = []

    # Execute remaining rows if i < 100
    if batch:
        i = execute_batch(cur, batch, i, lines_processed)

cur.close()
conn.close()

# -------------------------
# Write all matches to CSV
# -------------------------
with open('DVF_DPE_matches.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = list(all_matches[0].keys()) if all_matches else []
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_matches)

print(f"Saved {len(all_matches)} matches to DVF_DPE_matches2.csv")
print(f"Total matches found: {i}")
print(f"Total DVF lines processed: {lines_processed}")

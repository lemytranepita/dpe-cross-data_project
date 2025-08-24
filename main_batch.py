import csv
import psycopg2
import unicodedata
import re

# -------------------------
# Config
# -------------------------
BATCH_SIZE = 500

# -------------------------
# Helpers
# -------------------------
def remove_accents(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

def matches_street_number(dpe_address, numero_de_voie):
    """
    Check if dpe_address starts with the street number followed by a space
    """
    numero_de_voie_escaped = re.escape(numero_de_voie)
    pattern = f"^{numero_de_voie_escaped}(\\s|$)"
    return re.match(pattern, dpe_address) is not None

def format_postcode(code_postal):
    return code_postal.zfill(5)

# -------------------------
# Connect to Postgres and fetch all DPE data
# -------------------------
conn = psycopg2.connect(
    dbname="dpe",
    user="postgres",
    password="password",
    #host="192.168.0.100",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

cur.execute("""
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
ORDER BY a.id, d.date_etablissement_dpe DESC;
""")

dpe_rows = cur.fetchall()
cur.close()
conn.close()

# Preprocess DPE data: normalize addresses and index by postcode
dpe_index = {}
for row in dpe_rows:
    numero_dpe, date_etablissement_dpe, adresse_complete, code_postal, ville, score_dpe, score_ges = row
    adresse_clean = remove_accents((adresse_complete or "").lower())
    dpe_entry = {
        'numero_dpe': numero_dpe,
        'date_etablissement_dpe': date_etablissement_dpe,
        'adresse_complete': adresse_complete,
        'adresse_clean': adresse_clean,
        'code_postal': code_postal,
        'ville': ville,
        'score_dpe': score_dpe,
        'score_ges': score_ges
    }
    dpe_index.setdefault(code_postal, []).append(dpe_entry)

print(f"Loaded {len(dpe_rows)} DPE rows into memory.")

# -------------------------
# Main processing
# -------------------------
total_matches = 0
lines_processed = 0
written_set = set()  # To track duplicates

with open('DVF_DPE_matches2.csv', 'w', newline='', encoding='utf-8', buffering=1) as csvfile:
    fieldnames = [
        'DVF_code_postal', 'DVF_ville', 'DVF_code_departement',
        'DVF_numero_de_voie', 'DVF_type_de_voie', 'DVF_nom_de_voie', 'DVF_valeur_fonciere',
        'DPE_numero_dpe', 'DPE_date_etablissement_dpe', 'DPE_adresse_complete',
        'DPE_code_postal', 'DPE_ville', 'DPE_score_dpe'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    with open('DVF_maison_vente.csv', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter=';')

        for row in reader:
            if row['B/T/Q']:
                continue

            code_postal = format_postcode(row['Code postal'])
            numero_de_voie = row['No voie']
            nom_de_voie = remove_accents(row['Voie'].replace("'", " "))
            ville = row['Commune']
            code_departement = row['Code departement']
            type_de_voie = row['Type de voie']
            valeur_fonciere = row['Valeur fonciere']

            lines_processed += 1
            matched = None

            for dpe in dpe_index.get(code_postal, []):
                if matches_street_number(dpe['adresse_clean'], numero_de_voie) and nom_de_voie.lower() in dpe['adresse_clean']:
                    # Create a unique key for DVF + DPE combination
                    unique_key = (
                        code_postal, numero_de_voie, nom_de_voie.lower(),
                        dpe['numero_dpe']
                    )
                    if unique_key not in written_set:
                        written_set.add(unique_key)
                        matched = dpe
                        break

            if matched:
                total_matches += 1
                row_dict = {
                    'DVF_code_postal': code_postal,
                    'DVF_ville': ville,
                    'DVF_code_departement': code_departement,
                    'DVF_numero_de_voie': numero_de_voie,
                    'DVF_type_de_voie': type_de_voie,
                    'DVF_nom_de_voie': nom_de_voie,
                    'DVF_valeur_fonciere': valeur_fonciere,
                    'DPE_numero_dpe': matched['numero_dpe'],
                    'DPE_date_etablissement_dpe': matched['date_etablissement_dpe'],
                    'DPE_adresse_complete': matched['adresse_complete'],
                    'DPE_code_postal': matched['code_postal'],
                    'DPE_ville': matched['ville'],
                    'DPE_score_dpe': matched['score_dpe']
                }
                writer.writerow(row_dict)

print(f"Total matches found: {total_matches}")
print(f"Total DVF lines processed: {lines_processed}")

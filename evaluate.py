import csv
from collections import defaultdict

# File path for the matched CSV
input_file = 'DVF_DPE_matches2.csv'

# Initialize counters and value sums
rating_counts = defaultdict(int)
rating_sums = defaultdict(float)

with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        rating = row['DPE_score_dpe']
        valeur_fonciere = row['DVF_valeur_fonciere']

        # Skip if value or rating is missing
        if not rating or not valeur_fonciere:
            continue

        # Convert value to float (removing spaces, commas, etc.)
        valeur_fonciere_clean = valeur_fonciere.replace(' ', '').replace(',', '.')
        try:
            valeur = float(valeur_fonciere_clean)
        except ValueError:
            continue

        rating_counts[rating] += 1
        rating_sums[rating] += valeur

# Print results
print("DPE Rating Analysis:")
print(f"{'Rating':<6} {'Count':<10} {'Mean Value (€)':<15}")
for rating in sorted(rating_counts.keys()):
    count = rating_counts[rating]
    mean_value = rating_sums[rating] / count if count > 0 else 0
    print(f"{rating:<6} {count:<10} {mean_value:<15.2f}")

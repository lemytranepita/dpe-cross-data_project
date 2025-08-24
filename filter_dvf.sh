echo "***Downloading DVF files...***"

mkdir -p files/dl
mkdir files/raw
mkdir files/output

wget -O files/dl/dvf_2024.zip https://www.data.gouv.fr/api/1/datasets/r/5ffa8553-0e8f-4622-add9-5c0b593ca1f8
wget -O files/dl/dvf_2023.zip https://www.data.gouv.fr/api/1/datasets/r/bc213c7c-c4d4-4385-bf1f-719573d39e90
wget -O files/dl/dvf_2022.zip https://www.data.gouv.fr/api/1/datasets/r/b4f43708-c5a8-4f30-80dc-7adfa1265d74

7z x files/dl/dvf_2024.zip -ofiles/raw
7z x files/dl/dvf_2023.zip -ofiles/raw
7z x files/dl/dvf_2022.zip -ofiles/raw

mv files/raw/ValeursFoncieres-2024.txt files/raw/dvf_2024.csv
mv files/raw/ValeursFoncieres-2023.txt files/raw/dvf_2023.csv
mv files/raw/ValeursFoncieres-2022.txt files/raw/dvf_2022.csv

echo "***DVF files downloaded successfully!***"

echo "***Filtering DVF files***"

# CSV header
head -n 1 files/raw/dvf_2024.csv > files/output/dvf_2024.csv
head -n 1 files/raw/dvf_2023.csv > files/output/dvf_2023.csv
head -n 1 files/raw/dvf_2022.csv > files/output/dvf_2022.csv

echo "Found $(cat files/raw/dvf_2024.csv | grep \|Maison\| | grep \|Vente | wc -l) houses in files/raw/dvf_2024.csv."
echo "Found $(cat files/raw/dvf_2023.csv | grep \|Maison\| | grep \|Vente | wc -l) houses in files/raw/dvf_2023.csv."
echo "Found $(cat files/raw/dvf_2022.csv | grep \|Maison\| | grep \|Vente | wc -l) houses in files/raw/dvf_2022.csv."

# Filter houses that have been sold only.
cat files/raw/dvf_2024.csv | grep \|Maison\| | grep \|Vente >> files/output/dvf_2024.csv
cat files/raw/dvf_2023.csv | grep \|Maison\| | grep \|Vente >> files/output/dvf_2023.csv
cat files/raw/dvf_2022.csv | grep \|Maison\| | grep \|Vente >> files/output/dvf_2022.csv


# Remove unneeded columns from CSV file.
#   - First columns that don't contain any data
awk -F'|' -v OFS='|' '{for(i=9;i<=NF;i++) printf "%s%s",$i,(i==NF?ORS:OFS)}' files/output/dvf_2024.csv > tmp.csv
mv tmp.csv files/output/dvf_2024.csv

awk -F'|' -v OFS='|' '{for(i=9;i<=NF;i++) printf "%s%s",$i,(i==NF?ORS:OFS)}' files/output/dvf_2023.csv > tmp.csv
mv tmp.csv files/output/dvf_2023.csv

awk -F'|' -v OFS='|' '{for(i=9;i<=NF;i++) printf "%s%s",$i,(i==NF?ORS:OFS)}' files/output/dvf_2022.csv > tmp.csv
mv tmp.csv files/output/dvf_2022.csv

#   - Other unused columns
awk -F'|' 'NR==1 {for (i=1; i<=NF; i++) if ($i ~ /Date mutation|Valeur fonciere|No voie|Type de voie|Voie|Code postal|Commune|Code departement|Code commune|Type local|Surface reelle bati|Nombre pieces principales/) cols[i]; for (i=1; i<=NF; i++) if (i in cols) { printf("%s%s",sep,$i); sep="|" }; print ""; next } NR>1 { sep=""; for (i=1; i<=NF; i++) if (i in cols) { printf("%s%s",sep,$i); sep="|" } print "" }' files/output/dvf_2024.csv > tmp.csv
mv tmp.csv files/output/dvf_2024.csv

awk -F'|' 'NR==1 {for (i=1; i<=NF; i++) if ($i ~ /Date mutation|Valeur fonciere|No voie|Type de voie|Voie|Code postal|Commune|Code departement|Code commune|Type local|Surface reelle bati|Nombre pieces principales/) cols[i]; for (i=1; i<=NF; i++) if (i in cols) { printf("%s%s",sep,$i); sep="|" }; print ""; next } NR>1 { sep=""; for (i=1; i<=NF; i++) if (i in cols) { printf("%s%s",sep,$i); sep="|" } print "" }' files/output/dvf_2023.csv > tmp.csv
mv tmp.csv files/output/dvf_2023.csv

awk -F'|' 'NR==1 {for (i=1; i<=NF; i++) if ($i ~ /Date mutation|Valeur fonciere|No voie|Type de voie|Voie|Code postal|Commune|Code departement|Code commune|Type local|Surface reelle bati|Nombre pieces principales/) cols[i]; for (i=1; i<=NF; i++) if (i in cols) { printf("%s%s",sep,$i); sep="|" }; print ""; next } NR>1 { sep=""; for (i=1; i<=NF; i++) if (i in cols) { printf("%s%s",sep,$i); sep="|" } print "" }' files/output/dvf_2022.csv > tmp.csv
mv tmp.csv files/output/dvf_2022.csv
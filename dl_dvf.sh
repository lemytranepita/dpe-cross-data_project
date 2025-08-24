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

echo "***Merging DVF files...***"

# CSV header
head -n 1 files/raw/dvf_2024.csv > files/output/dvf.csv

tail -n +2 files/raw/dvf_2024.csv >> files/output/dvf.csv
tail -n +2 files/raw/dvf_2023.csv >> files/output/dvf.csv
tail -n +2 files/raw/dvf_2022.csv >> files/output/dvf.csv

echo "***DVF files merged!***"
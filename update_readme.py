import requests
import os
import re

# Haal de API key uit de GitHub Secrets
API_KEY = os.environ.get("APE_KEY")
URL = "https://api.monkeytype.com/users/personalBests"

headers = {"Authorization": f"ApeKey {API_KEY}"}
params = {"mode": "words", "mode2": "25"}

# Haal de data op
response = requests.get(URL, headers=headers, params=params)
data = response.json()

# Pak de WPM en Acc en rond af
wpm = round(data['data'][0]['wpm'])
acc = round(data['data'][0]['acc'])

# Genereer de tekst
stats = f"**{wpm} WPM** met {acc}% accuracy"

# Lees de huidige README
with open("README.md", "r", encoding="utf-8") as f:
    readme_content = f.read()

# Vervang alleen wat tussen de markers staat
new_readme = re.sub(
    r"(<!-- monkeytype-start -->).*?(<!-- monkeytype-end -->)",
    lambda m: f"{m.group(1)}{stats}{m.group(2)}",
    readme_content,
    flags=re.DOTALL,
)

# Schrijf de nieuwe tekst terug naar de README
with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

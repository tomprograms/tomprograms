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

# Pak de WPM en rond af
jouw_wpm = round(data['data'][0]['wpm'])

# Genereer de badge
badge = f"![Monkeytype 25 words](https://img.shields.io/badge/Monkeytype_25_words-{jouw_wpm}_WPM-e2b714?style=for-the-badge&logo=monkeytype&logoColor=2c2e31)"

# Lees de huidige README
with open("README.md", "r", encoding="utf-8") as f:
    readme_content = f.read()

# Vervang de tekst tussen de start en end markers met de nieuwe badge
new_readme = re.sub(
    r"(<!-- monkeytype-start -->\n).*?(\n?<!-- monkeytype-end -->)",
    rf"\g<1>{badge}\n\g<2>",
    readme_content,
    flags=re.DOTALL
)

# Schrijf de nieuwe tekst terug naar de README
with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

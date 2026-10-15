import os
import re
import sys
from pathlib import Path
import requests

API_KEY = os.environ.get("APE_KEY")
URL = "https://api.monkeytype.com/users/personalrecords"
README = Path("README.md")
MARKERS = r"(<!-- monkeytype-start -->).*?(<!-- monkeytype-end -->)"

def get_data() -> dict:
    """Get the 25-word personal record data from the Monkeytype API."""
    if not API_KEY:
        sys.exit("APE_KEY is not set")

    res = requests.get(
        URL,
        headers={"Authorization": f"ApeKey {API_KEY}"},
        params={"mode": "words", "mode2": "25"}
    )
    res.raise_for_status()

    results = res.json().get("data")
    if not results:
        sys.exit("No personal record found for 25 words")
    return results[0]

def main() -> None:
    record = get_data()
    stats = f"**{round(record['wpm'])} WPM** with {round(record['acc'])}% accuracy"

    content = README.read_text(encoding="utf-8")

    # Only replace the text between the markers
    new_content, count = re.subn(
        MARKERS,
        lambda m: f"{m.group(1)}{stats}{m.group(2)}",
        content,
        flags=re.DOTALL,
    )
    if count == 0:
        sys.exit("Markers not found in README.md")

    README.write_text(new_content, encoding="utf-8")


if __name__ == "__main__":
    main()

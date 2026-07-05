from pathlib import Path
import json
from datetime import datetime


# -------------------------------------------------
# TIMESTAMP AUS JSON LESEN
# -------------------------------------------------
def extract_timestamp(json_file: Path):

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        ts = data.get("photoTakenTime", {}).get("timestamp")

        if not ts:
            ts = data.get("creationTime", {}).get("timestamp")

        if not ts:
            ts = data.get("timestamp")

        if not ts:
            return None

        return int(ts)

    except Exception:
        return None


# -------------------------------------------------
# TIMESTAMP → LESBARES DATUM
# -------------------------------------------------
def format_timestamp(ts: int) -> str:
    return datetime.utcfromtimestamp(ts).strftime("%d.%m.%Y %H:%M:%S")


# -------------------------------------------------
# JSON FINDEN (FINAL STABLE VERSION)
# -------------------------------------------------
def find_matching_json(media_file: Path, json_lookup: dict):

    base = media_file.stem.lower()
    suffix = media_file.suffix.lower()

    # -------------------------------------------------
    # 1. EXAKTER DATEINAME (beste Qualität)
    # -------------------------------------------------
    direct = media_file.name.lower()
    if direct in json_lookup:
        return json_lookup[direct]

    # -------------------------------------------------
    # 2. MP4 SPECIAL CASE (Live Photo Handling)
    # -------------------------------------------------
    if suffix == ".mp4":

        # 2a: echtes MP4 JSON
        mp4_json = f"{base}.mp4.supplemental-metadata.json"
        if mp4_json in json_lookup:
            return json_lookup[mp4_json]

        # 2b: HEIC fallback (Live Photo)
        heic_json = f"{base}.heic.supplemental-metadata.json"
        if heic_json in json_lookup:
            return json_lookup[heic_json]

    # -------------------------------------------------
    # 3. HEIC NORMALFALL
    # -------------------------------------------------
    if suffix == ".heic":

        heic_json = f"{base}.heic.supplemental-metadata.json"
        if heic_json in json_lookup:
            return json_lookup[heic_json]

    # -------------------------------------------------
    # 4. GENERISCHER TAKEOUT FALLBACK (robust)
    # -------------------------------------------------
    generic_json = f"{base}.supplemental-metadata.json"
    if generic_json in json_lookup:
        return json_lookup[generic_json]

    # -------------------------------------------------
    # 5. ROBUSTER BASE-MATCH (für sup/suppl/verkürzt/etc.)
    # -------------------------------------------------
    best_match = None
    best_score = 0

    for key, value in json_lookup.items():

        k = key.lower()

        # 5a. harte Base-Übereinstimmung (wichtig!)
        if k.split(".")[0] == base:
            return value

        # 5b. Prefix Similarity (Screenshots, UUIDs etc.)
        common = 0

        for a, b in zip(base, k):
            if a == b:
                common += 1
            else:
                break

        if common > best_score:
            best_score = common
            best_match = value

    # nur übernehmen wenn wirklich sinnvoll
    if best_score >= max(6, int(len(base) * 0.6)):
        return best_match

    return None

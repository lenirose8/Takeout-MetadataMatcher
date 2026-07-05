from pathlib import Path

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
    ".heic",
    ".tif",
    ".tiff"
}

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".3gp",
    ".m4v"
}


def scan_takeout(folder):

    folder = Path(folder)

    images = []
    videos = []

    # -------------------------------------------------
    # JSON LOOKUP (STABIL + EINFACH)
    # -------------------------------------------------
    json_lookup = {}

    for file in folder.rglob("*"):

        if not file.is_file():
            continue

        suffix = file.suffix.lower()

        # -------------------------------------------------
        # JSON FILES
        # -------------------------------------------------
        if suffix == ".json":

            name_lower = file.name.lower()
            stem_lower = file.stem.lower()

            # 1. exakter Dateiname (WICHTIG)
            json_lookup[name_lower] = file

            # 2. Base-Key (IMG_0126 etc.)
            json_lookup[stem_lower] = file

        # -------------------------------------------------
        # IMAGES
        # -------------------------------------------------
        elif suffix in IMAGE_EXTENSIONS:
            images.append(file)

        # -------------------------------------------------
        # VIDEOS
        # -------------------------------------------------
        elif suffix in VIDEO_EXTENSIONS:
            videos.append(file)

    print(f"JSON Lookup erstellt: {len(json_lookup)} Einträge")

    return images, videos, json_lookup

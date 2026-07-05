import subprocess
from pathlib import Path
from datetime import datetime


EXIFTOOL_PATH = r"C:\Users\lenab\TakeoutMetadataRestorer\exiftool_files\exiftool-13.59_64\exiftool.exe"


def set_common_date(file_path: Path, timestamp: int) -> bool:

    try:

        dt = datetime.utcfromtimestamp(timestamp).strftime("%Y:%m:%d %H:%M:%S")

        suffix = file_path.suffix.lower()

        # -------------------------------------------------
        # 🎥 VIDEO (MP4) HANDLING
        # -------------------------------------------------
        if suffix == ".mp4":

            cmd = [
                EXIFTOOL_PATH,
                "-overwrite_original",

                f"-CreateDate={dt}",
                f"-MediaCreateDate={dt}",
                f"-MediaModifyDate={dt}",
                f"-TrackCreateDate={dt}",
                f"-TrackModifyDate={dt}",
                f"-ModifyDate={dt}",
                # 🔥 WICHTIG FÜR WINDOWS EXPLORER
                f"-FileCreateDate={dt}",
                f"-FileModifyDate={dt}",

                str(file_path)
            ]

        # -------------------------------------------------
        # 📷 IMAGE HANDLING (HEIC, JPG etc.)
        # -------------------------------------------------
        else:

            cmd = [
                EXIFTOOL_PATH,
                "-overwrite_original",

                f"-CreateDate={dt}",
                f"-MediaCreateDate={dt}",
                f"-MediaModifyDate={dt}",
                f"-TrackCreateDate={dt}",
                f"-TrackModifyDate={dt}",
                f"-ModifyDate={dt}",

                # 🔥 WICHTIG: Dateisystem-Zeit wirklich ändern
                f"-FileModifyDate={dt}",

                str(file_path)
            ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print("[EXIF ERROR]", file_path)
            print(result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"[EXIF ERROR] {file_path}: {e}")
        return False

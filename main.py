import os
from pathlib import Path

os.chdir(Path(__file__).parent)

from scanner import scan_takeout
from matcher import find_matching_json, extract_timestamp
from writer import set_common_date
from errors import ErrorLogger

import tkinter as tk
from tkinter import filedialog, messagebox
import threading


# -------------------------------------------------
# 🔍 DEBUG SWITCH
# True = zeigt JSON Matching Infos
# False = normaler Run
# -------------------------------------------------
DEBUG = False


class TakeoutMetadataRestorer:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Google Takeout Metadata Restorer")
        self.root.geometry("850x320")

        self.folder = tk.StringVar()

        self.error_logger = ErrorLogger()

        tk.Label(self.root, text="Takeout-Ordner:").pack(pady=(20, 5))

        frame = tk.Frame(self.root)
        frame.pack()

        tk.Entry(
            frame,
            width=80,
            textvariable=self.folder
        ).pack(side="left", padx=5)

        tk.Button(
            frame,
            text="Durchsuchen",
            command=self.select_folder
        ).pack(side="left")

        tk.Button(
            self.root,
            text="ANALYSE",
            command=self.analyze
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="FULL RUN (EXIFTOOL)",
            command=self.start_full_run
        ).pack(pady=10)

    # -------------------------
    # ORDNER AUSWÄHLEN
    # -------------------------
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder.set(folder)

    # -------------------------
    # ANALYSE
    # -------------------------
    def analyze(self):

        folder = self.folder.get()

        if not folder:
            messagebox.showerror("Fehler", "Bitte Ordner wählen.")
            return

        images, videos, json_lookup = scan_takeout(folder)

        messagebox.showinfo(
            "Analyse",
            f"Bilder: {len(images)}\n"
            f"Videos: {len(videos)}\n"
            f"JSON-Einträge: {len(json_lookup)}"
        )

    # -------------------------
    # THREAD START
    # -------------------------
    def start_full_run(self):
        thread = threading.Thread(target=self.full_run, daemon=True)
        thread.start()

    # -------------------------
    # FULL RUN (STABIL + THREAD SAFE)
    # -------------------------
    def full_run(self):

        try:

            folder = self.folder.get()

            if not folder:
                print("Kein Ordner ausgewählt.")
                return

            images, videos, json_lookup = scan_takeout(folder)
            all_files = images + videos

            total = len(all_files)

            success = 0
            no_json = 0
            no_timestamp = 0
            errors = 0

            print(f"START RUN: {total} Dateien")

            # -------------------------------------------------
            # 🔥 FULL LOOP
            # -------------------------------------------------
            for i, media in enumerate(all_files):

                try:

                    if DEBUG and i < 50:
                        print("\n-----------------------------")
                        print("FILE:", media.name)
                        print("BASE:", media.stem.lower())
                        print("JSON SAMPLE:", list(json_lookup.keys())[:3])

                    match = find_matching_json(media, json_lookup)

                    if DEBUG and i < 50:
                        print("MATCH:", match.name if match else None)

                    if not match:
                        no_json += 1
                        continue

                    ts = extract_timestamp(match)

                    if not ts:
                        no_timestamp += 1
                        continue

                    ok = set_common_date(media, ts)

                    if ok:
                        success += 1
                    else:
                        errors += 1
                        self.error_logger.add(
                            media,
                            "ExifTool write failed",
                            context={"timestamp": ts}
                        )

                    # -----------------------------
                    # PROGRESS (alle 100 Dateien)
                    # -----------------------------
                    if (i + 1) % 100 == 0:
                        print(f"{i + 1} / {total}")

                except Exception as e:
                    errors += 1
                    print(f"ERROR {media.name}: {e}")

                    self.error_logger.add(
                        media,
                        str(e),
                        context={"stage": "full_run_loop"}
                    )

            log_path = self.error_logger.save()

            print("\n==============================")
            print("RUN FERTIG")
            print("==============================")
            print(f"Gesamt        : {total}")
            print(f"Erfolgreich   : {success}")
            print(f"Keine JSON    : {no_json}")
            print(f"Kein Timestamp: {no_timestamp}")
            print(f"Fehler        : {errors}")
            print(f"Error Log     : {log_path}")

            self.error_logger.print_summary()

            messagebox.showinfo(
                "Fertig",
                f"Abgeschlossen!\n\n"
                f"Gesamt: {total}\n"
                f"Erfolgreich: {success}\n"
                f"Keine JSON: {no_json}\n"
                f"Kein Timestamp: {no_timestamp}\n"
                f"Fehler: {errors}"
            )

        except Exception as e:
            print("FATAL ERROR IN FULL RUN:", e)
            messagebox.showerror("Fatal Error", str(e))

    # -------------------------
    # START
    # -------------------------
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    TakeoutMetadataRestorer().run()

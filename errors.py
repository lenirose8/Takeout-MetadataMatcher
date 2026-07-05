from datetime import datetime
import json
from pathlib import Path
import traceback


class ErrorLogger:
    def __init__(self, output_path="error_log.json"):
        self.errors = []

        self.base_path = Path(output_path)

        print(f"[ERROR_LOGGER] Init path: {self.base_path.resolve()}")

    def add(self, file_path, error, context=None):
        self.errors.append({
            "file": str(file_path),
            "error": str(error),
            "context": context or {},
            "timestamp": datetime.now().isoformat()
        })

    def save(self):
        """
        Debug + robust save with full trace output
        """

        print("\n[ERROR_LOGGER] SAVE START")
        print("[ERROR_LOGGER] Target file:", self.base_path.resolve())
        print("[ERROR_LOGGER] Error count:", len(self.errors))

        data = {
            "created_at": datetime.now().isoformat(),
            "error_count": len(self.errors),
            "errors": self.errors
        }

        # Sicherstellen, dass Ordner existiert
        try:
            self.base_path.parent.mkdir(parents=True, exist_ok=True)
            print("[ERROR_LOGGER] Directory OK:", self.base_path.parent)
        except Exception as e:
            print("[ERROR_LOGGER] Directory creation failed:", e)

        # -------------------------
        # 1. Versuch: Hauptdatei
        # -------------------------
        try:
            print("[ERROR_LOGGER] Trying main file write...")

            with open(self.base_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print("[ERROR_LOGGER] SUCCESS main file write")
            return str(self.base_path)

        except Exception as e:
            print("[ERROR_LOGGER] MAIN WRITE FAILED")
            print("[ERROR_LOGGER] Error:", repr(e))
            traceback.print_exc()

        # -------------------------
        # 2. Fallback Datei
        # -------------------------
        try:
            fallback_path = self.base_path.with_name(
                f"error_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

            print("[ERROR_LOGGER] Trying fallback:", fallback_path.resolve())

            with open(fallback_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print("[ERROR_LOGGER] SUCCESS fallback write")
            return str(fallback_path)

        except Exception as e:
            print("[ERROR_LOGGER] FALLBACK WRITE FAILED")
            print("[ERROR_LOGGER] Error:", repr(e))
            traceback.print_exc()

        # -------------------------
        # 3. Emergency fallback
        # -------------------------
        try:
            emergency_path = Path.cwd() / "error_log_emergency.json"

            print("[ERROR_LOGGER] Trying emergency:", emergency_path.resolve())

            with open(emergency_path, "w", encoding="utf-8") as f:
                json.dump({
                    "created_at": datetime.now().isoformat(),
                    "fatal_error": "logging system failure",
                    "error_count": len(self.errors),
                    "errors": self.errors
                }, f, indent=4, ensure_ascii=False)

            print("[ERROR_LOGGER] SUCCESS emergency write")
            return str(emergency_path)

        except Exception as e:
            print("[ERROR_LOGGER] CRITICAL FAILURE - NO LOG WRITTEN")
            print(repr(e))
            traceback.print_exc()

        return None

    def print_summary(self):
        if not self.errors:
            print("\n[ERROR_LOGGER] No errors recorded.")
            return

        print(f"\n[ERROR_LOGGER] SUMMARY ({len(self.errors)} errors)")
        print("-" * 50)

        for i, err in enumerate(self.errors, 1):
            print(f"{i}. FILE: {err['file']}")
            print(f"   ERROR: {err['error']}")

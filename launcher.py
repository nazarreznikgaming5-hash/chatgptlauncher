
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

import minecraft_launcher_lib

APP_NAME = "ChatGPTLauncher"
GAME_DIR = Path(os.getenv("APPDATA", str(Path.home()))) / ".minecraft"

BG = "#202020"
GREEN = "#579d31"

class Launcher:
    def __init__(self, root):
        self.root = root
        root.title(APP_NAME)
        root.geometry("600x440")
        root.configure(bg=BG)
        root.resizable(False, False)

        tk.Label(
            root, text="🌿 ChatGPTLauncher",
            font=("Segoe UI", 25, "bold"),
            bg=BG, fg="white"
        ).pack(pady=25)

        tk.Label(
            root, text="Minecraft Java Edition",
            font=("Segoe UI", 13),
            bg=BG, fg="#cccccc"
        ).pack()

        self.version = ttk.Combobox(
            root, state="readonly", width=30
        )
        self.version.pack(pady=25)

        self.status = tk.StringVar(
            value="Завантаження версій..."
        )

        tk.Label(
            root, textvariable=self.status,
            bg=BG, fg="#b8e6a0"
        ).pack(pady=10)

        tk.Button(
            root, text="ВСТАНОВИТИ MINECRAFT",
            command=self.install,
            bg="#444444", fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20, pady=12
        ).pack(pady=12)

        tk.Button(
            root, text="ГРАТИ",
            command=self.play_notice,
            bg=GREEN, fg="white",
            font=("Segoe UI", 16, "bold"),
            padx=55, pady=12
        ).pack(pady=8)

        threading.Thread(
            target=self.load_versions,
            daemon=True
        ).start()

    def load_versions(self):
        try:
            versions = minecraft_launcher_lib.utils.get_version_list()
            releases = [
                v["id"] for v in versions
                if v.get("type") == "release"
            ]

            self.root.after(
                0, lambda: self.version.configure(values=releases)
            )

            if releases:
                self.root.after(
                    0, lambda: self.version.set(releases[0])
                )
                self.root.after(
                    0, lambda: self.status.set("Готовий до встановлення")
                )
        except Exception as error:
            self.root.after(
                0, lambda: self.status.set(f"Помилка: {error}")
            )

    def install(self):
        version = self.version.get()
        if not version:
            messagebox.showwarning(
                APP_NAME, "Спочатку вибери версію."
            )
            return

        self.status.set("Встановлення Minecraft...")

        def worker():
            try:
                minecraft_launcher_lib.install.install_minecraft_version(
                    version, str(GAME_DIR)
                )
                self.root.after(
                    0, lambda: self.status.set(
                        f"Minecraft {version} встановлено."
                    )
                )
            except Exception as error:
                self.root.after(
                    0, lambda: self.status.set(f"Помилка: {error}")
                )

        threading.Thread(target=worker, daemon=True).start()

    def play_notice(self):
        messagebox.showinfo(
            APP_NAME,
            "Microsoft-авторизація та запуск гри "
            "ще розробляються."
        )

if __name__ == "__main__":
    root = tk.Tk()
    Launcher(root)
    root.mainloop()

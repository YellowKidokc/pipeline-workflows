"""A searchable Windows desktop front door for repository actions."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from action_center_core import build_command, load_catalog


class ActionCenter(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Pipeline Action Center")
        self.geometry("1040x680")
        self.minsize(820, 540)
        self.actions = load_catalog(ROOT, HERE / "catalog.json")
        self.visible_actions: list[dict] = []
        self.search = tk.StringVar()
        self.category = tk.StringVar(value="All categories")
        self.file_path = tk.StringVar()
        self.folder_path = tk.StringVar()
        self.status = tk.StringVar(value=f"Loaded {len(self.actions)} actions. Nothing runs until you confirm.")
        self._build()
        self._refresh()

    def _build(self) -> None:
        outer = ttk.Frame(self, padding=14)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="Pipeline Action Center", font=("Segoe UI", 19, "bold")).pack(anchor="w")
        ttk.Label(outer, text="Search, choose inputs, preview the exact command, then launch it in a separate window.").pack(anchor="w", pady=(0, 12))
        filters = ttk.Frame(outer)
        filters.pack(fill="x")
        ttk.Label(filters, text="Search").pack(side="left")
        entry = ttk.Entry(filters, textvariable=self.search, width=42)
        entry.pack(side="left", padx=(7, 18))
        entry.bind("<KeyRelease>", lambda _event: self._refresh())
        ttk.Label(filters, text="Category").pack(side="left")
        choices = ["All categories"] + sorted({a["category"] for a in self.actions})
        box = ttk.Combobox(filters, textvariable=self.category, values=choices, state="readonly", width=27)
        box.pack(side="left", padx=7)
        box.bind("<<ComboboxSelected>>", lambda _event: self._refresh())
        body = ttk.Panedwindow(outer, orient="horizontal")
        body.pack(fill="both", expand=True, pady=12)
        left = ttk.Frame(body)
        right = ttk.Frame(body, padding=(14, 0, 0, 0))
        body.add(left, weight=2); body.add(right, weight=3)
        self.listbox = tk.Listbox(left, exportselection=False, font=("Segoe UI", 10))
        scroll = ttk.Scrollbar(left, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scroll.set)
        self.listbox.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y")
        self.listbox.bind("<<ListboxSelect>>", lambda _event: self._show_action())
        self.heading = ttk.Label(right, text="Choose an action", font=("Segoe UI", 14, "bold"), wraplength=520)
        self.heading.pack(anchor="w")
        self.description = ttk.Label(right, text="", wraplength=520, justify="left")
        self.description.pack(anchor="w", pady=(7, 18))
        self._picker(right, "File", self.file_path, self._pick_file)
        self._picker(right, "Folder", self.folder_path, self._pick_folder)
        ttk.Label(right, text="Command preview").pack(anchor="w", pady=(18, 4))
        self.preview = tk.Text(right, height=7, wrap="word", state="disabled", background="#f4f4f4")
        self.preview.pack(fill="x")
        buttons = ttk.Frame(right)
        buttons.pack(fill="x", pady=14)
        ttk.Button(buttons, text="Launch selected action", command=self._launch).pack(side="left")
        ttk.Button(buttons, text="Open selected folder", command=self._open_folder).pack(side="left", padx=8)
        ttk.Label(outer, textvariable=self.status, relief="sunken", anchor="w", padding=5).pack(fill="x")

    def _picker(self, parent, label, variable, command) -> None:
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=4)
        ttk.Label(row, text=label, width=7).pack(side="left")
        ttk.Entry(row, textvariable=variable).pack(side="left", fill="x", expand=True)
        ttk.Button(row, text="Browse…", command=command).pack(side="left", padx=(7, 0))
        variable.trace_add("write", lambda *_args: self._show_action())

    def _refresh(self) -> None:
        query = self.search.get().casefold().strip()
        category = self.category.get()
        self.visible_actions = [a for a in self.actions if (category == "All categories" or a["category"] == category)
                                and query in (a["name"] + " " + a["description"] + " " + a["category"]).casefold()]
        self.listbox.delete(0, "end")
        for action in self.visible_actions:
            self.listbox.insert("end", f'{action["category"]}  •  {action["name"]}')
        if self.visible_actions:
            self.listbox.selection_set(0); self._show_action()

    def _selected(self):
        chosen = self.listbox.curselection()
        return self.visible_actions[chosen[0]] if chosen else None

    def _show_action(self) -> None:
        action = self._selected()
        if not action:
            return
        self.heading.configure(text=action["name"])
        self.description.configure(text=f'{action["category"]}\n\n{action["description"]}\n\nInput: {action.get("selection", "none").replace("_", " + ")}')
        try:
            command = build_command(action, ROOT, self.file_path.get(), self.folder_path.get())
            preview = subprocess.list2cmdline(command)
        except ValueError as exc:
            preview = str(exc)
        self.preview.configure(state="normal"); self.preview.delete("1.0", "end"); self.preview.insert("1.0", preview); self.preview.configure(state="disabled")

    def _pick_file(self) -> None:
        value = filedialog.askopenfilename(title="Choose input file")
        if value: self.file_path.set(value)

    def _pick_folder(self) -> None:
        value = filedialog.askdirectory(title="Choose input folder")
        if value: self.folder_path.set(value)

    def _launch(self) -> None:
        action = self._selected()
        if not action: return
        try:
            command = build_command(action, ROOT, self.file_path.get(), self.folder_path.get())
        except ValueError as exc:
            messagebox.showwarning("Input needed", str(exc)); return
        preview = subprocess.list2cmdline(command)
        if not messagebox.askokcancel("Confirm launch", f'Launch “{action["name"]}”?\n\n{preview}\n\nThe selected tool controls its own file operations.'):
            return
        flags = subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
        try:
            subprocess.Popen(command, cwd=ROOT, creationflags=flags)
            self.status.set(f'Launched: {action["name"]}')
        except OSError as exc:
            messagebox.showerror("Could not launch", str(exc))

    def _open_folder(self) -> None:
        folder = self.folder_path.get() or str(ROOT)
        try:
            if sys.platform == "win32": subprocess.Popen(["explorer.exe", folder])
            elif sys.platform == "darwin": subprocess.Popen(["open", folder])
            else: subprocess.Popen(["xdg-open", folder])
        except OSError as exc: messagebox.showerror("Could not open folder", str(exc))


if __name__ == "__main__":
    ActionCenter().mainloop()


from __future__ import annotations

import json
import os
import queue
import shlex
import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import customtkinter as ctk
from tkinter import messagebox


APP_DIR = Path(__file__).resolve().parent
CATALOG_PATH = APP_DIR / "actions.json"


@dataclass(frozen=True)
class Action:
    id: str
    title: str
    description: str
    category: str
    source: str
    path: Path
    kind: str
    tags: list[str]
    risk: str
    needs_args: bool
    default_args: str
    enabled: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Action":
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            category=data.get("category", "Other"),
            source=data.get("source", "Unknown"),
            path=Path(data["path"]),
            kind=data.get("kind", Path(data["path"]).suffix.lstrip(".").lower()),
            tags=list(data.get("tags", [])),
            risk=data.get("risk", "safe"),
            needs_args=bool(data.get("needs_args", False)),
            default_args=data.get("default_args", ""),
            enabled=bool(data.get("enabled", True)),
        )


class PopupHub(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Stratum Popup Hub")
        self.geometry("1180x760")
        self.minsize(980, 640)

        self.actions = self.load_actions()
        self.selected_category = "All"
        self.selected_action: Action | None = None
        self.output_queue: queue.Queue[str] = queue.Queue()
        self.runner_thread: threading.Thread | None = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(3, weight=1)

        self.main = ctk.CTkFrame(self, corner_radius=0, fg_color="#10131a")
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(2, weight=1)

        self.detail = ctk.CTkFrame(self, width=360, corner_radius=0)
        self.detail.grid(row=0, column=2, sticky="nsew")
        self.detail.grid_rowconfigure(7, weight=1)

        self.build_sidebar()
        self.build_main()
        self.build_detail()
        self.refresh_action_list()
        self.after(100, self.drain_output)

    def load_actions(self) -> list[Action]:
        if not CATALOG_PATH.exists():
            return []
        with CATALOG_PATH.open("r", encoding="utf-8") as handle:
            return [Action.from_dict(row) for row in json.load(handle)]

    def build_sidebar(self) -> None:
        title = ctk.CTkLabel(
            self.sidebar,
            text="Stratum",
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, padx=18, pady=(22, 2), sticky="ew")

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Popup action hub",
            text_color="#9ca3af",
            anchor="w",
        )
        subtitle.grid(row=1, column=0, padx=18, pady=(0, 18), sticky="ew")

        self.category_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.category_frame.grid(row=2, column=0, sticky="new", padx=10)
        self.category_frame.grid_columnconfigure(0, weight=1)

        categories = ["All"] + sorted({action.category for action in self.actions})
        for index, category in enumerate(categories):
            count = len(self.actions) if category == "All" else sum(
                1 for action in self.actions if action.category == category
            )
            button = ctk.CTkButton(
                self.category_frame,
                text=f"{category}  {count}",
                anchor="w",
                height=36,
                corner_radius=6,
                fg_color="#2563eb" if category == self.selected_category else "transparent",
                hover_color="#1f2937",
                command=lambda value=category: self.set_category(value),
            )
            button.grid(row=index, column=0, sticky="ew", pady=2)

        footer = ctk.CTkLabel(
            self.sidebar,
            text="Safe first. Caution scripts ask before running.",
            text_color="#9ca3af",
            wraplength=180,
            justify="left",
        )
        footer.grid(row=4, column=0, padx=18, pady=18, sticky="sew")

    def build_main(self) -> None:
        header = ctk.CTkFrame(self.main, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 10))
        header.grid_columnconfigure(0, weight=1)

        heading = ctk.CTkLabel(
            header,
            text="Actions",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        heading.grid(row=0, column=0, sticky="w")

        reload_button = ctk.CTkButton(
            header,
            text="Reload",
            width=92,
            command=self.reload_catalog,
        )
        reload_button.grid(row=0, column=1, sticky="e")

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_action_list())
        self.search_entry = ctk.CTkEntry(
            self.main,
            textvariable=self.search_var,
            height=42,
            placeholder_text="Search by title, tag, category, or source",
        )
        self.search_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))

        self.action_list = ctk.CTkScrollableFrame(self.main, corner_radius=8, fg_color="#151922")
        self.action_list.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.action_list.grid_columnconfigure(0, weight=1)

    def build_detail(self) -> None:
        self.detail_title = ctk.CTkLabel(
            self.detail,
            text="Select an action",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
            wraplength=300,
            justify="left",
        )
        self.detail_title.grid(row=0, column=0, padx=18, pady=(22, 6), sticky="ew")

        self.detail_meta = ctk.CTkLabel(
            self.detail,
            text="",
            text_color="#9ca3af",
            anchor="w",
            justify="left",
            wraplength=300,
        )
        self.detail_meta.grid(row=1, column=0, padx=18, pady=(0, 12), sticky="ew")

        self.detail_desc = ctk.CTkLabel(
            self.detail,
            text="Choose something from the list to see what it does.",
            anchor="w",
            justify="left",
            wraplength=300,
        )
        self.detail_desc.grid(row=2, column=0, padx=18, pady=(0, 12), sticky="ew")

        self.args_label = ctk.CTkLabel(self.detail, text="Arguments", anchor="w")
        self.args_label.grid(row=3, column=0, padx=18, pady=(0, 4), sticky="ew")

        self.args_entry = ctk.CTkEntry(
            self.detail,
            placeholder_text="Optional command arguments",
            height=38,
        )
        self.args_entry.grid(row=4, column=0, padx=18, pady=(0, 12), sticky="ew")

        controls = ctk.CTkFrame(self.detail, fg_color="transparent")
        controls.grid(row=5, column=0, padx=18, pady=(0, 12), sticky="ew")
        controls.grid_columnconfigure((0, 1), weight=1)

        self.run_button = ctk.CTkButton(controls, text="Run", command=self.run_selected)
        self.run_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.open_button = ctk.CTkButton(
            controls,
            text="Open File",
            fg_color="#374151",
            hover_color="#4b5563",
            command=self.open_selected_file,
        )
        self.open_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        more_controls = ctk.CTkFrame(self.detail, fg_color="transparent")
        more_controls.grid(row=6, column=0, padx=18, pady=(0, 12), sticky="ew")
        more_controls.grid_columnconfigure((0, 1), weight=1)

        self.folder_button = ctk.CTkButton(
            more_controls,
            text="Open Folder",
            fg_color="#374151",
            hover_color="#4b5563",
            command=self.open_selected_folder,
        )
        self.folder_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.copy_button = ctk.CTkButton(
            more_controls,
            text="Copy Path",
            fg_color="#374151",
            hover_color="#4b5563",
            command=self.copy_selected_path,
        )
        self.copy_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        self.output_box = ctk.CTkTextbox(self.detail, wrap="word", corner_radius=8)
        self.output_box.grid(row=7, column=0, padx=18, pady=(0, 18), sticky="nsew")
        self.output_box.insert("end", "Output will appear here.\n")
        self.output_box.configure(state="disabled")

    def set_category(self, category: str) -> None:
        self.selected_category = category
        for child in self.category_frame.winfo_children():
            child.destroy()
        categories = ["All"] + sorted({action.category for action in self.actions})
        for index, item in enumerate(categories):
            count = len(self.actions) if item == "All" else sum(
                1 for action in self.actions if action.category == item
            )
            button = ctk.CTkButton(
                self.category_frame,
                text=f"{item}  {count}",
                anchor="w",
                height=36,
                corner_radius=6,
                fg_color="#2563eb" if item == self.selected_category else "transparent",
                hover_color="#1f2937",
                command=lambda value=item: self.set_category(value),
            )
            button.grid(row=index, column=0, sticky="ew", pady=2)
        self.refresh_action_list()

    def filtered_actions(self) -> list[Action]:
        query = self.search_var.get().strip().lower()
        rows = []
        for action in self.actions:
            if self.selected_category != "All" and action.category != self.selected_category:
                continue
            haystack = " ".join(
                [
                    action.title,
                    action.description,
                    action.category,
                    action.source,
                    action.kind,
                    action.risk,
                    " ".join(action.tags),
                ]
            ).lower()
            if query and query not in haystack:
                continue
            rows.append(action)
        return rows

    def refresh_action_list(self) -> None:
        for child in self.action_list.winfo_children():
            child.destroy()

        rows = self.filtered_actions()
        if not rows:
            empty = ctk.CTkLabel(
                self.action_list,
                text="No actions match that filter.",
                text_color="#9ca3af",
            )
            empty.grid(row=0, column=0, padx=18, pady=18, sticky="w")
            return

        for index, action in enumerate(rows):
            card = ctk.CTkFrame(self.action_list, corner_radius=8, fg_color="#1d2330")
            card.grid(row=index, column=0, sticky="ew", padx=10, pady=6)
            card.grid_columnconfigure(0, weight=1)

            risk_color = {
                "safe": "#22c55e",
                "caution": "#f59e0b",
                "admin": "#f97316",
                "destructive": "#ef4444",
            }.get(action.risk, "#9ca3af")

            title = ctk.CTkLabel(
                card,
                text=action.title,
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w",
            )
            title.grid(row=0, column=0, padx=14, pady=(10, 0), sticky="ew")

            meta = ctk.CTkLabel(
                card,
                text=f"{action.category} / {action.source} / {action.kind.upper()}",
                text_color="#9ca3af",
                anchor="w",
            )
            meta.grid(row=1, column=0, padx=14, pady=(0, 8), sticky="ew")

            risk = ctk.CTkLabel(
                card,
                text=action.risk.upper(),
                text_color=risk_color,
                font=ctk.CTkFont(size=12, weight="bold"),
            )
            risk.grid(row=0, column=1, padx=14, pady=(10, 0), sticky="e")

            select = ctk.CTkButton(
                card,
                text="Select",
                width=86,
                height=30,
                command=lambda value=action: self.select_action(value),
            )
            select.grid(row=1, column=1, padx=14, pady=(0, 8), sticky="e")

    def select_action(self, action: Action) -> None:
        self.selected_action = action
        self.detail_title.configure(text=action.title)
        self.detail_meta.configure(
            text=f"{action.category} / {action.source}\nRisk: {action.risk} / Type: {action.kind.upper()}"
        )
        exists = "found" if action.path.exists() else "missing"
        self.detail_desc.configure(text=f"{action.description}\n\nPath {exists}: {action.path}")
        self.args_entry.delete(0, "end")
        self.args_entry.insert(0, action.default_args)

    def reload_catalog(self) -> None:
        self.actions = self.load_actions()
        self.selected_category = "All"
        self.set_category("All")
        self.append_output("Catalog reloaded.\n")

    def build_command(self, action: Action, raw_args: str) -> list[str]:
        args = shlex.split(raw_args, posix=False) if raw_args.strip() else []
        if action.kind == "ps1":
            return [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(action.path),
                *args,
            ]
        if action.kind == "py":
            return ["py", "-3", str(action.path), *args]
        if action.kind in {"bat", "cmd"}:
            return ["cmd", "/c", str(action.path), *args]
        raise ValueError(f"Unsupported action kind: {action.kind}")

    def run_selected(self) -> None:
        action = self.selected_action
        if action is None:
            messagebox.showinfo("Popup Hub", "Select an action first.")
            return
        if not action.enabled:
            messagebox.showwarning("Popup Hub", "This action is disabled in the catalog.")
            return
        if not action.path.exists():
            messagebox.showerror("Popup Hub", f"Missing script:\n{action.path}")
            return
        if action.risk != "safe":
            allowed = messagebox.askyesno(
                "Confirm action",
                f"{action.title} is marked {action.risk.upper()}.\n\nRun it anyway?",
            )
            if not allowed:
                return
        if self.runner_thread and self.runner_thread.is_alive():
            messagebox.showinfo("Popup Hub", "A script is already running.")
            return

        raw_args = self.args_entry.get()
        try:
            command = self.build_command(action, raw_args)
        except ValueError as exc:
            messagebox.showerror("Popup Hub", str(exc))
            return

        self.run_button.configure(state="disabled", text="Running")
        self.append_output(f"\n> {' '.join(command)}\n")
        self.runner_thread = threading.Thread(
            target=self.run_command_worker,
            args=(command, action.path.parent),
            daemon=True,
        )
        self.runner_thread.start()

    def run_command_worker(self, command: list[str], cwd: Path) -> None:
        try:
            process = subprocess.Popen(
                command,
                cwd=str(cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
            assert process.stdout is not None
            for line in process.stdout:
                self.output_queue.put(line)
            code = process.wait()
            self.output_queue.put(f"\n[exit code {code}]\n")
        except Exception as exc:
            self.output_queue.put(f"\n[error] {exc}\n")
        finally:
            self.output_queue.put("__RUN_DONE__")

    def drain_output(self) -> None:
        try:
            while True:
                item = self.output_queue.get_nowait()
                if item == "__RUN_DONE__":
                    self.run_button.configure(state="normal", text="Run")
                else:
                    self.append_output(item)
        except queue.Empty:
            pass
        self.after(100, self.drain_output)

    def append_output(self, text: str) -> None:
        self.output_box.configure(state="normal")
        self.output_box.insert("end", text)
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    def open_selected_file(self) -> None:
        action = self.selected_action
        if action is None:
            return
        os.startfile(str(action.path))

    def open_selected_folder(self) -> None:
        action = self.selected_action
        if action is None:
            return
        os.startfile(str(action.path.parent))

    def copy_selected_path(self) -> None:
        action = self.selected_action
        if action is None:
            return
        self.clipboard_clear()
        self.clipboard_append(str(action.path))
        self.append_output(f"Copied path: {action.path}\n")


if __name__ == "__main__":
    app = PopupHub()
    app.mainloop()

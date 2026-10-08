import contextlib
import queue
import threading
import tkinter as tk
import traceback
from tkinter import filedialog, messagebox, scrolledtext, ttk

# The step scripts are run with runpy, so PyInstaller can't see what they import.
# Importing these here makes sure they are bundled into the .exe.
import csv  # noqa: F401
import json  # noqa: F401
import numpy  # noqa: F401
import openpyxl  # noqa: F401
import pandas  # noqa: F401

import paths  # noqa: F401  (used by the step scripts)
from main import find_steps, run_pipeline

STEP_LABELS = {
    1: "Extract IST",
    2: "Extract scanner (SCN)",
    3: "Extract VMR hardware",
    4: "Lookup HW POS + IST",
    5: "Lookup HW SC + IST",
    6: "Lookup store POS",
    7: "Lookup store SC",
    8: "Count POS / SC / scanner models",
}


class QueueWriter:
    """File-like object that sends printed text to the GUI thread."""

    def __init__(self, q):
        self.q = q

    def write(self, text):
        if text:
            self.q.put(text)

    def flush(self):
        pass


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hardware Capacity")
        self.geometry("760x560")
        self.log_queue = queue.Queue()
        self.running = False

        self.source = tk.StringVar()
        self.output = tk.StringVar()
        self.same_folder = tk.BooleanVar(value=True)
        self.step_vars = {n: tk.BooleanVar(value=True) for n in find_steps()}

        self._build()
        self.after(100, self._drain_log)

    def _build(self):
        pad = {"padx": 8, "pady": 4}
        frame = ttk.Frame(self)
        frame.pack(fill="x", **pad)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Source folder").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.source).grid(row=0, column=1, sticky="ew", padx=6)
        ttk.Button(frame, text="Browse...", command=self._browse_source).grid(row=0, column=2)

        ttk.Label(frame, text="Output folder").grid(row=1, column=0, sticky="w")
        self.output_entry = ttk.Entry(frame, textvariable=self.output)
        self.output_entry.grid(row=1, column=1, sticky="ew", padx=6)
        self.output_btn = ttk.Button(frame, text="Browse...", command=self._browse_output)
        self.output_btn.grid(row=1, column=2)
        ttk.Checkbutton(
            frame, text="Output = source folder", variable=self.same_folder, command=self._toggle_output
        ).grid(row=2, column=1, sticky="w", padx=6)
        self._toggle_output()

        steps = ttk.LabelFrame(self, text="Steps")
        steps.pack(fill="x", **pad)
        for i, number in enumerate(self.step_vars):
            label = f"{number}. {STEP_LABELS.get(number, find_steps()[number].stem)}"
            ttk.Checkbutton(steps, text=label, variable=self.step_vars[number]).grid(
                row=i % 4, column=i // 4, sticky="w", padx=8, pady=2
            )

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", **pad)
        self.run_btn = ttk.Button(buttons, text="Run", command=self._run)
        self.run_btn.pack(side="left")
        ttk.Button(buttons, text="Select all", command=lambda: self._set_all(True)).pack(side="left", padx=6)
        ttk.Button(buttons, text="Select none", command=lambda: self._set_all(False)).pack(side="left")

        self.log = scrolledtext.ScrolledText(self, state="disabled", height=18)
        self.log.pack(fill="both", expand=True, **pad)

    def _browse_source(self):
        folder = filedialog.askdirectory(title="Select source folder")
        if folder:
            self.source.set(folder)

    def _browse_output(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output.set(folder)

    def _toggle_output(self):
        state = "disabled" if self.same_folder.get() else "normal"
        self.output_entry.configure(state=state)
        self.output_btn.configure(state=state)

    def _set_all(self, value):
        for var in self.step_vars.values():
            var.set(value)

    def _append(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text)
        self.log.see("end")
        self.log.configure(state="disabled")

    def _drain_log(self):
        try:
            while True:
                self._append(self.log_queue.get_nowait())
        except queue.Empty:
            pass
        self.after(100, self._drain_log)

    def _run(self):
        if self.running:
            return
        source = self.source.get().strip()
        output = source if self.same_folder.get() else self.output.get().strip()
        numbers = [n for n, var in self.step_vars.items() if var.get()]
        if not source:
            messagebox.showwarning("Missing folder", "Select a source folder.")
            return
        if not output:
            messagebox.showwarning("Missing folder", "Select an output folder.")
            return
        if not numbers:
            messagebox.showwarning("No steps", "Select at least one step.")
            return

        self.running = True
        self.run_btn.configure(state="disabled")
        self._append(f"--- Run started: source={source} output={output} steps={numbers}\n")
        threading.Thread(target=self._worker, args=(source, output, numbers), daemon=True).start()

    def _worker(self, source, output, numbers):
        writer = QueueWriter(self.log_queue)
        try:
            with contextlib.redirect_stdout(writer), contextlib.redirect_stderr(writer):
                run_pipeline(source, output, numbers)
            self.log_queue.put("--- Done\n")
        except SystemExit as e:
            self.log_queue.put(f"--- Stopped: {e}\n")
        except Exception:
            self.log_queue.put(traceback.format_exc() + "--- Failed\n")
        finally:
            self.after(0, self._finish)

    def _finish(self):
        self.running = False
        self.run_btn.configure(state="normal")


if __name__ == "__main__":
    App().mainloop()

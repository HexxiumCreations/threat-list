import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import threading, socket, requests, re, csv, webbrowser, time
from concurrent.futures import ThreadPoolExecutor

DOMAIN_REGEX = re.compile(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")
PARKED = ["domain for sale","buy this domain","sedo","godaddy","parked"]

class DomainChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk Domain Checker Complete")
        self.root.geometry("1200x950")

        self.results = {}
        self.valid_domains = []

        self.dark_mode = False
        self.scanning = False

        # HEADER
        self.header1 = tk.Label(root, text="© 2026 Hexxium Creations", fg="blue")
        self.header1.pack()
        self.header2 = tk.Label(root, text="⚠ Disable antivirus/firewall before scanning", fg="red")
        self.header2.pack()
        tk.Label(root, text="Process: Rapid Scan OR Full Scan → Validation 1 → Validation 2").pack()
        tk.Label(root, text="This application accepts an imported list of domains and will attempt to verify if they are still online and output the result in various formats").pack()

        # DROP
        drop = tk.Label(root, text="⬇ Drag & Drop File Here", bg="#eaeaea")
        drop.pack(fill="x", padx=10, pady=5)
        drop.drop_target_register(DND_FILES)
        drop.dnd_bind("<<Drop>>", self.handle_drop)

        # INPUT
        self.input_box = scrolledtext.ScrolledText(root, height=6)
        self.input_box.pack(fill="both", padx=10)

        # SEARCH
        tk.Label(root, text="Search Results").pack()
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_results)
        self.search_entry = tk.Entry(root, textvariable=self.search_var)
        self.search_entry.pack(fill="x", padx=10)

        # PANELS
        panel = tk.Frame(root)
        panel.pack(fill="both", padx=10)

        self.invalid_box = self.make_box(panel, "Invalid Domains")
        self.duplicate_box = self.make_box(panel, "Duplicates")

        ip_frame = tk.Frame(root)
        ip_frame.pack(fill="both", padx=10)
        tk.Label(ip_frame, text="IP Addresses").pack()
        self.ip_box = scrolledtext.ScrolledText(ip_frame, height=4)
        self.ip_box.pack(fill="both")

        self.stats = tk.Label(root, text="Total: 0")
        self.stats.pack()

        # BUTTONS
        btn = tk.Frame(root)
        btn.pack()

        tk.Button(btn, text="Import", command=self.load_file).pack(side="left")
        tk.Button(btn, text="Analyze", command=self.preview_domains).pack(side="left")
        tk.Button(btn, text="Remove Duplicates", command=self.remove_duplicates).pack(side="left")
        tk.Button(btn, text="Full Scan", command=lambda: self.start_scan(full=True)).pack(side="left")
        tk.Button(btn, text="Rapid Scan", command=lambda: self.start_scan(full=False)).pack(side="left")
        tk.Button(btn, text="Export TXT", command=self.export_txt).pack(side="left")
        tk.Button(btn, text="Export CSV", command=self.export_csv).pack(side="left")
        tk.Button(btn, text="Report Issue", command=self.report_issue).pack(side="left")
        tk.Button(btn, text="🌙 Dark Mode", command=self.toggle_dark).pack(side="left")
        self.stage_label = tk.Label(root, text="Stage: Idle")
        self.stage_label.pack()

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=5)

        # TABS
        self.tabs = ttk.Notebook(root)
        self.online_tab = scrolledtext.ScrolledText(self.tabs)
        self.parked_tab = scrolledtext.ScrolledText(self.tabs)
        self.offline_tab = scrolledtext.ScrolledText(self.tabs)

        self.tabs.add(self.online_tab, text="Online (0)")
        self.tabs.add(self.parked_tab, text="Parked (0)")
        self.tabs.add(self.offline_tab, text="Offline (0)")
        self.tabs.pack(expand=1, fill="both")

        self.progress = tk.Label(root, text="Idle")
        self.progress.pack()

    def make_box(self, parent, label):
        f = tk.Frame(parent)
        f.pack(side="left", fill="both", expand=True)
        tk.Label(f, text=label).pack()
        box = scrolledtext.ScrolledText(f, height=5)
        box.pack(fill="both")
        return box

    def handle_drop(self, event):
        path = event.data.strip("{}")
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            self.input_box.delete("1.0", tk.END)
            self.input_box.insert(tk.END, f.read())
        self.preview_domains()

    def load_file(self):
        path = filedialog.askopenfilename()
        if path:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                self.input_box.delete("1.0", tk.END)
                self.input_box.insert(tk.END, f.read())
            self.preview_domains()

    def preview_domains(self):
        raw = [d.strip().lower() for d in self.input_box.get("1.0", tk.END).splitlines() if d.strip()]
        self.valid_domains = [d for d in raw if DOMAIN_REGEX.match(d)]
        self.stats.config(text=f"Total: {len(raw)} | Valid: {len(self.valid_domains)}")

    def remove_duplicates(self):
        raw = self.input_box.get("1.0", tk.END).splitlines()
        unique = list(dict.fromkeys(raw))
        self.input_box.delete("1.0", tk.END)
        self.input_box.insert(tk.END, "\n".join(unique))

    def start_scan(self, full=False):
        if not self.valid_domains:
            return
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = len(self.valid_domains)
        self.stage_label.config(text="Stage: Starting...")
        self.results.clear()
        self.scanning = True
        self.search_entry.config(state="disabled")

        for tab in [self.online_tab, self.parked_tab, self.offline_tab]:
            tab.delete("1.0", tk.END)

        threading.Thread(target=self.run_scan, args=(full,), daemon=True).start()

    def check_domain(self, domain):
        try:
            socket.gethostbyname(domain)
            r = requests.get("http://" + domain, timeout=5)

            # Treat HTTP Status codes 301,302,403 and 429 as online to prevent false removals

            if r.status_code == (301, 302, 403, 429):
                return "ONLINE", r.status_code

            if any(k in r.text.lower() for k in PARKED):
                return "PARKED", r.status_code

            return ("ONLINE", r.status_code) if r.status_code < 400 else ("OFFLINE", r.status_code)
        except:
            return "OFFLINE", 0

    def run_scan(self, full):
        passes = 3 if full else 1
        threads = 40 if full else 100

        counts = {"ONLINE":0,"PARKED":0,"OFFLINE":0}
        counted_domains = set()  # 🔥 prevents duplicate counting
        total = len(self.valid_domains)

        stages = ["Rapid First Scan", "Validation Stage 1 Running, Please Wait To Export", "Validation Stage 2 Running, Please Wait To Export"] if full else ["Rapid Scan"]

        for p in range(len(stages)):
            stage_name = stages[p]

            self.root.after(0, lambda s=stage_name: self.stage_label.config(text=f"Stage: {s}"))

            from concurrent.futures import as_completed

            with ThreadPoolExecutor(max_workers=threads) as ex:
                futures = {ex.submit(self.check_domain, d): d for d in self.valid_domains}

                for future in as_completed(futures):
                    domain = futures[future]
                    result = future.result()

                    old_status = self.results.get(domain, (None, None))[0]
                    new_status, code = result

                    # 🔒 Keep ONLINE locked
                    if old_status == "ONLINE":
                        continue

                    self.results[domain] = (new_status, code)

                    if domain not in counted_domains:
                        counted_domains.add(domain)
                        counts[new_status] += 1

                    def update(d=domain, s=new_status):
                        tab = {
                            "ONLINE": self.online_tab,
                            "PARKED": self.parked_tab,
                            "OFFLINE": self.offline_tab
                        }[s]

                        tab.insert(tk.END, d + "\n")

                        self.tabs.tab(0, text=f"Online ({counts['ONLINE']})")
                        self.tabs.tab(1, text=f"Parked ({counts['PARKED']})")
                        self.tabs.tab(2, text=f"Offline ({counts['OFFLINE']})")

                        # ✅ Live progress
                        self.progress_bar["value"] = len(counted_domains)
                        self.progress.config(text=f"{len(counted_domains)}/{total} scanned")

                    self.root.after(0, update)

                old_status = self.results.get(domain, (None, None))[0]
                new_status, code = result

                # 🔒 Lock ONLINE (do not downgrade)
                if old_status == "ONLINE":
                    continue

                self.results[domain] = (new_status, code)

                # ✅ ONLY COUNT FIRST TIME
                if domain not in counted_domains:
                    counted_domains.add(domain)
                    counts[new_status] += 1

                def update(d=domain, s=new_status):
                    tab = {"ONLINE":self.online_tab,
                           "PARKED":self.parked_tab,
                           "OFFLINE":self.offline_tab}[s]
                    self.progress_bar["value"] = len(counted_domains)

                    tab.insert(tk.END, d + "\n")

                    self.tabs.tab(0, text=f"Online ({counts['ONLINE']})")
                    self.tabs.tab(1, text=f"Parked ({counts['PARKED']})")
                    self.tabs.tab(2, text=f"Offline ({counts['OFFLINE']})")

                    # 🔥 FIXED PROGRESS
                    self.progress.config(text=f"{len(counted_domains)}/{total} scanned")

                self.root.after(0, update)

        self.scanning = False
        self.root.after(0, self.finish_scan)

    def finish_scan(self):
        self.search_entry.config(state="normal")
        self.stage_label.config(text="Stage: Complete")
        self.progress_bar["value"] = self.progress_bar["maximum"]
        messagebox.showinfo("Complete", "Scan finished successfully!")

    def filter_results(self, *args):
        if self.scanning:
            return

        term = self.search_var.get().lower()

        for tab in [self.online_tab, self.parked_tab, self.offline_tab]:
            tab.delete("1.0", tk.END)

        for d,(s,_) in self.results.items():
            if term and term not in d:
                continue

            if s == "ONLINE":
                self.online_tab.insert(tk.END, d+"\n")
            elif s == "PARKED":
                self.parked_tab.insert(tk.END, d+"\n")
            else:
                self.offline_tab.insert(tk.END, d+"\n")

    def export_txt(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if not path:
            return

        with open(path, "w") as f:
            for status in ["ONLINE","PARKED","OFFLINE"]:
                f.write(f"{status}:\n")
                for d,(s,_) in self.results.items():
                    if s == status:
                        f.write(d+"\n")
                f.write("\n")

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if not path:
            return

        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Domain","Status","Code"])
            for d,(s,c) in self.results.items():
                writer.writerow([d,s,c])

    def report_issue(self):
        webbrowser.open("mailto:admin@hexxiumcreations.com")

    def toggle_dark(self):
        self.dark_mode = not self.dark_mode
        bg = "#2b2b2b" if self.dark_mode else "white"
        fg = "white" if self.dark_mode else "black"

        for box in [self.input_box,self.invalid_box,self.duplicate_box,self.ip_box,
                    self.online_tab,self.parked_tab,self.offline_tab]:
            box.config(bg="#3a3a3a" if self.dark_mode else "white", fg=fg)

        self.header1.config(fg="blue")
        self.header2.config(fg="red")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = DomainChecker(root)
    root.mainloop()

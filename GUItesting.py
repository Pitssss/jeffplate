import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox

class ANPRDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("ANPR ACCESS - MONITOR")
        
        
        # Enable true full screen
        self.root.attributes('-fullscreen', True)
        
        # Optional: Bind the "Escape" key to exit full screen
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))
        
        self.root.configure(bg="#F8F3F3")

        # --- Top Navigation Bar ---
        self.top_nav = tk.Frame(self.root, bg="#c5d5e5")
        self.top_nav.pack(side="top", fill="x")

        self.root.bind(
            "<Configure>",
            lambda e: self.top_nav.config(
            height=int(self.root.winfo_height() * 0.05)
    )
)



        
        nav_items = ["Monitor", "Manage", "Setup", "About"]
        for item in nav_items:
            btn = tk.Button(self.top_nav, text=item, bg="#c5d5e5", fg="blue", relief="flat", font=("Arial", 9))
            btn.pack(side="left", padx=10)

        # --- Header Section ---
        self.header = tk.Frame(self.root, bg="#000000", height=60)
        self.header.pack(fill="x", pady=5)
        
        # Logo Area (Left)
        self.logo_label = tk.Label(self.header, text="AuraSoft", fg="white", bg="#000000", font=("Arial", 16, "bold"))
        self.logo_label.pack(side="left", padx=20)

        # Title Label (Center)
        self.title_label = tk.Label(self.header, text="ANPR ACCESS - MONITOR", bg="#c5d5e5", fg="black", 
                                    font=("Arial", 14, "bold"), width=40)
        self.title_label.pack(side="left", expand=True)

        # Logout (Right)
        self.logout_btn = tk.Button(
            self.header, 
            text="Logout", 
            bg="#87ceeb", 
            relief="raised",
            command=self.root.destroy  # This triggers the window closure
        )
        self.logout_btn.pack(side="right", padx=20)
        # --- Main Body Layout ---
        self.main_container = tk.Frame(self.root, bg="#000000")
        self.main_container.pack(fill="both", expand=True, padx=10)

        # 1. Sidebar (Icons)
        self.sidebar = tk.Frame(self.main_container, bg="#c5d5e5", width=150)
        self.sidebar.pack(side="left", fill="y", padx=(0, 5))
        
        icons = ["Vehicles", "History", "Groups", "Users"]
        for icon in icons:
            btn = tk.Button(self.sidebar, text=icon, width=15, height=3)
            btn.pack(pady=10, padx=5)

        # 2. Central Feed Area
        self.center_frame = tk.Frame(self.main_container, bg="#000000")
        self.center_frame.pack(side="left", fill="both", expand=True)

        # Status indicators
        self.status_bar = tk.Frame(self.center_frame, bg="#000000")
        self.status_bar.pack(fill="x")
        tk.Label(self.status_bar, text="Camera Status: ", fg="#90ee90", bg="#000000").pack(side="left", padx=10)
        tk.Label(self.status_bar, text="Relay Status: ", fg="#90ee90", bg="#000000").pack(side="left", padx=20)

        # Main Camera View (Placeholder)
        self.cam_view = tk.Label(self.center_frame, text="[ Qpal Si Jeff ]", bg="#333333", fg="white", height=20)
        self.cam_view.pack(fill="both", expand=True, pady=5)

        # 3. Right Information Panel
        self.info_panel = tk.Frame(self.main_container, bg="#000000", width=300)
        self.info_panel.pack(side="right", fill="y", padx=5)

        self.plate_display = tk.Label(self.info_panel, text="ADW502", fg="#00ff00", bg="#000000", font=("Arial", 24, "bold"))
        self.plate_display.pack(pady=10)

        # Detailed Info Grid
        details = [
            ("Date:", "2026-02-11"),
            ("Type:", "WHITELIST"),
            ("Access:", "ALLOWED"),
            ("Name:", "New Plate"),
            ("Color:", "White")
        ]
        
        for label, val in details:
            row = tk.Frame(self.info_panel, bg="#000000")
            row.pack(fill="x", pady=2)
            tk.Label(row, text=label, fg="white", bg="#000000", width=10, anchor="w").pack(side="left")
            tk.Label(row, text=val, fg="#90ee90", bg="#000000", anchor="w").pack(side="left")

        # Capture Crop (Placeholder)
        self.crop_view = tk.Label(self.info_panel, text="[PLATE CROP]", bg="#333333", fg="white", height=8)
        self.crop_view.pack(fill="x", pady=20)

        # --- Bottom Table (History) ---
        self.setup_table()

    def setup_table(self):
        columns = ("PlateNumber", "Name", "Department", "Country", "TimeIn", "Result")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Sample Data
        data = [
            ("ADW502", "New Plate", "None", "PK", "06:28:14 PM", "Allowed"),
            ("LEB5700", "Old Plate", "None", "PK", "05:09:03 PM", "Denied"),
        ]

        for row in data:
            self.tree.insert("", "end", values=row)

        self.tree.pack(fill="x", padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ANPRDashboard(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk

class ANPRSearchScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("ANPR - Plate Search")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")

        # --- Top Navigation Bar (Light Blue) ---
        self.top_nav = tk.Frame(self.root, bg="#c5d5e5", height=30)
        self.top_nav.pack(side="top", fill="x")
        
        nav_items = ["Monitor", "Manage", "Setup", "About"]
        for item in nav_items:
            btn = tk.Button(self.top_nav, text=item, bg="#c5d5e5", fg="#4a4a4a", 
                            relief="flat", font=("Arial", 9), padx=10)
            btn.pack(side="left")

        # --- Search Header Section ---
        self.search_frame = tk.Frame(self.root, bg="white", pady=20)
        self.search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(self.search_frame, text="Plate Number", bg="white", 
                 font=("Arial", 11)).pack(side="left", padx=(20, 10))
        
        self.search_entry = tk.Entry(self.search_frame, font=("Arial", 12), width=20, relief="solid")
        self.search_entry.pack(side="left", padx=5)

        # Search Button (Grey style)
        self.search_btn = tk.Button(self.search_frame, text="🔍 Search", bg="#e1e1e1", 
                                    relief="raised", width=10, pady=5)
        self.search_btn.pack(side="left", padx=20)

        # Close Button (With 'X' style)
        self.close_btn = tk.Button(self.search_frame, text="❌ Close", bg="#e1e1e1", 
                                   relief="raised", width=10, pady=5)
        self.close_btn.pack(side="left")

        # --- Data Table Section ---
        self.table_container = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        self.table_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.setup_treeview()

    def setup_treeview(self):
        # Define Columns
        columns = ("PlateNumber", "Name", "Description", "Color", "LastModified", "DateAdded", "Username", "IDNumber", "Department")
        
        self.tree = ttk.Treeview(self.table_container, columns=columns, show="headings")
        
        # Define Headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        # --- Styling the Rows (Colors) ---
        self.tree.tag_configure('blue_row', background='#0078d7', foreground='white')
        self.tree.tag_configure('red_row', background='#ff0000', foreground='white')

        # Sample Data Insertion
        self.tree.insert("", "end", values=("ADW502", "New Plate", "", "White", "5/16/2022 4:11 PM", "5/16/2022 4:11 PM", "admin", "123", "None"), tags=('blue_row',))
        self.tree.insert("", "end", values=("LEB5700", "Old Plate", "", "Bronze", "5/16/2022 5:00 PM", "5/16/2022 4:11 PM", "admin", "456", ""), tags=('red_row',))

        self.tree.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ANPRSearchScreen(root)
    root.mainloop()
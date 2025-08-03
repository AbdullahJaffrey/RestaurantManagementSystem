import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from fpdf import FPDF
import datetime
import os
import json

class ModernRestaurantBilling:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_database()
        self.setup_variables()
        self.create_modern_ui()
        self.load_customers()
        
    def setup_window(self):
        self.root.title("🍽️ Pakistani & Chinese Restaurant")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f2f5')
        try:
            self.root.state('zoomed')  # Maximize window
        except:
            pass  # In case zoomed is not supported
        
        # Modern color scheme
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#34495e',
            'white': '#ffffff',
            'gray': '#95a5a6'
        }
        
    def setup_database(self):
        """Initialize SQLite database for customers and orders"""
        self.conn = sqlite3.connect('restaurant_billing.db')
        self.cursor = self.conn.cursor()
        
        # Create customers table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                created_date DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        # Create orders table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                bill_number TEXT UNIQUE,
                order_data TEXT,
                subtotal REAL,
                tax_amount REAL,
                service_charge REAL,
                total_amount REAL,
                order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        self.conn.commit()
        
    def setup_variables(self):
        """Initialize all tkinter variables"""
        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.bill_number = tk.StringVar(value=f"BILL{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")
        
        # Pakistani and Chinese menu items with prices
        self.menu_items = {
            'Pakistani Dishes': {
                'Chicken Karahi': 450,
                'Mutton Karahi': 650,
                'Chicken Biryani': 320,
                'Mutton Biryani': 480,
                'Chicken Tikka': 380,
                'Seekh Kebab': 350,
                'Chapli Kebab': 320,
                'Nihari': 420,
                'Haleem': 280,
                'Chicken Handi': 400,
                'Mutton Handi': 550,
                'Daal Chawal': 180,
                'Aloo Gosht': 380,
                'Palak Gosht': 420,
                'Chicken Jalfrezi': 360
            },
            'Chinese Dishes': {
                'Chicken Chow Mein': 280,
                'Beef Chow Mein': 320,
                'Chicken Fried Rice': 250,
                'Vegetable Fried Rice': 200,
                'Sweet & Sour Chicken': 340,
                'Chicken Manchurian': 320,
                'Hot & Sour Soup': 150,
                'Chicken Corn Soup': 180,
                'Spring Rolls': 220,
                'Honey Chicken': 360,
                'Szechuan Chicken': 380,
                'Dragon Chicken': 400,
                'Crispy Beef': 450,
                'Vegetable Manchurian': 240,
                'Chicken 65': 350
            },
            'Beverages & Desserts': {
                'Fresh Lime': 80,
                'Mango Lassi': 120,
                'Rooh Afza': 60,
                'Green Tea': 50,
                'Kashmiri Chai': 80,
                'Kulfi': 100,
                'Kheer': 120,
                'Gulab Jamun': 100,
                'Ras Malai': 150,
                'Ice Cream': 80,
                'Fresh Juice': 100,
                'Cold Drinks': 60
            }
        }
        
        self.order_items = {}
        self.current_customer_id = None
        
    def create_modern_ui(self):
        """Create the modern UI with improved design"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_frame)
        
        # Content area
        content_frame = tk.Frame(main_frame, bg=self.colors['white'], relief='raised', bd=2)
        content_frame.pack(fill='both', expand=True, pady=10)
        
        # Create notebook for tabs
        style = ttk.Style()
        style.configure('Custom.TNotebook.Tab', padding=[20, 10])
        
        self.notebook = ttk.Notebook(content_frame, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Billing tab
        self.billing_frame = tk.Frame(self.notebook, bg=self.colors['white'])
        self.notebook.add(self.billing_frame, text='🛒 New Order')
        
        # Customer management tab
        self.customer_frame = tk.Frame(self.notebook, bg=self.colors['white'])
        self.notebook.add(self.customer_frame, text='👥 Customer Management')
        
        # Order history tab
        self.history_frame = tk.Frame(self.notebook, bg=self.colors['white'])
        self.notebook.add(self.history_frame, text='📋 Order History')
        
        # Create tab contents
        self.create_billing_tab()
        self.create_customer_tab()
        self.create_history_tab()
        
    def create_header(self, parent):
        """Create header with restaurant name and info"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Restaurant name
        title_label = tk.Label(header_frame, 
                              text="🍽️ PAKISTANI & CHINESE RESTAURANT",
                              font=('Arial', 24, 'bold'),
                              bg=self.colors['primary'], 
                              fg=self.colors['white'])
        title_label.place(relx=0.5, rely=0.3, anchor='center')
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="Authentic Pakistani Cuisine & Chinese Delicacies",
                                 font=('Arial', 12),
                                 bg=self.colors['primary'],
                                 fg=self.colors['light'])
        subtitle_label.place(relx=0.5, rely=0.7, anchor='center')
        
        # Current date/time
        datetime_label = tk.Label(header_frame,
                                 text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                 font=('Arial', 10),
                                 bg=self.colors['primary'],
                                 fg=self.colors['light'])
        datetime_label.place(relx=0.95, rely=0.5, anchor='e')
        
    def create_billing_tab(self):
        """Create the main billing interface"""
        # Left panel - Customer info and menu
        left_panel = tk.Frame(self.billing_frame, bg=self.colors['white'])
        left_panel.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Customer info section
        self.create_customer_info_section(left_panel)
        
        # Menu section
        self.create_menu_section(left_panel)
        
        # Right panel - Bill area and summary
        right_panel = tk.Frame(self.billing_frame, bg=self.colors['light'], width=400)
        right_panel.pack(side='right', fill='y', padx=10, pady=10)
        right_panel.pack_propagate(False)
        
        self.create_bill_section(right_panel)
        
    def create_customer_info_section(self, parent):
        """Create customer information input section"""
        customer_frame = tk.LabelFrame(parent, text="Customer Information", 
                                     font=('Arial', 12, 'bold'),
                                     bg=self.colors['white'],
                                     fg=self.colors['primary'],
                                     relief='groove', bd=2)
        customer_frame.pack(fill='x', pady=(0, 10))
        
        # Customer input row
        input_frame = tk.Frame(customer_frame, bg=self.colors['white'])
        input_frame.pack(fill='x', padx=10, pady=10)
        
        # Name
        tk.Label(input_frame, text="Name:", font=('Arial', 10, 'bold'),
                bg=self.colors['white']).grid(row=0, column=0, sticky='w', padx=5)
        name_entry = tk.Entry(input_frame, textvariable=self.customer_name, 
                             font=('Arial', 10), width=20)
        name_entry.grid(row=0, column=1, padx=5, pady=2)
        
        # Phone
        tk.Label(input_frame, text="Phone:", font=('Arial', 10, 'bold'),
                bg=self.colors['white']).grid(row=0, column=2, sticky='w', padx=5)
        phone_entry = tk.Entry(input_frame, textvariable=self.customer_phone, 
                              font=('Arial', 10), width=15)
        phone_entry.grid(row=0, column=3, padx=5, pady=2)
        
        # Buttons
        btn_frame = tk.Frame(input_frame, bg=self.colors['white'])
        btn_frame.grid(row=0, column=4, padx=10)
        
        find_btn = tk.Button(btn_frame, text="🔍 Find Customer",
                           command=self.find_customer,
                           bg=self.colors['secondary'], fg='white',
                           font=('Arial', 9, 'bold'), relief='flat')
        find_btn.pack(side='left', padx=2)
        
        edit_btn = tk.Button(btn_frame, text="✏️ Edit Order",
                           command=self.edit_order,
                           bg=self.colors['warning'], fg='white',
                           font=('Arial', 9, 'bold'), relief='flat')
        edit_btn.pack(side='left', padx=2)
        
        # Bill number display
        bill_frame = tk.Frame(customer_frame, bg=self.colors['white'])
        bill_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(bill_frame, text="Bill Number:", font=('Arial', 10, 'bold'),
                bg=self.colors['white']).pack(side='left')
        tk.Label(bill_frame, textvariable=self.bill_number, font=('Arial', 10),
                bg=self.colors['white'], fg=self.colors['danger']).pack(side='left', padx=10)
        
    def create_menu_section(self, parent):
        """Create menu items section with categories"""
        menu_frame = tk.LabelFrame(parent, text="Menu Items", 
                                 font=('Arial', 12, 'bold'),
                                 bg=self.colors['white'],
                                 fg=self.colors['primary'],
                                 relief='groove', bd=2)
        menu_frame.pack(fill='both', expand=True)
        
        # Create notebook for menu categories
        menu_notebook = ttk.Notebook(menu_frame)
        menu_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        for category, items in self.menu_items.items():
            self.create_category_tab(menu_notebook, category, items)
            
    def create_category_tab(self, parent, category, items):
        """Create a tab for each menu category"""
        tab_frame = tk.Frame(parent, bg=self.colors['white'])
        parent.add(tab_frame, text=category)
        
        # Create scrollable frame
        canvas = tk.Canvas(tab_frame, bg=self.colors['white'])
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add menu items
        row = 0
        col = 0
        for item_name, price in items.items():
            self.create_menu_item(scrollable_frame, item_name, price, row, col)
            col += 1
            if col > 2:  # 3 items per row
                col = 0
                row += 1
                
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def create_menu_item(self, parent, item_name, price, row, col):
        """Create individual menu item widget"""
        item_frame = tk.Frame(parent, bg=self.colors['light'], relief='raised', bd=1)
        item_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        
        # Item name and price
        tk.Label(item_frame, text=item_name, font=('Arial', 10, 'bold'),
                bg=self.colors['light']).pack(pady=2)
        tk.Label(item_frame, text=f"Rs. {price}", font=('Arial', 9),
                bg=self.colors['light'], fg=self.colors['danger']).pack()
        
        # Quantity controls
        qty_frame = tk.Frame(item_frame, bg=self.colors['light'])
        qty_frame.pack(pady=5)
        
        if item_name not in self.order_items:
            self.order_items[item_name] = tk.IntVar()
        
        # Decrease button
        dec_btn = tk.Button(qty_frame, text="-", font=('Arial', 10, 'bold'),
                           bg=self.colors['danger'], fg='white', width=2,
                           command=lambda item=item_name: self.decrease_quantity(item))
        dec_btn.pack(side='left')
        
        # Quantity display
        qty_label = tk.Label(qty_frame, textvariable=self.order_items[item_name],
                           font=('Arial', 10), bg='white', width=3, relief='sunken')
        qty_label.pack(side='left', padx=2)
        
        # Increase button
        inc_btn = tk.Button(qty_frame, text="+", font=('Arial', 10, 'bold'),
                           bg=self.colors['success'], fg='white', width=2,
                           command=lambda item=item_name: self.increase_quantity(item))
        inc_btn.pack(side='left')
        
    def create_bill_section(self, parent):
        """Create bill display and summary section"""
        # Bill display
        bill_frame = tk.LabelFrame(parent, text="Bill Details", 
                                 font=('Arial', 12, 'bold'),
                                 bg=self.colors['light'],
                                 fg=self.colors['primary'])
        bill_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Bill text area
        text_frame = tk.Frame(bill_frame)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.bill_text = tk.Text(text_frame, font=('Courier', 10),
                               bg='white', fg='black', wrap='word')
        bill_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.bill_text.yview)
        self.bill_text.configure(yscrollcommand=bill_scrollbar.set)
        
        self.bill_text.pack(side="left", fill="both", expand=True)
        bill_scrollbar.pack(side="right", fill="y")
        
        # Summary and buttons
        summary_frame = tk.LabelFrame(parent, text="Order Summary", 
                                    font=('Arial', 12, 'bold'),
                                    bg=self.colors['light'],
                                    fg=self.colors['primary'])
        summary_frame.pack(fill='x', pady=(0, 10))
        
        self.create_summary_section(summary_frame)
        
        # Action buttons
        self.create_action_buttons(parent)
        
    def create_summary_section(self, parent):
        """Create order summary with calculations"""
        summary_inner = tk.Frame(parent, bg=self.colors['light'])
        summary_inner.pack(fill='x', padx=10, pady=10)
        
        # Summary labels
        self.subtotal_var = tk.StringVar(value="0.0")
        self.tax_var = tk.StringVar(value="0.0")
        self.service_var = tk.StringVar(value="0.0")
        self.total_var = tk.StringVar(value="0.0")
        
        # Subtotal
        tk.Label(summary_inner, text="Subtotal:", font=('Arial', 11, 'bold'),
                bg=self.colors['light']).grid(row=0, column=0, sticky='w', pady=2)
        tk.Label(summary_inner, text="Rs.", font=('Arial', 11),
                bg=self.colors['light']).grid(row=0, column=1, sticky='e')
        tk.Label(summary_inner, textvariable=self.subtotal_var, font=('Arial', 11),
                bg=self.colors['light']).grid(row=0, column=2, sticky='e', padx=(5, 0))
        
        # Tax (18%)
        tk.Label(summary_inner, text="Tax (18%):", font=('Arial', 11, 'bold'),
                bg=self.colors['light']).grid(row=1, column=0, sticky='w', pady=2)
        tk.Label(summary_inner, text="Rs.", font=('Arial', 11),
                bg=self.colors['light']).grid(row=1, column=1, sticky='e')
        tk.Label(summary_inner, textvariable=self.tax_var, font=('Arial', 11),
                bg=self.colors['light']).grid(row=1, column=2, sticky='e', padx=(5, 0))
        
        # Service Charge (5%)
        tk.Label(summary_inner, text="Service Charge (5%):", font=('Arial', 11, 'bold'),
                bg=self.colors['light']).grid(row=2, column=0, sticky='w', pady=2)
        tk.Label(summary_inner, text="Rs.", font=('Arial', 11),
                bg=self.colors['light']).grid(row=2, column=1, sticky='e')
        tk.Label(summary_inner, textvariable=self.service_var, font=('Arial', 11),
                bg=self.colors['light']).grid(row=2, column=2, sticky='e', padx=(5, 0))
        
        # Total
        tk.Frame(summary_inner, height=2, bg=self.colors['dark']).grid(row=3, column=0, columnspan=3, sticky='ew', pady=5)
        
        tk.Label(summary_inner, text="TOTAL:", font=('Arial', 12, 'bold'),
                bg=self.colors['light'], fg=self.colors['danger']).grid(row=4, column=0, sticky='w', pady=2)
        tk.Label(summary_inner, text="Rs.", font=('Arial', 12, 'bold'),
                bg=self.colors['light'], fg=self.colors['danger']).grid(row=4, column=1, sticky='e')
        tk.Label(summary_inner, textvariable=self.total_var, font=('Arial', 12, 'bold'),
                bg=self.colors['light'], fg=self.colors['danger']).grid(row=4, column=2, sticky='e', padx=(5, 0))
        
        # Configure column weights
        summary_inner.columnconfigure(0, weight=1)
        summary_inner.columnconfigure(1, weight=0)
        summary_inner.columnconfigure(2, weight=0)
        
    def create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg=self.colors['light'])
        button_frame.pack(fill='x', pady=10)
        
        # Calculate Total button
        calc_btn = tk.Button(button_frame, text="📊 Calculate Total",
                           command=self.calculate_total,
                           bg=self.colors['primary'], fg='white',
                           font=('Arial', 11, 'bold'), height=2)
        calc_btn.pack(fill='x', pady=2)
        
        # Save Order button
        save_btn = tk.Button(button_frame, text="💾 Save Order",
                           command=self.save_order,
                           bg=self.colors['success'], fg='white',
                           font=('Arial', 11, 'bold'), height=2)
        save_btn.pack(fill='x', pady=2)
        
        # Generate PDF button
        pdf_btn = tk.Button(button_frame, text="📄 Generate PDF",
                          command=self.generate_pdf,
                          bg=self.colors['warning'], fg='white',
                          font=('Arial', 11, 'bold'), height=2)
        pdf_btn.pack(fill='x', pady=2)
        
        # New Order button
        new_order_btn = tk.Button(button_frame, text="🆕 New Order",
                                command=self.new_order,
                                bg=self.colors['secondary'], fg='white',
                                font=('Arial', 11, 'bold'), height=2)
        new_order_btn.pack(fill='x', pady=2)
        
        # Clear All button
        clear_btn = tk.Button(button_frame, text="🗑️ Clear All",
                            command=self.clear_all,
                            bg=self.colors['danger'], fg='white',
                            font=('Arial', 11, 'bold'), height=2)
        clear_btn.pack(fill='x', pady=2)
        
    def create_customer_tab(self):
        """Create customer management tab"""
        # Customer search
        search_frame = tk.Frame(self.customer_frame, bg=self.colors['white'])
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="Search Customer:", font=('Arial', 12, 'bold'),
                bg=self.colors['white']).pack(side='left')
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 11), width=30)
        search_entry.pack(side='left', padx=10)
        
        search_btn = tk.Button(search_frame, text="🔍 Search",
                             command=self.search_customers,
                             bg=self.colors['secondary'], fg='white',
                             font=('Arial', 10, 'bold'))
        search_btn.pack(side='left', padx=5)
        
        # Customer list
        list_frame = tk.Frame(self.customer_frame, bg=self.colors['white'])
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for customer list
        columns = ('ID', 'Name', 'Phone', 'Created Date')
        self.customer_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=150, anchor='center')
        
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.customer_tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")
        
    def create_history_tab(self):
        """Create order history tab"""
        # Order history search
        history_search_frame = tk.Frame(self.history_frame, bg=self.colors['white'])
        history_search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(history_search_frame, text="Search Orders:", font=('Arial', 12, 'bold'),
                bg=self.colors['white']).pack(side='left')
        
        self.history_search_var = tk.StringVar()
        history_search_entry = tk.Entry(history_search_frame, textvariable=self.history_search_var, 
                                      font=('Arial', 11), width=30)
        history_search_entry.pack(side='left', padx=10)
        
        history_search_btn = tk.Button(history_search_frame, text="🔍 Search Orders",
                                     command=self.search_orders,
                                     bg=self.colors['secondary'], fg='white',
                                     font=('Arial', 10, 'bold'))
        history_search_btn.pack(side='left', padx=5)
        
        # Order history list
        history_list_frame = tk.Frame(self.history_frame, bg=self.colors['white'])
        history_list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for order history
        order_columns = ('Bill No', 'Customer', 'Phone', 'Subtotal', 'Tax', 'Service Charge', 'Total', 'Date')
        self.order_tree = ttk.Treeview(history_list_frame, columns=order_columns, show='headings', height=15)
        
        for col in order_columns:
            self.order_tree.heading(col, text=col)
            if col in ['Subtotal', 'Tax', 'Service Charge', 'Total']:
                self.order_tree.column(col, width=100, anchor='center')
            else:
                self.order_tree.column(col, width=120, anchor='center')
        
        # Scrollbar for order treeview
        order_tree_scroll = ttk.Scrollbar(history_list_frame, orient="vertical", command=self.order_tree.yview)
        self.order_tree.configure(yscrollcommand=order_tree_scroll.set)
        
        self.order_tree.pack(side="left", fill="both", expand=True)
        order_tree_scroll.pack(side="right", fill="y")
        
        # Load order history
        self.load_order_history()
        
    def increase_quantity(self, item_name):
        """Increase quantity of an item"""
        current = self.order_items[item_name].get()
        self.order_items[item_name].set(current + 1)
        self.update_bill_display()
        
    def decrease_quantity(self, item_name):
        """Decrease quantity of an item"""
        current = self.order_items[item_name].get()
        if current > 0:
            self.order_items[item_name].set(current - 1)
        self.update_bill_display()
        
    def update_bill_display(self):
        """Update the bill display in real-time"""
        self.bill_text.delete(1.0, tk.END)
        
        # Header
        self.bill_text.insert(tk.END, "=" * 40 + "\n")
        self.bill_text.insert(tk.END, "  PAKISTANI & CHINESE RESTAURANT\n")
        self.bill_text.insert(tk.END, "  Authentic Cuisine & Delicacies\n")
        self.bill_text.insert(tk.END, "=" * 40 + "\n\n")
        
        # Bill details
        self.bill_text.insert(tk.END, f"Bill No: {self.bill_number.get()}\n")
        self.bill_text.insert(tk.END, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.bill_text.insert(tk.END, f"Customer: {self.customer_name.get()}\n")
        self.bill_text.insert(tk.END, f"Phone: {self.customer_phone.get()}\n")
        self.bill_text.insert(tk.END, "-" * 40 + "\n\n")
        
        # Items
        self.bill_text.insert(tk.END, "ITEM                     QTY   PRICE   TOTAL\n")
        self.bill_text.insert(tk.END, "-" * 40 + "\n")
        
        subtotal = 0
        for category, items in self.menu_items.items():
            for item_name, price in items.items():
                qty = self.order_items[item_name].get()
                if qty > 0:
                    total_price = qty * price
                    subtotal += total_price
                    # Format item line
                    item_line = f"{item_name[:20]:<20} {qty:>3} {price:>6} {total_price:>7}\n"
                    self.bill_text.insert(tk.END, item_line)
        
        if subtotal > 0:
            # Calculations
            tax = round(subtotal * 0.18, 2)
            service_charge = round(subtotal * 0.05, 2)
            total = round(subtotal + tax + service_charge, 2)
            
            # Summary
            self.bill_text.insert(tk.END, "\n" + "-" * 40 + "\n")
            self.bill_text.insert(tk.END, f"Subtotal:              Rs. {subtotal:.2f}\n")
            self.bill_text.insert(tk.END, f"Tax (18%):             Rs. {tax:.2f}\n")
            self.bill_text.insert(tk.END, f"Service Charge (5%):   Rs. {service_charge:.2f}\n")
            self.bill_text.insert(tk.END, "=" * 40 + "\n")
            self.bill_text.insert(tk.END, f"TOTAL:                 Rs. {total:.2f}\n")
            self.bill_text.insert(tk.END, "=" * 40 + "\n\n")
            self.bill_text.insert(tk.END, "Thank you for visiting!\n")
            self.bill_text.insert(tk.END, "Come again soon!\n")
            
            # Update summary variables
            self.subtotal_var.set(f"{subtotal:.2f}")
            self.tax_var.set(f"{tax:.2f}")
            self.service_var.set(f"{service_charge:.2f}")
            self.total_var.set(f"{total:.2f}")
        else:
            self.subtotal_var.set("0.00")
            self.tax_var.set("0.00")
            self.service_var.set("0.00")
            self.total_var.set("0.00")
    
    def calculate_total(self):
        """Calculate and display total"""
        self.update_bill_display()
        messagebox.showinfo("Calculation Complete", "Order total has been calculated!")
    
    def find_customer(self):
        """Find customer by phone number"""
        phone = self.customer_phone.get().strip()
        if not phone:
            messagebox.showwarning("Warning", "Please enter phone number to search!")
            return
        
        self.cursor.execute("SELECT * FROM customers WHERE phone = ?", (phone,))
        customer = self.cursor.fetchone()
        
        if customer:
            self.current_customer_id = customer[0]
            self.customer_name.set(customer[1])
            
            # Load last order if exists
            self.cursor.execute("""
                SELECT order_data FROM orders 
                WHERE customer_id = ? 
                ORDER BY order_date DESC LIMIT 1
            """, (customer[0],))
            
            last_order = self.cursor.fetchone()
            if last_order:
                try:
                    order_data = json.loads(last_order[0])
                    for item_name, qty in order_data.items():
                        if item_name in self.order_items:
                            self.order_items[item_name].set(qty)
                    self.update_bill_display()
                    messagebox.showinfo("Customer Found", f"Customer found! Last order loaded.\nName: {customer[1]}")
                except:
                    messagebox.showinfo("Customer Found", f"Customer found!\nName: {customer[1]}")
            else:
                messagebox.showinfo("Customer Found", f"Customer found!\nName: {customer[1]}")
        else:
            # Ask if want to create new customer
            result = messagebox.askyesno("Customer Not Found", 
                                       "Customer not found. Would you like to create a new customer?")
            if result:
                self.create_new_customer()
    
    def create_new_customer(self):
        """Create new customer dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Customer")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['white'])
        dialog.grab_set()
        
        # Center the dialog
        dialog.transient(self.root)
        
        # Customer form
        form_frame = tk.Frame(dialog, bg=self.colors['white'])
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Name
        tk.Label(form_frame, text="Customer Name:", font=('Arial', 11, 'bold'),
                bg=self.colors['white']).grid(row=0, column=0, sticky='w', pady=5)
        name_var = tk.StringVar(value=self.customer_name.get())
        tk.Entry(form_frame, textvariable=name_var, font=('Arial', 11), width=25).grid(row=0, column=1, pady=5, padx=10)
        
        # Phone
        tk.Label(form_frame, text="Phone Number:", font=('Arial', 11, 'bold'),
                bg=self.colors['white']).grid(row=1, column=0, sticky='w', pady=5)
        phone_var = tk.StringVar(value=self.customer_phone.get())
        tk.Entry(form_frame, textvariable=phone_var, font=('Arial', 11), width=25).grid(row=1, column=1, pady=5, padx=10)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg=self.colors['white'])
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        def save_customer():
            if not name_var.get().strip() or not phone_var.get().strip():
                messagebox.showerror("Error", "Name and phone are required!")
                return
            
            try:
                self.cursor.execute("""
                    INSERT INTO customers (name, phone) 
                    VALUES (?, ?, ?, ?)
                """, (name_var.get().strip(), phone_var.get().strip()))
                
                self.conn.commit()
                self.current_customer_id = self.cursor.lastrowid
                
                # Update main form
                self.customer_name.set(name_var.get().strip())
                self.customer_phone.set(phone_var.get().strip())
                
                messagebox.showinfo("Success", "Customer created successfully!")
                dialog.destroy()
                self.load_customers()
                
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Phone number already exists!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create customer: {str(e)}")
        
        tk.Button(btn_frame, text="💾 Save Customer", command=save_customer,
                 bg=self.colors['success'], fg='white', font=('Arial', 11, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy,
                 bg=self.colors['danger'], fg='white', font=('Arial', 11, 'bold')).pack(side='left', padx=5)
    
    def edit_order(self):
        """Edit current order"""
        if not any(var.get() > 0 for var in self.order_items.values()):
            messagebox.showwarning("Warning", "No items in current order to edit!")
            return
        
        # Create edit dialog
        edit_dialog = tk.Toplevel(self.root)
        edit_dialog.title("Edit Order")
        edit_dialog.geometry("600x500")
        edit_dialog.configure(bg=self.colors['white'])
        edit_dialog.grab_set()
        
        # Current order items
        current_frame = tk.LabelFrame(edit_dialog, text="Current Order Items", 
                                    font=('Arial', 12, 'bold'), bg=self.colors['white'])
        current_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollable frame for items
        canvas = tk.Canvas(current_frame, bg=self.colors['white'])
        scrollbar = ttk.Scrollbar(current_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add current items to edit dialog
        row = 0
        for category, items in self.menu_items.items():
            for item_name, price in items.items():
                qty = self.order_items[item_name].get()
                if qty > 0:
                    item_edit_frame = tk.Frame(scrollable_frame, bg=self.colors['light'], relief='raised', bd=1)
                    item_edit_frame.grid(row=row, column=0, columnspan=4, sticky='ew', padx=5, pady=2)
                    
                    tk.Label(item_edit_frame, text=item_name, font=('Arial', 11, 'bold'),
                            bg=self.colors['light']).grid(row=0, column=0, sticky='w', padx=10)
                    tk.Label(item_edit_frame, text=f"Rs. {price}", font=('Arial', 10),
                            bg=self.colors['light']).grid(row=0, column=1, padx=10)
                    
                    # Quantity controls
                    tk.Button(item_edit_frame, text="-", font=('Arial', 10, 'bold'),
                             bg=self.colors['danger'], fg='white', width=2,
                             command=lambda item=item_name: self.decrease_quantity(item)).grid(row=0, column=2, padx=2)
                    
                    qty_label = tk.Label(item_edit_frame, text=str(qty), font=('Arial', 10),
                                       bg='white', width=3, relief='sunken')
                    qty_label.grid(row=0, column=3, padx=2)
                    
                    tk.Button(item_edit_frame, text="+", font=('Arial', 10, 'bold'),
                             bg=self.colors['success'], fg='white', width=2,
                             command=lambda item=item_name: self.increase_quantity(item)).grid(row=0, column=4, padx=2)
                    
                    # Remove item button
                    tk.Button(item_edit_frame, text="🗑️", font=('Arial', 8),
                             bg=self.colors['danger'], fg='white',
                             command=lambda item=item_name: self.remove_item(item)).grid(row=0, column=5, padx=10)
                    
                    row += 1
        
        # Close button
        tk.Button(edit_dialog, text="✅ Done Editing", command=edit_dialog.destroy,
                 bg=self.colors['primary'], fg='white', font=('Arial', 11, 'bold')).pack(pady=10)
    
    def remove_item(self, item_name):
        """Remove item from order"""
        self.order_items[item_name].set(0)
        self.update_bill_display()
        messagebox.showinfo("Item Removed", f"{item_name} removed from order!")
    
    def save_order(self):
        """Save order to database"""
        if not self.customer_name.get().strip():
            messagebox.showerror("Error", "Please enter customer information!")
            return
        
        # Check if there are items in order
        order_data = {}
        total_items = 0
        for item_name, qty_var in self.order_items.items():
            qty = qty_var.get()
            if qty > 0:
                order_data[item_name] = qty
                total_items += qty
        
        if total_items == 0:
            messagebox.showerror("Error", "No items in order!")
            return
        
        # Calculate totals
        subtotal = float(self.subtotal_var.get())
        tax = float(self.tax_var.get())
        service_charge = float(self.service_var.get())
        total = float(self.total_var.get())
        
        try:
            # Save or update customer if needed
            if not self.current_customer_id:
                self.cursor.execute("""
                    INSERT OR IGNORE INTO customers (name, phone)
                """, (self.customer_name.get().strip(), self.customer_phone.get().strip(),))
                self.conn.commit()
                
                self.cursor.execute("SELECT id FROM customers WHERE phone = ?", (self.customer_phone.get().strip(),))
                result = self.cursor.fetchone()
                if result:
                    self.current_customer_id = result[0]
            
            # Save order
            self.cursor.execute("""
                INSERT INTO orders (customer_id, bill_number, order_data, subtotal, tax_amount, service_charge, total_amount)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.current_customer_id, self.bill_number.get(), json.dumps(order_data),
                 subtotal, tax, service_charge, total))
            
            self.conn.commit()
            
            # Show success message with options
            result = messagebox.askyesno("Order Saved Successfully!", 
                                       f"Order saved successfully!\nBill Number: {self.bill_number.get()}\n\nWould you like to start a new order?")
            
            # Refresh displays
            self.load_customers()
            self.load_order_history()
            
            # If user wants new order, reset the form
            if result:
                self.new_order()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save order: {str(e)}")
    
    def new_order(self):
        """Start a new order - reset form but keep customer info"""
        result = messagebox.askyesno("New Order", 
                                   "Start a new order?\n\nThis will clear current order items but keep customer information.")
        if result:
            # Clear order items only
            for var in self.order_items.values():
                var.set(0)
            
            # Generate new bill number
            self.bill_number.set(f"BILL{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")
            
            # Clear bill display
            self.bill_text.delete(1.0, tk.END)
            
            # Reset summary
            self.subtotal_var.set("0.00")
            self.tax_var.set("0.00")
            self.service_var.set("0.00")
            self.total_var.set("0.00")
            
            # Update bill display with header only
            self.update_bill_display()
            
            messagebox.showinfo("New Order", "Ready for new order! Customer information retained.")
    
    def generate_pdf(self):
        """Generate PDF bill"""
        if not self.customer_name.get().strip():
            messagebox.showerror("Error", "Please enter customer information!")
            return
        
        # Check if there are items
        total_items = sum(var.get() for var in self.order_items.values())
        if total_items == 0:
            messagebox.showerror("Error", "No items in order!")
            return
        
        try:
            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            
            # Header
            pdf.cell(0, 10, 'PAKISTANI & CHINESE RESTAURANT', 0, 1, 'C')
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 8, 'Authentic Pakistani Cuisine & Chinese Delicacies', 0, 1, 'C')
            pdf.ln(5)
            
            # Bill details
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, f'Bill Number: {self.bill_number.get()}', 0, 1)
            pdf.cell(0, 6, f'Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1)
            pdf.cell(0, 6, f'Customer: {self.customer_name.get()}', 0, 1)
            pdf.cell(0, 6, f'Phone: {self.customer_phone.get()}', 0, 1)
            pdf.ln(5)
            
            # Table header
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(100, 8, 'ITEM', 1, 0, 'C')
            pdf.cell(20, 8, 'QTY', 1, 0, 'C')
            pdf.cell(30, 8, 'PRICE', 1, 0, 'C')
            pdf.cell(30, 8, 'TOTAL', 1, 1, 'C')
            
            # Items
            pdf.set_font('Arial', '', 9)
            subtotal = 0
            
            for category, items in self.menu_items.items():
                for item_name, price in items.items():
                    qty = self.order_items[item_name].get()
                    if qty > 0:
                        total_price = qty * price
                        subtotal += total_price
                        
                        pdf.cell(100, 6, item_name[:35], 1, 0, 'L')
                        pdf.cell(20, 6, str(qty), 1, 0, 'C')
                        pdf.cell(30, 6, f'Rs. {price}', 1, 0, 'R')
                        pdf.cell(30, 6, f'Rs. {total_price}', 1, 1, 'R')
            
            # Calculations
            tax = round(subtotal * 0.18, 2)
            service_charge = round(subtotal * 0.05, 2)
            total = round(subtotal + tax + service_charge, 2)
            
            pdf.ln(5)
            pdf.set_font('Arial', 'B', 10)
            
            # Summary
            pdf.cell(150, 6, 'Subtotal:', 0, 0, 'R')
            pdf.cell(30, 6, f'Rs. {subtotal:.2f}', 0, 1, 'R')
            
            pdf.cell(150, 6, 'Tax (18%):', 0, 0, 'R')
            pdf.cell(30, 6, f'Rs. {tax:.2f}', 0, 1, 'R')
            
            pdf.cell(150, 6, 'Service Charge (5%):', 0, 0, 'R')
            pdf.cell(30, 6, f'Rs. {service_charge:.2f}', 0, 1, 'R')
            
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(2)
            
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(150, 8, 'TOTAL:', 0, 0, 'R')
            pdf.cell(30, 8, f'Rs. {total:.2f}', 0, 1, 'R')
            
            pdf.ln(10)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 6, 'Thank you for visiting!', 0, 1, 'C')
            pdf.cell(0, 6, 'Come again soon!', 0, 1, 'C')
            
            # Save PDF
            filename = f"Bill_{self.bill_number.get()}.pdf"
            pdf.output(filename)
            
            # Show success message with options
            result = messagebox.askyesno("PDF Generated Successfully!", 
                                       f"PDF bill saved as: {filename}\n\nWould you like to start a new order?")
            
            if result:
                self.new_order()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")
    
    def clear_all(self):
        """Clear all fields and reset form"""
        result = messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all data?")
        if result:
            # Clear customer info
            self.customer_name.set("")
            self.customer_phone.set("")
            
            # Clear order items
            for var in self.order_items.values():
                var.set(0)
            
            # Reset bill number
            self.bill_number.set(f"BILL{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")
            
            # Clear current customer id
            self.current_customer_id = None
            
            # Clear bill display
            self.bill_text.delete(1.0, tk.END)
            
            # Reset summary
            self.subtotal_var.set("0.00")
            self.tax_var.set("0.00")
            self.service_var.set("0.00")
            self.total_var.set("0.00")
            
            messagebox.showinfo("Cleared", "All fields have been cleared!")
    
    def load_customers(self):
        """Load customers into the treeview"""
        # Clear existing items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Load customers from database
        self.cursor.execute("SELECT * FROM customers ORDER BY created_date DESC")
        customers = self.cursor.fetchall()
        
        for customer in customers:
            self.customer_tree.insert('', 'end', values=customer)
    
    def load_order_history(self):
        """Load order history into the treeview"""
        # Clear existing items
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        # Load orders with customer details
        self.cursor.execute("""
            SELECT o.bill_number, c.name, c.phone, o.subtotal, o.tax_amount, 
                   o.service_charge, o.total_amount, o.order_date
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            ORDER BY o.order_date DESC
        """)
        orders = self.cursor.fetchall()
        
        for order in orders:
            # Format the order data for display
            formatted_order = (
                order[0],  # Bill number
                order[1],  # Customer name
                order[2],  # Phone
                f"Rs. {order[3]:.2f}",  # Subtotal
                f"Rs. {order[4]:.2f}",  # Tax
                f"Rs. {order[5]:.2f}",  # Service charge
                f"Rs. {order[6]:.2f}",  # Total
                order[7][:16]  # Date (formatted)
            )
            self.order_tree.insert('', 'end', values=formatted_order)
    
    def search_customers(self):
        """Search customers by name or phone"""
        search_term = self.search_var.get().strip().lower()
        if not search_term:
            self.load_customers()
            return
        
        # Clear existing items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Search customers
        self.cursor.execute("""
            SELECT * FROM customers 
            WHERE LOWER(name) LIKE ? OR phone LIKE ?
            ORDER BY created_date DESC
        """, (f'%{search_term}%', f'%{search_term}%'))
        
        customers = self.cursor.fetchall()
        for customer in customers:
            self.customer_tree.insert('', 'end', values=customer)
    
    def search_orders(self):
        """Search orders by customer name, phone, or bill number"""
        search_term = self.history_search_var.get().strip().lower()
        if not search_term:
            self.load_order_history()
            return
        
        # Clear existing items
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        # Search orders
        self.cursor.execute("""
            SELECT o.bill_number, c.name, c.phone, o.subtotal, o.tax_amount, 
                   o.service_charge, o.total_amount, o.order_date
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            WHERE LOWER(c.name) LIKE ? OR c.phone LIKE ? OR LOWER(o.bill_number) LIKE ?
            ORDER BY o.order_date DESC
        """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        
        orders = self.cursor.fetchall()
        for order in orders:
            formatted_order = (
                order[0],  # Bill number
                order[1],  # Customer name
                order[2],  # Phone
                f"Rs. {order[3]:.2f}",  # Subtotal
                f"Rs. {order[4]:.2f}",  # Tax
                f"Rs. {order[5]:.2f}",  # Service charge
                f"Rs. {order[6]:.2f}",  # Total
                order[7][:16]  # Date (formatted)
            )
            self.order_tree.insert('', 'end', values=formatted_order)
    
    def __del__(self):
        """Close database connection when object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = ModernRestaurantBilling(root)
    root.mainloop()

if __name__ == "__main__":
    main()
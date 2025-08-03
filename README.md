# 🧾 Restaurant Billing System

A desktop-based GUI application for restaurant billing, customer management, and order history tracking. Built with **Python**, using **Tkinter** for the frontend, **SQLite** for data storage, and **FPDF** for bill generation.

---

## 📌 Features

- 🔘 **Tabbed Interface**
  - `New Order` – Dynamic food menu selection with real-time billing.
  - `Customer Management` – Add, search, and manage customer info.
  - `Order History` – View past bills and search by customer or bill number.

- 📄 **Auto Bill Generation**
  - Calculates **subtotal**, **18% tax**, and **5% service charge**.
  - Exports a styled bill as **PDF**.
  - Saves complete order details to database.

- 🗂️ **Local Database (SQLite)**
  - Customer and order data stored locally.
  - Fast read/write performance for small to medium-scale restaurants.

---

## 🧑‍💼 Roles

- **Staff**: Add/select customers, take orders, save/export bills, view history.
- **Admin (Planned)**: Staff management, menu updates, reports, login system.

---

## 💻 Tech Stack

| Component       | Technology        |
|----------------|-------------------|
| Frontend GUI    | Python (Tkinter)  |
| Backend Logic   | Python            |
| Database        | SQLite            |
| PDF Generator   | FPDF (Python lib) |
| File Handling   | os, datetime      |
| Data Storage    | JSON (orders)     |

---

## 📂 Project Structure

```
📁 Restaurant Billing System/
│
├── main.py                   # Main app file (Tkinter GUI)
├── restaurant_billing.db     # SQLite database
├── RestaurantBillingSystemDocumentation.docx
├── Bill_BILLYYYYMMDDHHMM.pdf # Sample generated PDF
└── README.md                 # Project readme
```

---

## 🖼️ Sample UI

- **New Order Tab**:  
  - Food items with quantity buttons
  - Dynamic billing (real-time subtotal, tax, service charge)
  - Customer info form
  - PDF generation button

- **Customer Management**:  
  - Add/find customers

- **Order History**:  
  - Table with previous orders (searchable by name/number)

---

## 🔧 How to Run

1. Ensure Python 3.x is installed.
2. Install dependencies:
   ```bash
   pip install fpdf
   ```
3. Run the application:
   ```bash
   python main.py
   ```

---

## 🔒 Future Enhancements

- Admin login and user role management  
- Editable menu from interface  
- Sales report (CSV/Excel)  
- Web version or cloud integration


```Thanks and Regards ❤️ ```

```Abdullah Jaffrey``` 

```abdullahjafri8@gmail.com```

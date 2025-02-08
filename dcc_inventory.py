import sys
import sqlite3
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel,
    QTextEdit, QTableWidget, QTableWidgetItem, QMessageBox
)

SERVER_URL = "http://127.0.0.1:8000"

class DCCInventoryManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DCC Inventory Manager")
        self.setGeometry(100, 100, 500, 400)
        layout = QVBoxLayout()

        # Title Label
        self.title = QLabel("<h2>📦 DCC Inventory Manager</h2>")
        layout.addWidget(self.title)

        # Table Display
        self.inventory_table = QTableWidget(self)
        self.inventory_table.setColumnCount(2)
        self.inventory_table.setHorizontalHeaderLabels(["Item", "Quantity"])
        layout.addWidget(self.inventory_table)
        self.refresh_inventory()

        # Add Item
        self.item_name = QLineEdit(self)
        self.item_name.setPlaceholderText("Enter item name")
        layout.addWidget(self.item_name)

        self.item_quantity = QLineEdit(self)
        self.item_quantity.setPlaceholderText("Enter item quantity")
        layout.addWidget(self.item_quantity)

        self.add_btn = QPushButton("➕ Add Item", self)
        self.add_btn.clicked.connect(self.add_item)
        layout.addWidget(self.add_btn)

        # Remove Item
        self.remove_name = QLineEdit(self)
        self.remove_name.setPlaceholderText("Item to remove")
        layout.addWidget(self.remove_name)

        self.remove_btn = QPushButton("❌ Remove Item", self)
        self.remove_btn.clicked.connect(self.remove_item)
        layout.addWidget(self.remove_btn)

        # Update Quantity
        self.update_name = QLineEdit(self)
        self.update_name.setPlaceholderText("Item to update")
        layout.addWidget(self.update_name)

        self.update_quantity = QLineEdit(self)
        self.update_quantity.setPlaceholderText("New quantity")
        layout.addWidget(self.update_quantity)

        self.update_btn = QPushButton("🔄 Update Quantity", self)
        self.update_btn.clicked.connect(self.update_item)
        layout.addWidget(self.update_btn)

        # Status Output
        self.output = QTextEdit(self)  # Added to prevent AttributeError
        self.output.setPlaceholderText("Server Responses...")
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        # Refresh Button
        self.refresh_btn = QPushButton("🔄 Refresh Inventory", self)
        self.refresh_btn.clicked.connect(self.refresh_inventory)
        layout.addWidget(self.refresh_btn)

        self.setLayout(layout)

    def add_item(self):
        name = self.item_name.text()
        quantity = self.item_quantity.text()
        if not name or not quantity.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid name and quantity.")
            return
        response = requests.post(f"{SERVER_URL}/add-item?name={name}&quantity={quantity}")
        self.output.setText(response.text)
        self.refresh_inventory()

    def remove_item(self):
        name = self.remove_name.text()
        if not name:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid item name.")
            return
        response = requests.post(f"{SERVER_URL}/remove-item?name={name}")
        self.output.setText(response.text)
        self.refresh_inventory()

    def update_item(self):
        name = self.update_name.text()
        quantity = self.update_quantity.text()
        if not name or not quantity.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid name and numeric quantity.")
            return
        response = requests.post(f"{SERVER_URL}/update-quantity?name={name}&new_quantity={quantity}")
        self.output.setText(response.text)
        self.refresh_inventory()

    def refresh_inventory(self):
        """ Fetches the inventory and updates the table display """
        try:
            conn = sqlite3.connect("inventory.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventory")
            data = cursor.fetchall()
            conn.close()
            
            self.inventory_table.setRowCount(len(data))
            for i, (name, quantity) in enumerate(data):
                self.inventory_table.setItem(i, 0, QTableWidgetItem(name))
                self.inventory_table.setItem(i, 1, QTableWidgetItem(str(quantity)))
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error fetching inventory: {str(e)}")  # Fix for self.output error


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DCCInventoryManager()
    window.show()
    sys.exit(app.exec_())


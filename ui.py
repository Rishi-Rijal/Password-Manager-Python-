
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QLineEdit, QLabel, QCheckBox, QSizePolicy,
    QMessageBox, QProgressBar, QStackedWidget, QFrame, QComboBox, QInputDialog

)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from automateEmail import send_reset_email

from datetime import datetime
import random

import db
import pin_manager
import crypto_manager
from utils import get_password_strength, generate_password, generate_passphrase
import log_manager

class PasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.resize(2500, 1300)
        self.setStyleSheet(self.get_stylesheet())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.sidebar = self.create_sidebar()
        self.stack = QStackedWidget()

        self.home_page = QWidget()
        self.settings_page = QWidget()
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.settings_page)

        self.init_home_ui()
        self.init_settings_ui()

        main_layout = QHBoxLayout(self.central_widget)
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 4)

    def initUI(self):
        self.central = QStackedWidget()
        self.setCentralWidget(self.central)

        self.home_page = QWidget()
        self.setup_home_ui()

        self.settings_page = QWidget()
        self.setup_settings_ui()

        self.central.addWidget(self.home_page)
        self.central.addWidget(self.settings_page)
        self.central.setCurrentWidget(self.home_page)

        # Navigation
        nav = QHBoxLayout()
        nav_btn_home = QPushButton("Home")
        nav_btn_home.clicked.connect(lambda: self.central.setCurrentWidget(self.home_page))
        nav_btn_settings = QPushButton("Settings")
        nav_btn_settings.clicked.connect(lambda: self.central.setCurrentWidget(self.settings_page))

        nav.addWidget(nav_btn_home)
        nav.addWidget(nav_btn_settings)

        wrapper = QVBoxLayout()
        wrapper.addLayout(nav)
        wrapper.addWidget(self.central)

        container = QWidget()
        container.setLayout(wrapper)
        self.setCentralWidget(container)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        layout = QVBoxLayout(sidebar)

        home_btn = QPushButton("Home")
        home_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.home_page))

        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.settings_page))

        layout.addWidget(QLabel("\n  MENU"))
        layout.addWidget(home_btn)
        layout.addWidget(settings_btn)
        layout.addStretch()

        sidebar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        return sidebar
    
    def get_stylesheet(self):
        return """
        /* Base Widget Styling */
        QWidget {
            font-family: 'Segoe UI', sans-serif;
            font-size: 20px;
            background-color: #1e1e2f;
            color: #ffffff;
        }

        /* Headings and Labels */
        QLabel {
            font-size: 20px;
            padding: 6px;
        }

        /* Inputs and ComboBoxes */
        QLineEdit, QComboBox {
            background-color: #2a2e3d;
            border: 1px solid #444;
            border-radius: 8px;
            padding: 12px;
            font-size: 20px;
            color: #ffffff;
            selection-background-color: #55608f;
        }

        /* Buttons */
        QPushButton {
            background-color: #3A3F58;
            color: white;
            padding: 12px 24px;  /* ⬅️ More padding = more spacious */
            border: none;
            border-radius: 8px;
            font-size: 20px;
            font-weight: 500;
            min-width: 100px;
            min-height: 40px;
        }
        QPushButton:hover {
            background-color: #55608f;
        }
        QPushButton:pressed {
            background-color: #2c2f45;
        }
        QPushButton:checked {
            background-color: #2c2f45;
            color: #aad;
        }

        /* Checkboxes */
        QCheckBox {
            spacing: 8px;
            font-size: 20px;
        }
        QCheckBox::indicator {
            border: 1px solid #aaa;
            background: #2a2e3d;
            width: 18px;
            height: 20px;
            border-radius: 4px;
        }
        QCheckBox::indicator:checked {
            background-color: #5cb85c;
            border: 1px solid #5cb85c;
        }

        /* Tables */
        QTableWidget {
            background-color: #2a2e3d;
            alternate-background-color: #1e1e2f;
            border: 1px solid #444;
            color: #f0f0f0;
            font-size: 20px;
        }
        QHeaderView::section {
            background-color: #3A3F58;
            padding: 10px;
            font-size: 20px;
            font-weight: bold;
            border: none;
            color: white;
        }
        QTableWidget::item {
            padding: 10px;
        }
        QTableWidget::item:selected {
            background-color: #55608f;
        }

        /* Frames / Cards */
        QFrame {
            background-color: #2a2e3d;
            border-radius: 10px;
            padding: 16px;
        }

        /* Progress Bar */
        QProgressBar {
            border: 1px solid #444;
            border-radius: 8px;
            background-color: #2a2e3d;
            height: 24px;
            font-size: 20px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #5cb85c;
            border-radius: 8px;
        }

        /* ToolTips */
        QToolTip {
            background-color: #3A3F58;
            color: white;
            border: 1px solid #444;
            padding: 8px;
            border-radius: 6px;
            font-size: 20px;
        }

        """

    def init_home_ui(self):
        layout = QVBoxLayout(self.home_page)
        label = QLabel("Home Page")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        form_layout = QHBoxLayout()

        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("Website")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.textChanged.connect(self.update_strength)

        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setIcon(QIcon.fromTheme("edit-copy"))
        self.copy_btn.setToolTip("Copy password")
        self.copy_btn.clicked.connect(self.copy_password_to_clipboard)

        self.generate_btn = QPushButton("Generate")
        self.generate_btn.clicked.connect(self.fill_generated_password)

        self.generator_mode = QComboBox()
        self.generator_mode.addItems(["Random", "Passphrase"])
        self.generator_mode.setToolTip("Choose password generation method")
        form_layout.addWidget(self.generator_mode)


        self.show_password_cb = QCheckBox("Show")
        self.show_password_cb.toggled.connect(self.toggle_password_visibility)

        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setValue(0)
        self.strength_bar.setTextVisible(True)

        form_layout.addWidget(QLabel("Website:"))
        form_layout.addWidget(self.website_input)
        form_layout.addWidget(QLabel("Username:"))
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(QLabel("Password:"))
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.copy_btn)
        form_layout.addWidget(self.generate_btn)
        form_layout.addWidget(self.show_password_cb)
        form_layout.addWidget(self.strength_bar)

        layout.addLayout(form_layout)

        control_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_entry)

        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self.update_entry)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_entry)

        self.reveal_btn = QPushButton("Reveal")
        self.reveal_btn.clicked.connect(self.reveal_password)

        self.pin_btn = QPushButton("Change PIN")
        self.pin_btn.clicked.connect(self.change_pin)

        control_layout.addWidget(self.add_btn)
        control_layout.addWidget(self.update_btn)
        control_layout.addWidget(self.delete_btn)
        control_layout.addWidget(self.reveal_btn)
        control_layout.addWidget(self.pin_btn)
        layout.addLayout(control_layout)

        # --- Search Bar ---
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by website or username...")
        self.search_input.textChanged.connect(self.load_data)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        self.show_expired_btn = QPushButton("Show Expired Only")
        self.show_expired_btn.setCheckable(True)
        self.show_expired_btn.toggled.connect(self.load_data)
        search_layout.addWidget(self.show_expired_btn)


        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Website", "Username", "Password", "Last Updated"])

        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.cellClicked.connect(self.load_entry)

        layout.addWidget(self.table)
        self.load_data()

    def init_settings_ui(self):
        layout = QVBoxLayout(self.settings_page)
        label = QLabel("Settings Page")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        theme_toggle = QPushButton("Toggle Theme (Placeholder)")
        layout.addWidget(theme_toggle)

        export_btn = QPushButton("Export Vault (Placeholder)")
        layout.addWidget(export_btn)

        reset_btn = QPushButton("Reset App (Placeholder)")
        layout.addWidget(reset_btn)

    def toggle_password_visibility(self):
        self.password_input.setEchoMode(QLineEdit.Normal if self.show_password_cb.isChecked() else QLineEdit.Password)

    def load_data(self):
        query = self.search_input.text().lower() if hasattr(self, 'search_input') else ""
        show_only_expired = self.show_expired_btn.isChecked() if hasattr(self, 'show_expired_btn') else False

        self.table.setRowCount(0)
        for row_num, row_data in enumerate(db.view()):
            website = row_data[1].lower()
            username = row_data[2].lower()
            last_updated = row_data[4]

            # Apply text search filter
            if query and query not in website and query not in username:
                continue

            # Apply expired filter
            if show_only_expired:
                try:
                    dt = datetime.fromisoformat(last_updated)
                    days_old = (datetime.now() - dt).days
                    if days_old <= 90:
                        continue
                except:
                    continue

            self.table.insertRow(self.table.rowCount())
            for col_num, data in enumerate(row_data):
                if col_num == 3:  # mask password
                    self.table.setItem(row_num, col_num, QTableWidgetItem("********"))
                elif col_num == 4:  # format timestamp + expiry
                    item = QTableWidgetItem()
                    try:
                        dt = datetime.fromisoformat(data)
                        formatted = dt.strftime("%Y-%m-%d %H:%M")
                        days_old = (datetime.now() - dt).days
                        item.setText(formatted)
                        if days_old > 90:
                            item.setForeground(QtGui.QColor("red"))
                            item.setToolTip(f"Password is {days_old} days old. Click to update.")
                    except:
                        item.setText(data)
                    self.table.setItem(row_num, col_num, item)
                else:
                    self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))


    def load_entry(self, row, _):
        self.selected_id = int(self.table.item(row, 0).text())
        self.website_input.setText(self.table.item(row, 1).text())
        self.username_input.setText(self.table.item(row, 2).text())
        self.password_input.setText(self.table.item(row, 3).text())  # currently masked

        # Check if password is expired
        try:
            timestamp = self.table.item(row, 4).text()
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
            days_old = (datetime.now() - dt).days
            if days_old > 90:
                result = QMessageBox.question(
                    self,
                    "Password Expired",
                    f"This password is {days_old} days old.\nDo you want to generate a new one?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if result == QMessageBox.Yes:
                    self.fill_generated_password()
        except Exception as e:
            pass  # Ignore if timestamp parsing fails


    def add_entry(self):
        website = self.website_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if not website or not username or not password:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        strength = get_password_strength(password)
        if strength == "Weak":
            QMessageBox.warning(self, "Weak Password", "Choose a stronger password.")
            return

        db.insert(website, username, password)
        self.load_data()
        self.clear_inputs()
        log_manager.log_action("Add Entry", f"{website} / {username}")

    def update_entry(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "Error", "Select an entry first.")
            return
        password_text = self.password_input.text()
        if(password_text.count('*') > 7):
            QMessageBox.warning(self, "Not Valid Password", "Enter a valid password(Not *).")
            return
        db.update(
            self.selected_id,
            self.website_input.text(),
            self.username_input.text(),
            self.password_input.text())
        self.load_data()
        self.clear_inputs()

    def delete_entry(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "Error", "Select an entry to delete.")
            return
        
        response = QMessageBox.question(
            self,
            "Conformation",
            "Do You want to delete the password?",
            QMessageBox.Yes | QMessageBox.No
        )

        if response == QMessageBox.No:
            return

        db.delete(self.selected_id)
        self.load_data()
        self.clear_inputs()
        log_manager.log_action("Delete Entry", f"ID {self.selected_id}")


    def clear_inputs(self):
        self.website_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.selected_id = None
        self.table.clearSelection()

    def reveal_password(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "Error", "Select an entry first.")
            return
        pin, ok = QtWidgets.QInputDialog.getText(self, "PIN", "Enter PIN:", QLineEdit.Password)
        if ok and pin_manager.validate_pin(pin):
            for row in db.view():
                if row[0] == self.selected_id:
                    try:
                        decrypted = crypto_manager.decrypt_password(row[3])
                        QMessageBox.information(self, "Password", f"Password: {decrypted}")
                        QApplication.clipboard().setText(db.get_password(self.selected_id))
                    except Exception:
                        QMessageBox.critical(self, "Error", "Failed to decrypt password.")
        else:
            QMessageBox.warning(self, "Access Denied", "Incorrect PIN.")

    def change_pin(self):
        if pin_manager.pin_exists():
            old, ok = QtWidgets.QInputDialog.getText(self, "Current PIN", "Enter current PIN:", QLineEdit.Password)
            if not ok or not pin_manager.validate_pin(old):
                self.ask_for_reset()
                return
        new, ok1 = QtWidgets.QInputDialog.getText(self, "New PIN", "Enter new PIN:", QLineEdit.Password)
        confirm, ok2 = QtWidgets.QInputDialog.getText(self, "Confirm PIN", "Re-enter new PIN:", QLineEdit.Password)
        if ok1 and ok2:
            if new != confirm:
                QMessageBox.warning(self, "Error", "PIN Doesn't Match.")
            elif len(new) < 4:
                QMessageBox.warning(self, "Error", "PIN too short.")
            else:
                pin_manager.set_pin(new)
                QMessageBox.information(self, "Success", "PIN updated.")

    def ask_for_reset(self):
        response = QMessageBox.question(
            self,
            "Incorrect PIN",
            "Incorrect PIN.\nDo you want to reset your PIN?",
            QMessageBox.Yes | QMessageBox.No
        )

        if response == QMessageBox.Yes:
            self.handle_reset()
        else:
            QMessageBox.information(self, "Cancelled", "PIN reset cancelled.")

    def handle_reset(self):
        generated_code = str(random.randint(100000, 999999)) 
        send_reset_email("r.ramishir@gmail.com",generated_code)
        code, ok = QInputDialog.getText(self, "Enter Reset Code", "Enter your reset code:")
        if not ok:
            return

        if code.strip() == generated_code:
            new_pin, ok = QInputDialog.getText(self, "New PIN", "Enter your new 4-digit PIN:")
            if ok and new_pin:
                pin_manager.set_pin(new_pin)
                QMessageBox.information(self, "PIN Reset", "Your PIN has been reset successfully.")
        else:
            QMessageBox.warning(self, "Invalid Code", "Reset code is incorrect.")

    def update_strength(self):
        strength = get_password_strength(self.password_input.text())
        value = {"Weak": 25, "Moderate": 60, "Strong": 100}.get(strength, 0)
        color = {"Weak": "red", "Moderate": "orange", "Strong": "green"}.get(strength, "gray")

        self.strength_bar.setValue(value)
        self.strength_bar.setFormat(f"Strength: {strength}")
        self.strength_bar.setStyleSheet(f"""
            QProgressBar::chunk {{ background-color: {color}; }}
            QProgressBar {{ text-align: center; }}
        """)

    def fill_generated_password(self):
        mode = self.generator_mode.currentText()
        if mode == "Random":
            pwd = generate_password()
        else:
            pwd = generate_passphrase()
        self.password_input.setText(pwd)
        self.update_strength()


    def copy_password_to_clipboard(self):
        QApplication.clipboard().setText(self.password_input.text())
        QtWidgets.QToolTip.showText(self.copy_btn.mapToGlobal(self.copy_btn.rect().center()), "Copied!")
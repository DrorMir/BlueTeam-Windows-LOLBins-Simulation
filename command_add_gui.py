#!/usr/bin/env python3
"""
Command GUI - A PyQt6-based GUI for adding custom commands to the attack simulator.

This module provides a user-friendly interface for adding, editing, and managing
custom commands in the attack simulator's commands.json file.
"""

import sys
import json
import os
from typing import Dict, List, Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QLineEdit, QTextEdit, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QSplitter, QGroupBox, QLabel, QFileDialog, QTabWidget,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor


class CommandEntry:
    """Represents a single command entry with all its properties."""
    
    def __init__(self, command: str = "", description: str = "", 
                 severity: str = "Informational", mitre_tag: str = ""):
        self.command = command
        self.description = description
        self.severity = severity
        self.mitre_tag = mitre_tag
    
    def to_dict(self) -> Dict[str, str]:
        """Convert the command entry to a dictionary."""
        return {
            "Command": self.command,
            "Description": self.description,
            "Severity": self.severity,
            "MitreAttackTag": self.mitre_tag
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'CommandEntry':
        """Create a CommandEntry from a dictionary."""
        return cls(
            command=data.get("Command", ""),
            description=data.get("Description", ""),
            severity=data.get("Severity", "Informational"),
            mitre_tag=data.get("MitreAttackTag", "")
        )


class CommandInputWidget(QWidget):
    """Widget for inputting command details."""
    
    command_added = pyqtSignal(CommandEntry)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        
        # Create a group box for the input form
        input_group = QGroupBox("Add New Command")
        input_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #333333;
            }
        """)
        
        form_layout = QFormLayout()
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form_layout.setContentsMargins(15, 15, 15, 15)
        
        # Common stylesheet for input fields
        input_field_style = """
            QLineEdit, QTextEdit, QComboBox {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                color: #333333;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 1px solid #2196f3;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png); /* Placeholder for a down arrow icon */
            }
        """
        
        # Command input
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter the command to execute...")
        self.command_input.setMinimumHeight(35)
        self.command_input.setStyleSheet(input_field_style)
        form_layout.addRow("Command:", self.command_input)
        
        # Description input
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter a description of what this command does...")
        self.description_input.setMaximumHeight(100)
        self.description_input.setStyleSheet(input_field_style)
        form_layout.addRow("Description:", self.description_input)
        
        # Severity selection
        self.severity_combo = QComboBox()
        self.severity_combo.addItems([
            "Informational", "Low", "Medium", "High", "Critical"
        ])
        self.severity_combo.setMinimumHeight(35)
        self.severity_combo.setStyleSheet(input_field_style)
        form_layout.addRow("Severity:", self.severity_combo)
        
        # MITRE ATT&CK Tag input
        self.mitre_input = QLineEdit()
        self.mitre_input.setPlaceholderText("e.g., T1059.001")
        self.mitre_input.setMinimumHeight(35)
        self.mitre_input.setStyleSheet(input_field_style)
        form_layout.addRow("MITRE ATT&CK Tag:", self.mitre_input)
        
        input_group.setLayout(form_layout)
        layout.addWidget(input_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(15, 0, 15, 15)
        
        self.add_button = QPushButton("Add Command")
        self.add_button.setMinimumHeight(40)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.add_button.clicked.connect(self.add_command)
        
        self.clear_button = QPushButton("Clear Form")
        self.clear_button.setMinimumHeight(40)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        self.clear_button.clicked.connect(self.clear_form)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def add_command(self):
        """Add a new command based on the form input."""
        command = self.command_input.text().strip()
        description = self.description_input.toPlainText().strip()
        severity = self.severity_combo.currentText()
        mitre_tag = self.mitre_input.text().strip()
        
        if not command:
            QMessageBox.warning(self, "Input Error", "Command field is required!")
            return
        
        if not description:
            QMessageBox.warning(self, "Input Error", "Description field is required!")
            return
        
        entry = CommandEntry(command, description, severity, mitre_tag)
        self.command_added.emit(entry)
        self.clear_form()
    
    def clear_form(self):
        """Clear all form fields."""
        self.command_input.clear()
        self.description_input.clear()
        self.severity_combo.setCurrentIndex(0)
        self.mitre_input.clear()


class CommandTableWidget(QWidget):
    """Widget for displaying and managing commands in a table."""
    
    def __init__(self):
        super().__init__()
        self.commands: List[CommandEntry] = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        
        # Create a group box for the table
        table_group = QGroupBox("Current Commands")
        table_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #2196f3;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #333333;
            }
        """)
        
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create the table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Command", "Description", "Severity", "MITRE ATT&CK"
        ])
        
        # Configure table appearance
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:selected {
                background-color: #a0d8ff; /* Lighter blue for selection */
                color: black;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 10px;
                border: 1px solid #cccccc;
                font-weight: bold;
                font-size: 14px;
                color: #333333;
            }
        """)
        
        table_layout.addWidget(self.table)
        
        # Buttons for table operations
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setMinimumHeight(35)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        self.delete_button.clicked.connect(self.delete_selected)
        
        self.clear_all_button = QPushButton("Clear All")
        self.clear_all_button.setMinimumHeight(35)
        self.clear_all_button.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
            QPushButton:pressed {
                background-color: #ef6c00;
            }
        """)
        self.clear_all_button.clicked.connect(self.clear_all)
        
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_all_button)
        button_layout.addStretch()
        
        table_layout.addLayout(button_layout)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
        self.setLayout(layout)
    
    def add_command(self, command: CommandEntry):
        """Add a command to the table."""
        self.commands.append(command)
        self.refresh_table()
    
    def delete_selected(self):
        """Delete the selected command from the table."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(
                self, "Confirm Delete",
                "Are you sure you want to delete the selected command?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                del self.commands[current_row]
                self.refresh_table()
    
    def clear_all(self):
        """Clear all commands from the table."""
        if self.commands:
            reply = QMessageBox.question(
                self, "Confirm Clear All",
                "Are you sure you want to delete all commands?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.commands.clear()
                self.refresh_table()
    
    def refresh_table(self):
        """Refresh the table display."""
        self.table.setRowCount(len(self.commands))
        
        for row, command in enumerate(self.commands):
            self.table.setItem(row, 0, QTableWidgetItem(command.command))
            self.table.setItem(row, 1, QTableWidgetItem(command.description))
            
            # Color-code severity
            severity_item = QTableWidgetItem(command.severity)
            if command.severity == "Critical":
                severity_item.setBackground(QColor("#f44336"))
                severity_item.setForeground(QColor("white"))
            elif command.severity == "High":
                severity_item.setBackground(QColor("#ff9800"))
                severity_item.setForeground(QColor("white"))
            elif command.severity == "Medium":
                severity_item.setBackground(QColor("#ffeb3b"))
                severity_item.setForeground(QColor("black"))
            elif command.severity == "Low":
                severity_item.setBackground(QColor("#4caf50"))
                severity_item.setForeground(QColor("white"))
            else:  # Informational
                severity_item.setBackground(QColor("#2196f3"))
                severity_item.setForeground(QColor("white"))
            
            self.table.setItem(row, 2, severity_item)
            self.table.setItem(row, 3, QTableWidgetItem(command.mitre_tag))
    
    def load_commands(self, commands: List[CommandEntry]):
        """Load commands into the table."""
        self.commands = commands
        self.refresh_table()
    
    def get_commands(self) -> List[CommandEntry]:
        """Get all commands from the table."""
        return self.commands.copy()


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.commands_file = "commands.json"
        self.init_ui()
        self.load_existing_commands()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Attack Simulator - Command Manager")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #e0e0e0; /* Lighter grey background */
            }
            QWidget {
                font-family: "Segoe UI", "Helvetica Neue", "Arial", sans-serif;
                color: #333333;
            }
            QLabel {
                color: #333333;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Attack Simulator - Command Manager")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50; /* Darker blue-grey for title */
                padding: 20px;
                background-color: white;
                border-radius: 8px;
                margin-bottom: 10px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Create splitter for input and table
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #cccccc;
                width: 5px;
            }
            QSplitter::handle:hover {
                background-color: #a0a0a0;
            }
        """)
        
        # Input widget
        self.input_widget = CommandInputWidget()
        self.input_widget.command_added.connect(self.add_command)
        splitter.addWidget(self.input_widget)
        
        # Table widget
        self.table_widget = CommandTableWidget()
        splitter.addWidget(self.table_widget)
        
        # Set splitter proportions
        splitter.setSizes([400, 800])
        main_layout.addWidget(splitter)
        
        # File operations buttons
        file_layout = QHBoxLayout()
        file_layout.setContentsMargins(0, 10, 0, 0)
        file_layout.setSpacing(10)
        
        self.load_button = QPushButton("Load Commands")
        self.load_button.setMinimumHeight(40)
        self.load_button.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                padding: 8px 16px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #1565c0;
            }
        """)
        self.load_button.clicked.connect(self.load_commands)
        
        self.save_button = QPushButton("Save Commands")
        self.save_button.setMinimumHeight(40)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                padding: 8px 16px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.save_button.clicked.connect(self.save_commands)
        
        self.export_button = QPushButton("Export Commands")
        self.export_button.setMinimumHeight(40)
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                padding: 8px 16px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
            QPushButton:pressed {
                background-color: #ef6c00;
            }
        """)
        self.export_button.clicked.connect(self.export_commands)
        
        file_layout.addWidget(self.load_button)
        file_layout.addWidget(self.save_button)
        file_layout.addWidget(self.export_button)
        file_layout.addStretch()
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            QLabel {
                padding: 10px;
                background-color: white;
                border-top: 1px solid #cccccc;
                color: #666666;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        file_layout.addWidget(self.status_label)
        main_layout.addLayout(file_layout)
        
        central_widget.setLayout(main_layout)
    
    def add_command(self, command: CommandEntry):
        """Add a command to the table."""
        self.table_widget.add_command(command)
        self.status_label.setText(f"Added command: {command.command[:50]}...")
    
    def load_existing_commands(self):
        """Load existing commands from the commands.json file."""
        if os.path.exists(self.commands_file):
            try:
                with open(self.commands_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    commands = [CommandEntry.from_dict(item) for item in data]
                    self.table_widget.load_commands(commands)
                    self.status_label.setText(f"Loaded {len(commands)} commands from {self.commands_file}")
            except Exception as e:
                QMessageBox.warning(self, "Load Error", f"Failed to load commands: {str(e)}")
                self.status_label.setText("Failed to load existing commands")
    
    def load_commands(self):
        """Load commands from a selected file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Commands", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    commands = [CommandEntry.from_dict(item) for item in data]
                    self.table_widget.load_commands(commands)
                    self.status_label.setText(f"Loaded {len(commands)} commands from {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Load Error", f"Failed to load commands: {str(e)}")
                self.status_label.setText("Failed to load commands")
    
    def save_commands(self):
        """Save commands to the commands.json file."""
        try:
            commands = self.table_widget.get_commands()
            data = [command.to_dict() for command in commands]
            
            with open(self.commands_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            self.status_label.setText(f"Saved {len(commands)} commands to {self.commands_file}")
            QMessageBox.information(self, "Save Successful", f"Commands saved to {self.commands_file}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save commands: {str(e)}")
            self.status_label.setText("Failed to save commands")
    
    def export_commands(self):
        """Export commands to a selected file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Commands", "commands_export.json", "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                commands = self.table_widget.get_commands()
                data = [command.to_dict() for command in commands]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                
                self.status_label.setText(f"Exported {len(commands)} commands to {file_path}")
                QMessageBox.information(self, "Export Successful", f"Commands exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export commands: {str(e)}")
                self.status_label.setText("Failed to export commands")


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Attack Simulator Command Manager")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Security Tools")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

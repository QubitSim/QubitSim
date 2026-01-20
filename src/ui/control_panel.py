"""
Control Panel Widget

Provides controls for circuit execution:
- Step button: Execute one step at a time
- Run All button: Execute all remaining steps
- Reset button: Reset to initial state
- Number of qubits selector
- Target step selector
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel, 
    QSpinBox, QFrame
)
from PyQt6.QtCore import pyqtSignal, Qt


class ControlPanel(QFrame):
    """
    Control panel for circuit execution.
    
    Signals:
        step_clicked: Emitted when step button is clicked
        run_all_clicked: Emitted when run all button is clicked
        run_to_step_clicked: Emitted with target step when run to step is clicked
        reset_clicked: Emitted when reset button is clicked
        num_qubits_changed: Emitted when number of qubits changes
    """
    
    step_clicked = pyqtSignal()
    run_all_clicked = pyqtSignal()
    run_to_step_clicked = pyqtSignal(int)
    reset_clicked = pyqtSignal()
    num_qubits_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the control panel UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Frame for better visual separation - no hard-coded background
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setMaximumHeight(60)  # Limit height
        
        # Number of qubits control
        qubits_label = QLabel("Qubits:")
        qubits_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(qubits_label)
        
        self.qubits_spinbox = QSpinBox()
        self.qubits_spinbox.setMinimum(1)
        self.qubits_spinbox.setMaximum(16)
        self.qubits_spinbox.setValue(3)
        self.qubits_spinbox.setToolTip("Number of qubits in the circuit")
        self.qubits_spinbox.valueChanged.connect(self._on_qubits_changed)
        layout.addWidget(self.qubits_spinbox)
        
        layout.addSpacing(20)
        
        # Target step control
        step_label = QLabel("Run to:")
        step_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(step_label)
        
        self.target_step_spinbox = QSpinBox()
        self.target_step_spinbox.setMinimum(0)
        self.target_step_spinbox.setMaximum(9)
        self.target_step_spinbox.setValue(0)
        self.target_step_spinbox.setToolTip("Target step to run to")
        layout.addWidget(self.target_step_spinbox)
        
        layout.addSpacing(20)
        
        # Execution controls
        self.step_button = QPushButton("Step")
        self.step_button.setToolTip("Execute one step of the circuit")
        self.step_button.clicked.connect(self.step_clicked.emit)
        self.step_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 6px 16px;
                border-radius: 4px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #5CBF60;
            }
            QPushButton:pressed {
                background-color: #3C9F40;
            }
        """)
        layout.addWidget(self.step_button)
        
        self.run_to_button = QPushButton("Run To")
        self.run_to_button.setToolTip("Execute up to target step")
        self.run_to_button.clicked.connect(self._on_run_to_clicked)
        self.run_to_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                padding: 6px 16px;
                border-radius: 4px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #31A6FF;
            }
            QPushButton:pressed {
                background-color: #1186E3;
            }
        """)
        layout.addWidget(self.run_to_button)
        
        self.run_all_button = QPushButton("Run All")
        self.run_all_button.setToolTip("Execute all remaining steps")
        self.run_all_button.clicked.connect(self.run_all_clicked.emit)
        self.run_all_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                padding: 6px 16px;
                border-radius: 4px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #31A6FF;
            }
            QPushButton:pressed {
                background-color: #1186E3;
            }
        """)
        layout.addWidget(self.run_all_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setToolTip("Reset circuit to initial state")
        self.reset_button.clicked.connect(self.reset_clicked.emit)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-weight: bold;
                padding: 6px 16px;
                border-radius: 4px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #FFA820;
            }
            QPushButton:pressed {
                background-color: #EF8800;
            }
        """)
        layout.addWidget(self.reset_button)
        
        layout.addStretch()
        
        # Status indicator (for future use)
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("font-style: italic;")
        layout.addWidget(self.status_label)
    
    def _on_qubits_changed(self, value: int):
        """Handle change in number of qubits."""
        self.num_qubits_changed.emit(value)
    
    def _on_run_to_clicked(self):
        """Handle run to step button click."""
        target_step = self.target_step_spinbox.value()
        self.run_to_step_clicked.emit(target_step)
    
    def set_status(self, status: str):
        """Update the status label."""
        self.status_label.setText(status)

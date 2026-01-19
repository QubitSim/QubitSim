"""
Gate Palette Widget

The gate palette displays available quantum gates that users can drag
onto the circuit canvas.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag


class GateButton(QPushButton):
    """
    A draggable button representing a quantum gate.
    """
    
    def __init__(self, gate_name: str, gate_display: str = None, parent=None):
        super().__init__(parent)
        self.gate_name = gate_name
        self.gate_display = gate_display or gate_name
        
        self.setText(self.gate_display)
        self.setFixedSize(60, 50)
        self.setStyleSheet("""
            QPushButton {
                background-color: #D0E0FF;
                border: 2px solid #5080C0;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E0F0FF;
                border: 2px solid #6090D0;
            }
            QPushButton:pressed {
                background-color: #B0D0FF;
            }
        """)
    
    def mouseMoveEvent(self, event):
        """Start drag operation."""
        if event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.gate_name)
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.CopyAction)


class GatePalette(QWidget):
    """
    Palette of draggable quantum gates.
    
    Displays all available gates organized by category:
    - Single-qubit gates (H, X, Y, Z, S, T)
    - Rotation gates (Rx, Ry, Rz)
    - Multi-qubit gates (CNOT, SWAP, etc.) - for future implementation
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumWidth(150)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the gate palette UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("Gate Palette")
        title.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            padding: 5px;
            background-color: #F0F0F0;
            border-radius: 3px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Scroll area for gates
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        
        # Standard single-qubit gates
        scroll_layout.addWidget(self._create_category_label("Single-Qubit Gates"))
        
        standard_gates = [
            ("H", "H"),
            ("X", "X"),
            ("Y", "Y"),
            ("Z", "Z"),
            ("S", "S"),
            ("T", "T"),
        ]
        
        for gate_name, display in standard_gates:
            btn = GateButton(gate_name, display)
            scroll_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Rotation gates (placeholder - will need angle input later)
        scroll_layout.addWidget(self._create_category_label("Rotation Gates"))
        scroll_layout.addWidget(QLabel("(Coming soon)"))
        
        # rotation_gates = [
        #     ("Rx", "Rx(θ)"),
        #     ("Ry", "Ry(θ)"),
        #     ("Rz", "Rz(θ)"),
        # ]
        
        # for gate_name, display in rotation_gates:
        #     btn = GateButton(gate_name, display)
        #     scroll_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Control gates (placeholder)
        scroll_layout.addWidget(self._create_category_label("Control"))
        scroll_layout.addWidget(QLabel("(Coming soon)"))
        
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Instructions
        instructions = QLabel("Drag gates onto\nthe circuit canvas")
        instructions.setStyleSheet("""
            font-size: 10px;
            color: #666;
            padding: 5px;
        """)
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
    
    def _create_category_label(self, text: str) -> QLabel:
        """Create a category separator label."""
        label = QLabel(text)
        label.setStyleSheet("""
            font-size: 11px;
            font-weight: bold;
            color: #555;
            padding: 3px;
            background-color: #E8E8E8;
            border-radius: 2px;
        """)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

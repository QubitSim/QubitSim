"""
Gate Palette Widget

The gate palette displays available quantum gates that users can drag
onto the circuit canvas. Organized in categories with tabs.
"""

import math
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QTabWidget, QSlider, QSpinBox
)
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QDrag, QPainter, QPen, QColor


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


class ControlButton(QPushButton):
    """
    A button representing control or anticontrol markers.
    These are shown with circle symbols (● for control, ○ for anticontrol).
    """
    
    def __init__(self, control_type: str, parent=None):
        super().__init__(parent)
        self.control_type = control_type  # "C" or "A"
        
        if control_type == "C":
            self.setText("●")  # Filled circle for control
            self.setToolTip("Control (filled circle)")
        else:
            self.setText("○")  # Open circle for anticontrol
            self.setToolTip("Anti-control (open circle)")
        
        self.setFixedSize(60, 50)
        self.setStyleSheet("""
            QPushButton {
                background-color: #FFD0D0;
                border: 2px solid #C05050;
                border-radius: 5px;
                font-weight: bold;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: #FFE0E0;
                border: 2px solid #D06060;
            }
            QPushButton:pressed {
                background-color: #FFB0B0;
            }
        """)
    
    def mouseMoveEvent(self, event):
        """Start drag operation."""
        if event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.control_type)
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.CopyAction)


class GatePalette(QWidget):
    """
    Palette of draggable quantum gates.
    
    Displays all available gates organized by category with tabs:
    - Single-qubit gates (H, X, Y, Z, S, T)
    - Rotation gates (Rx, Ry, Rz) with theta slider
    - Control gates (control and anticontrol markers)
    """
    
    theta_changed = pyqtSignal(float)  # Emitted when theta angle changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumWidth(200)
        self.current_theta = 0.0
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
            border-radius: 3px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Tab widget for categories
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QTabBar::tab {
                padding: 5px 10px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                font-weight: bold;
            }
        """)
        
        # Create tabs for each category
        self.tabs.addTab(self._create_single_qubit_tab(), "Single")
        self.tabs.addTab(self._create_rotation_tab(), "Rotation")
        self.tabs.addTab(self._create_control_tab(), "Control")
        
        layout.addWidget(self.tabs)
        
        # Instructions
        instructions = QLabel("Drag gates onto\nthe circuit canvas")
        instructions.setStyleSheet("""
            font-size: 10px;
            padding: 5px;
        """)
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
    
    def _create_single_qubit_tab(self) -> QWidget:
        """Create tab for single-qubit gates."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
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
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        return widget
    
    def _create_rotation_tab(self) -> QWidget:
        """Create tab for rotation gates with theta control."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Theta control section
        theta_label = QLabel("Angle (θ):")
        theta_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(theta_label)
        
        # Theta value display and input
        theta_layout = QHBoxLayout()
        self.theta_spinbox = QSpinBox()
        self.theta_spinbox.setMinimum(0)
        self.theta_spinbox.setMaximum(360)
        self.theta_spinbox.setValue(0)
        self.theta_spinbox.setSuffix("°")
        self.theta_spinbox.valueChanged.connect(self._on_theta_spinbox_changed)
        theta_layout.addWidget(self.theta_spinbox)
        layout.addLayout(theta_layout)
        
        # Theta slider
        self.theta_slider = QSlider(Qt.Orientation.Horizontal)
        self.theta_slider.setMinimum(0)
        self.theta_slider.setMaximum(360)
        self.theta_slider.setValue(0)
        self.theta_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.theta_slider.setTickInterval(45)
        self.theta_slider.valueChanged.connect(self._on_theta_slider_changed)
        layout.addWidget(self.theta_slider)
        
        layout.addSpacing(10)
        
        # Rotation gates
        rotation_gates = [
            ("Rx", "Rx(θ)"),
            ("Ry", "Ry(θ)"),
            ("Rz", "Rz(θ)"),
        ]
        
        for gate_name, display in rotation_gates:
            btn = GateButton(gate_name, display)
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        return widget
    
    def _create_control_tab(self) -> QWidget:
        """Create tab for control and anticontrol markers."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Info label
        info = QLabel("Control markers:\n● Control\n○ Anti-control")
        info.setWordWrap(True)
        info.setStyleSheet("font-size: 10px; padding: 5px;")
        layout.addWidget(info)
        
        # Control button
        control_btn = ControlButton("C")
        layout.addWidget(control_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Anticontrol button
        anticontrol_btn = ControlButton("A")
        layout.addWidget(anticontrol_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        return widget
    
    def _on_theta_slider_changed(self, value: int):
        """Handle theta slider change."""
        self.theta_spinbox.blockSignals(True)
        self.theta_spinbox.setValue(value)
        self.theta_spinbox.blockSignals(False)
        self.current_theta = value * math.pi / 180.0  # Convert to radians
        self.theta_changed.emit(self.current_theta)
    
    def _on_theta_spinbox_changed(self, value: int):
        """Handle theta spinbox change."""
        self.theta_slider.blockSignals(True)
        self.theta_slider.setValue(value)
        self.theta_slider.blockSignals(False)
        self.current_theta = value * math.pi / 180.0  # Convert to radians
        self.theta_changed.emit(self.current_theta)
    
    def get_theta(self) -> float:
        """Get current theta value in radians."""
        return self.current_theta

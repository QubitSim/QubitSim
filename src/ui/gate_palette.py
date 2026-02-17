"""
Gate Palette Widget

The gate palette displays available quantum gates that users can drag
onto the circuit canvas. Organized in categories with tabs.
"""

import math
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget, QSlider, QSpinBox
)
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QDrag, QPainter, QPen, QColor

from ui.app_state import AppState
from ui.themes import Theme, LIGHT_THEME, get_theme, get_gate_button_stylesheet, get_control_button_stylesheet, get_palette_stylesheet

class GateButton(QPushButton):
    """
    A draggable button representing a quantum gate.
    """
    
    def __init__(self, gate_name: str, app_state: AppState, gate_display: str = None, parent=None):
        super().__init__(parent)
        self.gate_name = gate_name
        self.app_state = app_state
        self.gate_display = gate_display or gate_name
        self.current_theme = LIGHT_THEME
        
        self.setText(self.gate_display)
        self.setFixedSize(60, 50)
        self._apply_stylesheet()
    
    def _apply_stylesheet(self):
        """Apply current theme stylesheet."""
        self.setStyleSheet(get_gate_button_stylesheet(self.current_theme))
    
    def set_theme(self, theme: Theme):
        """Update button theme."""
        self.current_theme = theme
        self._apply_stylesheet()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.gate_name)
            mime_data.setData(
                "application/x-gate",
                f"{self.gate_name}".encode()
            )

            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.CopyAction)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.app_state.set_selected_gate(self.gate_name)
        super().mousePressEvent(event)



class ControlButton(QPushButton):
    """
    A button representing control or anticontrol markers.
    These are shown with circle symbols (● for control, ○ for anticontrol).
    """
    
    def __init__(self, control_type: str, app_state: AppState, parent=None):
        super().__init__(parent)
        self.control_type = control_type  # "C" or "AC"
        self.app_state = app_state
        self.current_theme = LIGHT_THEME
        
        if control_type == "C":
            self.setText("●")  # Filled circle for control
            self.setToolTip("Control (filled circle)")
        else:
            self.setText("○")  # Open circle for anticontrol
            self.setToolTip("Anti-control (open circle)")
        
        self.setFixedSize(60, 50)
        self._apply_stylesheet()
    
    def _apply_stylesheet(self):
        """Apply current theme stylesheet."""
        self.setStyleSheet(get_control_button_stylesheet(self.current_theme))
    
    def set_theme(self, theme: Theme):
        """Update button theme."""
        self.current_theme = theme
        self._apply_stylesheet()
    
    def mouseMoveEvent(self, event):
        """Start drag operation."""
        if event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.control_type)
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.CopyAction)

    def mousePressEvent(self, e):
        """Select control type on click."""
        if e.button() == Qt.MouseButton.LeftButton:
            self.app_state.set_selected_gate(self.control_type)
        super().mousePressEvent(e)


class GatePalette(QWidget):
    """
    Palette of draggable quantum gates.
    
    Displays all available gates organized by category with tabs:
    - Single-qubit gates (H, X, Y, Z, S, T)
    - Rotation gates (Rx, Ry, Rz) with theta slider
    - Control gates (control and anticontrol markers)
    """
        
    def __init__(self, app_state: AppState, parent=None, ):
        super().__init__(parent)
        self.setMaximumWidth(200)
        self.current_theta = 0.0
        self.app_state = app_state
        self.current_theme = LIGHT_THEME
        
        # Keep track of all buttons for theme updates
        self.all_buttons = []
        self.title_label = None
        self.instructions_label = None
        
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the gate palette UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Title
        self.title_label = QLabel("Gate Palette")
        layout.addWidget(self.title_label)
        
        # Tab widget for categories
        self.tabs = QTabWidget()
        
        # Create tabs for each category
        self.tabs.addTab(self._create_single_qubit_tab(), "Single")
        self.tabs.addTab(self._create_rotation_tab(), "Rotation")
        self.tabs.addTab(self._create_control_tab(), "Control")
        
        layout.addWidget(self.tabs)
        
        # Instructions
        self.instructions_label = QLabel("Drag gates onto\nthe circuit canvas")
        self.instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_label.setWordWrap(True)
        layout.addWidget(self.instructions_label)
        
        # Apply initial theme
        self.set_theme(self.current_theme)
    
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
            ("M", "M"),
        ]
        
        for gate_name, display in standard_gates:
            btn = GateButton(gate_name, self.app_state, display)
            if gate_name == "M":
                btn.setToolTip("Measurement")
            self.all_buttons.append(btn)
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
            ("RX", "Rx(θ)"),
            ("RY", "Ry(θ)"),
            ("RZ", "Rz(θ)"),
        ]
        
        for gate_name, display in rotation_gates:
            btn = GateButton(gate_name, self.app_state, display)
            self.all_buttons.append(btn)
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
        layout.addWidget(info)
        
        # Control button
        self.control_btn = ControlButton("C", self.app_state)
        self.all_buttons.append(self.control_btn)
        layout.addWidget(self.control_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Anticontrol button
        self.anticontrol_btn = ControlButton("AC", self.app_state)
        self.all_buttons.append(self.anticontrol_btn)
        layout.addWidget(self.anticontrol_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        return widget
    
    def set_theme(self, theme: Theme):
        """Update widget theme."""
        self.current_theme = theme
        
        # Update all buttons
        for btn in self.all_buttons:
            btn.set_theme(theme)
        
        # Update labels
        if self.title_label:
            self.title_label.setStyleSheet(f"""
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
                border-radius: 3px;
                color: {theme.text_primary};
            """)
        
        if self.instructions_label:
            self.instructions_label.setStyleSheet(f"""
                font-size: 10px;
                padding: 5px;
                color: {theme.text_primary};
            """)
        
        # Update tab widget and spinbox/slider
        self.tabs.setStyleSheet(get_palette_stylesheet(theme))
        self.setStyleSheet(f"QWidget {{ background-color: {theme.panel_bg}; }}")
    
    def _on_theta_slider_changed(self, value: int):
        self.theta_spinbox.blockSignals(True)
        self.theta_spinbox.setValue(value)
        self.theta_spinbox.blockSignals(False)

        theta = value * math.pi / 180.0
        self.app_state.set_selected_theta(theta)


    def _on_theta_spinbox_changed(self, value: int):
        self.theta_slider.blockSignals(True)
        self.theta_slider.setValue(value)
        self.theta_slider.blockSignals(False)

        theta = value * math.pi / 180.0
        self.app_state.set_selected_theta(theta)

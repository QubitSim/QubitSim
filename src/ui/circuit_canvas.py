"""
Circuit Canvas Widget

The circuit canvas is where users construct quantum circuits by dragging and
dropping gates onto horizontal wires representing qubits.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtGui import (
    QPainter, QPen, QColor, QFont,
    QDragEnterEvent, QDropEvent
)

from qcircuit.objects import GateOp
from ui.app_state import AppState
from ui.themes import Theme, LIGHT_THEME


ROTATION_GATES = {"RX", "RY", "RZ"}
CONTROL_MARKERS = {"C", "AC"}  # Control and anticontrol markers


class CircuitCanvas(QWidget):
    """
    Interactive canvas for building quantum circuits.
    """

    circuit_changed = pyqtSignal()

    def __init__(self, app_state: AppState, parent=None):
        super().__init__(parent)

        self.app_state = app_state
        self.current_theme = LIGHT_THEME

        # Visual settings
        self.cell_width = 80
        self.cell_height = 60
        self.top_margin = 40
        self.left_margin = 60

        self.setAcceptDrops(True)
        self._update_minimum_size()
        self._apply_stylesheet()

        # Connect to state changes to update the step indicator
        self.app_state.state_changed.connect(self.update)
        self.app_state.circuit_changed.connect(self.update)

    def _apply_stylesheet(self):
        """Apply current theme stylesheet."""
        self.setStyleSheet(f"background-color: {self.current_theme.canvas_bg};")

    def set_theme(self, theme: Theme):
        """Update widget theme."""
        self.current_theme = theme
        self._apply_stylesheet()
        self.update()

    # ------------------------------------------------------------------
    # Qt paint pipeline
    # ------------------------------------------------------------------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self._draw_grid(painter)
        self._draw_wires(painter)
        self._draw_qubit_labels(painter)
        self._draw_step_labels(painter)
        self._draw_control_links(painter)  # Draw control links before gates
        self._draw_gates(painter)
        self._draw_current_step_indicator(painter)

    def _draw_grid(self, painter):
        pen = QPen(QColor(self.current_theme.grid_color), 1, Qt.PenStyle.DashLine)
        painter.setPen(pen)

        for step in range(self.app_state.num_steps + 1):
            x = self.left_margin + step * self.cell_width
            y1 = self.top_margin
            y2 = self.top_margin + self.app_state.num_qubits * self.cell_height
            painter.drawLine(x, y1, x, y2)

    def _draw_wires(self, painter):
        painter.setPen(QPen(QColor(self.current_theme.wire_color), 3))

        for q in range(self.app_state.num_qubits):
            y = self.top_margin + q * self.cell_height + self.cell_height // 2
            painter.drawLine(
                self.left_margin,
                y,
                self.left_margin + self.app_state.num_steps * self.cell_width,
                y
            )

    def _draw_qubit_labels(self, painter):
        painter.setFont(QFont("Arial", 10))
        painter.setPen(QColor(self.current_theme.qubit_label_color))

        for q in range(self.app_state.num_qubits):
            y = self.top_margin + q * self.cell_height + self.cell_height // 2
            rect = QRect(10, y - 15, self.left_margin - 20, 30)
            painter.drawText(
                rect,
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                f"q{q}"
            )

    def _draw_step_labels(self, painter):
        painter.setFont(QFont("Arial", 9))
        painter.setPen(QColor(self.current_theme.step_label_color))

        for step in range(self.app_state.num_steps):
            x = self.left_margin + step * self.cell_width + self.cell_width // 2
            rect = QRect(x - 20, 5, 40, self.top_margin - 10)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"t{step}")

    def _draw_control_links(self, painter):
        """Draw lines connecting control markers to their controlled gates."""
        painter.setPen(QPen(QColor(self.current_theme.control_link_color), 2))
        
        for step in range(self.app_state.num_steps):
            for qubit in range(self.app_state.num_qubits):
                gate = self.app_state.steps[step][qubit]
                if gate is None:
                    continue
                
                # If this gate has controls, draw a line from control to this gate
                if gate.controls or gate.anti_controls:
                    control_qubits = gate.controls or gate.anti_controls
                    for ctrl_qubit in control_qubits:
                        # Calculate positions
                        x = self.left_margin + step * self.cell_width + self.cell_width // 2
                        
                        ctrl_y = self.top_margin + ctrl_qubit * self.cell_height + self.cell_height // 2
                        gate_y = self.top_margin + qubit * self.cell_height + self.cell_height // 2
                        
                        # Draw vertical line connecting them
                        painter.drawLine(x, ctrl_y, x, gate_y)

    def _draw_gates(self, painter):
        painter.setFont(QFont("Arial", 11, QFont.Weight.Bold))

        for step in range(self.app_state.num_steps):
            for qubit in range(self.app_state.num_qubits):
                gate = self.app_state.steps[step][qubit]
                if gate is None:
                    continue

                x = self.left_margin + step * self.cell_width
                y = self.top_margin + qubit * self.cell_height

                # Special handling for control markers
                if gate.name == "C":
                    # Draw filled circle for control marker
                    painter.setPen(QPen(QColor(self.current_theme.control_button_border), 2))
                    painter.setBrush(QColor(self.current_theme.control_button_border))
                    cx = x + self.cell_width // 2
                    cy = y + self.cell_height // 2
                    painter.drawEllipse(cx - 6, cy - 6, 12, 12)
                    continue
                elif gate.name == "AC":
                    # Draw open circle for anticontrol marker
                    painter.setPen(QPen(QColor(self.current_theme.control_button_border), 2))
                    painter.setBrush(Qt.BrushStyle.NoBrush)
                    cx = x + self.cell_width // 2
                    cy = y + self.cell_height // 2
                    painter.drawEllipse(cx - 6, cy - 6, 12, 12)
                    continue

                # Regular gate drawing
                painter.setPen(QPen(QColor(self.current_theme.gate_button_border), 2))
                painter.setBrush(QColor(self.current_theme.gate_button_bg))

                padding = 8
                rect = QRect(
                    x + padding,
                    y + padding,
                    self.cell_width - 2 * padding,
                    self.cell_height - 2 * padding
                )
                painter.drawRoundedRect(rect, 5, 5)

                painter.setPen(QColor(self.current_theme.text_primary))
                if gate.params and "theta" in gate.params:
                    label = f"{gate.name}\nθ={gate.params['theta']:.2f}"
                else:
                    label = gate.name

                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, label)

    def _draw_current_step_indicator(self, painter):
        if self.app_state.current_step >= self.app_state.num_steps:
            return

        painter.setPen(QPen(QColor(self.current_theme.step_indicator_color), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)

        x = self.left_margin + self.app_state.current_step * self.cell_width
        y = self.top_margin
        w = self.cell_width
        h = self.app_state.num_qubits * self.cell_height

        painter.drawRect(x, y, w, h)

    # ------------------------------------------------------------------
    # Drag & Drop
    # ------------------------------------------------------------------

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        gate_name = self.app_state.selected_gate
        theta = self.app_state.selected_theta

        if gate_name is None:
            return

        pos = event.position().toPoint()
        step = (pos.x() - self.left_margin) // self.cell_width
        qubit = (pos.y() - self.top_margin) // self.cell_height

        if not (0 <= step < self.app_state.num_steps and
                0 <= qubit < self.app_state.num_qubits):
            return

        # Check if this is a control/anticontrol marker
        if gate_name in CONTROL_MARKERS:
            # Just place the marker as-is
            op = GateOp(
                name=gate_name,
                targets=[qubit]
            )
            self.app_state.add_gate(step, op)
        else:
            # Check if there's a control marker at the same step on another qubit
            control_qubit = None
            control_type = None
            
            for q in range(self.app_state.num_qubits):
                if q != qubit:  # Look for control marker on different qubit
                    marker = self.app_state.steps[step][q]
                    if marker and marker.name in CONTROL_MARKERS:
                        control_qubit = q
                        control_type = marker.name
                        break
            
            params = {"theta": theta} if gate_name in ROTATION_GATES else None
            
            if control_type == "C":
                # Regular control
                op = GateOp(
                    name=gate_name,
                    targets=[qubit],
                    controls=[control_qubit],
                    params=params
                )
            elif control_type == "AC":
                # Anticontrol
                op = GateOp(
                    name=gate_name,
                    targets=[qubit],
                    anti_controls=[control_qubit],
                    params=params
                )
            else:
                # No control marker, just a regular gate
                op = GateOp(
                    name=gate_name,
                    targets=[qubit],
                    params=params
                )
            
            self.app_state.add_gate(step, op)

        self.update()
        self.circuit_changed.emit()

        event.acceptProposedAction()

    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.RightButton:
            return

        pos = event.pos()
        step = (pos.x() - self.left_margin) // self.cell_width
        qubit = (pos.y() - self.top_margin) // self.cell_height

        if 0 <= step < self.app_state.num_steps and 0 <= qubit < self.app_state.num_qubits:
            if self.app_state.steps[step][qubit]:
                self.app_state.remove_gate(step, qubit)
                self.update()
                self.circuit_changed.emit()

    # ------------------------------------------------------------------
    # State control
    # ------------------------------------------------------------------

    def _update_minimum_size(self):
        self.setMinimumSize(
            self.left_margin + self.app_state.num_steps * self.cell_width + 40,
            self.top_margin + self.app_state.num_qubits * self.cell_height + 40
        )

    def set_num_qubits(self, num_qubits: int):
        self.app_state.num_qubits = num_qubits
        self.app_state.steps = [
            [None for _ in range(num_qubits)]
            for _ in range(self.app_state.num_steps)
        ]
        self.app_state.current_step = 0
        self._update_minimum_size()
        self.update()
        self.circuit_changed.emit()

    def set_num_steps(self, num_steps: int):
        self.app_state.num_steps = num_steps
        self.app_state.steps = [
            [None for _ in range(self.app_state.num_qubits)]
            for _ in range(num_steps)
        ]
        self.app_state.current_step = 0
        self._update_minimum_size()
        self.update()
        self.circuit_changed.emit()

    def reset(self):
        self.app_state.current_step = 0
        self.update()

    def clear(self):
        self.app_state.steps = [
            [None for _ in range(self.app_state.num_qubits)]
            for _ in range(self.app_state.num_steps)
        ]
        self.reset()
        self.circuit_changed.emit()

"""
Circuit Canvas Widget

The circuit canvas is where users construct quantum circuits by dragging and
dropping gates onto horizontal wires representing qubits.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QDragEnterEvent, QDropEvent

from core.system import System


class CircuitCanvas(QWidget):
    """
    Interactive canvas for building quantum circuits.
    
    Features:
    - Horizontal wires representing qubits
    - Grid-based layout for gate placement
    - Drag-and-drop support for gates
    - Visual highlighting of current execution step
    """
    
    circuit_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.num_qubits = 3
        self.num_steps = 10
        self.current_step = 0
        
        # Circuit representation: grid[step][qubit] = gate_name or None
        self.circuit = [[None for _ in range(self.num_qubits)] 
                       for _ in range(self.num_steps)]
        
        # Quantum system
        self.system = System(self.num_qubits)
        
        # Visual settings
        self.cell_width = 80
        self.cell_height = 60
        self.wire_margin = 40
        self.top_margin = 40
        self.left_margin = 60
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        self.setMinimumSize(
            self.left_margin + self.num_steps * self.cell_width + 40,
            self.top_margin + self.num_qubits * self.cell_height + 40
        )
        
        # Style
        self.setStyleSheet("background-color: white;")
        
    def paintEvent(self, event):
        """Draw the circuit canvas."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        self._draw_grid(painter)
        self._draw_wires(painter)
        self._draw_qubit_labels(painter)
        self._draw_step_labels(painter)
        self._draw_gates(painter)
        self._draw_current_step_indicator(painter)
        
    def _draw_grid(self, painter):
        """Draw the grid lines (vertical only for time steps)."""
        pen = QPen(QColor(220, 220, 220))
        pen.setWidth(1)
        pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(pen)
        
        # Vertical grid lines (time steps)
        for step in range(self.num_steps + 1):
            x = self.left_margin + step * self.cell_width
            y1 = self.top_margin
            y2 = self.top_margin + self.num_qubits * self.cell_height
            painter.drawLine(x, y1, x, y2)
    
    def _draw_wires(self, painter):
        """Draw qubit wires - thick solid lines to clearly represent qubits."""
        pen = QPen(QColor(60, 60, 60))
        pen.setWidth(3)
        painter.setPen(pen)
        
        for qubit in range(self.num_qubits):
            y = self.top_margin + qubit * self.cell_height + self.cell_height // 2
            x1 = self.left_margin
            x2 = self.left_margin + self.num_steps * self.cell_width
            painter.drawLine(x1, y, x2, y)
    
    def _draw_qubit_labels(self, painter):
        """Draw qubit labels on the left."""
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))
        
        for qubit in range(self.num_qubits):
            y = self.top_margin + qubit * self.cell_height + self.cell_height // 2
            rect = QRect(10, y - 15, self.left_margin - 20, 30)
            painter.drawText(rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                           f"q{qubit}")
    
    def _draw_step_labels(self, painter):
        """Draw step labels on top."""
        font = QFont("Arial", 9)
        painter.setFont(font)
        painter.setPen(QColor(100, 100, 100))
        
        for step in range(self.num_steps):
            x = self.left_margin + step * self.cell_width + self.cell_width // 2
            rect = QRect(x - 20, 5, 40, self.top_margin - 10)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"t{step}")
    
    def _draw_gates(self, painter):
        """Draw gates on the circuit."""
        font = QFont("Arial", 11, QFont.Weight.Bold)
        painter.setFont(font)
        
        for step in range(self.num_steps):
            for qubit in range(self.num_qubits):
                gate = self.circuit[step][qubit]
                if gate:
                    x = self.left_margin + step * self.cell_width
                    y = self.top_margin + qubit * self.cell_height
                    
                    # Draw gate box
                    painter.setPen(QPen(QColor(50, 50, 200), 2))
                    painter.setBrush(QColor(200, 220, 255))
                    
                    padding = 8
                    rect = QRect(x + padding, y + padding,
                               self.cell_width - 2*padding,
                               self.cell_height - 2*padding)
                    painter.drawRoundedRect(rect, 5, 5)
                    
                    # Draw gate name
                    painter.setPen(QColor(0, 0, 100))
                    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, gate)
    
    def _draw_current_step_indicator(self, painter):
        """Highlight the current execution step."""
        if self.current_step >= self.num_steps:
            return
            
        pen = QPen(QColor(255, 100, 100))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        x = self.left_margin + self.current_step * self.cell_width
        y = self.top_margin
        width = self.cell_width
        height = self.num_qubits * self.cell_height
        
        painter.drawRect(x, y, width, height)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter events."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop events."""
        gate_name = event.mimeData().text()
        pos = event.position().toPoint()
        
        # Calculate grid position
        step = (pos.x() - self.left_margin) // self.cell_width
        qubit = (pos.y() - self.top_margin) // self.cell_height
        
        # Validate position
        if 0 <= step < self.num_steps and 0 <= qubit < self.num_qubits:
            self.circuit[step][qubit] = gate_name
            self.update()
            self.circuit_changed.emit()
        
        event.acceptProposedAction()
    
    def mousePressEvent(self, event):
        """Handle mouse press to remove gates."""
        if event.button() == Qt.MouseButton.RightButton:
            pos = event.pos()
            step = (pos.x() - self.left_margin) // self.cell_width
            qubit = (pos.y() - self.top_margin) // self.cell_height
            
            if 0 <= step < self.num_steps and 0 <= qubit < self.num_qubits:
                if self.circuit[step][qubit]:
                    self.circuit[step][qubit] = None
                    self.update()
                    self.circuit_changed.emit()
    
    def set_num_qubits(self, num_qubits: int):
        """Change the number of qubits."""
        self.num_qubits = num_qubits
        self.circuit = [[None for _ in range(self.num_qubits)] 
                       for _ in range(self.num_steps)]
        self.system = System(num_qubits)
        self.current_step = 0
        
        self.setMinimumSize(
            self.left_margin + self.num_steps * self.cell_width + 40,
            self.top_margin + self.num_qubits * self.cell_height + 40
        )
        self.update()
        self.circuit_changed.emit()
    
    def execute_step(self):
        """Execute the next step in the circuit."""
        if self.current_step < self.num_steps:
            # TODO: Apply gates at current_step to system
            # This will be implemented later when integrating with circuit.interpreter
            self.current_step += 1
            self.update()
    
    def execute_all(self):
        """Execute all remaining steps."""
        while self.current_step < self.num_steps:
            self.execute_step()
    
    def execute_to_step(self, target_step: int):
        """Execute up to a specific step."""
        target_step = max(0, min(target_step, self.num_steps - 1))
        while self.current_step <= target_step:
            self.execute_step()
    
    def reset(self):
        """Reset the circuit to initial state."""
        self.system = System(self.num_qubits)
        self.current_step = 0
        self.update()
    
    def clear(self):
        """Clear all gates from the circuit."""
        self.circuit = [[None for _ in range(self.num_qubits)] 
                       for _ in range(self.num_steps)]
        self.reset()
        self.circuit_changed.emit()
    
    def get_current_state(self) -> System:
        """Get the current quantum state."""
        return self.system

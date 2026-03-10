"""
Circuit Canvas Widget

The circuit canvas is where users construct quantum circuits by dragging and
dropping gates onto horizontal wires representing qubits.
"""

from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QSize
from PyQt6.QtGui import (
    QPainter, QPen, QColor, QFont,
    QDragEnterEvent, QDropEvent
)

from qcircuit.objects import GateOp
from ui.app_state import AppState
from ui.themes import Theme, LIGHT_THEME


ROTATION_GATES = {"RX", "RY", "RZ"}
U3_GATES = {"U3"}
CONTROL_MARKERS = {"C", "AC"}  # Control and anticontrol markers
MEASUREMENT_GATES = {"M"}

# Gates drawn as × nodes on each target connected by a vertical line
SWAP_GATES = {"SWAP", "iSWAP"}

# Gates that use built-in controls (stored in op.controls) and draw ● / ⊕
BUILT_IN_CONTROLLED_GATES = {"Toffoli", "Fredkin", "X3"}

# Gates drawn as a single labeled box spanning all their target qubits
SPANNING_GATES = {
    "H_LAYER", "GROVER_DIFFUSION", "QFT", "QFT_DAG",
    "ORACLE_MARK_STATE", "ORACLE_PARITY", "ORACLE_PHASE",
}

# Barrier gate (drawn as a vertical dashed line across target rows)
BARRIER_GATES = {"BARRIER"}

# Multi-qubit auto-placement config: consecutive qubit assignment from drop point.
# Layout: first `controls` qubits are control qubits, next `targets` are target qubits.
MULTI_QUBIT_GATE_CONFIGS: dict[str, dict] = {
    "SWAP":    {"controls": 0, "targets": 2},   # q0, q1 → targets
    "iSWAP":   {"controls": 0, "targets": 2},   # q0, q1 → targets
    "Toffoli": {"controls": 2, "targets": 1},   # q0, q1 → controls; q2 → target
    "Fredkin": {"controls": 1, "targets": 2},   # q0 → control; q1, q2 → targets
    "X3":      {"controls": 3, "targets": 1},   # q0..q2 → controls; q3 → target
}

# Gate symbol mapping for standard circuit notation
GATE_SYMBOL_MAP = {
    "Sdg": "S†",
    "Tdg": "T†",
    "QFT_DAG": "QFT†",
    # Multi-qubit gates 
    "iSWAP": "iSWAP",
    "Toffoli": "Toffoli",
    "Fredkin": "Fredkin",
    "X3": "3CX",
    # Algorithm components
    "H_LAYER": "H⊗ⁿ",
    "GROVER_DIFFUSION": "D",
    "QFT": "QFT",
    # Oracle components
    "ORACLE_MARK_STATE": "O",
    "ORACLE_PARITY": "O_p",
    "ORACLE_PHASE": "P",
}

def get_gate_display_name(gate: "GateOp") -> str:
    """
    Convert gate name to standard circuit notation.
    
    Maps internal gate names to their standard quantum circuit symbols:
    - Sdg -> S†
    - Tdg -> T†
    - RX -> Rx(θ) with actual angle value
    - Rotation gates display as Rx(θ), Ry(θ), Rz(θ) with actual values
    - U3 gates display as U(θ,φ,λ)
    - Algorithm components use standard symbols (H⊗ⁿ, D for Grover, QFT, etc.)
    
    Args:
        gate: GateOp object with name and optional params
    
    Returns:
        Display string following standard circuit notation
    """
    gate_name = gate.name
    
    # Check if it's a standard mapped gate
    if gate_name in GATE_SYMBOL_MAP:
        return GATE_SYMBOL_MAP[gate_name]
    
    # Handle rotation gates with parameters
    if gate_name in ROTATION_GATES:
        # RX -> Rx, RY -> Ry, RZ -> Rz
        axis = gate_name[1].lower()  # Get the axis letter (X, Y, or Z) and lowercase it
        if gate.params and "theta" in gate.params:
            theta = gate.params["theta"]
            # Display in radians with appropriate precision
            return f"R{axis}({theta:.2f})"
        else:
            return f"R{axis}(θ)"
    
    # Handle U3 gate with parameters
    if gate_name == "U3" and gate.params:
        theta = gate.params.get("theta", 0.0)
        phi = gate.params.get("phi", 0.0)
        lam = gate.params.get("lam", 0.0)
        return f"U({theta:.2f},{phi:.2f},{lam:.2f})"
    
    return gate_name


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
        # Expand to fill available space but also grow beyond it (scroll area takes care of overflow)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._apply_stylesheet()

        # Connect to state changes to update the step indicator
        self.app_state.state_changed.connect(self.update)
        self.app_state.circuit_changed.connect(self.update)

    def _apply_stylesheet(self):
        """Apply current theme stylesheet directly to this widget."""
        # Set the background via the palette so it is not affected by
        # ancestor QScrollArea / viewport stylesheet inheritance.
        from PyQt6.QtGui import QPalette
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(self.current_theme.canvas_bg))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def set_theme(self, theme: Theme):
        """Update widget theme."""
        self.current_theme = theme
        self._apply_stylesheet()
        self.update()

    # ------------------------------------------------------------------
    # Size hints – drive the QScrollArea
    # ------------------------------------------------------------------

    def _canvas_width(self) -> int:
        return self.left_margin + self.app_state.num_steps * self.cell_width + 40

    def _canvas_height(self) -> int:
        return self.top_margin + self.app_state.num_qubits * self.cell_height + 40

    def sizeHint(self) -> QSize:
        return QSize(self._canvas_width(), self._canvas_height())

    def minimumSizeHint(self) -> QSize:
        return QSize(self._canvas_width(), self._canvas_height())

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
        """Draw vertical lines connecting C/AC userspace markers to their target gate.

        Built-in multi-qubit gates (Toffoli, Fredkin, X3, SWAP, iSWAP, spanning
        gates, barriers) are drawn entirely inside _draw_gates, so they are
        intentionally skipped here.
        """
        SKIP = (BUILT_IN_CONTROLLED_GATES | SWAP_GATES |
                SPANNING_GATES | BARRIER_GATES | CONTROL_MARKERS)

        painter.setPen(QPen(QColor(self.current_theme.control_link_color), 2))

        for step in range(self.app_state.num_steps):
            for qubit in range(self.app_state.num_qubits):
                gate = self.app_state.steps[step][qubit]
                if gate is None or gate.name in SKIP:
                    continue

                if gate.controls or gate.anti_controls:
                    control_qubits = gate.controls or gate.anti_controls
                    for ctrl_qubit in control_qubits:
                        x = self.left_margin + step * self.cell_width + self.cell_width // 2
                        ctrl_y = self.top_margin + ctrl_qubit * self.cell_height + self.cell_height // 2
                        gate_y = self.top_margin + qubit * self.cell_height + self.cell_height // 2
                        painter.drawLine(x, ctrl_y, x, gate_y)

    # ------------------------------------------------------------------
    # Gate drawing helpers
    # ------------------------------------------------------------------

    def _cx(self, step: int) -> int:
        """Horizontal center pixel for a circuit step column."""
        return self.left_margin + step * self.cell_width + self.cell_width // 2

    def _cy(self, qubit: int) -> int:
        """Vertical center pixel for a qubit row."""
        return self.top_margin + qubit * self.cell_height + self.cell_height // 2

    def _draw_control_dot(self, painter, cx: int, cy: int):
        """Filled circle – standard control marker (●)."""
        painter.setPen(QPen(QColor(self.current_theme.control_button_border), 2))
        painter.setBrush(QColor(self.current_theme.control_button_border))
        painter.drawEllipse(cx - 6, cy - 6, 12, 12)

    def _draw_anticontrol_dot(self, painter, cx: int, cy: int):
        """Open circle – anti-control marker (○)."""
        painter.setPen(QPen(QColor(self.current_theme.control_button_border), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(cx - 6, cy - 6, 12, 12)

    def _draw_xor_target(self, painter, cx: int, cy: int):
        """⊕ symbol – X/CNOT/Toffoli target."""
        r = 10
        painter.setPen(QPen(QColor(self.current_theme.pauli_x_button_border), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(cx - r, cy - r, 2 * r, 2 * r)
        painter.drawLine(cx - r, cy, cx + r, cy)
        painter.drawLine(cx, cy - r, cx, cy + r)

    def _draw_swap_node(self, painter, cx: int, cy: int):
        """× symbol – SWAP node."""
        r = 8
        painter.setPen(QPen(QColor(self.current_theme.control_link_color), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(cx - r, cy - r, cx + r, cy + r)
        painter.drawLine(cx - r, cy + r, cx + r, cy - r)

    def _draw_vert_link(self, painter, step: int, q_min: int, q_max: int):
        """Vertical connecting line through all qubit rows for a gate."""
        cx = self._cx(step)
        painter.setPen(QPen(QColor(self.current_theme.control_link_color), 2))
        painter.drawLine(cx, self._cy(q_min), cx, self._cy(q_max))

    def _draw_gate_box(self, painter, step: int, qubit: int, label: str,
                       row_span: int = 1):
        """Standard rounded-rect gate box, optionally spanning multiple rows."""
        padding = 8
        x = self.left_margin + step * self.cell_width
        y = self.top_margin + qubit * self.cell_height
        rect = QRect(
            x + padding,
            y + padding,
            self.cell_width - 2 * padding,
            row_span * self.cell_height - 2 * padding,
        )
        painter.setPen(QPen(QColor(self.current_theme.gate_button_border), 2))
        painter.setBrush(QColor(self.current_theme.gate_button_bg))
        painter.drawRoundedRect(rect, 5, 5)
        painter.setPen(QColor(self.current_theme.text_primary))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, label)

    # ------------------------------------------------------------------
    # _draw_gates
    # ------------------------------------------------------------------

    def _draw_gates(self, painter):
        painter.setFont(QFont("Arial", 11, QFont.Weight.Bold))

        # Track which GateOp objects have already been fully rendered so that
        # multi-qubit gates (whose reference is stored in several rows) are not
        # drawn more than once.
        drawn_ids: set[int] = set()

        for step in range(self.app_state.num_steps):
            for qubit in range(self.app_state.num_qubits):
                gate = self.app_state.steps[step][qubit]
                if gate is None:
                    continue

                gid = id(gate)
                if gid in drawn_ids:
                    continue
                drawn_ids.add(gid)

                cx = self._cx(step)
                cy = self._cy(qubit)

                name = gate.name

                # ----------------------------------------------------------
                # Control / anti-control userspace markers
                # ----------------------------------------------------------
                if name == "C":
                    self._draw_control_dot(painter, cx, cy)
                    continue

                if name == "AC":
                    self._draw_anticontrol_dot(painter, cx, cy)
                    continue

                # ----------------------------------------------------------
                # Measurement gate
                # ----------------------------------------------------------
                if name in MEASUREMENT_GATES:
                    self._draw_gate_box(painter, step, qubit, "M")
                    continue

                # ----------------------------------------------------------
                # X gate – always drawn as ⊕ (standard convention; also
                # serves as CNOT / Toffoli target when linked to controls)
                # ----------------------------------------------------------
                if name == "X":
                    self._draw_xor_target(painter, cx, cy)
                    continue

                # ----------------------------------------------------------
                # SWAP / iSWAP  – × nodes on each target, connected by line
                # ----------------------------------------------------------
                if name in SWAP_GATES:
                    t0, t1 = gate.targets[0], gate.targets[1]
                    self._draw_vert_link(painter, step, min(t0, t1), max(t0, t1))
                    self._draw_swap_node(painter, cx, self._cy(t0))
                    self._draw_swap_node(painter, cx, self._cy(t1))
                    if name == "iSWAP":
                        # Small "i" label between the nodes
                        mid_y = (self._cy(t0) + self._cy(t1)) // 2
                        painter.setPen(QColor(self.current_theme.text_primary))
                        painter.drawText(cx + 4, mid_y + 5, "i")
                    continue

                # ----------------------------------------------------------
                # Toffoli (CCNOT)  – ● ● ⊕
                # ----------------------------------------------------------
                if name == "Toffoli":
                    controls = gate.controls or []
                    target = gate.targets[0]
                    all_qs = sorted(controls + [target])
                    self._draw_vert_link(painter, step, all_qs[0], all_qs[-1])
                    for c in controls:
                        self._draw_control_dot(painter, cx, self._cy(c))
                    self._draw_xor_target(painter, cx, self._cy(target))
                    continue

                # ----------------------------------------------------------
                # X3 (CCCX)  – ● ● ● ⊕
                # ----------------------------------------------------------
                if name == "X3":
                    controls = gate.controls or []
                    target = gate.targets[0]
                    all_qs = sorted(controls + [target])
                    self._draw_vert_link(painter, step, all_qs[0], all_qs[-1])
                    for c in controls:
                        self._draw_control_dot(painter, cx, self._cy(c))
                    self._draw_xor_target(painter, cx, self._cy(target))
                    continue

                # ----------------------------------------------------------
                # Fredkin (CSWAP)  – ● × ×
                # ----------------------------------------------------------
                if name == "Fredkin":
                    ctrl = (gate.controls or [])[0]
                    t0, t1 = gate.targets[0], gate.targets[1]
                    all_qs = sorted([ctrl, t0, t1])
                    self._draw_vert_link(painter, step, all_qs[0], all_qs[-1])
                    self._draw_control_dot(painter, cx, self._cy(ctrl))
                    self._draw_swap_node(painter, cx, self._cy(t0))
                    self._draw_swap_node(painter, cx, self._cy(t1))
                    continue

                # ----------------------------------------------------------
                # Spanning algorithm / oracle gates – single labeled box
                # ----------------------------------------------------------
                if name in SPANNING_GATES:
                    targets = gate.targets
                    if not targets:
                        targets = list(range(self.app_state.num_qubits))
                    q_min, q_max = min(targets), max(targets)
                    label = get_gate_display_name(gate)
                    self._draw_gate_box(painter, step, q_min, label,
                                        row_span=(q_max - q_min + 1))
                    continue

                # ----------------------------------------------------------
                # Barrier – dashed vertical line across target rows
                # ----------------------------------------------------------
                if name in BARRIER_GATES:
                    targets = gate.targets
                    if not targets:
                        targets = list(range(self.app_state.num_qubits))
                    q_min, q_max = min(targets), max(targets)
                    y_top = self.top_margin + q_min * self.cell_height + 4
                    y_bot = self.top_margin + (q_max + 1) * self.cell_height - 4
                    painter.setPen(QPen(QColor(self.current_theme.control_link_color), 2,
                                        Qt.PenStyle.DashLine))
                    painter.drawLine(cx, y_top, cx, y_bot)
                    continue

                # ----------------------------------------------------------
                # Single-qubit gates (regular box)
                # ----------------------------------------------------------
                label = get_gate_display_name(gate)
                self._draw_gate_box(painter, step, qubit, label)

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

        num_q = self.app_state.num_qubits

        # ----------------------------------------------------------------
        # Control / anti-control userspace marker
        # ----------------------------------------------------------------
        if gate_name in CONTROL_MARKERS:
            op = GateOp(name=gate_name, targets=[qubit])
            self.app_state.add_gate(step, op)

        # ----------------------------------------------------------------
        # Measurement gate
        # ----------------------------------------------------------------
        elif gate_name in MEASUREMENT_GATES:
            op = GateOp(name=gate_name, targets=[qubit])
            self.app_state.add_gate(step, op)

        # ----------------------------------------------------------------
        # Multi-qubit gates with consecutive auto-assignment
        # Layout: first cfg["controls"] qubits are controls, then targets.
        # Dropped qubit becomes the FIRST qubit in the sequence.
        # ----------------------------------------------------------------
        elif gate_name in MULTI_QUBIT_GATE_CONFIGS:
            cfg = MULTI_QUBIT_GATE_CONFIGS[gate_name]
            nc, nt = cfg["controls"], cfg["targets"]
            total = nc + nt

            if qubit + total > num_q:
                # Not enough room below – shift up so the gate fits
                qubit = max(0, num_q - total)

            controls = list(range(qubit, qubit + nc)) if nc else None
            targets = list(range(qubit + nc, qubit + nc + nt))

            op = GateOp(name=gate_name, targets=targets, controls=controls)
            self.app_state.add_gate(step, op)

        # ----------------------------------------------------------------
        # Spanning algorithm / oracle gates – always occupy all qubits
        # ----------------------------------------------------------------
        elif gate_name in SPANNING_GATES:
            targets = list(range(num_q))
            op = GateOp(name=gate_name, targets=targets)
            self.app_state.add_gate(step, op)

        # ----------------------------------------------------------------
        # Barrier – spans all qubits
        # ----------------------------------------------------------------
        elif gate_name in BARRIER_GATES:
            targets = list(range(num_q))
            op = GateOp(name=gate_name, targets=targets)
            self.app_state.add_gate(step, op)

        # ----------------------------------------------------------------
        # Standard single-qubit gate (optionally with C/AC control marker)
        # ----------------------------------------------------------------
        else:
            # Check if there is a userspace control marker in the same step
            control_qubit = None
            control_type = None
            for q in range(num_q):
                if q != qubit:
                    marker = self.app_state.steps[step][q]
                    if marker and marker.name in CONTROL_MARKERS:
                        control_qubit = q
                        control_type = marker.name
                        break

            if gate_name in ROTATION_GATES:
                params = {"theta": theta}
            elif gate_name in U3_GATES:
                params = {"theta": theta, "phi": 0.0, "lam": 0.0}
            else:
                params = None

            if control_type == "C":
                op = GateOp(name=gate_name, targets=[qubit],
                            controls=[control_qubit], params=params)
            elif control_type == "AC":
                op = GateOp(name=gate_name, targets=[qubit],
                            anti_controls=[control_qubit], params=params)
            else:
                op = GateOp(name=gate_name, targets=[qubit], params=params)

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
        """Notify the scroll area that our preferred size has changed."""
        self.updateGeometry()

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

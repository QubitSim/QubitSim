"""
State Display Widget

Displays the current quantum state in various representations:
- State vector (amplitudes)
- Measurement probabilities
- State details
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QTabWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.app_state import AppState


EPS = 1e-10


class StateDisplay(QWidget):
    """
    Display quantum state information.

    This widget is read-only and reacts to AppState updates.
    """

    def __init__(self, app_state: AppState, parent=None):
        super().__init__(parent)

        self.app_state = app_state
        self.setMinimumWidth(300)

        self._init_ui()

        # React to global state changes
        self.app_state.state_changed.connect(self.refresh)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        title = QLabel("Quantum State")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            padding: 5px;
            background-color: #F0F0F0;
            border-radius: 3px;
        """)
        layout.addWidget(title)

        self.tabs = QTabWidget()

        self.amplitudes_text = QTextEdit(readOnly=True)
        self.amplitudes_text.setFont(QFont("Courier", 10))
        self.tabs.addTab(self.amplitudes_text, "Amplitudes")

        self.probabilities_text = QTextEdit(readOnly=True)
        self.probabilities_text.setFont(QFont("Courier", 10))
        self.tabs.addTab(self.probabilities_text, "Probabilities")

        self.details_text = QTextEdit(readOnly=True)
        self.details_text.setFont(QFont("Courier", 9))
        self.tabs.addTab(self.details_text, "Details")

        layout.addWidget(self.tabs)

        self.clear()

    def refresh(self):
        """Refresh display from AppState."""
        system = self.app_state.system

        if system is None:
            self.clear()
            return

        self._update_amplitudes(system)
        self._update_probabilities(system)
        self._update_details(system)

    def _update_amplitudes(self, system):
        text = "State Vector:\n\n"
        state = system.state
        n = system.num_qubits

        for i, amp in enumerate(state[:, 0]):
            if abs(amp) < EPS:
                continue

            basis = format(i, f"0{n}b")
            r, im = amp.real, amp.imag

            if abs(im) < EPS:
                text += f"|{basis}⟩: {r:+.4f}\n"
            elif abs(r) < EPS:
                text += f"|{basis}⟩: {im:+.4f}i\n"
            else:
                text += f"|{basis}⟩: {r:+.4f} {im:+.4f}i\n"

        self.amplitudes_text.setPlainText(text)

    def _update_probabilities(self, system):
        text = "Measurement Probabilities:\n\n"
        state = system.state
        n = system.num_qubits

        for i, amp in enumerate(state[:, 0]):
            p = abs(amp) ** 2
            if p < EPS:
                continue

            basis = format(i, f"0{n}b")
            text += f"|{basis}⟩: {p * 100:.2f}%\n"

        self.probabilities_text.setPlainText(text)

    def _update_details(self, system):
        n = system.num_qubits
        dim = len(system.state)

        probs = abs(system.state[:, 0]) ** 2
        total = probs.sum()
        purity = (probs ** 2).sum()
        non_zero = (probs > EPS).sum()

        text = (
            f"Number of qubits: {n}\n"
            f"State dimension: {dim}\n"
            f"Total probability: {total:.6f}\n"
            f"Purity: {purity:.6f}\n\n"
            f"State type: Pure state\n"
            f"Non-zero components: {non_zero}/{dim}\n"
        )

        self.details_text.setPlainText(text)

    def clear(self):
        self.amplitudes_text.setPlainText("State: |0⟩")
        self.probabilities_text.setPlainText("|0⟩: 100.0%")
        self.details_text.setPlainText("Ready")

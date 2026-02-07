"""
Control Panel Widget

Provides controls for circuit execution and configuration.
"""

from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QPushButton, QLabel, QSpinBox
)
from PyQt6.QtCore import Qt

from ui.app_state import AppState


class ControlPanel(QFrame):
    """
    Control panel bound to AppState.

    This widget mutates AppState directly and reacts to its updates.
    """

    def __init__(self, app_state: AppState, parent=None):
        super().__init__(parent)

        self.app_state = app_state

        self._init_ui()
        self._sync_from_state()

        # React to global state changes
        self.app_state.state_changed.connect(self._sync_from_state)
        self.app_state.circuit_changed.connect(self._sync_from_state)

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setMaximumHeight(60)

        # --- Qubits ----------------------------------------------------

        layout.addWidget(self._bold_label("Qubits:"))

        self.qubits_spinbox = QSpinBox()
        self.qubits_spinbox.setRange(1, 16)
        self.qubits_spinbox.valueChanged.connect(self._on_qubits_changed)
        layout.addWidget(self.qubits_spinbox)

        layout.addSpacing(20)

        # --- Target step -----------------------------------------------

        layout.addWidget(self._bold_label("Run to:"))

        self.target_step_spinbox = QSpinBox()
        self.target_step_spinbox.setMinimum(0)
        layout.addWidget(self.target_step_spinbox)

        layout.addSpacing(20)

        # --- Execution buttons -----------------------------------------

        self.step_button = self._make_button(
            "Step", "#4CAF50", self.app_state.step
        )
        layout.addWidget(self.step_button)

        self.run_to_button = self._make_button(
            "Run To", "#2196F3", self._on_run_to
        )
        layout.addWidget(self.run_to_button)

        self.run_all_button = self._make_button(
            "Run All", "#2196F3", self.app_state.run_all
        )
        layout.addWidget(self.run_all_button)

        self.reset_button = self._make_button(
            "Reset", "#FF9800", self.app_state.reset
        )
        layout.addWidget(self.reset_button)

        layout.addStretch()

        # --- Status ----------------------------------------------------

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("font-style: italic;")
        layout.addWidget(self.status_label)

    def _bold_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet("font-weight: bold;")
        return lbl

    def _make_button(self, text, color, callback):
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-weight: bold;
                padding: 6px 16px;
                border-radius: 4px;
                min-width: 70px;
            }}
            QPushButton:hover {{
                background-color: {color}AA;
            }}
        """)
        return btn

    def _sync_from_state(self):
        """Synchronize UI from AppState."""
        self.qubits_spinbox.blockSignals(True)
        self.qubits_spinbox.setValue(self.app_state.num_qubits)
        self.qubits_spinbox.blockSignals(False)

        self.target_step_spinbox.setMaximum(
            max(0, self.app_state.num_steps - 1)
        )

        self.status_label.setText(
            f"Step {self.app_state.current_step}/{self.app_state.num_steps}"
        )

        # Disable stepping when finished
        finished = self.app_state.current_step >= self.app_state.num_steps
        self.step_button.setEnabled(not finished)
        self.run_all_button.setEnabled(not finished)
        self.run_to_button.setEnabled(not finished)

    def _on_qubits_changed(self, value: int):
        self.app_state.set_num_qubits(value)

    def _on_num_steps_changed(self, value: int):
        self.app_state.set_num_steps(value)

    def _on_run_to(self):
        target = self.target_step_spinbox.value()
        self.app_state.run_to(target)

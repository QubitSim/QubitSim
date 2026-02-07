from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QSplitter
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from ui.app_state import AppState
from ui.circuit_canvas import CircuitCanvas
from ui.gate_palette import GatePalette
from ui.state_display import StateDisplay
from ui.control_panel import ControlPanel


class MainWindow(QMainWindow):
    """
    Main application window for QubitSim.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QubitSim - Quantum Circuit Simulator")
        self.setGeometry(100, 100, 1400, 800)

        # Centralized application state
        self.app_state = AppState(num_qubits=4, num_steps=10)

        self._init_ui()
        self._create_menu_bar()
        self._connect_state_signals()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        content_splitter = QSplitter(Qt.Orientation.Horizontal)

        self.gate_palette = GatePalette(self.app_state)
        content_splitter.addWidget(self.gate_palette)

        self.circuit_canvas = CircuitCanvas(self.app_state)
        content_splitter.addWidget(self.circuit_canvas)

        self.state_display = StateDisplay(self.app_state)
        content_splitter.addWidget(self.state_display)

        content_splitter.setStretchFactor(0, 1)
        content_splitter.setStretchFactor(1, 3)
        content_splitter.setStretchFactor(2, 2)

        main_layout.addWidget(content_splitter)

        self.control_panel = ControlPanel(self.app_state)
        main_layout.addWidget(self.control_panel)

    def _connect_state_signals(self):
        """
        MainWindow reacts only to AppState signals.
        Widgets update themselves internally.
        """
        self.app_state.circuit_changed.connect(self.on_circuit_changed)
        self.app_state.system_changed.connect(self.on_system_changed)

    def _create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")

        new_action = QAction("&New Circuit", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.on_new_circuit)
        file_menu.addAction(new_action)

        open_action = QAction("&Open Circuit", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.on_open_circuit)
        file_menu.addAction(open_action)

        save_action = QAction("&Save Circuit", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.on_save_circuit)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("&Edit")

        clear_action = QAction("&Clear Circuit", self)
        clear_action.triggered.connect(self.on_clear_circuit)
        edit_menu.addAction(clear_action)

        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About QubitSim", self)
        about_action.triggered.connect(self.on_about)
        help_menu.addAction(about_action)

    def on_circuit_changed(self):
        """
        Circuit structure changed.
        Canvas & state display react automatically.
        """
        pass

    def on_system_changed(self):
        """
        Execution state changed (statevector, probabilities, step).
        """
        pass

    def on_new_circuit(self):
        self.app_state.reset_execution()
        self.app_state.steps = [[] for _ in range(self.app_state.num_steps)]
        self.app_state.circuit_changed.emit()

    def on_clear_circuit(self):
        self.app_state.steps = [[] for _ in range(self.app_state.num_steps)]
        self.app_state.reset_execution()
        self.app_state.circuit_changed.emit()

    def on_open_circuit(self):
        # TODO: deserialize steps, num_qubits, num_steps
        pass

    def on_save_circuit(self):
        # TODO: serialize AppState.steps
        pass

    def on_about(self):
        # TODO: About dialog
        pass

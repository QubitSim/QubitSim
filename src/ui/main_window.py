from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QSplitter, QScrollArea
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
        self.setMinimumSize(800, 500)

        # Centralized application state
        self.app_state = AppState(num_qubits=4, num_steps=20)

        self._init_ui()
        self._create_menu_bar()
        self._connect_state_signals()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(4, 4, 4, 4)

        self.content_splitter = QSplitter(Qt.Orientation.Horizontal)
        # Allow every panel to collapse to a small but usable size
        self.content_splitter.setChildrenCollapsible(False)

        # --- Gate palette (left) ---
        self.gate_palette = GatePalette(self.app_state)
        self.gate_palette.setMinimumWidth(120)
        self.content_splitter.addWidget(self.gate_palette)

        # --- Circuit canvas wrapped in a scroll area (centre) ---
        self.circuit_canvas = CircuitCanvas(self.app_state)

        self.canvas_scroll = QScrollArea()
        self.canvas_scroll.setWidget(self.circuit_canvas)
        self.canvas_scroll.setWidgetResizable(True)          # canvas fills scroll area when it's smaller
        self.canvas_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.canvas_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.canvas_scroll.setMinimumWidth(300)
        self.content_splitter.addWidget(self.canvas_scroll)

        # --- State display (right) ---
        self.state_display = StateDisplay(self.app_state)
        self.state_display.setMinimumWidth(200)
        self.content_splitter.addWidget(self.state_display)

        # Proportional initial sizes: palette=1, canvas=4, state=2
        self.content_splitter.setStretchFactor(0, 1)
        self.content_splitter.setStretchFactor(1, 4)
        self.content_splitter.setStretchFactor(2, 2)

        self.main_layout.addWidget(self.content_splitter, stretch=1)

        self.control_panel = ControlPanel(self.app_state)
        self.main_layout.addWidget(self.control_panel)

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

        view_menu = menubar.addMenu("&View")

        light_theme_action = QAction("&Light Theme", self, checkable=True)
        light_theme_action.setChecked(self.app_state.theme == "light")
        light_theme_action.triggered.connect(lambda: self.on_set_theme("light"))
        view_menu.addAction(light_theme_action)

        dark_theme_action = QAction("&Dark Theme", self, checkable=True)
        dark_theme_action.setChecked(self.app_state.theme == "dark")
        dark_theme_action.triggered.connect(lambda: self.on_set_theme("dark"))
        view_menu.addAction(dark_theme_action)

        # Store theme actions for later toggle
        self.light_theme_action = light_theme_action
        self.dark_theme_action = dark_theme_action

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

    def on_set_theme(self, theme_name: str):
        """Set the application theme."""
        self.app_state.set_theme(theme_name)
        
        # Update menu checkstates
        self.light_theme_action.setChecked(theme_name == "light")
        self.dark_theme_action.setChecked(theme_name == "dark")
        
        # Trigger theme update in all child widgets
        self._apply_theme_to_widgets(theme_name)

    def _apply_theme_to_widgets(self, theme_name: str):
        """Apply theme to all UI widgets."""
        from ui.themes import get_theme

        theme = get_theme(theme_name)

        # Canvas and its scroll area must share the same background colour so
        # neither the QScrollArea frame nor its viewport bleeds through.
        canvas_bg = theme.canvas_bg
        self.canvas_scroll.setStyleSheet(
            f"QScrollArea {{ background-color: {canvas_bg}; border: none; }}"
        )
        self.canvas_scroll.viewport().setStyleSheet(
            f"background-color: {canvas_bg};"
        )
        self.circuit_canvas.set_theme(theme)

        # Update other widgets
        self.gate_palette.set_theme(theme)
        self.control_panel.set_theme(theme)
        self.state_display.set_theme(theme)

        # Update main window background
        self.setStyleSheet(f"QMainWindow {{ background-color: {theme.window_bg}; }}")

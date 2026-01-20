"""
Main Window for QubitSim Application

The main window provides the primary interface for the quantum circuit simulator,
containing the circuit canvas, gate palette, state display, and control panel.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, 
    QSplitter
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from ui.circuit_canvas import CircuitCanvas
from ui.gate_palette import GatePalette
from ui.state_display import StateDisplay
from ui.control_panel import ControlPanel


class MainWindow(QMainWindow):
    """
    Main application window for QubitSim.
    
    Layout:
    - Top: Menu bar
    - Left: Gate palette (draggable gates)
    - Center: Circuit canvas (drop zone for gates)
    - Right: State display (state vector, probabilities, etc.)
    - Bottom: Control panel (step, run all, reset buttons)
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QubitSim - Quantum Circuit Simulator")
        self.setGeometry(100, 100, 1400, 800)
        
        self._init_ui()
        self._create_menu_bar()
        
    def _init_ui(self):
        """Initialize the user interface components."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Horizontal splitter for main content
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Gate Palette
        self.gate_palette = GatePalette()
        content_splitter.addWidget(self.gate_palette)
        
        # Center panel - Circuit Canvas
        self.circuit_canvas = CircuitCanvas()
        content_splitter.addWidget(self.circuit_canvas)
        
        # Right panel - State Display
        self.state_display = StateDisplay()
        content_splitter.addWidget(self.state_display)
        
        # Set splitter proportions (1:3:2)
        content_splitter.setStretchFactor(0, 1)
        content_splitter.setStretchFactor(1, 3)
        content_splitter.setStretchFactor(2, 2)
        
        main_layout.addWidget(content_splitter)
        
        # Bottom panel - Control Panel
        self.control_panel = ControlPanel()
        main_layout.addWidget(self.control_panel)
        
        # Connect signals
        self._connect_signals()
        
    def _connect_signals(self):
        """Connect signals between components."""
        # Control panel signals
        self.control_panel.step_clicked.connect(self.on_step)
        self.control_panel.run_all_clicked.connect(self.on_run_all)
        self.control_panel.run_to_step_clicked.connect(self.on_run_to_step)
        self.control_panel.reset_clicked.connect(self.on_reset)
        self.control_panel.num_qubits_changed.connect(self.on_num_qubits_changed)
        
        # Circuit canvas signals
        self.circuit_canvas.circuit_changed.connect(self.on_circuit_changed)
        
    def _create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
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
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        clear_action = QAction("&Clear Circuit", self)
        clear_action.triggered.connect(self.on_clear_circuit)
        edit_menu.addAction(clear_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About QubitSim", self)
        about_action.triggered.connect(self.on_about)
        help_menu.addAction(about_action)
    
    # Slot methods
    def on_step(self):
        """Execute one step of the circuit."""
        self.circuit_canvas.execute_step()
        self.state_display.update_state(self.circuit_canvas.get_current_state())
    
    def on_run_all(self):
        """Execute all remaining steps of the circuit."""
        self.circuit_canvas.execute_all()
        self.state_display.update_state(self.circuit_canvas.get_current_state())
    
    def on_run_to_step(self, target_step: int):
        """Execute up to a specific step."""
        self.circuit_canvas.execute_to_step(target_step)
        self.state_display.update_state(self.circuit_canvas.get_current_state())
    
    def on_reset(self):
        """Reset the circuit to initial state."""
        self.circuit_canvas.reset()
        self.state_display.update_state(self.circuit_canvas.get_current_state())
    
    def on_num_qubits_changed(self, num_qubits: int):
        """Handle change in number of qubits."""
        self.circuit_canvas.set_num_qubits(num_qubits)
        self.state_display.update_state(self.circuit_canvas.get_current_state())
    
    def on_circuit_changed(self):
        """Handle circuit modification."""
        # Update state display when circuit structure changes
        self.state_display.update_state(self.circuit_canvas.get_current_state())
    
    def on_new_circuit(self):
        """Create a new circuit."""
        self.circuit_canvas.clear()
        self.state_display.clear()
    
    def on_open_circuit(self):
        """Open a circuit from file (JSON)."""
        # TODO: Implement file dialog and loading
        pass
    
    def on_save_circuit(self):
        """Save circuit to file (JSON)."""
        # TODO: Implement file dialog and saving
        pass
    
    def on_clear_circuit(self):
        """Clear the current circuit."""
        self.circuit_canvas.clear()
        self.state_display.clear()
    
    def on_about(self):
        """Show about dialog."""
        # TODO: Implement about dialog
        pass

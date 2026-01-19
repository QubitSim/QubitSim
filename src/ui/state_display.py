"""
State Display Widget

Displays the current quantum state in various representations:
- State vector (amplitudes)
- Measurement probabilities
- Single-qubit views (for future: Bloch sphere representation)
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, 
    QTabWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from core.system import System


class StateDisplay(QWidget):
    """
    Display quantum state information.
    
    Provides multiple views of the quantum state:
    - Amplitudes tab: Complex amplitudes of basis states
    - Probabilities tab: Measurement probabilities
    - Details tab: Additional quantum state information
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(300)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the state display UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title = QLabel("Quantum State")
        title.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            padding: 5px;
            background-color: #F0F0F0;
            border-radius: 3px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Tab widget for different views
        self.tabs = QTabWidget()
        
        # Amplitudes tab
        self.amplitudes_text = QTextEdit()
        self.amplitudes_text.setReadOnly(True)
        self.amplitudes_text.setFont(QFont("Courier", 10))
        self.amplitudes_text.setPlainText("State: |0⟩")
        self.tabs.addTab(self.amplitudes_text, "Amplitudes")
        
        # Probabilities tab
        self.probabilities_text = QTextEdit()
        self.probabilities_text.setReadOnly(True)
        self.probabilities_text.setFont(QFont("Courier", 10))
        self.probabilities_text.setPlainText("|0⟩: 100.0%")
        self.tabs.addTab(self.probabilities_text, "Probabilities")
        
        # Details tab
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setFont(QFont("Courier", 9))
        self.details_text.setPlainText("Number of qubits: 3\nDimension: 8")
        self.tabs.addTab(self.details_text, "Details")
        
        layout.addWidget(self.tabs)
    
    def update_state(self, system: System):
        """Update the display with the current quantum state."""
        if system is None:
            return
        
        self._update_amplitudes(system)
        self._update_probabilities(system)
        self._update_details(system)
    
    def _update_amplitudes(self, system: System):
        """Update the amplitudes display."""
        text = "State Vector:\n\n"
        
        state = system.state
        num_qubits = system.num_qubits
        
        for i in range(len(state)):
            amplitude = state[i][0]
            
            # Format basis state
            basis = format(i, f'0{num_qubits}b')
            
            # Format complex amplitude
            real = amplitude.real
            imag = amplitude.imag
            
            if abs(amplitude) < 1e-10:
                continue  # Skip negligible amplitudes
            
            if abs(imag) < 1e-10:
                # Pure real
                text += f"|{basis}⟩: {real:+.4f}\n"
            elif abs(real) < 1e-10:
                # Pure imaginary
                text += f"|{basis}⟩: {imag:+.4f}i\n"
            else:
                # Complex
                text += f"|{basis}⟩: {real:+.4f} {imag:+.4f}i\n"
        
        self.amplitudes_text.setPlainText(text)
    
    def _update_probabilities(self, system: System):
        """Update the probabilities display."""
        text = "Measurement Probabilities:\n\n"
        
        state = system.state
        num_qubits = system.num_qubits
        
        for i in range(len(state)):
            amplitude = state[i][0]
            probability = abs(amplitude) ** 2
            
            if probability < 1e-10:
                continue  # Skip negligible probabilities
            
            basis = format(i, f'0{num_qubits}b')
            text += f"|{basis}⟩: {probability*100:.2f}%\n"
        
        self.probabilities_text.setPlainText(text)
    
    def _update_details(self, system: System):
        """Update the details display."""
        num_qubits = system.num_qubits
        dimension = len(system.state)
        
        # Calculate total probability (should be 1.0)
        total_prob = sum(abs(system.state[i][0])**2 for i in range(dimension))
        
        # Calculate purity (for pure states should be 1.0)
        purity = sum(abs(system.state[i][0])**4 for i in range(dimension))
        
        text = f"Number of qubits: {num_qubits}\n"
        text += f"State dimension: {dimension}\n"
        text += f"Total probability: {total_prob:.6f}\n"
        text += f"Purity: {purity:.6f}\n"
        text += f"\nState type: Pure state\n"
        
        # Count non-zero amplitudes
        non_zero = sum(1 for i in range(dimension) if abs(system.state[i][0]) > 1e-10)
        text += f"Non-zero components: {non_zero}/{dimension}\n"
        
        self.details_text.setPlainText(text)
    
    def clear(self):
        """Clear all displays."""
        self.amplitudes_text.setPlainText("State: |0⟩")
        self.probabilities_text.setPlainText("|0⟩: 100.0%")
        self.details_text.setPlainText("Ready")

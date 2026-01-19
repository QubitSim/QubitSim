"""
Example: Programmatically Building a Circuit

This example demonstrates how to interact with the QubitSim UI
programmatically to build and execute a simple circuit.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from ui.main_window import MainWindow


def build_example_circuit(window):
    """Build a simple example circuit."""
    canvas = window.circuit_canvas
    
    # Place H gate on qubit 0 at time step 0
    canvas.circuit[0][0] = "H"
    
    # Place X gate on qubit 1 at time step 2
    canvas.circuit[2][1] = "X"
    
    # Place Z gate on qubit 2 at time step 1
    canvas.circuit[1][2] = "Z"
    
    # Update the canvas
    canvas.update()
    canvas.circuit_changed.emit()
    
    print("Example circuit built!")
    print("Circuit structure:")
    for step in range(3):
        print(f"  Step {step}: {canvas.circuit[step]}")


def main():
    """Launch the application with an example circuit."""
    app = QApplication(sys.argv)
    app.setApplicationName("QubitSim Example")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Build example circuit after window is shown
    QTimer.singleShot(100, lambda: build_example_circuit(window))
    
    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

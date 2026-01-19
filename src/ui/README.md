# QubitSim UI Module

PyQt6-based graphical user interface for the QubitSim quantum circuit simulator.

## Overview

The UI module provides an interactive desktop application for building and visualizing quantum circuits. It implements a drag-and-drop interface where users can construct circuits by placing gates on a grid representing qubits and time steps.

## Architecture

The UI is organized into the following components:

### Main Window (`main_window.py`)
The primary application window that coordinates all UI components:
- Menu bar for file operations (New, Open, Save)
- Integrated layout with splitters for flexible sizing
- Signal/slot connections between components

### Circuit Canvas (`circuit_canvas.py`)
Interactive canvas for circuit construction:
- Grid-based layout with qubit wires and time steps
- Drag-and-drop support for gate placement
- Visual indication of current execution step
- Right-click to remove gates
- Configurable number of qubits (1-16)

### Gate Palette (`gate_palette.py`)
Scrollable palette of available quantum gates:
- Single-qubit gates: H, X, Y, Z, S, T
- Draggable gate buttons
- Organized by category
- Placeholders for rotation gates and control operations (coming soon)

### State Display (`state_display.py`)
Multi-tab display of quantum state information:
- **Amplitudes tab**: Complex amplitudes of basis states
- **Probabilities tab**: Measurement probabilities
- **Details tab**: System metadata (purity, dimensions, etc.)

### Control Panel (`control_panel.py`)
Execution controls:
- **Qubits spinner**: Adjust number of qubits (1-16)
- **Step button**: Execute one time step
- **Run All button**: Execute all remaining steps
- **Reset button**: Reset to initial state |0⟩

## Usage

### Running the Application

```bash
cd src
python3 main.py
```

### Building a Circuit

1. Select the number of qubits using the spinner in the control panel
2. Drag gates from the palette on the left
3. Drop them onto the circuit canvas grid
4. Right-click on a gate to remove it

### Executing the Circuit

- **Step**: Execute gates at the current time step (indicated by red outline)
- **Run All**: Execute all remaining steps sequentially
- **Reset**: Return to initial state |000...0⟩

### Viewing the State

The right panel shows the quantum state in multiple representations:
- Real-time updates as circuit executes
- Negligible amplitudes (< 10⁻¹⁰) are hidden for clarity

## Integration with Core Modules

The UI integrates with existing QubitSim modules:

- **`core.system.System`**: Quantum state representation
- **`core.gates`**: Gate definitions (H, X, Y, Z, S, T)
- **`circuit.interpreter`**: Circuit execution (integration pending)

## Future Enhancements

The current implementation provides a solid foundation. Planned improvements include:

1. **Circuit Execution**: Full integration with `CircuitInterpreter` to apply gates
2. **Rotation Gates**: Dialog for parameterized gates (Rx(θ), Ry(θ), Rz(θ))
3. **Control Gates**: Support for CNOT and multi-controlled operations
4. **File I/O**: Save/load circuits in JSON format
5. **Bloch Sphere**: 3D visualization for single-qubit states
6. **Measurement**: Visual measurement operation with collapse
7. **Export**: Circuit export to Qiskit/Cirq format

## Design Principles

The UI follows QubitSim's core design principles:

- **Circuit-centric**: Users build circuits, state is derived
- **Immediate feedback**: State updates after each step
- **Educational focus**: Clear visualization over performance
- **Small-scale correctness**: Optimized for ~3-16 qubits
- **No approximations**: Exact linear algebra

## Dependencies

- PyQt6 >= 6.4.0
- numpy >= 1.24.0

## File Structure

```
ui/
├── __init__.py           # Module initialization
├── main_window.py        # Main application window
├── circuit_canvas.py     # Circuit building canvas
├── gate_palette.py       # Draggable gate palette
├── state_display.py      # Quantum state visualization
└── control_panel.py      # Execution controls
```

## Development Notes

- All UI code is in `/src/ui` directory
- Core quantum logic (`/src/core`) and circuit logic (`/src/circuit`) are not modified
- The UI is designed to be extended without breaking existing functionality
- Uses PyQt6's signal/slot mechanism for component communication

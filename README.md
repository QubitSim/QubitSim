# Qiskit Backend Integration - Quick Start Guide

## How to Use

### 1. Install Dependencies

```bash
cd /home/andresgomez31/git/QubitSim
pip install -r requirements.txt
```

Or with the virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Application

```bash
cd src
python main.py
```

Or with full path:
```bash
python /home/andresgomez31/git/QubitSim/src/main.py
```

### 3. Build and Execute Circuits

1. **Select a gate** from the left palette (H, X, Y, Z, RX, RY, RZ, etc.)
2. **Drag and drop** onto the circuit canvas
3. **Click "Step"** to execute one step at a time
4. **Click "Run All"** to execute the entire circuit
5. **Watch the quantum state** evolve in the right panel

### 4. View Results

The right panel shows:
- **Amplitudes**: Complex amplitudes for each basis state
- **Probabilities**: Measurement probabilities for each outcome
- **Details**: System metadata and state information
- **Probability chart**: Visual representation of probabilities
- **Bloch Sphere**: Visualization of single-qubit states
- **Phase Plot**: Visualization of complex amplitudes
- **Statistics**: Numerical data about the current state

## Testing

All tests passing:

```bash
# Backend unit tests (5/5 passing)
PYTHONPATH=src python test_backend.py

# Integration tests (3/3 passing)
PYTHONPATH=src python test_integration.py

# UI smoke tests (all passing)
PYTHONPATH=src python test_ui_smoke.py

# To capture the new UI tests, run with:
PYTHONPATH=src python test_ui_updates.py

# To test the visualizations
PYTHONPATH=src python test_visualizations.py

```

With virtual environment:
```bash
PYTHONPATH=src ./venv/bin/python test_backend.py
PYTHONPATH=src ./venv/bin/python test_integration.py
PYTHONPATH=src ./venv/bin/python test_ui_smoke.py
PYTHONPATH=src ./venv/bin/python test_ui_updates.py
PYTHONPATH=src ./venv/bin/python test_visualizations.py
```

## Example: Creating a Bell State

1. Start with 2 qubits
2. Add H gate to qubit 0 at step 0
3. Add CNOT (controlled X) to qubit 1 at step 0 (with control on qubit 0)
4. Click "Run All"
5. Result: Entangled state (|00⟩ + |11⟩)/√2

## Features Working

Single-qubit gates (H, X, Y, Z, S, T)
Rotation gates (RX, RY, RZ) with parameters
Controlled gates (CNOT, CY, CZ, CH)
SWAP gates
Step-by-step execution
Full circuit execution
State visualization
Measurement probabilities
Reset and circuit modification
Dynamic qubit count

## Architecture

```
User Interface (PyQt6)
    ↓
AppState (State Management)
    ↓
QiskitBackend (Simulation)
    ↓
CircuitInterpreter (Circuit Building)
    ↓
Qiskit (Quantum Simulation)
```

## Next Steps

### For Demonstration
- The temporary Qiskit backend is ready for demos
- All UI features are functional
- State visualization works in real-time

### For Custom Backend Development
When ready to implement the custom backend in `core/`:

1. Implement `core.Operator` matrix operations
2. Implement `core.Gate` using Operator
3. Implement `core.System` state evolution
4. Create `CustomBackend` in `qcircuit/backend.py`
5. Replace `QiskitBackend` with `CustomBackend` in `app_state.py`

## File Structure

```
QubitSim/
├── src/
│   ├── main.py                         # Application entry point
│   ├── core/                           # Custom backend (future)
│   │   ├── __init__.py
│   │   ├── system.py                  # System class
│   │   ├── operator.py                # Operator class
│   │   ├── gate.py                    # Gate base class
│   │   └── gates.py                   # Gate implementations
│   ├── qcircuit/                       # Intermediary layer
│   │   ├── __init__.py
│   │   ├── backend.py                 # Qiskit backend
│   │   ├── interpreter.py             # Circuit builder
│   │   └── objects.py                 # Gate definitions
│   └── ui/                             # PyQt6 UI components
│       ├── __init__.py
│       ├── README.md                  # UI documentation
│       ├── main_window.py             # Main window
│       ├── app_state.py               # Backend integration
│       ├── circuit_canvas.py          # Circuit editor
│       ├── gate_palette.py            # Gate selection
│       ├── control_panel.py           # Execution controls
│       ├── state_display.py           # State visualization
│       ├── themes.py                  # UI themes
│       ├── visualization_utils.py     # Visualization utilities
│       └── visualization_widgets.py   # Visualization components
├── test_backend.py                    # Backend tests
├── test_integration.py                # Integration tests
├── test_ui_smoke.py                   # UI tests
├── README.md                          # This file
└── requirements.txt                   # Dependencies
```

## Technical Notes

### Qubit Ordering
Qiskit uses little-endian qubit ordering:
- 2-qubit basis: |q1,q0⟩
- H on q0: (|00⟩ + |01⟩)/√2

### Performance
- Statevector simulation: Exact, but exponential memory
- Practical limit: ~20-25 qubits
- For larger circuits: Switch to custom backend with optimizations

### Error Handling
- Circuit execution errors are caught and logged
- System resets to |0⟩ state on error
- UI remains responsive

## Support

For issues or questions:
1. Check `IMPLEMENTATION.md` for technical details
2. Run tests to verify installation
3. Check console output for error messages

## Success Criteria 

All requirements met:
- Qiskit backend implemented
- Integrated with AppState
- UI connects to backend
- Step-by-step execution works
- State visualization works
- All tests passing
- Ready for demonstration

---

**Status**: Demonstration Ready.

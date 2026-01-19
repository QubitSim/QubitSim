# QubitSim Examples

This directory contains example scripts demonstrating how to use QubitSim.

## Running Examples

Make sure you have installed the required dependencies:

```bash
pip install -r ../requirements.txt
```

### Example Circuit

Demonstrates programmatically building a circuit:

```bash
python example_circuit.py
```

This will launch the QubitSim UI with a pre-built circuit containing:
- H gate on qubit 0 at time step 0
- Z gate on qubit 2 at time step 1
- X gate on qubit 1 at time step 2

## Creating Your Own Circuits

You can modify the circuit by:
1. Dragging gates from the palette
2. Right-clicking to remove gates
3. Using the Step/Run All buttons to execute

Or programmatically:

```python
# Access the circuit canvas
canvas = window.circuit_canvas

# Place a gate at step, qubit
canvas.circuit[step][qubit] = "H"

# Update the display
canvas.update()
canvas.circuit_changed.emit()
```

Available gates: H, X, Y, Z, S, T

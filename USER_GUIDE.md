# QubitSim User Guide

Welcome to QubitSim! This is a beginner-friendly guide to learning how to use the quantum circuit simulator. If you're new to quantum computing, this guide will help you get started.

---

## What is QubitSim?

QubitSim is a **visual quantum circuit simulator** designed for learning. Think of it like a laboratory where you can:

- **Build** quantum circuits by dragging and dropping gates
- **Run** circuits and watch what happens step-by-step
- **Observe** how quantum states change as you apply gates

Unlike production quantum computing tools, QubitSim is **educational-focused**: it lets you see exactly what's happening at each step, rather than just showing you the final answer.

---

## Getting Started

### Starting the Application

1. Open a terminal and navigate to your QubitSim folder:
   ```bash
   cd /path/to/QubitSim
   ```

2. Activate the virtual environment (optional but recommended):
   ```bash
   source venv/bin/activate
   ```

3. Run the simulator:
   ```bash
   python src/main.py
   ```

4. A window should appear with:
   - **Left side**: Gate palette (colorful buttons with gate names)
   - **Middle**: Circuit canvas (grid where you place gates)
   - **Right side**: State display (shows results)

---

## The Main Screen

```
┌──────────────────────────────────┐
│        QubitSim Window           │
├──────────────────────────────────┤
│ Gate  │                  │State  │
│Palette│   Circuit Canvas │Display│
│ (H,X, │        (Grid)    │amps   │
│ Y, Z) │                  │prob   │
│ ...   │                  │       │
├──────────────────────────────────┤
│       Control Buttons            │
│   [ Step ] [ Run All ] [ Reset ] │
└──────────────────────────────────┘
```

### Left Panel: Gate Palette
Contains all available quantum gates organized by type:
- **Basic gates**: H, X, Y, Z (fundamental quantum operations)
- **Rotation gates**: RX, RY, RZ (controlled rotations)
- **Phase gates**: S, T, and their inverses
- **Multi-qubit gates**: CNOT, SWAP, Toffoli (gates affecting multiple qubits)
- **Advanced gates**: Various algorithms and oracle components

### Middle Panel: Circuit Canvas
The grid where you build your quantum circuit:
- **Horizontal lines** = quantum bits (qubits)
- **Vertical columns** = time steps
- Each cell is where you place gates

### Right Panel: State Display
Shows the current quantum state with three tabs:
1. **Amplitudes**: Complex numbers describing the quantum state
2. **Probabilities**: Chances of measuring each outcome
3. **Details**: Information about your system

---

## Building Your First Circuit

### Step 1: Drag a Gate onto the Canvas

1. Click and hold a gate button from the **left panel** (e.g., "H" for Hadamard)
2. Drag it to the circuit canvas
3. Release over the qubit and time position where you want it
4. The gate appears on the canvas

### Step 2: Run Your Circuit

- **Step**: Execute one time step at a time (useful for watching changes)
- **Run All**: Execute the entire circuit at once
- **Reset**: Start over with all qubits in the initial state

### Step 3: Check the Results

Look at the **State Display** on the right:
- **Amplitudes tab**: See the complex amplitudes (⟨basis state | state⟩)
- **Probabilities tab**: See measurement probabilities (|amplitude|²)

---

## Guided Example: Create a Bell State (Entangled Qubits)

A **Bell state** is a famous example of **entanglement**—two qubits that are mysteriously connected.

### Instructions:

1. **Set up the canvas with 2 qubits**
   - The canvas defaults to showing multiple qubits

2. **Place an H (Hadamard) gate on qubit 0 at time step 0**
   - Drag the "H" button from the left panel
   - Drop it on the first qubit (top line) at the first time column
   - This creates a superposition: the qubit is now in a "both 0 and 1 at once" state

3. **Place a CNOT gate (Controlled-NOT) on qubits 0→1 at time step 1**
   - Find "CNOT" in the gate palette
   - Drag and drop it to time step 1
   - The control qubit should be qubit 0, target qubit 1
   - This "links" the two qubits together

4. **Click "Run All"**
   - Watch the quantum state update in the right panel

5. **Check the results in the Probabilities tab**
   - You should see two possible measurement outcomes with 50% probability each:
     - |00⟩ with 50% chance
     - |11⟩ with 50% chance
   - This is entanglement! The qubits are forever linked—you always measure them the same.

### Why This Matters:

- Before the CNOT, measuring qubit 0 would give 50% |0⟩ or 50% |1⟩ (random)
- Before the CNOT, measuring qubit 1 would always give |0⟩ (certain)
- **After** the CNOT: if you measure qubit 0 and get |0⟩, qubit 1 is definitely |0⟩. If qubit 0 is |1⟩, qubit 1 is definitely |1⟩
- The CNOT gate *entangled* them!

---

## Common Gates Explained

Here are the most useful gates to start with:

| Gate | What It Does | Symbol |
|------|-------------|--------|
| **H** (Hadamard) | Creates superposition (50% each outcome) | H |
| **X** (Pauli-X) | Flips the qubit (like a NOT gate) | X |
| **Z** | Applies a phase flip | Z |
| **CNOT** | If control is 1, flip the target. Otherwise, do nothing | ⊕ |
| **SWAP** | Exchange the states of two qubits | ✕ |

---

## Tips for Learning

**Do:**
- Start simple: use just H and X gates
- Use the "Step" button to watch changes one at a time
- Check the Probabilities tab after each circuit
- Try the Bell state example above
- Experiment! Quantum mechanics is surprising

**Don't:**
- Worry about the complex numbers in Amplitudes (that's advanced)
- Try to understand all 97 gates at once
- Feel bad if you're confused—quantum mechanics is weird!

---

## Useful Patterns

### Pattern 1: Create Equal Superposition
Place **H gates on all qubits** at time step 0.
- Result: All measurement outcomes equally likely

### Pattern 2: Create Entanglement
Place **H on qubit 0**, then **CNOT from 0 to 1**.
- Result: Two qubits always measure the same

### Pattern 3: Flip a Qubit
Place an **X gate** on any qubit.
- Result: |0⟩ becomes |1⟩ and vice versa

---

## Frequently Asked Questions

**Q: What's the difference between "Step" and "Run All"?**
A: "Step" executes one time column at a time so you can watch changes. "Run All" executes the whole circuit instantly.

**Q: Why do the same circuit sometimes give different results?**
A: That's quantum mechanics! Certain measurements are random. Run the circuit multiple times to see the probability distribution.

**Q: What do the imaginary numbers (i) in Amplitudes mean?**
A: They represent quantum phases—a subtle but crucial part of quantum mechanics. For learning basics, focus on Probabilities instead.

**Q: Can I build circuits with more than 2 qubits?**
A: Yes! You can use up to 16 qubits, but remember: state visualization gets more complex with more qubits.

**Q: What if I make a mistake?**
A: Click "Reset" to return all qubits to the initial state and start over.

---

## Next Steps

- Try building different circuits and observing the state changes
- Read the [Technical Documentation](./README.md) if you want to understand how QubitSim works internally
- Check the [Project Overview](./DOCS.md) for more details about scope and design

---

## Need Help?

- **Quantum Basics**: Review your quantum mechanics notes (especially superposition and entanglement)
- **Gate Definitions**: Each gate has a mathematical definition; consult a quantum computing textbook or online resource
- **Bug Reports**: Check if your issue is clear before reporting

Enjoy your quantum learning journey!

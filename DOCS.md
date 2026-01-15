## Final project definition (locked)

### **Project type**

Educational **quantum circuit simulator** with explicit, step-by-step state visualization.

### **Target audience**

* Undergraduate **Computer Science**
* Undergraduate **Physics**
* Assumes:

  * Linear algebra familiarity
  * Basic quantum mechanics (Dirac notation, measurement postulate)
  * No prior experience with quantum SDKs

---

## Core purpose (this is the paper’s backbone)

> **Enable students to explicitly observe how a quantum circuit transforms a quantum system over time, instead of treating the circuit as a black box.**

This is your **unique value proposition**.

You are not optimizing, abstracting, or hiding complexity.
You are **surfacing it intentionally**.

---

## Functional scope (what the simulator WILL do)

### 1. Circuit construction

* Standard quantum circuit representation:

  * Horizontal wires = qubits
  * Discrete gate placement
* Supported gates (strictly defined):

  * Single-qubit: X, Y, Z, H, S, T
  * Parametric: RX, RY, RZ
  * Multi-qubit: CNOT, CZ
* Max qubits: **5**

  * This is *pedagogically optimal*
  * Enough to show entanglement without UI overload

### 2. Execution model

* **Step-by-step execution**
* Each gate application is a discrete event
* No batch execution unless explicitly requested

### 3. State representation (critical)

The simulator maintains **one canonical internal state**, with two exposed views:

* **State vector** (pure states)
* **Density matrix** (always derivable)

Important design choice (recommended):

* Internally store the **state vector**
* Derive density matrix on demand
  This keeps the system simple and explainable.

### 4. Visualization (this is the real contribution)

At each step, the user can see:

* State vector:

  * Complex amplitudes
  * Basis labels (|000⟩ … |11111⟩)
* Density matrix:

  * Matrix view (real/imaginary or magnitude/phase)
* Optional:

  * Probability distribution per basis state

What you **do not** visualize:

* Bloch sphere per qubit (tempting, but distracts from circuits)
* Noise models (out of scope)

---

## What this project is explicitly NOT

You must state this in the paper.

* ❌ Not a quantum compiler
* ❌ Not a performance-oriented simulator
* ❌ Not scalable beyond educational limits
* ❌ Not intended to replace Qiskit / Cirq
* ❌ No noise, decoherence, or hardware modeling

This protects you academically.

---

## Why this is a valid scientific/academic contribution

Because most tools optimize for **usage**, not **understanding**.

Your simulator:

* Makes tensor products explicit
* Shows amplitude redistribution after each gate
* Makes measurement collapse visible
* Forces the student to confront exponential state growth

This directly addresses a **well-known learning barrier** in QC education.

---

## Backend architecture (important for your HPC trajectory)

Even though the value is frontend-centric, the backend must be **cleanly abstracted**.

### Required abstraction layer

```text
QuantumState
  - apply_gate(gate, targets)
  - measure(qubit)
  - get_state_vector()
  - get_density_matrix()
```

Below that:

```text
LinearAlgebraBackend
  - vector ops
  - matrix ops
  - tensor product
```

This is what allows:

* Python backend now
* C++ backend later
* Zero redesign

You mention this **explicitly** in the paper.

---

## Paper positioning (now clear)

### What the paper argues

* Students struggle because quantum circuits hide state evolution
* Explicit visualization improves conceptual understanding
* A carefully limited simulator can expose this without overwhelming users

### What the paper demonstrates

* Correct quantum evolution
* Step-wise state transformation
* Entanglement emergence
* Measurement collapse

### What the paper does NOT claim

* Performance gains
* Hardware realism
* Large-scale simulation

---

## Verdict

Your proposal is:

* ✔ Pedagogically strong
* ✔ Academically defensible
* ✔ Cleanly separable from HPC work
* ✔ Easy to extend later without rewriting history

This is the **right scope**.


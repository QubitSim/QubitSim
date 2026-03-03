# State Display Visualization Guide

## Quick Start

The State Display panel now includes 7 tabs for understanding quantum states:

### Text-Based Tabs (Original)
1. **Amplitudes** - Raw complex amplitudes |ψ⟩ = Σ αᵢ |i⟩
2. **Probabilities** - Measurement probabilities P(i) = |αᵢ|²
3. **Details** - System properties (qubits, dimension, purity, measurements)

### Visual Tabs (New)
4. **Prob. Chart** - Interactive probability visualization
5. **Bloch Sphere** - 3D single-qubit state representation
6. **Phase Plot** - Amplitude magnitudes with phase coloring
7. **Statistics** - Entropy, purity, and distribution analysis

---

## Tab Guide

### 1. Amplitudes Tab
**Use when:** You need exact complex amplitude values

**Shows:**
- State vector in basis notation |basis⟩: amplitude
- Both real and imaginary parts
- All non-zero amplitudes (>1e-10)

**Example:**
```
State Vector:
|00⟩: +0.7071
|11⟩: +0.7071
```

### 2. Probabilities Tab
**Use when:** You want measurement outcome probabilities

**Shows:**
- Probability percentage for each basis state
- P = |α|² where α is the amplitude
- Automatically sorted by basis state

**Example:**
```
Measurement Probabilities:
|00⟩: 50.00%
|11⟩: 50.00%
```

### 3. Details Tab
**Use when:** You need system information

**Shows:**
- Number of qubits (n)
- Hilbert space dimension (2ⁿ)
- Total probability (should be ~1.0)
- Purity (1.0 for pure states)
- Non-zero components count
- Last measurement result

**Interpretation:**
- Purity = 1.0 → Pure state
- Purity < 1.0 → Mixed state
- Non-zero components << 2ⁿ → Sparse state

### 4. Prob. Chart Tab
**Use when:** You want visual comparison of probabilities

**Features:**
- 📊 Bar chart showing each state's probability
- 🎚️ **Threshold slider** (0-10%) - Hide states with lower probability
- 📈 **Log scale toggle** - For systems with many states
- 🎨 Color gradient - Darker blue = higher probability
- 📍 Probability percentage shown on each bar

**How to use:**
1. Increase threshold to focus on dominant states
2. Use log scale for systems > 8 qubits
3. Hover over bars to see exact values (tooltip)

**Interpretation:**
- Sharp peaks → Deterministic behavior
- Flat distribution → Maximum uncertainty (H ≈ n bits)
- Multiple peaks → Entanglement patterns

### 5. Bloch Sphere Tab
**Use when:** Analyzing single-qubit states

**Features:**
- 🌐 3D Bloch sphere visualization
- 🔴 **Qubit selector** - Choose which qubit to visualize (for multi-qubit systems)
- 📍 State vector (black arrow) showing qubit position
- 🧭 Color axes: Red=X, Green=Y, Blue=Z
- 📐 Coordinates display: θ (polar angle), φ (azimuthal angle)

**Interpretation:**
- |0⟩ at north pole: θ = 0, φ = any
- |1⟩ at south pole: θ = π, φ = any
- Equal superposition (|0⟩ + |1⟩)/√2 at equator: θ = π/2, φ = 0
- Superposition with phase (|0⟩ + i|1⟩)/√2 at equator: θ = π/2, φ = π/2

**Reading coordinates:**
```
θ (theta): 0 to π radians
  θ = 0:     |0⟩ state (north pole)
  θ = π/2:   Equatorial plane (+ superposition)
  θ = π:     |1⟩ state (south pole)

φ (phi): 0 to 2π radians
  φ = 0:     Real amplitude front
  φ = π/2:   Imaginary i amplitude left
  φ = π:     Real amplitude back
  φ = 3π/2:  Imaginary -i amplitude right
```

### 6. Phase Plot Tab
**Use when:** Understanding phase relationships between amplitudes

**Features:**
- 📊 Bar chart with amplitude magnitudes
- 🌈 Bar colors encode phase angles (HSL color space)
- 📏 Bar height = magnitude |α|
- 📉 Bars sorted by magnitude (largest first)

**Color coding:**
- 🔴 Red (0 rad): Zero phase
- 🟡 Yellow (π/2 rad): +90° phase
- 🟦 Cyan (π rad): 180° phase (opposite direction)
- 🔵 Blue (3π/2 rad): -90° phase

**Interpretation:**
- All bars same color → No relative phase differences
- Mixed colors → Quantum interference possible
- Symmetric colors (red + cyan) → Standing wave patterns in superposition

**Example - Bell State (|00⟩ + |11⟩)/√2:**
```
|00⟩: magnitude 0.707, phase 0 (red)
|11⟩: magnitude 0.707, phase 0 (red)
→ Constructive interference possible
```

**Example - Bell State (|00⟩ - |11⟩)/√2:**
```
|00⟩: magnitude 0.707, phase 0 (red)
|11⟩: magnitude 0.707, phase π (cyan)
→ Destructive interference possible
```

### 7. Statistics Tab
**Use when:** Understanding quantum properties of the state

**Displays:**

#### Entropy Analysis
```
Von Neumann Entropy: H = -Σ pᵢ log₂(pᵢ)
  Range: 0 to n bits
  H = 0:   Pure, deterministic
  H = n:   Maximally mixed/uncertain
  
Max possible entropy: log₂(2ⁿ)
Entropy ratio: H / H_max (0 to 1)
```

#### Purity Analysis
```
Purity: P = Σ pᵢ²
  P = 1.0:    Pure state (100% confident in state)
  P < 1.0:    Mixed state (uncertainty/decoherence)
  
Examples:
  |0⟩:        Purity = 1.0 (pure)
  (|0⟩ + |1⟩)/√2: Purity = 0.5 (maximally mixed)
```

#### Probability Distribution
```
Total states: 2ⁿ (Hilbert space dimension)
Non-zero amplitudes: Count of |α| > 1e-10
Sparsity: (1 - non-zero/total) × 100%
  0% sparsity → All basis states occupied
  99% sparsity → Only 1 state occupied (sparse)
```

#### Dominant State
```
The most probable basis state
Useful for verification and debugging
```

#### Measurement Statistics
```
States for 90% probability: n
States for 99% probability: m
  Tells you how many measurement outcomes are likely
  Small numbers → concentrated distribution
  Large numbers → spread distribution
```

---

## Use Cases & Examples

### Case 1: Verify |0⟩ Preparation
**Expected Results:**
- Amplitudes tab: Only |00...0⟩ = 1.0
- Prob. Chart: Single bar at 100%
- Statistics: Entropy = 0, Purity = 1.0
- Bloch Sphere: Vector at north pole

### Case 2: Create Equal Superposition
**Run:** H gates on all qubits
**Expected Results:**
- Amplitudes tab: All basis states with equal amplitude 1/√2ⁿ
- Prob. Chart: Flat distribution (all bars equal height)
- Statistics: Entropy = n bits, Sparsity = 0%
- Phase Plot: All bars same color (0 phase)

### Case 3: Create Entangled State (Bell Pair)
**Run:** H on qubit 0, CNOT(0,1)
**Expected Results:**
- Amplitudes tab: |00⟩ + |11⟩ only
- Prob. Chart: Two bars at 50% each
- Bloch Sphere (Q0): Mixed phase (equatorial)
- Bloch Sphere (Q1): Entangled with Q0
- Statistics: Entropy = 1 bit

### Case 4: Create Phase Superposition
**Run:** H → RZ(π/4)
**Expected Results:**
- Phase Plot: Both bars present but different colors
- Amplitudes tab: Different phases visible (±0.707e^(iπ/8))
- Bloch Sphere: Off the equator due to phase

---

## Tips & Tricks

### 📊 Probability Chart Tips
- Use **threshold** to focus on significant outcomes
- **Log scale** makes it easier to see small probabilities
- Compare before/after circuit changes by toggling tabs

### 🌐 Bloch Sphere Tips
- Click **Qubit selector** to inspect individual qubits
- For multi-qubit systems, each qubit has its own view
- Positions on sphere indicate:
  - **North pole** = |0⟩ (p₀=1.0)
  - **South pole** = |1⟩ (p₁=1.0)
  - **Equator** = Superposition (p₀=p₁=0.5)

### 🌈 Phase Plot Tips
- **Red bars** indicate zero phase (constructive)
- **Cyan bars** indicate π phase (destructive)
- Mixed colors show quantum interference effects
- Useful for debugging phase-sensitive gates (S, T, RZ)

### 📈 Statistics Tips
- **Entropy = 0** means state is deterministic ✓
- **Entropy = n** means uniform superposition  
- **Purity < 1** indicates decoherence or mixed states
- **Sparsity** helps identify sparse vs dense states

---

## Keyboard Shortcuts
- **Ctrl+Tab** - Next visualization tab
- **Ctrl+Shift+Tab** - Previous visualization tab

## Performance Notes

| System Size | Chart Performance | Bloch Sphere | Update Speed |
|-------------|------------------|--------------|--------------|
| 1-4 qubits  | Instant          | Instant      | <10ms        |
| 5-8 qubits  | Fast             | Fast         | <50ms        |
| 9-12 qubits | Good             | Good         | <200ms       |
| 13+ qubits  | Use log scale    | N/A          | <500ms       |

---

## Troubleshooting

**Q: Bloch Sphere shows all zeros**
A: You're viewing a superposition state. Multi-qubit systems require partial trace.

**Q: Probability Chart is hard to read**
A: Try the log scale option, especially for >8 qubits or >256 states.

**Q: All bars in Phase Plot same color**
A: Your state has no relative phase differences (real amplitudes only).

**Q: Entropy seems wrong**
A: Check that your state is normalized (total probability ≈ 1.0).

---

## Mathematical Background

### Bloch Sphere
For single-qubit state |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩

- **θ** (theta): Polar angle from north pole (0 to π)
- **φ** (phi): Azimuthal angle in xy-plane (0 to 2π)

### Von Neumann Entropy
H = -Σᵢ pᵢ log₂(pᵢ)

Measures uncertainty. Range [0, log₂(d)] where d is Hilbert space dimension.

### Purity
P = Σᵢ pᵢ² = Tr(ρ²)

Indicates how pure the state is. Pure states: P=1, Maximally mixed: P=1/d.

---

## Learn More

- **Quantum Superposition** → See Amplitude & Phase tabs
- **Quantum Entanglement** → Use Bloch Sphere for individual qubits
- **Quantum Interference** → Study Phase Plot colors
- **Quantum Measurement** → Check Probability Chart & Statistics

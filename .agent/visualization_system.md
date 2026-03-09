# Visualization System

Detailed reference for the state display / visualization subsystem.

---

## Architecture

```
StateDisplay (state_display.py)
│   Listens to: AppState.system_changed
│   Calls: update_display(system) on all tab widgets
│
├── Tab 1: Amplitudes       (QTextEdit, plain text)
├── Tab 2: Probabilities    (QTextEdit, plain text)
├── Tab 3: Details          (QTextEdit, plain text)
├── Tab 4: Prob. Chart      → ProbabilityChartWidget
├── Tab 5: Bloch Sphere     → BlochSphereWidget
├── Tab 6: Phase Plot       → StateVectorPhaseWidget
└── Tab 7: Statistics       → EnhancedStatisticsWidget

visualization_widgets.py
    ProbabilityChartWidget      (matplotlib FigureCanvasQTAgg)
    BlochSphereWidget           (matplotlib 3D axes)
    StateVectorPhaseWidget      (matplotlib + HSL coloring)
    EnhancedStatisticsWidget    (QLabel / QTextEdit)

visualization_utils.py
    (pure functions, no Qt, no Qiskit)
    All utilities that transform System → display data
```

---

## `visualization_utils.py` — Function Reference

### Density Matrix / Bloch Sphere

```python
partial_trace(statevector: np.ndarray, keep_qubit: int, n_qubits: int) -> np.ndarray
```
Returns the 2×2 reduced density matrix for `keep_qubit` by tracing out all other qubits.

```python
get_single_qubit_state(statevector, qubit_index, n_qubits) -> np.ndarray
```
Convenience wrapper around `partial_trace`. Returns 2×2 density matrix.

```python
density_matrix_to_bloch_vector(rho: np.ndarray) -> tuple[float, float, float]
```
Maps 2×2 density matrix to Bloch vector (x, y, z) using Pauli decomposition:
- x = Tr(ρ σ_x), y = Tr(ρ σ_y), z = Tr(ρ σ_z)

```python
bloch_vector_to_angles(bv: tuple) -> tuple[float, float]
```
Returns (θ, φ) in radians:
- θ ∈ [0, π]: polar angle from north pole
- φ ∈ [0, 2π]: azimuthal angle

### Data Extraction

```python
get_probability_data(system: System) -> list[tuple[str, float]]
```
Returns sorted list of (basis_state_label, probability), e.g. `[("00", 0.5), ("11", 0.5)]`.

```python
get_amplitude_data(system: System) -> list[tuple[str, float, float]]
```
Returns list of (label, magnitude, phase_radians) for each non-zero amplitude.

### Statistical Measures

```python
calculate_entropy(probs: dict | list) -> float
```
Von Neumann entropy H = −Σ pᵢ log₂(pᵢ) in bits. Returns 0 for pure deterministic states, log₂(2ⁿ) for maximally mixed.

```python
calculate_purity(statevector: np.ndarray) -> float
```
Purity P = Tr(ρ²). For pure states: P = 1.0. For fully mixed states: P = 1/d.

### Utilities

```python
phase_to_color(phase: float) -> tuple[float, float, float]
```
Maps phase angle (radians) → RGB via HSL. Convention:
- 0 rad → red
- π/2 → yellow
- π → cyan
- 3π/2 → blue

```python
filter_probabilities(prob_data: list, threshold: float) -> list
```
Removes entries with probability below `threshold` (0.0–1.0).

```python
get_statistics_text(system: System) -> str
```
Returns formatted multi-line string with entropy, purity, sparsity, dominant state, etc.

---

## `visualization_widgets.py` — Widget Reference

### `ProbabilityChartWidget`

Matplotlib bar chart embedded in PyQt6.

**Controls exposed to user:**
- Threshold slider (0–10%): hides states below threshold
- Log scale toggle
- Bars sorted by probability (descending by default)
- Probability percentage shown on each bar

**Key method**: `update_display(system: System)` — re-draws entire chart.

---

### `BlochSphereWidget`

3D Bloch sphere using `matplotlib` `Axes3D`.

**Controls:**
- Qubit selector dropdown (for multi-qubit systems — traces out other qubits)

**Rendering:**
- Sphere wireframe
- X/Y/Z axis arrows (red/green/blue)
- State vector arrow (black)
- Coordinate display: θ, φ in radians

**Interpretation guide:**
| State | θ | φ |
|-------|---|---|
| \|0⟩ | 0 | — |
| \|1⟩ | π | — |
| (\|0⟩+\|1⟩)/√2 | π/2 | 0 |
| (\|0⟩+i\|1⟩)/√2 | π/2 | π/2 |

**Key method**: `update_display(system: System)` — recomputes Bloch vector and redraws.

---

### `StateVectorPhaseWidget`

Bar chart where:
- **Height** = amplitude magnitude |α|
- **Color** = phase angle (HSL hue, via `phase_to_color`)

Bars sorted by magnitude (largest first). Shows interference patterns visually.

**Key method**: `update_display(system: System)`

---

### `EnhancedStatisticsWidget`

QLabel / rich-text display showing:
- Von Neumann entropy (bits + ratio to maximum)
- Purity (scalar + "pure"/"mixed" classification)
- Probability distribution stats (total states, non-zero, sparsity %)
- Dominant state (most probable basis state + its probability)
- Measurement statistics (states needed to cover 90% / 99% probability)

**Key method**: `update_display(system: System)`

---

## Updating / Extending Visualizations

### Add a new visual tab

1. Create a widget class in `visualization_widgets.py` with an `update_display(system)` method
2. In `state_display.py`, instantiate the widget and add it as a tab:
   ```python
   self.my_widget = MyWidget()
   self.tab_widget.addTab(self.my_widget, "My Tab")
   ```
3. In `StateDisplay.refresh()`, call `self.my_widget.update_display(self.system)`

### Modify an existing chart

All charts follow the pattern:
```python
self.figure.clear()
ax = self.figure.add_subplot(...)
# ... draw ...
self.canvas.draw()
```
Just edit the drawing logic inside `update_display()` directly. No signals involved.

---

## Performance Notes

| System size | Rendering behavior |
|-------------|-------------------|
| ≤ 8 qubits (≤256 states) | Real-time, all tabs smooth |
| 9–12 qubits (512–4096 states) | Fast with threshold filtering on Prob. Chart |
| > 12 qubits (>4096 states) | Use log scale; Bloch sphere may slow (partial trace still fast) |

Bloch sphere partial trace is O(2ⁿ) but fast in practice up to ~15 qubits.
Matplotlib redraws are the main bottleneck for large systems — consider caching `figure` objects if needed.

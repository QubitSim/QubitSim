"""
Quantum State Visualization Widgets

Provides visual representations of quantum states:
- ProbabilityChartWidget: Bar chart of measurement probabilities
- BlochSphereWidget: 3D Bloch sphere visualization
- StateVectorPhaseWidget: Polar plot of amplitudes with phase coloring
- EnhancedStatisticsWidget: Statistics panel with analysis
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QSpinBox,
    QCheckBox, QTextEdit, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import mpl_toolkits.mplot3d.axes3d as p3

from ui.visualization_utils import (
    get_single_qubit_state,
    get_probability_data,
    get_amplitude_data,
    density_matrix_to_bloch_vector,
    bloch_vector_to_angles,
    phase_to_color,
    calculate_entropy,
    calculate_purity,
    filter_probabilities,
    get_cumulative_probability,
    get_statistics_text
)


EPS = 1e-10


class ProbabilityChartWidget(QWidget):
    """
    Display measurement probabilities as interactive bar chart.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = None
        self.num_qubits = 0
        self.threshold = 0.01  # 1% minimum to display
        
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        controls_layout.addWidget(QLabel("Threshold (%)"))
        self.threshold_spin = QSpinBox()
        self.threshold_spin.setMinimum(0)
        self.threshold_spin.setMaximum(10)
        self.threshold_spin.setValue(1)
        self.threshold_spin.valueChanged.connect(self._on_threshold_changed)
        controls_layout.addWidget(self.threshold_spin)
        
        self.log_scale_check = QCheckBox("Log Scale")
        self.log_scale_check.stateChanged.connect(self._on_log_scale_changed)
        controls_layout.addWidget(self.log_scale_check)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Canvas
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def update_state(self, state: np.ndarray, num_qubits: int):
        """Update chart with new state."""
        self.state = state
        self.num_qubits = num_qubits
        self._render_chart()

    def _render_chart(self):
        if self.state is None:
            self.figure.clear()
            self.canvas.draw()
            return

        # Get probability data
        labels, probs = get_probability_data(self.state, self.num_qubits)
        
        # Apply threshold filter
        threshold = self.threshold_spin.value() / 100.0
        labels, probs = filter_probabilities(labels, probs, threshold)
        
        if not labels:
            self.figure.clear()
            self.canvas.draw()
            return

        # Create chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Color bars by probability (brighter = higher probability)
        colors = plt.cm.Blues(np.linspace(0.5, 1.0, len(probs)))
        
        bars = ax.bar(range(len(labels)), probs, color=colors, edgecolor='black', linewidth=0.5)
        
        # Add probability values on top of bars
        for i, (bar, prob) in enumerate(zip(bars, probs)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{prob*100:.1f}%',
                   ha='center', va='bottom', fontsize=9)
        
        # Apply log scale if selected
        if self.log_scale_check.isChecked():
            ax.set_yscale('log')
            ax.set_ylabel('Probability (log scale)')
        else:
            ax.set_ylabel('Probability')
        
        ax.set_xlabel('Quantum State')
        ax.set_title('Measurement Probability Distribution')
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
        
        self.figure.tight_layout()
        self.canvas.draw()

    def _on_threshold_changed(self):
        self._render_chart()

    def _on_log_scale_changed(self):
        self._render_chart()


class Arrow3D(FancyArrowPatch):
    """3D Arrow for Bloch sphere visualization."""
    
    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = [x, y, z]
        self._dxdydz = [dx, dy, dz]

    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        
        xs = [x1, x1+dx]
        ys = [y1, y1+dy]
        zs = [z1, z1+dz]

        xs, ys = proj3d.proj_transform(xs, ys, zs, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        
        super().draw(renderer)


class BlochSphereWidget(QWidget):
    """
    Display single-qubit state on Bloch sphere.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = None
        self.num_qubits = 0
        self.selected_qubit = 0
        
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Qubit selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Qubit:"))
        self.qubit_combo = QComboBox()
        self.qubit_combo.currentIndexChanged.connect(self._on_qubit_selected)
        selector_layout.addWidget(self.qubit_combo)
        selector_layout.addStretch()
        layout.addLayout(selector_layout)
        
        # Coordinates display
        self.coords_label = QLabel("θ: -- rad  φ: -- rad")
        self.coords_label.setFont(QFont("Courier", 10))
        layout.addWidget(self.coords_label)
        
        # Canvas
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def update_state(self, state: np.ndarray, num_qubits: int):
        """Update Bloch sphere with new state."""
        self.state = state
        self.num_qubits = num_qubits
        
        # Update qubit selector
        self.qubit_combo.blockSignals(True)
        self.qubit_combo.clear()
        for i in range(num_qubits):
            self.qubit_combo.addItem(f"Q{i}")
        self.qubit_combo.blockSignals(False)
        
        self._render_sphere()

    def _render_sphere(self):
        if self.state is None:
            self.figure.clear()
            self.canvas.draw()
            return

        # Get single-qubit state
        try:
            rho = get_single_qubit_state(self.state, self.selected_qubit, self.num_qubits)
        except:
            self.figure.clear()
            self.canvas.draw()
            return

        # Convert to Bloch vector
        x, y, z = density_matrix_to_bloch_vector(rho)
        theta, phi = bloch_vector_to_angles(x, y, z)
        
        # Update coordinates display
        self.coords_label.setText(f"θ: {theta:.4f} rad  φ: {phi:.4f} rad")

        # Create 3D plot
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')

        # Draw Bloch sphere
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        sphere_x = np.outer(np.cos(u), np.sin(v))
        sphere_y = np.outer(np.sin(u), np.sin(v))
        sphere_z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        ax.plot_surface(sphere_x, sphere_y, sphere_z, alpha=0.1, color='cyan')

        # Draw axes
        axis_length = 1.2
        ax.quiver(0, 0, 0, axis_length, 0, 0, color='red', arrow_length_ratio=0.1, linewidth=2, label='X')
        ax.quiver(0, 0, 0, 0, axis_length, 0, color='green', arrow_length_ratio=0.1, linewidth=2, label='Y')
        ax.quiver(0, 0, 0, 0, 0, axis_length, color='blue', arrow_length_ratio=0.1, linewidth=2, label='Z')

        # Draw state vector
        magnitude = np.sqrt(x**2 + y**2 + z**2)
        if magnitude > EPS:
            ax.quiver(0, 0, 0, x, y, z, color='black', arrow_length_ratio=0.15, linewidth=3, label='State')

        # Labels and formatting
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim([-1.5, 1.5])
        ax.set_ylim([-1.5, 1.5])
        ax.set_zlim([-1.5, 1.5])
        ax.set_title(f'Bloch Sphere - Qubit {self.selected_qubit}')

        self.figure.tight_layout()
        self.canvas.draw()

    def _on_qubit_selected(self, index):
        self.selected_qubit = index
        self._render_sphere()


class StateVectorPhaseWidget(QWidget):
    """
    Visualize state vector amplitudes with phase coloring.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = None
        self.num_qubits = 0
        
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Info
        info_label = QLabel("Amplitude magnitudes with phase color coding (0=red, π=cyan, 2π=red)")
        info_label.setFont(QFont("Arial", 9))
        info_label.setStyleSheet("color: gray;")
        layout.addWidget(info_label)
        
        # Canvas
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def update_state(self, state: np.ndarray, num_qubits: int):
        """Update phase visualization with new state."""
        self.state = state
        self.num_qubits = num_qubits
        self._render_chart()

    def _render_chart(self):
        if self.state is None:
            self.figure.clear()
            self.canvas.draw()
            return

        # Get amplitude data
        labels, magnitudes, phases = get_amplitude_data(self.state, self.num_qubits)
        
        if not labels:
            self.figure.clear()
            self.canvas.draw()
            return

        # Create polar-like visualization
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Color bars by phase
        colors = [phase_to_color(phase) for phase in phases]
        
        bars = ax.bar(range(len(labels)), magnitudes, color=colors, edgecolor='black', linewidth=0.5)
        
        # Add magnitude values on top
        for i, (bar, mag) in enumerate(zip(bars, magnitudes)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{mag:.2f}',
                   ha='center', va='bottom', fontsize=8)
        
        ax.set_xlabel('Quantum State')
        ax.set_ylabel('Amplitude Magnitude')
        ax.set_title('State Vector Amplitudes (colored by phase)')
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
        ax.set_ylim([0, max(magnitudes) * 1.1])
        
        # Add phase legend
        phase_text = "Phase (angle → color):\n0 → Red\nπ/2 → Yellow\nπ → Cyan\n3π/2 → Blue"
        ax.text(0.98, 0.97, phase_text, transform=ax.transAxes,
               fontsize=8, verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        self.figure.tight_layout()
        self.canvas.draw()


class EnhancedStatisticsWidget(QWidget):
    """
    Display quantum state statistics and analysis.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = None
        self.num_qubits = 0
        
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Statistics display
        self.stats_text = QTextEdit(readOnly=True)
        self.stats_text.setFont(QFont("Courier", 10))
        layout.addWidget(self.stats_text)

    def update_state(self, state: np.ndarray, num_qubits: int):
        """Update statistics with new state."""
        self.state = state
        self.num_qubits = num_qubits
        self._update_display()

    def _update_display(self):
        if self.state is None:
            self.stats_text.setPlainText("No state to display")
            return

        probs = np.abs(self.state[:, 0]) ** 2
        
        # Statistics
        entropy = calculate_entropy(self.state)
        purity = calculate_purity(self.state)
        non_zero = np.sum(probs > EPS)
        
        # Find dominant state
        max_idx = np.argmax(probs)
        dominant_prob = probs[max_idx]
        dominant_state = format(max_idx, f"0{self.num_qubits}b")
        
        # Calculate cumulative probability for 90% threshold
        sorted_probs = np.sort(probs)[::-1]
        cumsum = np.cumsum(sorted_probs)
        n_for_90 = np.searchsorted(cumsum, 0.9) + 1
        
        text = f"""
═══ QUANTUM STATE STATISTICS ═══

ENTROPY ANALYSIS:
  Von Neumann Entropy: {entropy:.6f} bits
  Max possible entropy: {np.log2(len(probs)):.4f} bits
  Entropy ratio: {entropy / np.log2(len(probs)):.4f}

PURITY ANALYSIS:
  Purity (Tr(ρ²)): {purity:.6f}
  State type: {'Pure' if purity > 0.99 else 'Mixed'}

PROBABILITY DISTRIBUTION:
  Total states: {len(probs)}
  Non-zero amplitudes: {non_zero}
  Sparsity: {(1 - non_zero/len(probs))*100:.1f}%

DOMINANT STATE:
  State: |{dominant_state}⟩
  Probability: {dominant_prob*100:.4f}%

MEASUREMENT STATISTICS:
  States for 90% probability: {n_for_90}
  States for 99% probability: {np.searchsorted(cumsum, 0.99) + 1}
  
═════════════════════════════════
"""
        
        self.stats_text.setPlainText(text.strip())

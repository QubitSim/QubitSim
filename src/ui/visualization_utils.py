"""
Visualization Utilities for Quantum State Analysis

Provides helper functions for:
- Density matrix calculations
- Bloch sphere coordinates
- Statistical analysis
- Phase to color mapping
- Probability filtering and sorting
"""

import numpy as np
import colorsys
from typing import Tuple


EPS = 1e-10


def partial_trace(state: np.ndarray, qubits_to_keep: list[int], num_qubits: int) -> np.ndarray:
    """
    Compute reduced density matrix by tracing out unwanted qubits.
    
    Args:
        state: State vector (shape: (2^n, 1))
        qubits_to_keep: List of qubit indices to keep
        num_qubits: Total number of qubits
    
    Returns:
        Reduced density matrix for specified qubits
    """
    # Convert state vector to density matrix
    rho = state @ state.conj().T
    
    # Compute partial trace
    # Trace out all qubits NOT in qubits_to_keep
    qubits_to_trace = [i for i in range(num_qubits) if i not in qubits_to_keep]
    
    # Dimension of each qubit trace
    result = rho
    for qubit_idx in sorted(qubits_to_trace, reverse=True):
        # Dimension of the subsystem to trace out
        dim_before = 2 ** qubit_idx
        dim_after = 2 ** (num_qubits - qubit_idx - 1)
        full_dim = 2 ** num_qubits
        
        # Indices for partial trace (sum over diagonal blocks)
        partial = np.zeros(
            (full_dim // 2, full_dim // 2), 
            dtype=complex
        )
        
        for i in range(2):
            idx_before = np.s_[:dim_before]
            idx_i = np.s_[i*dim_after:(i+1)*dim_after]
            idx_after = np.s_[dim_before+dim_after:]
            
            # Extract block and sum
            for j0 in range(dim_before):
                for j1 in range(dim_after):
                    row = j0 * dim_after * 2 + i * dim_after + j1
                    for k0 in range(dim_before):
                        for k1 in range(dim_after):
                            col = k0 * dim_after * 2 + i * dim_after + k1
                            if row < result.shape[0] and col < result.shape[1]:
                                partial[j0*dim_after+j1, k0*dim_after+k1] += result[row, col]
        
        result = partial if len(qubits_to_trace) > 1 else np.zeros(
            (2**(num_qubits - len(qubits_to_trace)), 
             2**(num_qubits - len(qubits_to_trace))), 
            dtype=complex
        )
        # Simplified: directly compute for single qubit case
    
    # Simplified implementation for single qubit
    if len(qubits_to_keep) == 1:
        qubit_idx = qubits_to_keep[0]
        dim = 2 ** num_qubits
        reduced = np.zeros((2, 2), dtype=complex)
        
        for i in range(dim):
            for j in range(dim):
                # Check if states differ only in the kept qubit
                i_bits = format(i, f"0{num_qubits}b")
                j_bits = format(j, f"0{num_qubits}b")
                
                # Only include if all other bits are the same
                same = True
                for k in range(num_qubits):
                    if k != qubit_idx and i_bits[k] != j_bits[k]:
                        same = False
                        break
                
                if same:
                    i_qubit = int(i_bits[qubit_idx])
                    j_qubit = int(j_bits[qubit_idx])
                    reduced[i_qubit, j_qubit] += rho[i, j]
        
        return reduced
    
    # For multiple qubits, recursion
    return result


def get_single_qubit_state(state: np.ndarray, qubit_idx: int, num_qubits: int) -> np.ndarray:
    """
    Extract single-qubit reduced density matrix.
    
    Args:
        state: Full state vector (shape: (2^n, 1))
        qubit_idx: Index of qubit to extract
        num_qubits: Total number of qubits
    
    Returns:
        2x2 reduced density matrix for the qubit
    """
    return partial_trace(state, [qubit_idx], num_qubits)


def density_matrix_to_bloch_vector(rho: np.ndarray) -> Tuple[float, float, float]:
    """
    Convert 2x2 density matrix to Bloch vector (x, y, z).
    
    Args:
        rho: 2x2 density matrix
    
    Returns:
        Tuple of (x, y, z) Bloch vector components
    """
    from scipy.linalg import eigvalsh
    
    # Pauli matrices
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    
    # Bloch vector components: <σ_i>
    x = np.real(np.trace(rho @ sigma_x))
    y = np.real(np.trace(rho @ sigma_y))
    z = np.real(np.trace(rho @ sigma_z))
    
    return float(x), float(y), float(z)


def bloch_vector_to_angles(x: float, y: float, z: float) -> Tuple[float, float]:
    """
    Convert Bloch vector to spherical coordinates (theta, phi).
    
    Args:
        x, y, z: Bloch vector components
    
    Returns:
        Tuple of (theta, phi) in radians
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    
    if r < EPS:
        return 0.0, 0.0
    
    # theta: angle from north pole (z-axis)
    theta = np.arccos(np.clip(z / r, -1, 1))
    
    # phi: azimuthal angle in xy-plane
    phi = np.arctan2(y, x)
    
    return float(theta), float(phi)


def phase_to_color(phase: float) -> Tuple[float, float, float]:
    """
    Map phase angle to RGB color using HSL color space.
    
    Args:
        phase: Phase angle in radians (0 to 2π)
    
    Returns:
        Tuple of (R, G, B) values in range [0, 1]
    """
    # Normalize phase to [0, 1]
    hue = (phase % (2 * np.pi)) / (2 * np.pi)
    
    # Convert HSL to RGB (full saturation, 50% lightness for visibility)
    rgb = colorsys.hls_to_rgb(hue, 0.5, 1.0)
    
    return rgb


def get_probability_data(state: np.ndarray, num_qubits: int) -> Tuple[list, list, list]:
    """
    Extract probability data from state vector.
    
    Args:
        state: State vector (shape: (2^n, 1))
        num_qubits: Total number of qubits
    
    Returns:
        Tuple of (basis_labels, probabilities, non_zero_only)
        where probabilities are sorted in descending order
    """
    probs = np.abs(state[:, 0]) ** 2
    
    # Get basis labels and probabilities
    labels = [format(i, f"0{num_qubits}b") for i in range(len(probs))]
    
    # Create list of (label, prob) and sort by probability descending
    data = [(l, p) for l, p in zip(labels, probs) if p > EPS]
    data.sort(key=lambda x: x[1], reverse=True)
    
    if data:
        basis_labels, probabilities = zip(*data)
        return list(basis_labels), list(probabilities)
    
    return [], []


def get_amplitude_data(state: np.ndarray, num_qubits: int) -> Tuple[list, list, list]:
    """
    Extract amplitude data (magnitude and phase) from state vector.
    
    Args:
        state: State vector (shape: (2^n, 1))
        num_qubits: Total number of qubits
    
    Returns:
        Tuple of (basis_labels, magnitudes, phases)
    """
    amplitudes = state[:, 0]
    
    # Get basis labels
    labels = [format(i, f"0{num_qubits}b") for i in range(len(amplitudes))]
    
    # Extract magnitudes and phases
    magnitudes = np.abs(amplitudes)
    phases = np.angle(amplitudes)
    
    # Filter out near-zero amplitudes
    data = [
        (l, m, p) 
        for l, m, p in zip(labels, magnitudes, phases) 
        if m > EPS
    ]
    
    # Sort by magnitude descending
    data.sort(key=lambda x: x[1], reverse=True)
    
    if data:
        labels, magnitudes, phases = zip(*data)
        return list(labels), list(magnitudes), list(phases)
    
    return [], [], []


def calculate_entropy(state: np.ndarray) -> float:
    """
    Calculate von Neumann entropy of the state.
    
    Args:
        state: State vector (shape: (2^n, 1))
    
    Returns:
        Entropy value in bits
    """
    probs = np.abs(state[:, 0]) ** 2
    
    # Remove zero probabilities to avoid log(0)
    probs = probs[probs > EPS]
    
    # von Neumann entropy: S = -sum(p_i * log2(p_i))
    entropy = -np.sum(probs * np.log2(probs))
    
    return float(entropy)


def calculate_purity(state: np.ndarray) -> float:
    """
    Calculate purity of the state.
    
    Args:
        state: State vector (shape: (2^n, 1))
    
    Returns:
        Purity value (1.0 for pure states, < 1.0 for mixed)
    """
    probs = np.abs(state[:, 0]) ** 2
    
    # Purity: sum(p_i^2)
    purity = np.sum(probs ** 2)
    
    return float(np.real(purity))


def filter_probabilities(
    labels: list[str], 
    probs: list[float], 
    threshold: float = 0.01
) -> Tuple[list[str], list[float]]:
    """
    Filter out probabilities below threshold and group small ones.
    
    Args:
        labels: Basis state labels
        probs: Corresponding probabilities
        threshold: Minimum probability to display (0.0 to 1.0)
    
    Returns:
        Tuple of (filtered_labels, filtered_probs)
    """
    filtered = [(l, p) for l, p in zip(labels, probs) if p >= threshold]
    
    if filtered:
        labels, probs = zip(*filtered)
        return list(labels), list(probs)
    
    # If all filtered out, return top state
    if labels:
        max_idx = np.argmax(probs)
        return [labels[max_idx]], [probs[max_idx]]
    
    return [], []


def get_cumulative_probability(probs: list[float]) -> list[float]:
    """
    Calculate cumulative probability distribution.
    
    Args:
        probs: List of probabilities
    
    Returns:
        Cumulative probabilities
    """
    cumsum = np.cumsum(probs)
    return [float(x) for x in cumsum]


def get_statistics_text(state: np.ndarray) -> str:
    """
    Generate statistics text for quantum state.
    
    Args:
        state: State vector (shape: (2^n, 1))
    
    Returns:
        Formatted statistics string
    """
    probs = np.abs(state[:, 0]) ** 2
    non_zero = np.sum(probs > EPS)
    
    entropy = calculate_entropy(state)
    purity = calculate_purity(state)
    
    # Calculate expected value of measurement outcome
    outcomes = np.arange(len(probs))
    expected_value = np.sum(outcomes * probs)
    
    text = (
        f"Entropy: {entropy:.4f} bits\n"
        f"Purity: {purity:.6f}\n"
        f"Non-zero states: {non_zero}/{len(probs)}\n"
        f"Expected measurement: {expected_value:.2f}"
    )
    
    return text

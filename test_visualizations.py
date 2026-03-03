#!/usr/bin/env python3
"""
Test script for visualization utilities and widgets.
Validates core functionality without GUI rendering.
"""

import sys
sys.path.insert(0, 'src')

import numpy as np
from ui.visualization_utils import (
    partial_trace,
    get_single_qubit_state,
    density_matrix_to_bloch_vector,
    bloch_vector_to_angles,
    phase_to_color,
    get_probability_data,
    get_amplitude_data,
    calculate_entropy,
    calculate_purity,
    filter_probabilities,
    get_statistics_text
)


def test_single_qubit_state():
    """Test extraction of single-qubit state."""
    # Create a simple 2-qubit state |00⟩
    state = np.array([[1.0, 0, 0, 0]]).T
    
    rho = get_single_qubit_state(state, 0, 2)
    assert rho.shape == (2, 2), f"Expected shape (2, 2), got {rho.shape}"
    print("✓ Single-qubit state extraction")


def test_bloch_vector():
    """Test Bloch vector calculations."""
    # |0⟩ state
    state = np.array([[1.0, 0]]).T
    rho = state @ state.conj().T
    
    x, y, z = density_matrix_to_bloch_vector(rho)
    assert abs(z - 1.0) < 1e-6, f"Expected z≈1 for |0⟩ state, got {z}"
    
    theta, phi = bloch_vector_to_angles(x, y, z)
    assert abs(theta) < 1e-6, f"Expected θ≈0 for |0⟩ state, got {theta}"
    print("✓ Bloch vector calculations")


def test_phase_coloring():
    """Test phase to color mapping."""
    # Test a few phases
    for phase in [0, np.pi/2, np.pi, 3*np.pi/2]:
        r, g, b = phase_to_color(phase)
        assert 0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1
        assert (r, g, b) != (0, 0, 0), "Color should not be black"
    print("✓ Phase to color mapping")


def test_probability_extraction():
    """Test probability data extraction."""
    # Create equal superposition |00⟩ + |11⟩ (normalized)
    state = np.array([[1/np.sqrt(2), 0, 0, 1/np.sqrt(2)]]).T
    
    labels, probs = get_probability_data(state, 2)
    assert len(labels) == 2, f"Expected 2 states, got {len(labels)}"
    assert abs(probs[0] - 0.5) < 1e-6, f"Expected probability 0.5, got {probs[0]}"
    print("✓ Probability extraction")


def test_amplitude_extraction():
    """Test amplitude data extraction."""
    # Create a state with amplitudes 0.6 and 0.8 (normalized)
    state = np.array([[0.6, 0, 0.8, 0]]).T
    
    labels, mags, phases = get_amplitude_data(state, 2)
    assert len(labels) == 2, f"Expected 2 amplitudes, got {len(labels)}"
    assert abs(mags[0] - 0.8) < 1e-6, f"Expected max magnitude 0.8, got {mags[0]}"
    print("✓ Amplitude extraction")


def test_entropy():
    """Test entropy calculation."""
    # Uniform superposition: maximum entropy
    n = 2
    state = np.ones((2**n, 1), dtype=complex) / np.sqrt(2**n)
    entropy = calculate_entropy(state)
    max_entropy = np.log2(2**n)
    assert abs(entropy - max_entropy) < 1e-6, f"Expected max entropy {max_entropy}, got {entropy}"
    
    # Pure state |0⟩: zero entropy
    state = np.zeros((4, 1), dtype=complex)
    state[0, 0] = 1.0
    entropy = calculate_entropy(state)
    assert entropy < 1e-6, f"Expected entropy ≈0 for pure state, got {entropy}"
    print("✓ Entropy calculation")


def test_purity():
    """Test purity calculation."""
    # Pure state: purity = 1
    state = np.zeros((4, 1), dtype=complex)
    state[0, 0] = 1.0
    purity = calculate_purity(state)
    assert abs(purity - 1.0) < 1e-6, f"Expected purity=1 for pure state, got {purity}"
    print("✓ Purity calculation")


def test_probability_filtering():
    """Test probability filtering."""
    labels = ['00', '01', '10', '11']
    probs = [0.7, 0.2, 0.08, 0.02]
    
    filtered_labels, filtered_probs = filter_probabilities(labels, probs, 0.1)
    assert len(filtered_labels) == 2, f"Expected 2 states after filtering, got {len(filtered_labels)}"
    print("✓ Probability filtering")


def test_statistics_text():
    """Test statistics text generation."""
    # Create simple state
    state = np.zeros((4, 1), dtype=complex)
    state[0, 0] = 1.0
    
    text = get_statistics_text(state)
    assert "Entropy:" in text, "Statistics should contain Entropy"
    assert "Purity:" in text, "Statistics should contain Purity"
    print("✓ Statistics text generation")


if __name__ == "__main__":
    print("\nRunning visualization utilities tests...\n")
    
    test_single_qubit_state()
    test_bloch_vector()
    test_phase_coloring()
    test_probability_extraction()
    test_amplitude_extraction()
    test_entropy()
    test_purity()
    test_probability_filtering()
    test_statistics_text()
    
    print("\n✓ All tests passed!\n")

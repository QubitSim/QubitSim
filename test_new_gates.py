#!/usr/bin/env python3
"""
Test script for Plan 2: Missing Quantum Circuit Components
Tests all newly implemented gates and components.
"""

import sys
sys.path.insert(0, '/home/andresaugom/git/QubitSim/src')

from qcircuit.objects import GateOp, GATE_DISPATCH
from qcircuit.interpreter import CircuitInterpreter
from qcircuit.backend import QiskitBackend
import numpy as np

def test_basic_gates():
    """Test basic Pauli and phase gates."""
    print("\n=== Testing Basic Gates (S†, T†, I, U3) ===")
    
    gates_to_test = [
        ("Sdg", "S-dagger (S†)"),
        ("Tdg", "T-dagger (T†)"),
        ("I", "Identity (I)"),
    ]
    
    backend = QiskitBackend(2)
    
    for gate_name, description in gates_to_test:
        steps = [[GateOp(name=gate_name, targets=[0])]]
        try:
            result = backend.execute(steps)
            print(f"✓ {gate_name}: {description} - PASSED")
        except Exception as e:
            print(f"✗ {gate_name}: {description} - FAILED: {e}")
    
    # Test U3 with parameters
    U3_tests = [
        {"theta": np.pi/2, "phi": 0, "lam": 0},
        {"theta": np.pi/4, "phi": np.pi/2, "lam": np.pi/4},
    ]
    
    for params in U3_tests:
        steps = [[GateOp(name="U3", targets=[0], params=params)]]
        try:
            result = backend.execute(steps)
            print(f"✓ U3({params['theta']:.3f}, {params['phi']:.3f}, {params['lam']:.3f}) - PASSED")
        except Exception as e:
            print(f"✗ U3 with params - FAILED: {e}")

def test_advanced_gates():
    """Test advanced multi-qubit gates."""
    print("\n=== Testing Advanced Multi-Qubit Gates ===")
    
    backend = QiskitBackend(4)  # Need 4 qubits for Toffoli and X3
    
    # Test Toffoli (Fredkin)
    print("Testing Toffoli (CCNOT)...")
    steps = [[GateOp(name="Toffoli", targets=[2], controls=[0, 1])]]
    try:
        result = backend.execute(steps)
        print("✓ Toffoli - PASSED")
    except Exception as e:
        print(f"✗ Toffoli - FAILED: {e}")
    
    # Test Fredkin (CSWAP)
    print("Testing Fredkin (CSWAP)...")
    steps = [[GateOp(name="Fredkin", targets=[1, 2], controls=[0])]]
    try:
        result = backend.execute(steps)
        print("✓ Fredkin - PASSED")
    except Exception as e:
        print(f"✗ Fredkin - FAILED: {e}")
    
    # Test iSWAP
    print("Testing iSWAP...")
    steps = [[GateOp(name="iSWAP", targets=[0, 1])]]
    try:
        result = backend.execute(steps)
        print("✓ iSWAP - PASSED")
    except Exception as e:
        print(f"✗ iSWAP - FAILED: {e}")
    
    # Test 3-Control X
    print("Testing 3-Control X (CCCX)...")
    steps = [[GateOp(name="X3", targets=[3], controls=[0, 1, 2])]]
    try:
        result = backend.execute(steps)
        print("✓ 3-Control X - PASSED")
    except Exception as e:
        print(f"✗ 3-Control X - FAILED: {e}")

def test_algorithm_components():
    """Test algorithm components."""
    print("\n=== Testing Algorithm Components ===")
    
    backend = QiskitBackend(3)
    
    # Test Hadamard Layer
    print("Testing Hadamard Layer...")
    steps = [[GateOp(name="H_LAYER", targets=[0, 1, 2])]]
    try:
        result = backend.execute(steps)
        print("✓ Hadamard Layer - PASSED")
    except Exception as e:
        print(f"✗ Hadamard Layer - FAILED: {e}")
    
    # Test Grover Diffusion
    print("Testing Grover Diffusion...")
    steps = [[GateOp(name="GROVER_DIFFUSION", targets=[0, 1, 2])]]
    try:
        result = backend.execute(steps)
        print("✓ Grover Diffusion - PASSED")
    except Exception as e:
        print(f"✗ Grover Diffusion - FAILED: {e}")
    
    # Test QFT
    print("Testing QFT...")
    steps = [[GateOp(name="QFT", targets=[0, 1, 2])]]
    try:
        result = backend.execute(steps)
        print("✓ QFT - PASSED")
    except Exception as e:
        print(f"✗ QFT - FAILED: {e}")
    
    # Test QFT†
    print("Testing QFT†...")
    steps = [[GateOp(name="QFT_DAG", targets=[0, 1, 2])]]
    try:
        result = backend.execute(steps)
        print("✓ QFT† - PASSED")
    except Exception as e:
        print(f"✗ QFT† - FAILED: {e}")

def test_oracle_components():
    """Test oracle components."""
    print("\n=== Testing Oracle Components ===")
    
    backend = QiskitBackend(3)
    
    # Test Mark State Oracle
    print("Testing Mark State Oracle...")
    steps = [[GateOp(
        name="ORACLE_MARK_STATE", 
        targets=[0, 1, 2], 
        params={"state": "101"}
    )]]
    try:
        result = backend.execute(steps)
        print("✓ Mark State Oracle - PASSED")
    except Exception as e:
        print(f"✗ Mark State Oracle - FAILED: {e}")
    
    # Test Parity Oracle
    print("Testing Parity Oracle...")
    steps = [[GateOp(
        name="ORACLE_PARITY", 
        targets=[0, 1, 2], 
        params={"parity": "odd"}
    )]]
    try:
        result = backend.execute(steps)
        print("✓ Parity Oracle - PASSED")
    except Exception as e:
        print(f"✗ Parity Oracle - FAILED: {e}")
    
    # Test Phase Oracle
    print("Testing Phase Oracle...")
    steps = [[GateOp(
        name="ORACLE_PHASE", 
        targets=[0, 1, 2], 
        params={"angle": np.pi}
    )]]
    try:
        result = backend.execute(steps)
        print("✓ Phase Oracle - PASSED")
    except Exception as e:
        print(f"✗ Phase Oracle - FAILED: {e}")

def test_visualization_components():
    """Test barrier and label components."""
    print("\n=== Testing Visualization Components ===")
    
    backend = QiskitBackend(2)
    
    # Test Barrier
    print("Testing Barrier...")
    steps = [[GateOp(name="BARRIER", targets=[0, 1])]]
    try:
        result = backend.execute(steps)
        print("✓ Barrier - PASSED")
    except Exception as e:
        print(f"✗ Barrier - FAILED: {e}")
    
    # Test Label
    print("Testing Label...")
    steps = [[GateOp(name="LABEL", targets=[0], params={"text": "Test Label"})]]
    try:
        result = backend.execute(steps)
        print("✓ Label - PASSED")
    except Exception as e:
        print(f"✗ Label - FAILED: {e}")

def test_gate_dispatch():
    """Verify all gates are registered in GATE_DISPATCH."""
    print("\n=== Verifying Gate Dispatch Registration ===")
    
    expected_gates = [
        # Basic gates
        "H", "X", "Y", "Z", "S", "T", "Sdg", "Tdg", "I",
        # Rotation gates
        "RX", "RY", "RZ",
        # Parametrized gates
        "U3",
        # Multi-qubit gates
        "SWAP", "Toffoli", "CCNOT", "Fredkin", "CSWAP", "iSWAP", "X3", "CCCX",
        # Algorithm components
        "H_LAYER", "GROVER_DIFFUSION", "QFT", "QFT_DAG",
        # Oracle components
        "ORACLE_MARK_STATE", "ORACLE_PARITY", "ORACLE_PHASE",
        # Visualization
        "BARRIER", "LABEL",
        # Control
        "C", "AC",
    ]
    
    missing = []
    for gate in expected_gates:
        if gate not in GATE_DISPATCH:
            missing.append(gate)
            print(f"✗ {gate} - NOT FOUND in GATE_DISPATCH")
        else:
            print(f"✓ {gate} - registered")
    
    if missing:
        print(f"\nMissing gates: {missing}")
    else:
        print("\n✓ All gates registered successfully!")

def test_complete_circuit():
    """Test a complete circuit with various new gates."""
    print("\n=== Testing Complete Circuit ===")
    
    backend = QiskitBackend(3)
    
    # Build a circuit using new gates
    steps = [
        [GateOp(name="H_LAYER", targets=[0, 1, 2])],
        [GateOp(name="ORACLE_MARK_STATE", targets=[0, 1, 2], params={"state": "101"})],
        [GateOp(name="GROVER_DIFFUSION", targets=[0, 1, 2])],
        [GateOp(name="BARRIER", targets=[])],
        [GateOp(name="QFT", targets=[0, 1, 2])],
    ]
    
    try:
        result = backend.execute(steps)
        print("✓ Complete circuit with mixed gates - PASSED")
        print(f"  Final state probabilities: {list(result['probabilities'].items())[:3]}...")
    except Exception as e:
        print(f"✗ Complete circuit - FAILED: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Plan 2: Missing Quantum Circuit Components")
    print("=" * 60)
    
    test_gate_dispatch()
    test_basic_gates()
    test_advanced_gates()
    test_algorithm_components()
    test_oracle_components()
    test_visualization_components()
    test_complete_circuit()
    
    print("\n" + "=" * 60)
    print("Testing complete!")
    print("=" * 60)

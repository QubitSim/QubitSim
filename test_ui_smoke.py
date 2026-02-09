"""
Smoke test - Verify UI can be instantiated without errors
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_ui_instantiation():
    """Test that MainWindow can be created without errors"""
    print("Testing UI instantiation...")
    
    from PyQt6.QtWidgets import QApplication
    from ui.main_window import MainWindow
    from qcircuit.objects import GateOp
    
    # Create Qt application (required for widgets)
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    
    # Verify components exist
    assert window.app_state is not None
    assert window.circuit_canvas is not None
    assert window.state_display is not None
    assert window.control_panel is not None
    assert window.gate_palette is not None
    
    print("✓ MainWindow created successfully")
    
    # Test adding a gate
    window.app_state.add_gate(0, GateOp("H", targets=[0]))
    assert window.app_state.steps[0][0] is not None
    print("✓ Gate can be added to circuit")
    
    # Test stepping (should not crash)
    window.app_state.step()
    assert window.app_state.current_step == 1
    assert window.app_state.system is not None
    print("✓ Circuit execution works")
    
    # Test state display
    state = window.app_state.system.state[:, 0]
    assert len(state) == 2**window.app_state.num_qubits
    print("✓ Quantum state is available")
    
    print("\n✓ All UI smoke tests passed!")
    return True

if __name__ == "__main__":
    try:
        test_ui_instantiation()
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ UI smoke test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

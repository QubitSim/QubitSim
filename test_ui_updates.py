"""Test script to capture a screenshot of the updated UI"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("QubitSim")
    
    window = MainWindow()
    window.show()
    
    def take_screenshot():
        pixmap = window.grab()
        pixmap.save('/home/runner/work/QubitSim/QubitSim/screenshot_updated.png')
        print("Screenshot saved!")
        app.quit()
    
    QTimer.singleShot(500, take_screenshot)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

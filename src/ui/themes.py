"""
Theme definitions for QubitSim UI.

Provides light and dark theme color schemes with carefully selected palettes
for better visual hierarchy and accessibility.
"""

from dataclasses import dataclass


@dataclass
class Theme:
    """Color scheme for the application."""
    
    # Window and backgrounds
    window_bg: str
    panel_bg: str
    text_primary: str
    text_secondary: str
    border_color: str
    
    # Gate buttons
    gate_button_bg: str
    gate_button_border: str
    gate_button_hover: str
    gate_button_pressed: str
    
    # Control buttons
    control_button_bg: str
    control_button_border: str
    control_button_hover: str
    control_button_pressed: str
    
    # Canvas
    canvas_bg: str
    wire_color: str
    grid_color: str
    control_link_color: str
    qubit_label_color: str
    step_label_color: str
    step_indicator_color: str
    
    # State display
    state_display_title_bg: str
    text_edit_bg: str
    
    # Buttons (control panel)
    step_button_color: str
    run_button_color: str
    reset_button_color: str
    button_text_color: str


# Light Theme - Clean, professional appearance
LIGHT_THEME = Theme(
    # Window and backgrounds
    window_bg="#FFFFFF",
    panel_bg="#F5F5F5",
    text_primary="#1A1A1A",
    text_secondary="#545454",
    border_color="#CCCCCC",
    
    # Gate buttons (Blue palette)
    gate_button_bg="#D4E5FF",
    gate_button_border="#4A7FBF",
    gate_button_hover="#E8F0FF",
    gate_button_pressed="#B8D5FF",
    
    # Control buttons (Red/Coral palette)
    control_button_bg="#FFD9D9",
    control_button_border="#C84040",
    control_button_hover="#FFE8E8",
    control_button_pressed="#FFC4C4",
    
    # Canvas
    canvas_bg="#FFFFFF",
    wire_color="#2A2A2A",
    grid_color="#E0E0E0",
    control_link_color="#D9534F",
    qubit_label_color="#2A2A2A",
    step_label_color="#666666",
    step_indicator_color="#FFD54F",
    
    # State display
    state_display_title_bg="#F0F0F0",
    text_edit_bg="#FFFFFF",
    
    # Buttons (control panel)
    step_button_color="#5DADE2",
    run_button_color="#17A589",
    reset_button_color="#F39C12",
    button_text_color="#FFFFFF",
)


# Dark Theme - Modern, easy on the eyes
DARK_THEME = Theme(
    # Window and backgrounds
    window_bg="#1E1E1E",
    panel_bg="#252525",
    text_primary="#E8E8E8",
    text_secondary="#B0B0B0",
    border_color="#404040",
    
    # Gate buttons (Cyan/Blue palette for better dark mode contrast)
    gate_button_bg="#2A4A7F",
    gate_button_border="#6DAEE0",
    gate_button_hover="#34567A",
    gate_button_pressed="#1E3A5F",
    
    # Control buttons (Coral/Orange palette for dark mode)
    control_button_bg="#5C3333",
    control_button_border="#FF8080",
    control_button_hover="#6B3F3F",
    control_button_pressed="#4A2828",
    
    # Canvas
    canvas_bg="#1A1A1A",
    wire_color="#D0D0D0",
    grid_color="#333333",
    control_link_color="#FF9999",
    qubit_label_color="#D0D0D0",
    step_label_color="#999999",
    step_indicator_color="#FFEB3B",
    
    # State display
    state_display_title_bg="#333333",
    text_edit_bg="#252525",
    
    # Buttons (control panel)
    step_button_color="#6DAEE0",
    run_button_color="#3DD9A3",
    reset_button_color="#F39C12",
    button_text_color="#1A1A1A",
)


# Theme registry
THEMES = {
    "light": LIGHT_THEME,
    "dark": DARK_THEME,
}


def get_theme(name: str) -> Theme:
    """Get a theme by name. Defaults to light theme if not found."""
    return THEMES.get(name.lower(), LIGHT_THEME)


def get_gate_button_stylesheet(theme: Theme) -> str:
    """Generate stylesheet for gate buttons."""
    return f"""
        QPushButton {{
            background-color: {theme.gate_button_bg};
            border: 2px solid {theme.gate_button_border};
            border-radius: 5px;
            font-weight: bold;
            font-size: 14px;
            color: {theme.text_primary};
        }}
        QPushButton:hover {{
            background-color: {theme.gate_button_hover};
            border: 2px solid {theme.gate_button_border};
        }}
        QPushButton:pressed {{
            background-color: {theme.gate_button_pressed};
        }}
    """.strip()


def get_control_button_stylesheet(theme: Theme) -> str:
    """Generate stylesheet for control buttons."""
    return f"""
        QPushButton {{
            background-color: {theme.control_button_bg};
            border: 2px solid {theme.control_button_border};
            border-radius: 5px;
            font-weight: bold;
            font-size: 24px;
            color: {theme.control_button_border};
        }}
        QPushButton:hover {{
            background-color: {theme.control_button_hover};
            border: 2px solid {theme.control_button_border};
        }}
        QPushButton:pressed {{
            background-color: {theme.control_button_pressed};
        }}
    """.strip()


def get_palette_stylesheet(theme: Theme) -> str:
    """Generate stylesheet for gate palette widget."""
    return f"""
        QLabel {{
            color: {theme.text_primary};
        }}
        QTabWidget::pane {{
            border: 1px solid {theme.border_color};
            border-radius: 3px;
            background-color: {theme.panel_bg};
        }}
        QTabBar::tab {{
            padding: 5px 10px;
            margin: 2px;
            color: {theme.text_primary};
            background-color: {theme.panel_bg};
        }}
        QTabBar::tab:selected {{
            font-weight: bold;
            background-color: {theme.window_bg};
        }}
        QSpinBox {{
            background-color: {theme.panel_bg};
            color: {theme.text_primary};
            border: 1px solid {theme.border_color};
        }}
        QSlider::groove:horizontal {{
            background-color: {theme.panel_bg};
        }}
        QSlider::handle:horizontal {{
            background-color: {theme.gate_button_border};
        }}
    """.strip()


def get_canvas_stylesheet(theme: Theme) -> str:
    """Generate stylesheet for circuit canvas."""
    return f"""
        QWidget {{
            background-color: {theme.canvas_bg};
        }}
    """.strip()


def get_control_panel_stylesheet(theme: Theme) -> str:
    """Generate stylesheet for control panel."""
    return f"""
        QFrame {{
            background-color: {theme.panel_bg};
            border: 1px solid {theme.border_color};
        }}
        QLabel {{
            color: {theme.text_primary};
        }}
        QSpinBox {{
            background-color: {theme.window_bg};
            color: {theme.text_primary};
            border: 1px solid {theme.border_color};
        }}
        QPushButton {{
            color: {theme.button_text_color};
            border-radius: 3px;
            border: none;
            padding: 5px 10px;
            font-weight: bold;
        }}
    """.strip()


def get_state_display_stylesheet(theme: Theme) -> str:
    """Generate stylesheet for state display."""
    return f"""
        QWidget {{
            background-color: {theme.panel_bg};
        }}
        QLabel {{
            color: {theme.text_primary};
        }}
        QTextEdit {{
            background-color: {theme.text_edit_bg};
            color: {theme.text_primary};
            border: 1px solid {theme.border_color};
        }}
        QTabWidget::pane {{
            border: 1px solid {theme.border_color};
        }}
        QTabBar::tab {{
            color: {theme.text_primary};
            background-color: {theme.panel_bg};
        }}
        QTabBar::tab:selected {{
            font-weight: bold;
            background-color: {theme.window_bg};
        }}
    """.strip()

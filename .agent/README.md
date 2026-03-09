# Agent Context Directory

This directory contains context files for AI coding agents working on QubitSim.
All files here are generated summaries, maps, and references — **not user-facing docs**.

## Files

| File | Purpose |
|------|---------|
| [project_overview.md](project_overview.md) | What the project is, goals, tech stack, architecture, signals |
| [codebase_map.md](codebase_map.md) | File-by-file guide to every module, class, and key method |
| [gate_reference.md](gate_reference.md) | Complete reference for all 34+ gate types with examples |
| [implementation_history.md](implementation_history.md) | Chronological record of all implementation phases |
| [visualization_system.md](visualization_system.md) | Visualization subsystem: widgets, utils, data flow |

## Quick Project Facts

- **Language**: Python 3.10+
- **UI**: PyQt6
- **Quantum backend**: Qiskit Statevector simulator (via `qiskit-aer`)
- **Entry point**: `src/main.py`
- **Virtual env**: `venv/` at repo root
- **Run command**: `cd src && python main.py` (with venv activated)
- **Test command**: `PYTHONPATH=src python test_*.py`
- **Status**: Fully functional. Two major feature phases complete.

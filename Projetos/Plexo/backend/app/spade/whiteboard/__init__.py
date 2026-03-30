# FEATURE: Multi-Agent Communication
# Módulo de Whiteboard para monitoramento compartilhado

from .whiteboard import Whiteboard, WhiteboardStatus
from .whiteboard_entry import WhiteboardEntry, ActionType
from .whiteboard_manager import WhiteboardManager

__all__ = [
    "Whiteboard",
    "WhiteboardStatus",
    "WhiteboardEntry",
    "ActionType",
    "WhiteboardManager",
]

# FEATURE: Multi-Agent Communication
# Módulo de Teams para comunicação em grupo

from .team import Team, TeamStatus
from .team_chat import TeamChat
from .team_manager import TeamManager

__all__ = [
    "Team",
    "TeamStatus",
    "TeamChat",
    "TeamManager",
]

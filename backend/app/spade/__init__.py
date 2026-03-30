# FEATURE: Multi-Agent Communication
# Módulo SPADE para comunicação multi-agente no Plexo

from .agent_base import PlexoAgent
from .behaviors.base_behavior import BaseBehavior, BasePeriodicBehavior, BaseOneShotBehavior
from .behaviors.message_behavior import MessageBehavior, BroadcastBehavior
from .behaviors.checkpoint_behavior import CheckpointManager, Checkpoint, CheckpointStatus
from .protocols.xmpp_protocol import XMPPProtocol
from .protocols.urgency_protocol import UrgencyProtocol, UrgentMessage, UrgencyLevel
from .registry.agent_registry import AgentRegistry, get_agent_registry

from .teams.team import Team, TeamStatus, TeamMember
from .teams.team_chat import TeamChat, TeamMessage
from .teams.team_manager import TeamManager

from .whiteboard.whiteboard import Whiteboard, WhiteboardStatus
from .whiteboard.whiteboard_entry import WhiteboardEntry, ActionType
from .whiteboard.whiteboard_manager import WhiteboardManager

from .agents.specialist_agent import SpecialistAgent, SpecialistType, Assignment
from .agents.monitor_agent import MonitorAgent, MonitorRole, MonitorAction
from .agents.executor_agent import ExecutorAgent, ExecutorStatus, ExecutionStep

__all__ = [
    "PlexoAgent",
    "BaseBehavior",
    "BasePeriodicBehavior",
    "BaseOneShotBehavior",
    "MessageBehavior",
    "BroadcastBehavior",
    "CheckpointManager",
    "Checkpoint",
    "CheckpointStatus",
    "XMPPProtocol",
    "UrgencyProtocol",
    "UrgentMessage",
    "UrgencyLevel",
    "AgentRegistry",
    "get_agent_registry",
    "Team",
    "TeamStatus",
    "TeamMember",
    "TeamChat",
    "TeamMessage",
    "TeamManager",
    "Whiteboard",
    "WhiteboardStatus",
    "WhiteboardEntry",
    "ActionType",
    "WhiteboardManager",
    "SpecialistAgent",
    "SpecialistType",
    "Assignment",
    "MonitorAgent",
    "MonitorRole",
    "MonitorAction",
    "ExecutorAgent",
    "ExecutorStatus",
    "ExecutionStep",
]

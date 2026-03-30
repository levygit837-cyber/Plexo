# FEATURE: Multi-Agent Communication
# Módulo de protocolos para comunicação XMPP

from .xmpp_protocol import XMPPProtocol
from .urgency_protocol import UrgencyProtocol, UrgentMessage, UrgencyLevel
from .p2p_protocol import P2PProtocol, P2PMessage, MessageType

__all__ = [
    "XMPPProtocol",
    "UrgencyProtocol",
    "UrgentMessage",
    "UrgencyLevel",
    "P2PProtocol",
    "P2PMessage",
    "MessageType",
]

# FEATURE: Multi-Agent Communication
# Módulo de protocolos para comunicação XMPP

from .xmpp_protocol import XMPPProtocol
from .urgency_protocol import UrgencyProtocol, UrgentMessage, UrgencyLevel

__all__ = [
    "XMPPProtocol",
    "UrgencyProtocol",
    "UrgentMessage",
    "UrgencyLevel",
]

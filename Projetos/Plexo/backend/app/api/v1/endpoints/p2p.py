# FEATURE: Multi-Agent Communication
# Endpoints para comunicação P2P entre agentes

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.p2p import (
    P2PMessageCreate,
    P2PMessageResponse,
    P2PRequestCreate,
    P2PResponseCreate,
    P2PUrgentMessageCreate,
    P2PNotificationCreate,
    ConversationResponse,
    P2PStatsResponse
)
from app.schemas.xmpp_connection import (
    XMPPRegisterRequest,
    XMPPConnectRequest,
    XMPPConnectionResponse,
    XMPPSendMessageRequest,
    XMPPSendMessageResponse,
    ConnectedAgentsResponse,
    AgentStatusResponse
)
from app.api.deps import get_xmpp_service, get_p2p_service
from app.services.xmpp_service import XMPPService
from app.services.p2p_service import P2PService
from app.core.logging.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/register", response_model=XMPPConnectionResponse, status_code=status.HTTP_201_CREATED)
async def register_agent(
    data: XMPPRegisterRequest,
    xmpp_service: XMPPService = Depends(get_xmpp_service)
):
    """Registra um novo agente no servidor XMPP.
    
    Args:
        data: Dados de registro
        xmpp_service: Serviço XMPP
        
    Returns:
        Resposta de registro
    """
    result = await xmpp_service.register_agent(data.username, data.password)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Falha ao registrar agente")
        )
    return XMPPConnectionResponse(
        success=True,
        jid=result.get("jid"),
        username=result.get("username"),
        message=result.get("message")
    )


@router.post("/connect", response_model=XMPPConnectionResponse)
async def connect_agent(
    data: XMPPConnectRequest,
    xmpp_service: XMPPService = Depends(get_xmpp_service)
):
    """Conecta um agente ao servidor XMPP.
    
    Args:
        data: Dados de conexão
        xmpp_service: Serviço XMPP
        
    Returns:
        Resposta de conexão
    """
    result = await xmpp_service.connect_agent(data.username, data.password)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Falha ao conectar agente")
        )
    return XMPPConnectionResponse(
        success=True,
        jid=result.get("jid"),
        username=result.get("username"),
        message=result.get("message")
    )


@router.post("/disconnect/{username}")
async def disconnect_agent(
    username: str,
    xmpp_service: XMPPService = Depends(get_xmpp_service)
):
    """Desconecta um agente do servidor XMPP.
    
    Args:
        username: Username do agente
        xmpp_service: Serviço XMPP
        
    Returns:
        Resposta de desconexão
    """
    result = await xmpp_service.disconnect_agent(username)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Falha ao desconectar agente"
        )
    return {"success": True, "message": f"Agente {username} desconectado"}


@router.post("/send-message", response_model=XMPPSendMessageResponse)
async def send_message(
    from_username: str,
    data: XMPPSendMessageRequest,
    xmpp_service: XMPPService = Depends(get_xmpp_service)
):
    """Envia mensagem entre agentes.
    
    Args:
        from_username: Username do remetente
        data: Dados da mensagem
        xmpp_service: Serviço XMPP
        
    Returns:
        Resposta de envio
    """
    result = await xmpp_service.send_message(
        from_username=from_username,
        to_username=data.to_username,
        content=data.content,
        urgency=data.urgency
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Falha ao enviar mensagem")
        )
    return XMPPSendMessageResponse(
        success=True,
        from_jid=result.get("from"),
        to_jid=result.get("to"),
        content=result.get("content"),
        urgency=result.get("urgency"),
        timestamp=result.get("timestamp")
    )


@router.get("/connected-agents", response_model=ConnectedAgentsResponse)
async def get_connected_agents(
    xmpp_service: XMPPService = Depends(get_xmpp_service)
):
    """Retorna lista de agentes conectados.
    
    Args:
        xmpp_service: Serviço XMPP
        
    Returns:
        Lista de agentes conectados
    """
    agents = xmpp_service.get_connected_agents()
    return ConnectedAgentsResponse(
        agents=agents,
        total=len(agents)
    )


@router.get("/agent-status/{username}", response_model=AgentStatusResponse)
async def get_agent_status(
    username: str,
    xmpp_service: XMPPService = Depends(get_xmpp_service)
):
    """Retorna status de conexão de um agente.
    
    Args:
        username: Username do agente
        xmpp_service: Serviço XMPP
        
    Returns:
        Status de conexão
    """
    is_connected = xmpp_service.is_agent_connected(username)
    jid = xmpp_service.get_agent_jid(username)
    return AgentStatusResponse(
        username=username,
        is_connected=is_connected,
        jid=jid
    )


@router.post("/send-direct", response_model=P2PMessageResponse)
async def send_direct_message(
    from_agent: str,
    data: P2PMessageCreate,
    p2p_service: P2PService = Depends(get_p2p_service)
):
    """Envia mensagem direta entre agentes.
    
    Args:
        from_agent: Username do agente remetente
        data: Dados da mensagem
        p2p_service: Serviço P2P
        
    Returns:
        Resposta de envio
    """
    result = await p2p_service.send_direct_message(
        from_agent=from_agent,
        to_agent=data.to_agent,
        content=data.content,
        urgency=data.urgency.value
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Falha ao enviar mensagem")
        )
    return P2PMessageResponse(
        message_id=result.get("message_id", ""),
        from_agent=from_agent,
        to_agent=data.to_agent,
        content=data.content,
        message_type=data.message_type.value,
        urgency=data.urgency.value,
        requires_response=data.requires_response,
        timestamp=result.get("timestamp"),
        metadata=data.metadata
    )


@router.post("/send-request", response_model=P2PMessageResponse)
async def send_request(
    from_agent: str,
    data: P2PRequestCreate,
    p2p_service: P2PService = Depends(get_p2p_service)
):
    """Envia request que requer resposta.
    
    Args:
        from_agent: Username do agente remetente
        data: Dados da request
        p2p_service: Serviço P2P
        
    Returns:
        Resposta de envio
    """
    result = await p2p_service.send_request(
        from_agent=from_agent,
        to_agent=data.to_agent,
        content=data.content,
        urgency=data.urgency.value
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Falha ao enviar request")
        )
    return P2PMessageResponse(
        message_id=result.get("message_id", ""),
        from_agent=from_agent,
        to_agent=data.to_agent,
        content=data.content,
        message_type="request",
        urgency=data.urgency.value,
        requires_response=True,
        timestamp=result.get("timestamp"),
        metadata=data.metadata
    )


@router.post("/send-response", response_model=P2PMessageResponse)
async def send_response(
    from_agent: str,
    data: P2PResponseCreate,
    p2p_service: P2PService = Depends(get_p2p_service)
):
    """Envia response a uma request.
    
    Args:
        from_agent: Username do agente remetente
        data: Dados da response
        p2p_service: Serviço P2P
        
    Returns:
        Resposta de envio
    """
    result = await p2p_service.send_response(
        from_agent=from_agent,
        to_agent=data.to_agent,
        original_message_id=data.original_message_id,
        content=data.content
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Falha ao enviar response")
        )
    return P2PMessageResponse(
        message_id=result.get("message_id", ""),
        from_agent=from_agent,
        to_agent=data.to_agent,
        content=data.content,
        message_type="response",
        urgency="MEDIUM",
        requires_response=False,
        timestamp=result.get("timestamp"),
        metadata=data.metadata
    )


@router.post("/send-urgent", response_model=P2PMessageResponse)
async def send_urgent_message(
    from_agent: str,
    data: P2PUrgentMessageCreate,
    p2p_service: P2PService = Depends(get_p2p_service)
):
    """Envia mensagem urgente.
    
    Args:
        from_agent: Username do agente remetente
        data: Dados da mensagem urgente
        p2p_service: Serviço P2P
        
    Returns:
        Resposta de envio
    """
    result = await p2p_service.send_urgent_message(
        from_agent=from_agent,
        to_agent=data.to_agent,
        content=data.content
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Falha ao enviar mensagem urgente")
        )
    return P2PMessageResponse(
        message_id=result.get("message_id", ""),
        from_agent=from_agent,
        to_agent=data.to_agent,
        content=data.content,
        message_type="urgent",
        urgency="CRITICAL",
        requires_response=True,
        timestamp=result.get("timestamp"),
        metadata=data.metadata
    )


@router.post("/send-notification", response_model=P2PMessageResponse)
async def send_notification(
    from_agent: str,
    data: P2PNotificationCreate,
    p2p_service: P2PService = Depends(get_p2p_service)
):
    """Envia notificação.
    
    Args:
        from_agent: Username do agente remetente
        data: Dados da notificação
        p2p_service: Serviço P2P
        
    Returns:
        Resposta de envio
    """
    result = await p2p_service.send_notification(
        from_agent=from_agent,
        to_agent=data.to_agent,
        content=data.content
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Falha ao enviar notificação")
        )
    return P2PMessageResponse(
        message_id=result.get("message_id", ""),
        from_agent=from_agent,
        to_agent=data.to_agent,
        content=data.content,
        message_type="notification",
        urgency="LOW",
        requires_response=False,
        timestamp=result.get("timestamp"),
        metadata=data.metadata
    )


@router.get("/conversation/{agent_id}/{other_agent}", response_model=ConversationResponse)
async def get_conversation(
    agent_id: str,
    other_agent: str,
    p2p_service: P2PService = Depends(get_p2p_service)
):
    """Retorna conversa entre dois agentes.
    
    Args:
        agent_id: ID do agente
        other_agent: Username do outro agente
        p2p_service: Serviço P2P
        
    Returns:
        Conversa entre os agentes
    """
    messages = p2p_service.get_conversation_with(agent_id, other_agent)
    return ConversationResponse(
        agent_id=agent_id,
        other_agent=other_agent,
        messages=[P2PMessageResponse(**msg) for msg in messages],
        total=len(messages)
    )


@router.get("/stats/{agent_id}", response_model=P2PStatsResponse)
async def get_p2p_stats(
    agent_id: str,
    p2p_service: P2PService = Depends(get_p2p_service)
):
    """Retorna estatísticas P2P de um agente.
    
    Args:
        agent_id: ID do agente
        p2p_service: Serviço P2P
        
    Returns:
        Estatísticas P2P
    """
    stats = p2p_service.get_stats(agent_id)
    return P2PStatsResponse(**stats)


@router.get("/pending-requests/{agent_id}", response_model=List[P2PMessageResponse])
async def get_pending_requests(
    agent_id: str,
    p2p_service: P2PService = Depends(get_p2p_service)
):
    """Retorna requests pendentes de um agente.
    
    Args:
        agent_id: ID do agente
        p2p_service: Serviço P2P
        
    Returns:
        Lista de requests pendentes
    """
    requests = p2p_service.get_pending_requests(agent_id)
    return [P2PMessageResponse(**req) for req in requests]


@router.get("/message-history/{agent_id}", response_model=List[P2PMessageResponse])
async def get_message_history(
    agent_id: str,
    limit: int = 100,
    p2p_service: P2PService = Depends(get_p2p_service)
):
    """Retorna histórico de mensagens de um agente.
    
    Args:
        agent_id: ID do agente
        limit: Limite de mensagens
        p2p_service: Serviço P2P
        
    Returns:
        Lista de mensagens
    """
    messages = p2p_service.get_message_history(agent_id, limit)
    return [P2PMessageResponse(**msg) for msg in messages]

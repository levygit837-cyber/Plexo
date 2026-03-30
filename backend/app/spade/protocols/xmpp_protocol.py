# XMPP protocol utilities for SPADE agents.
# FEATURE: Multi-Agent Communication

from typing import Optional, Dict, Any, List
from datetime import datetime
import json

from spade.message import Message
from spade.template import Template

from app.core.logging import get_logger
from app.core.errors import AgentCommunicationError


logger = get_logger(__name__)


class XMPPProtocol:
    """
    XMPP protocol utilities for message formatting and parsing.
    
    Provides helper methods for creating and parsing XMPP messages
    with standardized metadata and content structure.
    """

    @staticmethod
    def create_message(
        to_jid: str,
        content: str,
        message_type: str = "default",
        metadata: Optional[Dict[str, Any]] = None,
        sender_id: Optional[str] = None,
    ) -> Message:
        """
        Create standardized XMPP message.
        
        Args:
            to_jid: Recipient JID
            content: Message content
            message_type: Type of message
            metadata: Optional additional metadata
            sender_id: Optional sender identifier
            
        Returns:
            Configured SPADE Message
        """
        msg = Message(to=to_jid)
        msg.body = content
        
        msg.set_metadata("type", message_type)
        msg.set_metadata("timestamp", datetime.utcnow().isoformat())
        
        if sender_id:
            msg.set_metadata("sender_id", sender_id)
        
        if metadata:
            for key, value in metadata.items():
                msg.set_metadata(key, str(value))
        
        return msg

    @staticmethod
    def create_request(
        to_jid: str,
        action: str,
        params: Optional[Dict[str, Any]] = None,
        sender_id: Optional[str] = None,
    ) -> Message:
        """
        Create request message.
        
        Args:
            to_jid: Recipient JID
            action: Action to request
            params: Optional request parameters
            sender_id: Optional sender identifier
            
        Returns:
            Request message
        """
        content = json.dumps({
            "action": action,
            "params": params or {},
        })
        
        return XMPPProtocol.create_message(
            to_jid=to_jid,
            content=content,
            message_type="request",
            sender_id=sender_id,
        )

    @staticmethod
    def create_response(
        to_jid: str,
        result: Any,
        success: bool = True,
        error: Optional[str] = None,
        sender_id: Optional[str] = None,
    ) -> Message:
        """
        Create response message.
        
        Args:
            to_jid: Recipient JID
            result: Response result
            success: Whether request was successful
            error: Optional error message
            sender_id: Optional sender identifier
            
        Returns:
            Response message
        """
        content = json.dumps({
            "success": success,
            "result": result,
            "error": error,
        })
        
        return XMPPProtocol.create_message(
            to_jid=to_jid,
            content=content,
            message_type="response",
            sender_id=sender_id,
        )

    @staticmethod
    def create_notification(
        to_jid: str,
        event: str,
        data: Optional[Dict[str, Any]] = None,
        sender_id: Optional[str] = None,
    ) -> Message:
        """
        Create notification message.
        
        Args:
            to_jid: Recipient JID
            event: Event name
            data: Optional event data
            sender_id: Optional sender identifier
            
        Returns:
            Notification message
        """
        content = json.dumps({
            "event": event,
            "data": data or {},
        })
        
        return XMPPProtocol.create_message(
            to_jid=to_jid,
            content=content,
            message_type="notification",
            sender_id=sender_id,
        )

    @staticmethod
    def parse_message(message: Message) -> Dict[str, Any]:
        """
        Parse XMPP message into structured data.
        
        Args:
            message: SPADE message to parse
            
        Returns:
            Parsed message data
        """
        try:
            sender = str(message.sender)
            content = message.body
            metadata = message.metadata if hasattr(message, 'metadata') else {}
            
            message_type = metadata.get("type", "default")
            timestamp = metadata.get("timestamp")
            sender_id = metadata.get("sender_id")
            
            parsed_content = None
            if message_type in ["request", "response", "notification"]:
                try:
                    parsed_content = json.loads(content)
                except json.JSONDecodeError:
                    parsed_content = content
            else:
                parsed_content = content
            
            return {
                "sender": sender,
                "sender_id": sender_id,
                "type": message_type,
                "content": parsed_content,
                "timestamp": timestamp,
                "metadata": metadata,
            }
            
        except Exception as e:
            logger.error(f"Failed to parse message: {e}")
            raise AgentCommunicationError(
                message="Failed to parse XMPP message",
                details={"error": str(e)}
            )

    @staticmethod
    def create_template(
        sender: Optional[str] = None,
        message_type: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Template:
        """
        Create message template for filtering.
        
        Args:
            sender: Optional sender JID to match
            message_type: Optional message type to match
            metadata: Optional metadata to match
            
        Returns:
            SPADE Template for message filtering
        """
        template = Template()
        
        if sender:
            template.sender = sender
        
        if message_type:
            template.set_metadata("type", message_type)
        
        if metadata:
            for key, value in metadata.items():
                template.set_metadata(key, value)
        
        return template

    @staticmethod
    def validate_jid(jid: str) -> bool:
        """
        Validate XMPP JID format.
        
        Args:
            jid: JID to validate
            
        Returns:
            True if JID is valid
        """
        if not jid or "@" not in jid:
            return False
        
        parts = jid.split("@")
        if len(parts) != 2:
            return False
        
        username, domain = parts
        if not username or not domain:
            return False
        
        return True

    @staticmethod
    def extract_username(jid: str) -> str:
        """
        Extract username from JID.
        
        Args:
            jid: Full JID
            
        Returns:
            Username part of JID
        """
        if "@" in jid:
            return jid.split("@")[0]
        return jid

    @staticmethod
    def extract_domain(jid: str) -> str:
        """
        Extract domain from JID.
        
        Args:
            jid: Full JID
            
        Returns:
            Domain part of JID
        """
        if "@" in jid:
            domain_part = jid.split("@")[1]
            if "/" in domain_part:
                return domain_part.split("/")[0]
            return domain_part
        return ""

    @staticmethod
    def build_jid(username: str, domain: str, resource: Optional[str] = None) -> str:
        """
        Build JID from components.
        
        Args:
            username: Username
            domain: Domain
            resource: Optional resource
            
        Returns:
            Full JID
        """
        jid = f"{username}@{domain}"
        if resource:
            jid = f"{jid}/{resource}"
        return jid

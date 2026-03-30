# FEATURE: Multi-Agent Communication
# Entrada do Whiteboard com tipos de ação

import uuid
from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field


class ActionType(Enum):
    """Tipos de ação registradas no whiteboard"""
    FUNCTION_CREATED = "function_created"
    FUNCTION_MODIFIED = "function_modified"
    FUNCTION_DELETED = "function_deleted"
    CLASS_CREATED = "class_created"
    CLASS_MODIFIED = "class_modified"
    CLASS_DELETED = "class_deleted"
    FILE_CREATED = "file_created"
    FILE_MODIFIED = "file_modified"
    FILE_DELETED = "file_deleted"
    TEST_CREATED = "test_created"
    TEST_PASSED = "test_passed"
    TEST_FAILED = "test_failed"
    API_CALLED = "api_called"
    DATABASE_QUERY = "database_query"
    ERROR_DETECTED = "error_detected"
    ERROR_FIXED = "error_fixed"
    CODE_REVIEW = "code_review"
    REFACTORING = "refactoring"
    DOCUMENTATION = "documentation"
    CONFIGURATION = "configuration"
    DEPLOYMENT = "deployment"
    OTHER = "other"


@dataclass
class WhiteboardEntry:
    """Entrada no quadro branco"""
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    whiteboard_id: str = ""
    author_id: str = ""
    action_type: ActionType = ActionType.OTHER
    content: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    line_number: Optional[int] = None
    file_path: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "entry_id": self.entry_id,
            "whiteboard_id": self.whiteboard_id,
            "author_id": self.author_id,
            "action_type": self.action_type.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "line_number": self.line_number,
            "file_path": self.file_path,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WhiteboardEntry':
        """Cria instância a partir de dicionário"""
        return cls(
            entry_id=data.get("entry_id", str(uuid.uuid4())),
            whiteboard_id=data.get("whiteboard_id", ""),
            author_id=data.get("author_id", ""),
            action_type=ActionType(data.get("action_type", "other")),
            content=data.get("content", ""),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            line_number=data.get("line_number"),
            file_path=data.get("file_path"),
            metadata=data.get("metadata", {})
        )
    
    @staticmethod
    def create_function_entry(
        whiteboard_id: str,
        author_id: str,
        function_name: str,
        description: str,
        line_number: Optional[int] = None,
        file_path: Optional[str] = None
    ) -> 'WhiteboardEntry':
        """Cria entrada para criação de função"""
        content = f"O Executor escreveu uma função chamada '{function_name}' que {description}"
        if line_number:
            content += f"... na linha {line_number}"
        
        return WhiteboardEntry(
            whiteboard_id=whiteboard_id,
            author_id=author_id,
            action_type=ActionType.FUNCTION_CREATED,
            content=content,
            line_number=line_number,
            file_path=file_path,
            metadata={"function_name": function_name, "description": description}
        )
    
    @staticmethod
    def create_class_entry(
        whiteboard_id: str,
        author_id: str,
        class_name: str,
        description: str,
        line_number: Optional[int] = None,
        file_path: Optional[str] = None
    ) -> 'WhiteboardEntry':
        """Cria entrada para criação de classe"""
        content = f"O Executor escreveu uma classe chamada '{class_name}' que {description}"
        if line_number:
            content += f"... na linha {line_number}"
        
        return WhiteboardEntry(
            whiteboard_id=whiteboard_id,
            author_id=author_id,
            action_type=ActionType.CLASS_CREATED,
            content=content,
            line_number=line_number,
            file_path=file_path,
            metadata={"class_name": class_name, "description": description}
        )
    
    @staticmethod
    def create_test_entry(
        whiteboard_id: str,
        author_id: str,
        test_name: str,
        passed: bool,
        details: str = ""
    ) -> 'WhiteboardEntry':
        """Cria entrada para teste"""
        action_type = ActionType.TEST_PASSED if passed else ActionType.TEST_FAILED
        status = "passou" if passed else "falhou"
        content = f"O teste '{test_name}' {status}"
        if details:
            content += f": {details}"
        
        return WhiteboardEntry(
            whiteboard_id=whiteboard_id,
            author_id=author_id,
            action_type=action_type,
            content=content,
            metadata={"test_name": test_name, "passed": passed, "details": details}
        )
    
    @staticmethod
    def create_error_entry(
        whiteboard_id: str,
        author_id: str,
        error_message: str,
        file_path: Optional[str] = None,
        line_number: Optional[int] = None
    ) -> 'WhiteboardEntry':
        """Cria entrada para erro detectado"""
        content = f"Erro detectado: {error_message}"
        if file_path:
            content += f" em {file_path}"
        if line_number:
            content += f" linha {line_number}"
        
        return WhiteboardEntry(
            whiteboard_id=whiteboard_id,
            author_id=author_id,
            action_type=ActionType.ERROR_DETECTED,
            content=content,
            line_number=line_number,
            file_path=file_path,
            metadata={"error_message": error_message}
        )

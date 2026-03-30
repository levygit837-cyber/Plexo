# Base tool class for LangChain integration.
# FEATURE: LangChain Integration

from typing import Optional, Dict, Any, Type
from abc import ABC, abstractmethod
import asyncio
from datetime import datetime

from langchain.tools import BaseTool as LangChainBaseTool
from pydantic import BaseModel, Field

from app.core.logging import get_logger
from app.core.errors import PlexoException


logger = get_logger(__name__)


class BaseToolInput(BaseModel):
    """
    Base input schema for tools.
    
    Extend this class to define custom tool inputs.
    """
    pass


class BaseTool(LangChainBaseTool, ABC):
    """
    Base tool class for all LangChain tools in Plexo.
    
    Extends LangChain BaseTool and provides common functionality
    for tool execution, error handling, and logging.
    """

    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    args_schema: Type[BaseModel] = BaseToolInput

    def __init__(self, **kwargs):
        """
        Initialize BaseTool.
        
        Args:
            **kwargs: Additional tool configuration
        """
        super().__init__(**kwargs)
        self._logger = get_logger(f"{__name__}.{self.name}")
        self._execution_count = 0
        self._error_count = 0
        self._total_duration = 0.0

    def _run(self, *args, **kwargs) -> Any:
        """
        Synchronous tool execution.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Tool execution result
        """
        start_time = datetime.utcnow()
        
        try:
            self._execution_count += 1
            
            self._logger.info(
                f"Executing tool {self.name}",
                extra={"execution_count": self._execution_count}
            )
            
            result = self._execute(*args, **kwargs)
            
            duration = (datetime.utcnow() - start_time).total_seconds()
            self._total_duration += duration
            
            self._logger.info(
                f"Tool {self.name} completed",
                extra={
                    "execution_count": self._execution_count,
                    "duration": duration
                }
            )
            
            return result
            
        except Exception as e:
            self._error_count += 1
            self._logger.error(
                f"Tool {self.name} failed: {e}",
                extra={
                    "execution_count": self._execution_count,
                    "error_count": self._error_count
                }
            )
            raise PlexoException(
                message=f"Tool execution failed: {self.name}",
                details={"error": str(e), "args": args, "kwargs": kwargs}
            )

    async def _arun(self, *args, **kwargs) -> Any:
        """
        Asynchronous tool execution.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Tool execution result
        """
        start_time = datetime.utcnow()
        
        try:
            self._execution_count += 1
            
            self._logger.info(
                f"Executing async tool {self.name}",
                extra={"execution_count": self._execution_count}
            )
            
            result = await self._aexecute(*args, **kwargs)
            
            duration = (datetime.utcnow() - start_time).total_seconds()
            self._total_duration += duration
            
            self._logger.info(
                f"Async tool {self.name} completed",
                extra={
                    "execution_count": self._execution_count,
                    "duration": duration
                }
            )
            
            return result
            
        except Exception as e:
            self._error_count += 1
            self._logger.error(
                f"Async tool {self.name} failed: {e}",
                extra={
                    "execution_count": self._execution_count,
                    "error_count": self._error_count
                }
            )
            raise PlexoException(
                message=f"Async tool execution failed: {self.name}",
                details={"error": str(e), "args": args, "kwargs": kwargs}
            )

    @abstractmethod
    def _execute(self, *args, **kwargs) -> Any:
        """
        Execute tool logic synchronously.
        
        Override this method to implement custom tool logic.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Tool execution result
        """
        pass

    async def _aexecute(self, *args, **kwargs) -> Any:
        """
        Execute tool logic asynchronously.
        
        Override this method to implement custom async tool logic.
        Default implementation calls synchronous version.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Tool execution result
        """
        return self._execute(*args, **kwargs)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get tool execution statistics.
        
        Returns:
            Dictionary with tool stats
        """
        avg_duration = (
            self._total_duration / self._execution_count
            if self._execution_count > 0
            else 0.0
        )
        
        return {
            "name": self.name,
            "execution_count": self._execution_count,
            "error_count": self._error_count,
            "total_duration": self._total_duration,
            "average_duration": avg_duration,
            "success_rate": (
                (self._execution_count - self._error_count) / self._execution_count
                if self._execution_count > 0
                else 0.0
            ),
        }

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate tool input.
        
        Args:
            input_data: Input data to validate
            
        Returns:
            True if input is valid
        """
        try:
            self.args_schema(**input_data)
            return True
        except Exception as e:
            self._logger.error(f"Input validation failed: {e}")
            return False

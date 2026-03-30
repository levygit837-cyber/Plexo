# Base chain class for LangChain integration.
# FEATURE: LangChain Integration

from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
import asyncio
from datetime import datetime

from langchain.chains.base import Chain
from langchain.callbacks.manager import CallbackManagerForChainRun, AsyncCallbackManagerForChainRun

from app.core.logging import get_logger
from app.core.errors import PlexoException


logger = get_logger(__name__)


class BaseChain(Chain, ABC):
    """
    Base chain class for all LangChain chains in Plexo.
    
    Extends LangChain Chain and provides common functionality
    for chain execution, error handling, and logging.
    """

    def __init__(self, **kwargs):
        """
        Initialize BaseChain.
        
        Args:
            **kwargs: Additional chain configuration
        """
        super().__init__(**kwargs)
        self._logger = get_logger(f"{__name__}.{self.__class__.__name__}")
        self._execution_count = 0
        self._error_count = 0
        self._total_duration = 0.0

    @property
    def input_keys(self) -> List[str]:
        """
        Get input keys for the chain.
        
        Returns:
            List of input key names
        """
        return self._get_input_keys()

    @property
    def output_keys(self) -> List[str]:
        """
        Get output keys for the chain.
        
        Returns:
            List of output key names
        """
        return self._get_output_keys()

    @abstractmethod
    def _get_input_keys(self) -> List[str]:
        """
        Define input keys for the chain.
        
        Override this method to specify input keys.
        
        Returns:
            List of input key names
        """
        pass

    @abstractmethod
    def _get_output_keys(self) -> List[str]:
        """
        Define output keys for the chain.
        
        Override this method to specify output keys.
        
        Returns:
            List of output key names
        """
        pass

    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        """
        Synchronous chain execution.
        
        Args:
            inputs: Input dictionary
            run_manager: Optional callback manager
            
        Returns:
            Output dictionary
        """
        start_time = datetime.utcnow()
        
        try:
            self._execution_count += 1
            
            self._logger.info(
                f"Executing chain {self.__class__.__name__}",
                extra={"execution_count": self._execution_count}
            )
            
            result = self._execute(inputs, run_manager)
            
            duration = (datetime.utcnow() - start_time).total_seconds()
            self._total_duration += duration
            
            self._logger.info(
                f"Chain {self.__class__.__name__} completed",
                extra={
                    "execution_count": self._execution_count,
                    "duration": duration
                }
            )
            
            return result
            
        except Exception as e:
            self._error_count += 1
            self._logger.error(
                f"Chain {self.__class__.__name__} failed: {e}",
                extra={
                    "execution_count": self._execution_count,
                    "error_count": self._error_count
                }
            )
            raise PlexoException(
                message=f"Chain execution failed: {self.__class__.__name__}",
                details={"error": str(e), "inputs": inputs}
            )

    async def _acall(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronous chain execution.
        
        Args:
            inputs: Input dictionary
            run_manager: Optional async callback manager
            
        Returns:
            Output dictionary
        """
        start_time = datetime.utcnow()
        
        try:
            self._execution_count += 1
            
            self._logger.info(
                f"Executing async chain {self.__class__.__name__}",
                extra={"execution_count": self._execution_count}
            )
            
            result = await self._aexecute(inputs, run_manager)
            
            duration = (datetime.utcnow() - start_time).total_seconds()
            self._total_duration += duration
            
            self._logger.info(
                f"Async chain {self.__class__.__name__} completed",
                extra={
                    "execution_count": self._execution_count,
                    "duration": duration
                }
            )
            
            return result
            
        except Exception as e:
            self._error_count += 1
            self._logger.error(
                f"Async chain {self.__class__.__name__} failed: {e}",
                extra={
                    "execution_count": self._execution_count,
                    "error_count": self._error_count
                }
            )
            raise PlexoException(
                message=f"Async chain execution failed: {self.__class__.__name__}",
                details={"error": str(e), "inputs": inputs}
            )

    @abstractmethod
    def _execute(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        """
        Execute chain logic synchronously.
        
        Override this method to implement custom chain logic.
        
        Args:
            inputs: Input dictionary
            run_manager: Optional callback manager
            
        Returns:
            Output dictionary
        """
        pass

    async def _aexecute(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        """
        Execute chain logic asynchronously.
        
        Override this method to implement custom async chain logic.
        Default implementation calls synchronous version.
        
        Args:
            inputs: Input dictionary
            run_manager: Optional async callback manager
            
        Returns:
            Output dictionary
        """
        return self._execute(inputs, None)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get chain execution statistics.
        
        Returns:
            Dictionary with chain stats
        """
        avg_duration = (
            self._total_duration / self._execution_count
            if self._execution_count > 0
            else 0.0
        )
        
        return {
            "name": self.__class__.__name__,
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

    @property
    def _chain_type(self) -> str:
        """
        Get chain type identifier.
        
        Returns:
            Chain type string
        """
        return self.__class__.__name__.lower()

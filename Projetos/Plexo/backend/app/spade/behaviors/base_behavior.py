# Base behavior class for SPADE agents.
# FEATURE: Multi-Agent Communication

from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
import asyncio
from datetime import datetime

from spade.behaviour import CyclicBehaviour, PeriodicBehaviour, OneShotBehaviour
from spade.message import Message

from app.core.logging import get_logger
from app.core.errors import BehaviorError


logger = get_logger(__name__)


class BaseBehavior(CyclicBehaviour, ABC):
    """
    Base behavior class for all agent behaviors.
    
    Extends SPADE CyclicBehaviour and provides common functionality
    for behavior lifecycle and error handling.
    """

    def __init__(self, period: Optional[float] = None):
        """
        Initialize BaseBehavior.
        
        Args:
            period: Optional period in seconds for periodic execution
        """
        super().__init__()
        self._period = period
        self._logger = get_logger(f"{__name__}.{self.__class__.__name__}")
        self._started_at: Optional[datetime] = None
        self._execution_count = 0
        self._error_count = 0

    async def on_start(self) -> None:
        """
        Called when behavior starts.
        
        Override this method to add custom startup logic.
        """
        self._started_at = datetime.utcnow()
        self._logger.info(
            f"Behavior {self.__class__.__name__} started",
            extra={"agent_jid": str(self.agent.jid)}
        )

    async def run(self) -> None:
        """
        Main behavior execution loop.
        
        Calls execute() and handles errors.
        """
        try:
            self._execution_count += 1
            await self.execute()
            
            if self._period:
                await asyncio.sleep(self._period)
                
        except Exception as e:
            self._error_count += 1
            self._logger.error(
                f"Error in behavior {self.__class__.__name__}: {e}",
                extra={
                    "agent_jid": str(self.agent.jid),
                    "execution_count": self._execution_count,
                    "error_count": self._error_count
                }
            )
            await self.on_error(e)

    @abstractmethod
    async def execute(self) -> None:
        """
        Execute behavior logic.
        
        Override this method to implement custom behavior logic.
        """
        pass

    async def on_error(self, error: Exception) -> None:
        """
        Handle behavior errors.
        
        Override this method to add custom error handling.
        
        Args:
            error: Exception that occurred
        """
        raise BehaviorError(
            agent_id=str(self.agent.jid),
            behavior_name=self.__class__.__name__,
            reason=str(error)
        )

    async def on_end(self) -> None:
        """
        Called when behavior ends.
        
        Override this method to add custom cleanup logic.
        """
        self._logger.info(
            f"Behavior {self.__class__.__name__} ended",
            extra={
                "agent_jid": str(self.agent.jid),
                "execution_count": self._execution_count,
                "error_count": self._error_count
            }
        )

    def get_stats(self) -> Dict[str, Any]:
        """
        Get behavior statistics.
        
        Returns:
            Dictionary with behavior stats
        """
        return {
            "name": self.__class__.__name__,
            "started_at": self._started_at.isoformat() if self._started_at else None,
            "execution_count": self._execution_count,
            "error_count": self._error_count,
            "period": self._period,
        }


class BasePeriodicBehavior(PeriodicBehaviour, ABC):
    """
    Base periodic behavior class.
    
    Extends SPADE PeriodicBehaviour for behaviors that run at fixed intervals.
    """

    def __init__(self, period: float, start_at: Optional[datetime] = None):
        """
        Initialize BasePeriodicBehavior.
        
        Args:
            period: Period in seconds between executions
            start_at: Optional datetime to start the behavior
        """
        super().__init__(period=period, start_at=start_at)
        self._logger = get_logger(f"{__name__}.{self.__class__.__name__}")
        self._execution_count = 0
        self._error_count = 0

    async def on_start(self) -> None:
        """
        Called when behavior starts.
        """
        self._logger.info(
            f"Periodic behavior {self.__class__.__name__} started",
            extra={"agent_jid": str(self.agent.jid), "period": self.period}
        )

    async def run(self) -> None:
        """
        Main periodic execution.
        """
        try:
            self._execution_count += 1
            await self.execute()
        except Exception as e:
            self._error_count += 1
            self._logger.error(
                f"Error in periodic behavior {self.__class__.__name__}: {e}",
                extra={
                    "agent_jid": str(self.agent.jid),
                    "execution_count": self._execution_count
                }
            )
            await self.on_error(e)

    @abstractmethod
    async def execute(self) -> None:
        """
        Execute periodic behavior logic.
        """
        pass

    async def on_error(self, error: Exception) -> None:
        """
        Handle periodic behavior errors.
        
        Args:
            error: Exception that occurred
        """
        raise BehaviorError(
            agent_id=str(self.agent.jid),
            behavior_name=self.__class__.__name__,
            reason=str(error)
        )


class BaseOneShotBehavior(OneShotBehaviour, ABC):
    """
    Base one-shot behavior class.
    
    Extends SPADE OneShotBehaviour for behaviors that run once.
    """

    def __init__(self):
        """
        Initialize BaseOneShotBehavior.
        """
        super().__init__()
        self._logger = get_logger(f"{__name__}.{self.__class__.__name__}")
        self._executed = False

    async def on_start(self) -> None:
        """
        Called when behavior starts.
        """
        self._logger.info(
            f"One-shot behavior {self.__class__.__name__} started",
            extra={"agent_jid": str(self.agent.jid)}
        )

    async def run(self) -> None:
        """
        Main one-shot execution.
        """
        try:
            await self.execute()
            self._executed = True
        except Exception as e:
            self._logger.error(
                f"Error in one-shot behavior {self.__class__.__name__}: {e}",
                extra={"agent_jid": str(self.agent.jid)}
            )
            await self.on_error(e)

    @abstractmethod
    async def execute(self) -> None:
        """
        Execute one-shot behavior logic.
        """
        pass

    async def on_error(self, error: Exception) -> None:
        """
        Handle one-shot behavior errors.
        
        Args:
            error: Exception that occurred
        """
        raise BehaviorError(
            agent_id=str(self.agent.jid),
            behavior_name=self.__class__.__name__,
            reason=str(error)
        )

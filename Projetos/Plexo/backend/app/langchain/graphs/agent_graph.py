# Agent graph for LangGraph integration.
# FEATURE: LangChain Integration

from typing import Optional, Dict, Any, List, Callable
from abc import ABC, abstractmethod
import asyncio
from datetime import datetime

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor

from app.core.logging import get_logger
from app.core.errors import PlexoException


logger = get_logger(__name__)


class AgentState(Dict[str, Any]):
    """
    State container for agent graph.
    
    Extends dict to provide typed state management.
    """
    pass


class BaseAgentGraph(ABC):
    """
    Base agent graph class for LangGraph integration.
    
    Provides common functionality for building and executing
    agent graphs with state management.
    """

    def __init__(self):
        """
        Initialize BaseAgentGraph.
        """
        self._logger = get_logger(f"{__name__}.{self.__class__.__name__}")
        self._graph: Optional[StateGraph] = None
        self._compiled_graph = None
        self._execution_count = 0
        self._error_count = 0

    @abstractmethod
    def build_graph(self) -> StateGraph:
        """
        Build the agent graph.
        
        Override this method to define graph structure.
        
        Returns:
            Configured StateGraph
        """
        pass

    def compile(self) -> None:
        """
        Compile the agent graph.
        """
        try:
            self._graph = self.build_graph()
            self._compiled_graph = self._graph.compile()
            
            self._logger.info(
                f"Graph {self.__class__.__name__} compiled successfully"
            )
            
        except Exception as e:
            self._logger.error(f"Failed to compile graph: {e}")
            raise PlexoException(
                message=f"Graph compilation failed: {self.__class__.__name__}",
                details={"error": str(e)}
            )

    def execute(self, initial_state: AgentState) -> AgentState:
        """
        Execute the graph synchronously.
        
        Args:
            initial_state: Initial state dictionary
            
        Returns:
            Final state after execution
        """
        if not self._compiled_graph:
            raise PlexoException(
                message="Graph not compiled. Call compile() first."
            )
        
        try:
            self._execution_count += 1
            
            self._logger.info(
                f"Executing graph {self.__class__.__name__}",
                extra={"execution_count": self._execution_count}
            )
            
            result = self._compiled_graph.invoke(initial_state)
            
            self._logger.info(
                f"Graph {self.__class__.__name__} completed",
                extra={"execution_count": self._execution_count}
            )
            
            return result
            
        except Exception as e:
            self._error_count += 1
            self._logger.error(
                f"Graph {self.__class__.__name__} execution failed: {e}",
                extra={
                    "execution_count": self._execution_count,
                    "error_count": self._error_count
                }
            )
            raise PlexoException(
                message=f"Graph execution failed: {self.__class__.__name__}",
                details={"error": str(e), "initial_state": initial_state}
            )

    async def aexecute(self, initial_state: AgentState) -> AgentState:
        """
        Execute the graph asynchronously.
        
        Args:
            initial_state: Initial state dictionary
            
        Returns:
            Final state after execution
        """
        if not self._compiled_graph:
            raise PlexoException(
                message="Graph not compiled. Call compile() first."
            )
        
        try:
            self._execution_count += 1
            
            self._logger.info(
                f"Executing async graph {self.__class__.__name__}",
                extra={"execution_count": self._execution_count}
            )
            
            result = await self._compiled_graph.ainvoke(initial_state)
            
            self._logger.info(
                f"Async graph {self.__class__.__name__} completed",
                extra={"execution_count": self._execution_count}
            )
            
            return result
            
        except Exception as e:
            self._error_count += 1
            self._logger.error(
                f"Async graph {self.__class__.__name__} execution failed: {e}",
                extra={
                    "execution_count": self._execution_count,
                    "error_count": self._error_count
                }
            )
            raise PlexoException(
                message=f"Async graph execution failed: {self.__class__.__name__}",
                details={"error": str(e), "initial_state": initial_state}
            )

    def stream(self, initial_state: AgentState):
        """
        Stream graph execution.
        
        Args:
            initial_state: Initial state dictionary
            
        Yields:
            State updates during execution
        """
        if not self._compiled_graph:
            raise PlexoException(
                message="Graph not compiled. Call compile() first."
            )
        
        try:
            self._logger.info(
                f"Streaming graph {self.__class__.__name__}"
            )
            
            for state in self._compiled_graph.stream(initial_state):
                yield state
                
        except Exception as e:
            self._logger.error(
                f"Graph {self.__class__.__name__} streaming failed: {e}"
            )
            raise PlexoException(
                message=f"Graph streaming failed: {self.__class__.__name__}",
                details={"error": str(e)}
            )

    async def astream(self, initial_state: AgentState):
        """
        Stream graph execution asynchronously.
        
        Args:
            initial_state: Initial state dictionary
            
        Yields:
            State updates during execution
        """
        if not self._compiled_graph:
            raise PlexoException(
                message="Graph not compiled. Call compile() first."
            )
        
        try:
            self._logger.info(
                f"Streaming async graph {self.__class__.__name__}"
            )
            
            async for state in self._compiled_graph.astream(initial_state):
                yield state
                
        except Exception as e:
            self._logger.error(
                f"Async graph {self.__class__.__name__} streaming failed: {e}"
            )
            raise PlexoException(
                message=f"Async graph streaming failed: {self.__class__.__name__}",
                details={"error": str(e)}
            )

    def get_stats(self) -> Dict[str, Any]:
        """
        Get graph execution statistics.
        
        Returns:
            Dictionary with graph stats
        """
        return {
            "name": self.__class__.__name__,
            "execution_count": self._execution_count,
            "error_count": self._error_count,
            "success_rate": (
                (self._execution_count - self._error_count) / self._execution_count
                if self._execution_count > 0
                else 0.0
            ),
            "compiled": self._compiled_graph is not None,
        }


class SimpleAgentGraph(BaseAgentGraph):
    """
    Simple agent graph with basic node structure.
    
    Provides a template for building simple linear agent graphs.
    """

    def __init__(self, nodes: List[tuple[str, Callable]]):
        """
        Initialize SimpleAgentGraph.
        
        Args:
            nodes: List of (node_name, node_function) tuples
        """
        super().__init__()
        self._nodes = nodes

    def build_graph(self) -> StateGraph:
        """
        Build simple linear graph.
        
        Returns:
            Configured StateGraph
        """
        graph = StateGraph(AgentState)
        
        for i, (node_name, node_func) in enumerate(self._nodes):
            graph.add_node(node_name, node_func)
            
            if i > 0:
                prev_node_name = self._nodes[i - 1][0]
                graph.add_edge(prev_node_name, node_name)
        
        if self._nodes:
            graph.set_entry_point(self._nodes[0][0])
            graph.add_edge(self._nodes[-1][0], END)
        
        return graph


class ConditionalAgentGraph(BaseAgentGraph):
    """
    Agent graph with conditional routing.
    
    Supports conditional edges based on state.
    """

    def __init__(self):
        """
        Initialize ConditionalAgentGraph.
        """
        super().__init__()
        self._nodes: Dict[str, Callable] = {}
        self._edges: List[tuple[str, str]] = []
        self._conditional_edges: List[tuple[str, Callable, Dict[str, str]]] = []
        self._entry_point: Optional[str] = None

    def add_node(self, name: str, func: Callable) -> None:
        """
        Add node to graph.
        
        Args:
            name: Node name
            func: Node function
        """
        self._nodes[name] = func

    def add_edge(self, from_node: str, to_node: str) -> None:
        """
        Add edge between nodes.
        
        Args:
            from_node: Source node name
            to_node: Target node name
        """
        self._edges.append((from_node, to_node))

    def add_conditional_edge(
        self,
        from_node: str,
        condition_func: Callable,
        condition_map: Dict[str, str]
    ) -> None:
        """
        Add conditional edge.
        
        Args:
            from_node: Source node name
            condition_func: Function that returns condition key
            condition_map: Map of condition keys to target nodes
        """
        self._conditional_edges.append((from_node, condition_func, condition_map))

    def set_entry_point(self, node_name: str) -> None:
        """
        Set graph entry point.
        
        Args:
            node_name: Entry node name
        """
        self._entry_point = node_name

    def build_graph(self) -> StateGraph:
        """
        Build conditional graph.
        
        Returns:
            Configured StateGraph
        """
        graph = StateGraph(AgentState)
        
        for name, func in self._nodes.items():
            graph.add_node(name, func)
        
        for from_node, to_node in self._edges:
            graph.add_edge(from_node, to_node)
        
        for from_node, condition_func, condition_map in self._conditional_edges:
            graph.add_conditional_edges(from_node, condition_func, condition_map)
        
        if self._entry_point:
            graph.set_entry_point(self._entry_point)
        
        return graph

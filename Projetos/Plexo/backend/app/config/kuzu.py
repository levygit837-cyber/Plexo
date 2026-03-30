"""
KuzuDB configuration for graph database and vector embeddings.

This module provides KuzuDB database management for storing
graph relationships and vector embeddings.
"""

from pathlib import Path
from typing import Optional

import kuzu

from .settings import get_settings


# Global KuzuDB instance
_kuzu_db: Optional[kuzu.Database] = None
_kuzu_conn: Optional[kuzu.Connection] = None


def get_kuzu_db() -> kuzu.Database:
    """
    Get or create the KuzuDB database instance.
    
    Returns:
        KuzuDB Database instance
    """
    global _kuzu_db
    if _kuzu_db is None:
        settings = get_settings()
        db_path = Path(settings.kuzu_db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        _kuzu_db = kuzu.Database(str(db_path))
    return _kuzu_db


def get_kuzu_connection() -> kuzu.Connection:
    """
    Get or create a KuzuDB connection.
    
    Returns:
        KuzuDB Connection instance
    """
    global _kuzu_conn
    if _kuzu_conn is None:
        db = get_kuzu_db()
        _kuzu_conn = kuzu.Connection(db)
    return _kuzu_conn


async def init_kuzu_schema() -> None:
    """
    Initialize KuzuDB schema for agents, memories, and embeddings.
    
    This creates the necessary node and relationship tables.
    """
    conn = get_kuzu_connection()
    
    # Create Agent node table
    conn.execute("""
        CREATE NODE TABLE IF NOT EXISTS Agent(
            id STRING,
            name STRING,
            type STRING,
            status STRING,
            capabilities STRING,
            created_at TIMESTAMP,
            PRIMARY KEY (id)
        )
    """)
    
    # Create Memory node table
    conn.execute("""
        CREATE NODE TABLE IF NOT EXISTS Memory(
            id STRING,
            agent_id STRING,
            content STRING,
            memory_type STRING,
            embedding FLOAT[],
            created_at TIMESTAMP,
            PRIMARY KEY (id)
        )
    """)
    
    # Create Task node table
    conn.execute("""
        CREATE NODE TABLE IF NOT EXISTS Task(
            id STRING,
            name STRING,
            status STRING,
            priority INT64,
            created_at TIMESTAMP,
            PRIMARY KEY (id)
        )
    """)
    
    # Create relationships
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS ASSIGNED_TO(
            FROM Task TO Agent,
            assigned_at TIMESTAMP
        )
    """)
    
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS HAS_MEMORY(
            FROM Agent TO Memory,
            created_at TIMESTAMP
        )
    """)
    
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS COMMUNICATES_WITH(
            FROM Agent TO Agent,
            message_count INT64,
            last_communication TIMESTAMP
        )
    """)


async def close_kuzu() -> None:
    """
    Close KuzuDB connections and cleanup resources.
    
    This should be called during application shutdown.
    """
    global _kuzu_conn, _kuzu_db
    if _kuzu_conn is not None:
        _kuzu_conn = None
    if _kuzu_db is not None:
        _kuzu_db = None


def execute_query(query: str, parameters: Optional[dict] = None) -> kuzu.QueryResult:
    """
    Execute a Cypher query on KuzuDB.
    
    Args:
        query: Cypher query string
        parameters: Optional query parameters
        
    Returns:
        Query result
    """
    conn = get_kuzu_connection()
    if parameters:
        return conn.execute(query, parameters)
    return conn.execute(query)


async def store_embedding(
    node_id: str,
    node_type: str,
    embedding: list[float],
    metadata: Optional[dict] = None,
) -> None:
    """
    Store a vector embedding in KuzuDB.
    
    Args:
        node_id: Unique identifier for the node
        node_type: Type of node (e.g., 'agent', 'memory', 'task')
        embedding: Vector embedding as list of floats
        metadata: Optional metadata dictionary
    """
    conn = get_kuzu_connection()
    
    # Store embedding based on node type
    if node_type == "memory":
        query = """
            MERGE (m:Memory {id: $id})
            SET m.embedding = $embedding
        """
        conn.execute(query, {"id": node_id, "embedding": embedding})


async def search_similar_embeddings(
    embedding: list[float],
    node_type: str = "memory",
    limit: int = 10,
) -> list[dict]:
    """
    Search for similar embeddings using cosine similarity.
    
    Args:
        embedding: Query embedding vector
        node_type: Type of nodes to search
        limit: Maximum number of results
        
    Returns:
        List of similar nodes with similarity scores
    """
    # Note: KuzuDB doesn't have built-in vector similarity search yet
    # This is a placeholder for future implementation
    # In production, you might want to use a dedicated vector database
    # or implement custom similarity calculation
    
    conn = get_kuzu_connection()
    
    if node_type == "memory":
        query = f"""
            MATCH (m:Memory)
            RETURN m.id AS id, m.content AS content, m.embedding AS embedding
            LIMIT {limit}
        """
        result = conn.execute(query)
        
        # Manual cosine similarity calculation
        # This is a simplified version - in production use optimized vector search
        results = []
        while result.has_next():
            row = result.get_next()
            results.append({
                "id": row[0],
                "content": row[1],
                "embedding": row[2],
            })
        
        return results
    
    return []
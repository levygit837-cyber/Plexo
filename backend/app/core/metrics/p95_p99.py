"""
Percentile calculation utilities for latency tracking.

This module provides functions to calculate P95 and P99 percentiles
for performance monitoring.
"""

from typing import List
import statistics


def calculate_percentile(values: List[float], percentile: float) -> float:
    """
    Calculate a specific percentile from a list of values.
    
    Args:
        values: List of numeric values
        percentile: Percentile to calculate (0-100)
        
    Returns:
        The calculated percentile value
        
    Raises:
        ValueError: If values list is empty or percentile is invalid
    """
    if not values:
        raise ValueError("Cannot calculate percentile of empty list")
    
    if not 0 <= percentile <= 100:
        raise ValueError("Percentile must be between 0 and 100")
    
    sorted_values = sorted(values)
    index = (percentile / 100) * (len(sorted_values) - 1)
    
    if index.is_integer():
        return sorted_values[int(index)]
    
    # Linear interpolation between two closest values
    lower_index = int(index)
    upper_index = lower_index + 1
    weight = index - lower_index
    
    return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight


def calculate_p95(values: List[float]) -> float:
    """
    Calculate the 95th percentile (P95) of a list of values.
    
    Args:
        values: List of numeric values (e.g., latencies in milliseconds)
        
    Returns:
        The P95 value
    """
    return calculate_percentile(values, 95.0)


def calculate_p99(values: List[float]) -> float:
    """
    Calculate the 99th percentile (P99) of a list of values.
    
    Args:
        values: List of numeric values (e.g., latencies in milliseconds)
        
    Returns:
        The P99 value
    """
    return calculate_percentile(values, 99.0)


def calculate_statistics(values: List[float]) -> dict:
    """
    Calculate comprehensive statistics for a list of values.
    
    Args:
        values: List of numeric values
        
    Returns:
        Dictionary containing mean, median, p50, p95, p99, min, max
    """
    if not values:
        return {
            "count": 0,
            "mean": 0.0,
            "median": 0.0,
            "p50": 0.0,
            "p95": 0.0,
            "p99": 0.0,
            "min": 0.0,
            "max": 0.0,
        }
    
    return {
        "count": len(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "p50": calculate_percentile(values, 50.0),
        "p95": calculate_p95(values),
        "p99": calculate_p99(values),
        "min": min(values),
        "max": max(values),
    }
"""
Metrics collector for system monitoring.

This module provides a centralized metrics collection system for tracking
latencies, throughput, and other performance metrics.
"""

from collections import defaultdict
from datetime import datetime, timedelta
from threading import Lock
from typing import Dict, List, Optional

from .p95_p99 import calculate_p95, calculate_p99, calculate_statistics


class MetricsCollector:
    """
    Collect and aggregate system metrics.
    
    This class provides thread-safe metric collection with automatic
    time-based windowing for calculating percentiles and statistics.
    """
    
    def __init__(self, window_size: int = 300):
        """
        Initialize the metrics collector.
        
        Args:
            window_size: Time window in seconds for metric retention (default: 5 minutes)
        """
        self._metrics: Dict[str, List[tuple[datetime, float]]] = defaultdict(list)
        self._lock = Lock()
        self._window_size = window_size
    
    def record_latency(self, endpoint: str, duration: float) -> None:
        """
        Record a latency measurement for an endpoint.
        
        Args:
            endpoint: The endpoint identifier (e.g., "GET /api/agents")
            duration: Duration in milliseconds
        """
        with self._lock:
            metric_key = f"latency.{endpoint}"
            self._metrics[metric_key].append((datetime.utcnow(), duration))
            self._cleanup_old_metrics(metric_key)
    
    def record_counter(self, name: str, value: float = 1.0) -> None:
        """
        Record a counter metric.
        
        Args:
            name: Counter name
            value: Value to add to the counter
        """
        with self._lock:
            metric_key = f"counter.{name}"
            self._metrics[metric_key].append((datetime.utcnow(), value))
            self._cleanup_old_metrics(metric_key)
    
    def record_gauge(self, name: str, value: float) -> None:
        """
        Record a gauge metric (point-in-time value).
        
        Args:
            name: Gauge name
            value: Current value
        """
        with self._lock:
            metric_key = f"gauge.{name}"
            self._metrics[metric_key].append((datetime.utcnow(), value))
            self._cleanup_old_metrics(metric_key)
    
    def get_p95(self, metric: str) -> float:
        """
        Get the P95 value for a metric.
        
        Args:
            metric: Metric name
            
        Returns:
            P95 value, or 0.0 if no data available
        """
        values = self._get_metric_values(metric)
        if not values:
            return 0.0
        return calculate_p95(values)
    
    def get_p99(self, metric: str) -> float:
        """
        Get the P99 value for a metric.
        
        Args:
            metric: Metric name
            
        Returns:
            P99 value, or 0.0 if no data available
        """
        values = self._get_metric_values(metric)
        if not values:
            return 0.0
        return calculate_p99(values)
    
    def get_statistics(self, metric: str) -> dict:
        """
        Get comprehensive statistics for a metric.
        
        Args:
            metric: Metric name
            
        Returns:
            Dictionary with count, mean, median, p50, p95, p99, min, max
        """
        values = self._get_metric_values(metric)
        return calculate_statistics(values)
    
    def get_all_metrics(self) -> Dict[str, dict]:
        """
        Get statistics for all collected metrics.
        
        Returns:
            Dictionary mapping metric names to their statistics
        """
        with self._lock:
            result = {}
            for metric_key in self._metrics.keys():
                values = [value for _, value in self._metrics[metric_key]]
                if values:
                    result[metric_key] = calculate_statistics(values)
            return result
    
    def clear_metrics(self, metric: Optional[str] = None) -> None:
        """
        Clear collected metrics.
        
        Args:
            metric: Specific metric to clear, or None to clear all
        """
        with self._lock:
            if metric:
                self._metrics.pop(metric, None)
            else:
                self._metrics.clear()
    
    def _get_metric_values(self, metric: str) -> List[float]:
        """
        Get all values for a metric within the time window.
        
        Args:
            metric: Metric name
            
        Returns:
            List of metric values
        """
        with self._lock:
            if metric not in self._metrics:
                return []
            return [value for _, value in self._metrics[metric]]
    
    def _cleanup_old_metrics(self, metric_key: str) -> None:
        """
        Remove metrics older than the window size.
        
        Args:
            metric_key: The metric key to clean up
        """
        cutoff_time = datetime.utcnow() - timedelta(seconds=self._window_size)
        self._metrics[metric_key] = [
            (timestamp, value)
            for timestamp, value in self._metrics[metric_key]
            if timestamp > cutoff_time
        ]


# Global metrics collector instance
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """
    Get the global metrics collector instance.
    
    Returns:
        The global MetricsCollector instance
    """
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector


def track_latency(endpoint: str, duration: float) -> None:
    """
    Convenience function to track endpoint latency.
    
    Args:
        endpoint: The endpoint identifier
        duration: Duration in milliseconds
    """
    collector = get_metrics_collector()
    collector.record_latency(endpoint, duration)
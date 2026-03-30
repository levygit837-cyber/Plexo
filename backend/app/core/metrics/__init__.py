"""Metrics collection module for Plexo system."""

from .collector import MetricsCollector, get_metrics_collector, track_latency
from .p95_p99 import (
    calculate_p95,
    calculate_p99,
    calculate_percentile,
    calculate_statistics,
)

__all__ = [
    # Percentile calculations
    "calculate_percentile",
    "calculate_p95",
    "calculate_p99",
    "calculate_statistics",
    # Metrics collector
    "MetricsCollector",
    "get_metrics_collector",
    "track_latency",
]
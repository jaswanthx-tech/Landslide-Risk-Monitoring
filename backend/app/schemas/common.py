"""
Common Enums and Value Types
"""

from enum import Enum


class RiskLevelEnum(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class SeverityEnum(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ReportStatusEnum(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    RESOLVED = "RESOLVED"


class PriorityLevelEnum(str, Enum):
    LOW = "LOW PRIORITY"
    MEDIUM = "MEDIUM PRIORITY"
    HIGH = "HIGH PRIORITY"
    CRITICAL = "CRITICAL PRIORITY"

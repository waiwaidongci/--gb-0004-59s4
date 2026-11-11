from enum import Enum
class Role(str,Enum):
    ADMIN='admin'
    ANALYST='analyst'
    VIEWER='viewer'
class RunStatus(str,Enum):
    QUEUED='queued'
    RUNNING='running'
    COMPLETED='completed'
    FAILED='failed'

from enum import StrEnum


class JobStatus(StrEnum):
    SUBMITTED = "submitted"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    ERROR = "error"


class JobType(StrEnum):
    TASK = "task"
    REVIEW = "review"

from datetime import date, datetime, time, timedelta
from enum import Enum
from typing import List, Optional, Type
from uuid import UUID

import pytest
from pydantic import (
    UUID3,
    UUID4,
    BaseModel,
    EmailStr,
    HttpUrl,
    IPvAnyAddress,
    ValidationError,
)
from pydantic.types import NegativeInt

from dydantic import create_model_from_schema


class StatusEnum(str, Enum):
    planning = "planning"
    active = "active"
    completed = "completed"
    archived = "archived"


class RoleEnum(str, Enum):
    owner = "owner"
    admin = "admin"
    contributor = "contributor"
    viewer = "viewer"


class TaskStatusEnum(str, Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class Member(BaseModel):
    user_id: UUID4
    role: RoleEnum
    joined_date: datetime


class SubTask(BaseModel):
    sub_task_id: UUID3
    name: str
    status: TaskStatusEnum


class Task(BaseModel):
    task_id: UUID
    name: str
    task_description: Optional[str] = None
    status: TaskStatusEnum
    priority: PriorityEnum
    assigned_to: List[UUID4] = []
    due_date: datetime
    sub_tasks: List[SubTask]


class Project(BaseModel):
    project_id: UUID4
    project_name: str
    start_date: datetime
    end_date: datetime
    status: StatusEnum
    budget: Optional[float] = None
    days_left: Optional[NegativeInt] = None
    members: List[Member] = []
    tasks: List[Task] = []


@pytest.mark.parametrize(
    "x, error_message",
    [
        # Test case 1: Valid input
        (
            {
                "project_id": "3dd68ce0-91af-4782-8fe0-3e5fd4ff9a57",
                "project_name": "Test Project",
                "start_date": "2022-01-01T00:00:00Z",
                "end_date": "2022-01-31T23:59:59Z",
                "status": "active",
                "budget": 1000.0,
                "members": [
                    {
                        "user_id": "ac77f482-0033-41d0-9f50-4730c6799661",
                        "role": "owner",
                        "joined_date": "2022-01-01T00:00:00Z",
                    },
                    {
                        "user_id": "ac77f482-0033-41d0-9f50-4730c6799661",
                        "role": "contributor",
                        "joined_date": "2022-01-02T00:00:00Z",
                    },
                ],
                "tasks": [
                    {
                        "task_id": "ac77f482-0033-41d0-9f50-4730c6799661",
                        "name": "Task 1",
                        "status": "not_started",
                        "priority": "medium",
                        "assigned_to": [
                            "ac77f482-0033-41d0-9f50-4730c6799661",
                            "ac77f482-0033-41d0-9f50-4730c6799661",
                        ],
                        "due_date": "2022-01-10T23:59:59Z",
                        "sub_tasks": [
                            {
                                "sub_task_id": "9073926b-929f-31c2-abc9-fad77ae3e8eb",
                                "name": "Subtask 1",
                                "status": "not_started",
                            },
                            {
                                "sub_task_id": "9073926b-929f-31c2-abc9-fad77ae3e8eb",
                                "name": "Subtask 2",
                                "status": "not_started",
                            },
                        ],
                    }
                ],
            },
            None,
        ),
        (
            {
                "project_id": "3dd68ce0-91af-4782-8fe0-3e5fd4ff9a57",
                "project_name": "Test Project",
                "start_date": "2022-01-01T00:00:00Z",
                "end_date": "My favorite day",
                "status": "active",
                "budget": 1000.0,
                "members": [],
                "tasks": [],
            },
            "1 validation error for Project\nend_date\n",
        ),
        # Test task ID is not a valid UUID
        (
            {
                "project_id": "3dd68ce0-91af-4782-8fe0-3e5fd4ff9a57",
                "project_name": "Test Project",
                "start_date": "2022-01-01T00:00:00Z",
                "end_date": "2022-01-31T23:59:59Z",
                "status": "active",
                "budget": 1000.0,
                "members": [],
                "tasks": [
                    {
                        # Bad UUID
                        "task_id": "Z23e4567-e89b-12d3-a456-426614174003",
                        "name": "Task 1",
                        "task_description": "Description 1",
                        "status": "not_started",
                        "priority": "medium",
                        "assigned_to": [],
                        "due_date": "2022-01-10T23:59:59Z",
                        "sub_tasks": [],
                    }
                ],
            },
            "2 validation errors for Project\ntasks",
        ),
    ],
)
def test_nested_create_model_from_schema(x: dict, error_message: Optional[str]):
    model = create_model_from_schema(Project.model_json_schema())
    if not error_message:
        model.model_validate(x)
    else:
        with pytest.raises(ValidationError, match=error_message):
            model.model_validate(x)


class DateModel(BaseModel):
    date_field: date


class TimeModel(BaseModel):
    time_field: time


class DateTimeModel(BaseModel):
    datetime_field: datetime


class DurationModel(BaseModel):
    duration_field: timedelta


class EmailModel(BaseModel):
    email_field: EmailStr


class IPv4Model(BaseModel):
    ipv4_field: IPvAnyAddress


class IPv6Model(BaseModel):
    ipv6_field: IPvAnyAddress


class UriModel(BaseModel):
    uri_field: HttpUrl


class UuidModel(BaseModel):
    uuid_field: UUID


@pytest.mark.parametrize(
    "model, inputs",
    [
        (DateModel, {"date_field": "2022-01-01"}),
        (DateModel, {"date_field": "invalid-date"}),
        (TimeModel, {"time_field": "12:34:56"}),
        (TimeModel, {"time_field": "invalid-time"}),
        (DateTimeModel, {"datetime_field": "2022-01-01T12:34:56Z"}),
        (DateTimeModel, {"datetime_field": "invalid-datetime"}),
        (DurationModel, {"duration_field": "P3DT12H30M5S"}),
        (DurationModel, {"duration_field": "invalid-duration"}),
        (EmailModel, {"email_field": "user@example.com"}),
        (EmailModel, {"email_field": "invalid-email"}),
        (IPv4Model, {"ipv4_field": "192.168.0.1"}),
        (IPv4Model, {"ipv4_field": "invalid-ipv4"}),
        (IPv6Model, {"ipv6_field": "2001:db8::8a2e:370:7334"}),
        (IPv6Model, {"ipv6_field": "invalid-ipv6"}),
        (UriModel, {"uri_field": "https://example.com"}),
        (UriModel, {"uri_field": "invalid-uri"}),
        (UuidModel, {"uuid_field": "123e4567-e89b-12d3-a456-426614174000"}),
        (UuidModel, {"uuid_field": "invalid-uuid"}),
    ],
)
def test_create_model_from_schema_formats(model: Type[BaseModel], inputs: dict):
    dynamic_model = create_model_from_schema(model.model_json_schema())
    dynamic_model.schema_json()  # test it is serializable
    dynamic_model.model_json_schema()  # test it is serializable
    error = None
    try:
        model.model_validate(inputs)
    except Exception as e:
        error = str(e)
    if not error:
        dynamic_model.model_validate(inputs)
    else:
        with pytest.raises(Exception):
            dynamic_model.model_validate(inputs)

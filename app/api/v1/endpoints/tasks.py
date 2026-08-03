import uuid

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    service = TaskService(db)
    task = service.create_task(user_id=current_user.id, payload=payload)
    return TaskResponse.model_validate(task)


@router.get("", response_model=TaskListResponse)
def list_tasks(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskListResponse:
    service = TaskService(db)
    result = service.list_tasks(
        user_id=current_user.id,
        page=page,
        size=size,
        search=search,
        status=status,
        priority=priority,
    )
    return TaskListResponse(**result)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: uuid.UUID | str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    service = TaskService(db)
    task = service.get_task(task_id=task_id, user_id=current_user.id)
    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: uuid.UUID | str,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    service = TaskService(db)
    task = service.update_task(task_id=task_id, user_id=current_user.id, payload=payload)
    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: uuid.UUID | str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    service = TaskService(db)
    service.delete_task(task_id=task_id, user_id=current_user.id)

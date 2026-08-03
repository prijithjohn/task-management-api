from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session) -> None:
        self.task_repo = TaskRepository(db)

    def create_task(self, *, user_id: uuid.UUID, payload: TaskCreate) -> dict[str, Any]:
        task_data = payload.model_dump()
        task = self.task_repo.create(user_id=user_id, task_data=task_data)
        return self._serialize_task(task)

    def get_task(self, *, task_id: uuid.UUID | str, user_id: uuid.UUID) -> dict[str, Any]:
        task = self.task_repo.get_by_id(task_id, user_id)
        if task is None:
            raise NotFoundException("Task not found")
        return self._serialize_task(task)

    def list_tasks(
        self,
        *,
        user_id: uuid.UUID,
        page: int,
        size: int,
        search: str | None = None,
        status: str | None = None,
        priority: str | None = None,
    ) -> dict[str, Any]:
        items, total = self.task_repo.list_for_user(
            user_id=user_id,
            page=page,
            size=size,
            search=search,
            status=status,
            priority=priority,
        )
        return {
            "items": [self._serialize_task(task) for task in items],
            "total": total,
            "page": page,
            "size": size,
        }

    def update_task(self, *, task_id: uuid.UUID | str, user_id: uuid.UUID, payload: TaskUpdate) -> dict[str, Any]:
        task = self.task_repo.get_by_id(task_id, user_id)
        if task is None:
            raise NotFoundException("Task not found")

        update_data = payload.model_dump(exclude_unset=True)
        task = self.task_repo.update(task, update_data)
        return self._serialize_task(task)

    def delete_task(self, *, task_id: uuid.UUID | str, user_id: uuid.UUID) -> None:
        task = self.task_repo.get_by_id(task_id, user_id)
        if task is None:
            raise NotFoundException("Task not found")
        self.task_repo.delete(task)

    def _serialize_task(self, task: Any) -> dict[str, Any]:
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date,
            "user_id": task.user_id,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
        }

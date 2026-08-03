from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.task import Task


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, *, user_id: uuid.UUID, task_data: dict[str, Any]) -> Task:
        task = Task(user_id=user_id, **task_data)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: uuid.UUID | str, user_id: uuid.UUID | str) -> Task | None:
        if isinstance(task_id, str):
            task_id = uuid.UUID(task_id)
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        return self.db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    def list_for_user(
        self,
        *,
        user_id: uuid.UUID,
        page: int,
        size: int,
        search: str | None = None,
        status: str | None = None,
        priority: str | None = None,
    ) -> tuple[list[Task], int]:
        query = self.db.query(Task).filter(Task.user_id == user_id)

        if search:
            search_filter = f"%{search.lower()}%"
            query = query.filter(or_(Task.title.ilike(search_filter), Task.description.ilike(search_filter)))

        if status:
            query = query.filter(Task.status == status)

        if priority:
            query = query.filter(Task.priority == priority)

        total = query.count()
        items = query.order_by(Task.created_at.desc()).offset((page - 1) * size).limit(size).all()
        return items, total

    def update(self, task: Task, task_data: dict[str, Any]) -> Task:
        for key, value in task_data.items():
            if value is not None:
                setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()

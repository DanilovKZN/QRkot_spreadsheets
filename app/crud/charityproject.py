from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_by_name(
            self,
            project_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        project_name = await session.execute(
            select(CharityProject).where(
                CharityProject.name == project_name
            )
        )
        project_name = project_name.scalars().first()
        return project_name


    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ):
        """Получаем все закрытые проекты, отсортированные по скорости закрытия."""

        def sort_collection_time(project_dict):
            collection_time = project_dict.close_date - project_dict.create_date
            return collection_time


        close_projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested)
        )
        close_projects = close_projects.scalars().all()
        return sorted(close_projects, key=sort_collection_time)


charity_project_crud = CRUDCharityProject(CharityProject)

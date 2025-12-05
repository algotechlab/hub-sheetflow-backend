from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.dtos.groups import GroupBaseDto, GroupOutDto
from src.core.domain.interface.groups import GroupsRepositoriesInterface
from src.core.domain.models.groups import Groups
from src.core.exceptions.custom import DatabaseException


class GroupsRepositoriesPostgres(GroupsRepositoriesInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_groups(self, groups: GroupBaseDto) -> GroupOutDto:
        try:
            print('Grupo coletado', groups)
            db_groups = Groups(**groups.model_dump())
            self.session.add(db_groups)
            await self.session.commit()
            await self.session.refresh(db_groups)
            return GroupOutDto.model_validate(db_groups)
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

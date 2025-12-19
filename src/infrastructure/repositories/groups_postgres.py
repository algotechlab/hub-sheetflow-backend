from typing import Union
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.groups import (
    GroupBaseDto,
    GroupOutDto,
    GroupsListOutDto,
    GroupsMappingsDto,
    GroupsMappingsOutDto,
    GroupsMappinsgListOutDto,
    GroupsUpdateDto,
)
from src.core.domain.interface.groups import GroupsRepositoriesInterface
from src.core.domain.models.groups import Groups
from src.core.domain.models.mappings_groups import MappingsGroups
from src.core.exceptions.custom import DatabaseException


class GroupsRepositoriesPostgres(GroupsRepositoriesInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __add_mappings_groups(self, groups_id: UUID):
        try:
            db_mappings_groups = MappingsGroups(groups_id=groups_id)
            self.session.add(db_mappings_groups)
            await self.session.commit()
            return True
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def add_groups(self, groups: GroupBaseDto) -> GroupOutDto:
        try:
            db_groups = Groups(**groups.model_dump())
            self.session.add(db_groups)
            await self.session.commit()
            await self.session.refresh(db_groups)
            return GroupOutDto.model_validate(db_groups)
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def list_groups(self):
        try:
            query = (
                select(
                    Groups.id,
                    Groups.name,
                    Groups.created_at,
                    Groups.updated_at,
                )
                .where(Groups.is_deleted.__eq__(False))
                .order_by(Groups.created_at)
            )

            result = await self.session.execute(query)
            return [
                GroupsListOutDto.model_validate(row._mapping) for row in result.all()
            ]
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def update_group(
        self, group_id: UUID, group: GroupsUpdateDto
    ) -> Union[GroupOutDto, None]:
        try:
            update_data = group.model_dump(exclude_unset=True)

            stmt = (
                update(Groups)
                .where(Groups.id.__eq__(group_id), Groups.is_deleted.__eq__(False))
                .values(**update_data)
                .returning(Groups)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_group = result.scalar_one_or_none()

            if updated_group is None:
                return None

            return GroupOutDto.model_validate(updated_group)

        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def delete_group(self, group_id: UUID) -> bool:
        try:
            stmt = (
                update(Groups)
                .where(Groups.id.__eq__(group_id), Groups.is_deleted.__eq__(False))
                .values(is_deleted=True)
                .returning(Groups)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_group = result.scalar_one_or_none()

            return updated_group is not None
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def list_users_to_grupo(
        self, pagination: PaginationParamsDTO, group_id: UUID
    ):
        try:
            query = (
                select(
                    MappingsGroups.id,
                    MappingsGroups.name,
                    MappingsGroups.depedencias_pid,
                    MappingsGroups.localidade,
                    MappingsGroups.nome,
                    MappingsGroups.contato,
                    MappingsGroups.pasta_drive,
                    MappingsGroups.cpf_cnpj,
                    MappingsGroups.senha_portal,
                    MappingsGroups.aba_plataforma,
                    MappingsGroups.status,
                    MappingsGroups.data_atual,
                    MappingsGroups.data_intimacao,
                    MappingsGroups.prazo,
                    MappingsGroups.data_final,
                    MappingsGroups.oficio,
                    MappingsGroups.valor_indenizacao,
                    MappingsGroups.valor_honorario,
                    MappingsGroups.observacao,
                    MappingsGroups.groups_id,
                    MappingsGroups.created_at,
                    MappingsGroups.updated_at,
                )
                .where(
                    MappingsGroups.is_deleted.__eq__(False),
                    MappingsGroups.groups_id.__eq__(group_id),
                )
                .order_by(MappingsGroups.created_at)
            )

            if pagination.filter_by and pagination.filter_value:
                query = query.filter(
                    getattr(MappingsGroups, pagination.filter_by).__eq__(
                        pagination.filter_value
                    )
                )

            result = await self.session.execute(query)
            return [
                GroupsMappinsgListOutDto.model_validate(row._mapping)
                for row in result.all()
            ]
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def add_user_to_group(
        self, group_id: UUID, mappings: GroupsMappingsDto
    ) -> GroupsMappingsOutDto:
        try:
            mappings_dto = MappingsGroups(groups_id=group_id, **mappings.model_dump())
            self.session.add(mappings_dto)
            await self.session.commit()
            await self.session.refresh(mappings_dto)
            return GroupsMappingsOutDto.model_validate(mappings_dto)
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def updated_user_to_group(
        self, group_id: UUID, mappings: GroupsMappingsDto
    ) -> GroupsMappingsOutDto:
        try:
            update_data = mappings.model_dump(exclude_unset=True)

            stmt = (
                update(MappingsGroups)
                .where(
                    MappingsGroups.id.__eq__(group_id),
                    MappingsGroups.is_deleted.__eq__(False),
                )
                .values(**update_data)
                .returning(MappingsGroups)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_group = result.scalar_one_or_none()

            if updated_group is None:
                return None

            return GroupsMappingsOutDto.model_validate(updated_group)
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def delete_user_to_group(self, group_id: UUID, user_id: UUID):
        try:
            stmt = (
                update(MappingsGroups)
                .where(
                    MappingsGroups.groups_id.__eq__(group_id),
                    MappingsGroups.is_deleted.__eq__(False),
                    MappingsGroups.id.__eq__(user_id),
                )
                .values(is_deleted=True)
                .returning(MappingsGroups)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            updated_group = result.scalar_one_or_none()

            return updated_group is not None
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def transfer_user_to_group(self, group_id: UUID, user_id: UUID) -> None:
        try:
            stmt = (
                update(MappingsGroups)
                .where(
                    MappingsGroups.id.__eq__(user_id),
                    MappingsGroups.is_deleted.is_(False),
                )
                .values(groups_id=group_id)
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

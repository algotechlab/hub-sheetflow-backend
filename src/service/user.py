from sqlalchemy import func, select

from src.db.database import db
from src.model.user import User
from src.utils.metadata import ApiResponse, ModelSerializer
from src.utils.pagination import Pagination


class UserService:
    def __init__(self, user_id: int, *args, **kwargs):
        self.user_id = user_id
        self.user = User
        self.db_session = db.session

    def list_users(self, data: dict) -> ApiResponse:
        try:
            # filtro
            pagination = Pagination(data)
            pagination_params, error = pagination.validate_params()
            if error:
                return ApiResponse(
                    status_code=400,
                    message_id="invalid_pagination_params",
                    error=True,
                ).to_response()

            # query
            stmt = select(self.user.id, self.user.name, self.user.email).where(
                self.user.is_deleted.__eq__(False)
            )

            # aplicando o filtro, sorty by e paginação
            if pagination_params.filter_by:
                filter_value = f"%{pagination_params.filter_by}%"
                try:
                    stmt = stmt.filter(
                        func.unaccent(self.user.name).ilike(
                            func.unaccent(filter_value)
                        )
                    )
                except Exception:
                    stmt = stmt.filter(self.user.name.ilike(filter_value))

            sort_column = getattr(self.user, pagination_params.order_by, None)
            if sort_column:
                stmt = stmt.order_by(
                    sort_column.asc()
                    if pagination_params.sort_by == "asc"
                    else sort_column.desc()
                )

            total_count = db.session.execute(
                select(func.count()).select_from(stmt.subquery())
            ).scalar()

            paginated_stmt = stmt.offset(
                (pagination_params.current_page - 1)
                * pagination_params.rows_per_page
            ).limit(pagination_params.rows_per_page)

            result = db.session.execute(paginated_stmt).fetchall()

            metadata = pagination.build_metadata(
                total_count, pagination_params
            )
            serializer = ModelSerializer(result)
            serialized_data = serializer.to_list()

            return ApiResponse(
                status_code=200,
                data=serialized_data,
                message_id="list_users_success",
                error=False,
                metadata=metadata if metadata else {},
            ).to_response()

        except Exception:
            self.db_session.rollback()
            return ApiResponse(
                status_code=500,
                data=None,
                message_id="something_went_wrong",
                error=True,
            ).to_response()

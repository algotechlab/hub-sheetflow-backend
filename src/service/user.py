from sqlalchemy import func, select

from src.db.database import db
from src.model.user import User
from src.utils.metadata import ApiResponse, ModelSerializer
from src.utils.pagination import Pagination
from src.utils.security import get_password_hash


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

    def add_user(self, data: dict) -> ApiResponse:
        try:
            # 1. Validação de campos obrigatórios
            required_fields = ["name", "email", "password", "role"]
            if not all(key in data for key in required_fields):
                return ApiResponse(
                    status_code=400,
                    message_id="missing_fields",
                    error=True,
                    data={"required": required_fields},
                ).to_response()

            email = data.get("email")

            stmt = select(self.user).where(
                self.user.email.__eq__(email),
                self.user.is_deleted.__eq__(False),
            )
            existing_user = self.db_session.execute(stmt).scalar_one_or_none()

            if existing_user:
                return ApiResponse(
                    status_code=400,
                    message_id="email_already_registered",
                    error=True,
                ).to_response()

            hashed_password = get_password_hash(data.get("password"))

            new_user = self.user(
                name=data.get("name"),
                email=email,
                password_hash=hashed_password,
                role=data.get("role"),
                is_deleted=False,  # Garantindo default
            )

            # 5. Persistência
            self.db_session.add(new_user)
            self.db_session.commit()

            # 6. Serialização Manual (para retorno limpo sem senha)
            return ApiResponse(
                status_code=201,
                message_id="user_created_success",
                error=False,
            ).to_response()

        except Exception as e:
            # Log do erro real pode ser útil aqui: print(e) ou logger.error(e)
            self.db_session.rollback()
            return ApiResponse(
                status_code=500,
                data=None,
                message_id="something_went_wrong",
                error=True,
            ).to_response()

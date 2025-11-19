import traceback

from flask import jsonify, request
from flask_cors import cross_origin
from flask_restx import Namespace, Resource, fields, reqparse

from src.resource.commons.pagination import PaginationArguments
from src.service.user import UserService


pagination_arguments = reqparse.RequestParser()
PaginationArguments.add_to_parser(pagination_arguments)

user_us = Namespace("users", description="Manager users")

# TODO - ajustar esse payload de acordo com oque pede na US
payload_add_users = user_us.model(
    "PayloadAddUser",
    {
        "username": fields.String(
            required=True, example="User name", max_length=120
        ),
        "phone": fields.String(
            required=True, example="User phone", max_length=40
        ),
        "email": fields.String(
            required=False, example="User email", max_length=120
        ),
        "password": fields.String(
            required=True, example="User password", max_length=300
        ),
    },
)

# TODO - ajustar esse payload de acordo com oque pede na US
payload_update_users = user_us.model(
    "PayloadUpdateUser",
    {
        "username": fields.String(
            required=False, example="User name", max_length=120
        ),
        "phone": fields.String(
            required=True, example="User phone", max_length=40
        ),
        "email": fields.String(
            required=False, example="User email", max_length=120
        ),
        "password": fields.String(
            required=False, example="User password", max_length=300
        ),
    },
)


@user_us.route("")
class UserResource(Resource):
    @user_us.doc(description="List Users")
    @user_us.expect(pagination_arguments, validate=True)
    @cross_origin()
    def get(self):
        """List users"""
        try:
            user_id = request.headers.get("Id", request.environ.get("Id"))
            return UserService(user_id=user_id).list_users(
                request.args.to_dict()
            )
        except Exception:
            return jsonify(
                {
                    "status_code": 500,
                    "message_id": "something_went_wrong",
                    "traceback": traceback.format_exc(),
                }
            )

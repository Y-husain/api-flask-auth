"""Handle Requests routes."""
from flask_restplus import Resource, Namespace, fields
from app.models.request import requests_data, Request
from app.models.token import token_required
from flask import request

request_namespace = Namespace('user', description='Request Related Operation.')

request_model = request_namespace.model(
    'request_model', {
        'Request':
        fields.String(
            required=True,
            description='Create a request',
            example='plumbering'),
        'Category':
        fields.String(
            required=True,
            description="Category which request belongs",
            example="Maintenance/Repair"),
        'Location':
        fields.String(
            required=True,
            description="Area",
            example="EASTMAERT St 45F Hurlin"),
        'Duration':
        fields.String(
            required=True,
            description="How long do the request take",
            example="3-7 weeks")
    })


@request_namespace.route('/requests')
@request_namespace.doc(
    responses={
        200: 'Requests found successfully',
        404: 'Requests not found',
        201: 'Request successfully created',
        400: 'Invalid parameters provided'
    },
    security='apikey')
class UserReaquests(Resource):
    """Handles requests [GET] endpoint routes"""

    @token_required
    def get(self, current_user):
        """Fetch all the requests of a logged in user."""
        return requests_data

    @token_required
    @request_namespace.expect(request_model)
    def post(self, current_user):
        """Create a request."""
        data = request.get_json()
        user_request = data["Request"]
        category = data["Category"]
        duration = data["Duration"]
        location = data["Location"]

        reqst = Request(user_request, duration, location, category)
        reqst.create()

        return {"status": " Request successfully created"}, 201


@request_namespace.route('/requests/<int:requestID>')
@request_namespace.doc(
    responses={
        201: 'Request successfully updated!',
        400: 'Invalid parameters provided',
        404: 'Requests not found',
        403: 'Access Denied'
    },
    security="apikey")
class UpdateRequest(Resource):
    """Handle [UPDATE] endpoint routes with ID """

    @token_required
    def get(self, current_user, requestID):
        """Fetch a request that belongs to a logged in user"""
        a_req = [req for req in requests_data if req['ID'] == requestID]
        if len(a_req) == 0:
            return {'message': 'No request found'}
        return a_req

    @token_required
    @request_namespace.expect(request_model)
    def put(self, current_user, requestID):
        """Modify a request."""
        update_data = [
            req_data for req_data in requests_data
            if req_data["ID"] == requestID
        ]
        if len(update_data) == 0:
            return {'message': 'No request found'}
        else:
            data = request.get_json()
            update_data[0]["Request"] = data["Request"]
            update_data[0]["Category"] = data["Category"]
            update_data[0]["Duration"] = data["Duration"]
            update_data[0]["Location"] = data["Location"]

            return {"status": " Request successfully created"}, 201

    @token_required
    @request_namespace.expect(request_model)
    def delete(self, current_user, requestID):
        del requests_data[requestID]
        return {"status": "Request successfully deleted"}
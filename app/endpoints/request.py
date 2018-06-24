"""Handle Requests routes."""
from flask_restplus import Resource, Namespace, fields
from app.models.request import requests_data, Request
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
    })
@request_namespace.route('/requests')
@request_namespace.doc(
    responses={
        200: 'Requests found successfully',
        404: 'Requests not found',
        201: 'Request successfully created',
        400: 'Invalid parameters provided'
    })
class UserReaquests(Resource):
    """Handles requests [GET] endpoint routes"""

    def get(self):
        """Fetch all the requests of a logged in user."""
        return requests_data

    @request_namespace.expect(request_model)
    def post(self):
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
    })
class UpdateRequest(Resource):
    """Handle [UPDATE] endpoint routes with ID """

    def get(self, requestID):
        """Fetch a request that belongs to a logged in user"""
        return requests_data[requestID]

    @request_namespace.expect(request_model)
    def put(self, requestID):
        """Modify a request."""
        data = request.get_json(requestID)
        user_request = data["Request"]
        category = data["Category"]
        duration = data["Duration"]
        location = data["Location"]
        reqst_update = Request(user_request, duration, location, category)
        reqst_update.create()

        return {"status": "Request successfully updated"}

    @request_namespace.expect(request_model)
    def delete(self, requestID):
        del requests_data[requestID]
        return {"status": "Request successfully deleted"}
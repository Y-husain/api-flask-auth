requests_data = []


class Request:
    """request of the user"""
    requestID = 0

    def __init__(self, request, duration, location, category):
        self.request = request
        self.duration = duration
        self.location = location
        self.category = category

    def create(self):
        my_request = {
            "ID": Request.requestID,
            "Request": self.request,
            "Duration": self.duration,
            "Location": self.location,
            "category": self.category
        }
        Request.requestID += 1
        return requests_data.append(my_request)

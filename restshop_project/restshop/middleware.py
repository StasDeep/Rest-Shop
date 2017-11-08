from rest_framework.response import Response


class JsonApiMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if isinstance(response, Response) and response.accepted_media_type == 'application/json':
            data = response.data
            response.data = {}

            if response.status_code >= 400:
                response.data['error'] = data
            elif data is None:
                response.data['data'] = data
            elif 'detail' in data and isinstance(data['detail'], str) and data['detail'].startswith('Session'):
                # Session authentication returns "detail" message which is unnecessary.
                response.data['data'] = None
            elif 'meta' in data:
                # If "meta" key is in data, then "data" key is there, too.
                response.data = data
            else:
                response.data['data'] = data

            response.data['status'] = response.status_code

            # Need to change private attribute `_is_render` to call render second time.
            response._is_rendered = False
            response.render()

        return response

import json

from TestAlice.WebInterfaceApp.models import UserRequest


def save_request_middleware(get_response):
    def middleware(request):
        if request.path == '/':
            parsed = json.loads(request.read())
            request.parsed_body = parsed
            try:
                UserRequest(user_id=parsed['session']['user_id'],
                            session_id=parsed['session']['session_id'],
                            command=parsed['request']['command']).save()
            except KeyError:
                pass
        response = get_response(request)
        return response
    return middleware

import json
from django.http import HttpResponse

from TestAlice.AliceSkillApp.command_process import process_command


def alice_handler(request):
    parsed = request.parsed_body if hasattr(request, 'parsed_body') else json.loads(request.read())

    answer = process_command(command_str=parsed['request']['command'],
                             entities=parsed['request']['nlu']['entities'],
                             session_id=parsed['session']['session_id'])
    answer_prepared = '\n---\n'.join(answer) if isinstance(answer, list) else answer
    response = {
        "version": parsed['version'],
        "session": parsed['session'],
        "response": {
            "text": answer_prepared,
            "end_session": False
        }
    }

    return HttpResponse(json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    ))

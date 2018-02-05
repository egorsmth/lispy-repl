from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from backend.lispy.input_handler import parse as parse_lispy
from backend.lispy.outhput_handler import eval_lispy


# Create your views here.
@require_GET
def index(request):
    return render(request, 'index.html')


@require_POST
def evaluate(request):
    print(request.POST)
    code = request.POST['code']
    try:
        parsed = parse_lispy(code)
        evaled, err = eval_lispy(parsed)
        print('ok', type(evaled))
        if err is None:
            resp = {
                'result': 'success',
                'out': evaled,
            }
        else:
            resp = {
                'result': 'error',
                'out': err
            }
        return JsonResponse(resp)
    except Exception as e:
        return JsonResponse({
            'result': 'error',
            'out': e.__str__()
        })

from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')


def evaluate(request):
    code = request.POST['code']
    parsed = parse_lispy(code)
    err, evaled = eval_lispy(parsed)
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
    return json_response(request, json.serialize(resp))
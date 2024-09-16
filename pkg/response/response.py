from django.http import JsonResponse


class APIResponse(JsonResponse):
    def __init__(self, code=0, msg="", data={}):
        data = {"code": code, "msg": msg, "data": data}
        super().__init__(data=data, safe=True)

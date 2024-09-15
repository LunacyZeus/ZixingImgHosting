from django.shortcuts import render

from pkg.response.response import APIResponse


# Create your views here.

def index_view(request):
    return APIResponse(code=0, msg="success")

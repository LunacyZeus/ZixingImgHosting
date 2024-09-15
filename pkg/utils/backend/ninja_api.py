from typing import Any, List, Dict

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from ninja import Field, Schema
from ninja.pagination import PaginationBase
from ninja.types import DictStrAny
from ninja_extra import NinjaExtraAPI
from ninja_extra import exceptions


class CustomNinjaAPI(NinjaExtraAPI):
    def create_response(
            self, request: HttpRequest, data: Any, *, status: int = 200, code: int = 2000, msg: str = "success",
            temporal_response: HttpResponse = None,
    ) -> HttpResponse:
        std_data = {
            "code": code,
            "result": data,
            "message": msg,
            "success": True
        }
        content = self.renderer.render(request, std_data, response_status=status)
        content_type = "{}; charset={}".format(
            self.renderer.media_type, self.renderer.charset
        )

        return HttpResponse(content, status=status, content_type=content_type)

    def api_exception_handler(
            self, request: HttpRequest, exc: exceptions.APIException
    ) -> HttpResponse:
        headers: Dict = {}
        if isinstance(exc, exceptions.Throttled):
            headers["Retry-After"] = "%d" % float(exc.wait or 0.0)

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {"detail": exc.detail}

        '''
        data = {
            "code": -1,
            "msg": exc.detail,
            "data": data,
        }
        '''

        data = {
            "code": -1,
            "result": data,
            "message": exc.detail,
            "success": True
        }

        response = self.create_response(request, data, status=exc.status_code)
        for k, v in headers.items():
            response.setdefault(k, v)

        return response


class MyPagination(PaginationBase):
    class Input(Schema):
        pageSize: int = Field(10, gt=0)
        page: int = Field(1, gt=-1)

    class Output(Schema):
        items: List[Any]
        total: int

    def paginate_queryset(
            self,
            queryset: QuerySet,
            pagination: Input,
            **params: DictStrAny,
    ) -> Any:
        offset = pagination.pageSize * (pagination.page - 1)
        limit: int = pagination.pageSize
        return {
            "page": offset,
            "limit": limit,
            "items": queryset[offset: offset + limit],
            "total": self._items_count(queryset),
        }  # noqa: E203


class FuFilters(Schema):
    creator_id: int = Field(None, alias="creator_id")
    belong_dept: int = Field(None, alias="belong_dept")
    belong_dept__in: List[int] = Field(None, alias="belong_dept__in")

class InvalidToken(Exception):
    pass

class NoPermissionToken(Exception):
    pass
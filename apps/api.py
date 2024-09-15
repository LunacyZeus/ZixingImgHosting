from pkg.utils.backend.ninja_api import CustomNinjaAPI, InvalidToken, NoPermissionToken

ninja_api = CustomNinjaAPI(
    title="图床API",
    description="图床管理",
    urls_namespace="img_hosting",
    # auth=GlobalAuth(),
)
ninja_api.auto_discover_controllers()


@ninja_api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    return ninja_api.create_response(request, {"detail": "Invalid token supplied"}, status=401)


@ninja_api.exception_handler(NoPermissionToken)
def on_no_permission(request, exc):
    return ninja_api.create_response(request, {"detail": "no permission"}, status=403)

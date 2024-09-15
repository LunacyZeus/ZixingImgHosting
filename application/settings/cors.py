ALLOWED_HOSTS = ("*",)

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

CSRF_TRUSTED_ORIGINS = (
    "http://localhost:3000/",
    "http://120.79.195.0:8304/",
)

# CORS_REPLACE_HTTPS_REFERER = True

# CSRF_COOKIE_DOMAIN = '*.66daili.cn'

CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "http://120.79.195.0:8304",
)

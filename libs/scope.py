"""
访问权限配置
"""

from fastapi import Request


class Scope:
    allow_api = []
    allow_module = []
    forbidden = []

    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))

        return self


class UserScope(Scope):
    """用户权限"""

    allow_module = ["auth", "user", "role", "permission"]
    # 不允许访问
    forbidden = []

    def __init__(self):
        pass


class AdminScope(Scope):
    """管理员权限"""

    allow_module = []

    def __init__(self):
        self + UserScope()


def is_in_scope(scope: str, request: Request):
    """用户权限验证"""
    scope = globals()[scope]()
    scopes = request.url.path.split("/")
    scopes = scopes[2:]
    route = scopes[0]
    endpoint = "+".join(scopes)

    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if route in scope.allow_module:
        return True
    else:
        return False

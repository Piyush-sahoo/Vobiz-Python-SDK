# -*- coding: utf-8 -*-
class VobizRestError(Exception):
    pass


class AuthenticationError(VobizRestError):
    pass


class InvalidRequestError(VobizRestError):
    pass


class VobizServerError(VobizRestError):
    pass


class VobizXMLError(VobizRestError):
    pass


class ResourceNotFoundError(VobizRestError):
    pass


class ValidationError(VobizRestError):
    pass


class ForbiddenError(VobizRestError):
    pass

class GeoPermissionError(VobizRestError):
    pass

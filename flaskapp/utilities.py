from dataclasses import dataclass
from enum import Enum, unique

from flask import redirect, url_for, flash





@unique
class BootStrapMsgCategory(Enum):
    DANGER="danger"
    WARNING="warning"
    PRIMARY="primary"

@dataclass
class ResponseData():
    code: int
    message: str
    category: BootStrapMsgCategory

    def __post_init__(self):
        self.category = self.category.value


@unique
class ResponseCode(Enum):
    # INFORMATIONAL RESPONSES (100–199)
    CONTINUE = ResponseData(code=100,
                            message="Continue",
                            category=BootStrapMsgCategory.PRIMARY)
    SWITCHING_PROTOCOL = 101
    PROCESSING = 102
    EARLY_HINTS = 103

    # SUCCESSFUL RESPONSES (200–299)
    OK = ResponseData(code=200,
                        message="OK.",
                        category=BootStrapMsgCategory.PRIMARY)

    CREATED = ResponseData(code=201,
                            message="Member created.",
                            category=BootStrapMsgCategory.PRIMARY)
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206
    MULTI_STATUS = 207
    ALREADY_REPORTED = 208
    IM_USED = 226

    # REDIRECTS (300–399)
    MULTIPLE_CHOICE = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    USE_PROXY = 305
    UNUSED = 306
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308

    # CLIENT ERRORS (400–499)
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    REQUESTED_RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    IM_A_TEAPOT = 418
    MISDIRECTED_REQUEST = 421
    UNPROCESSABLE_ENTITY = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    TOO_EARLY = 425
    UPGRADE_REQUIRED = 426
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    UNAVAILABLE_FOR_LEGAL_REASONS = 451

    USER_ALREADY_EXISTS = ResponseData(code=460,
                            message="Member already exists.",
                            category=BootStrapMsgCategory.WARNING)

    USER_DOES_NOT_EXIST = ResponseData(code=461,
                            message="Member does not exist.",
                            category=BootStrapMsgCategory.WARNING)

    BAD_PASSWORD = ResponseData(code=462,
                            message="Bad password for member.",
                            category=BootStrapMsgCategory.WARNING)

    # SERVER ERRORS (500–599)
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
    VARIANT_ALSO_NEGOTIATES = 506
    INSUFFICIENT_STORAGE = 507
    LOOP_DETECTED = 508
    NOT_EXTENDED = 510
    NETWORK_AUTHENTICATION_REQUIRED = 511



def reroute(endpoint, response_code):
    response_data = response_code.value
    flash(response_data.message,
          category=response_data.category)

    return redirect(url_for(endpoint), response_data.code)
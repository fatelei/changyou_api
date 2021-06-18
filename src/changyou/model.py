from dataclasses import dataclass


@dataclass
class CommonReponse(object):

    request_id: str
    hmac: str
    result_code: str
    sign_type: str
    reserved_1: str
    reserved_2: str
    partener_id: str
    inter_code: str
    type: str
    message: str
    version: str


@dataclass
class QueryCMCCBalanceResponse(CommonReponse):

    points: int


@dataclass
class RegisterPageResponse(object):

    url: str


@dataclass
class QueryOrderResponse(CommonReponse):

    status: str
    order_id: str
    

@dataclass
class PlaceOrderResponse(CommonReponse):

    out_token_id: str
    order_id: str
    good_order_id: str
    points: str
    trans_time: str
    cmcc_mobile: str


@dataclass
class DetectOrderResponse(object):

    result_code: str
    message: str


@dataclass
class CmccSmsResponse(CommonReponse):

    order_id: str
    mobile: str
    sms_status: str


@dataclass
class CancelOrderResponse(CommonReponse):

    good_order_id: str
    points: str
    status: str


@dataclass
class CheckoutOrderResponse(CommonReponse):

    good_order_id: str


@dataclass
class SendPaySmsResponse(object):

    result_code: str
    message: str


@dataclass
class ExchangeResponse(object):

    order_id: str
    mobile: str
    trans_time: str
    good_order_id: str
    result_code: str
    out_token_id: str
    message: str


@dataclass
class QueryChangyoPointsResponse(CommonReponse):

    out_token_id: str
    points: str

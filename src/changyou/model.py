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
class DetectOrderResponse(CommonReponse):

    out_token_id: str
    order_id: str
    good_order_id: str
    mobile: str
    trans_status: str
    trans_time: str


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

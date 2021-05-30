import requests
from datetime import datetime
from typing import Tuple
from typing import OrderedDict
from typing import Union

from .exception import BadRequest
from .exception import InternalServerError
from .exception import MobileRequiredException

from .model import CancelOrderResponse
from .model import CmccSmsResponse
from .model import DetectOrderResponse
from .model import QueryCMCCBalanceResponse
from .model import QueryOrderResponse
from .model import PlaceOrderResponse
from .utils import helper


class ChangyouClient(object):

    def __init__(self, auth_token: str, sign_key: str, endpoint: str, public_ip: str, partener_id: str):
        self.auth_token = auth_token
        self.sign_key = sign_key
        self.endpoint = endpoint
        self.public_ip = public_ip
        self.partener_id = partener_id

    def query_cmcc_balance(self,
                           mobile: str,
                           channel_source: str,
                           out_token_id: str,
                           callback_url: str,
                           out_type: str,
                           reserved_1: Union[str, None] = None,
                           reserved_2: Union[str, None] = None) -> QueryCMCCBalanceResponse:
        if not mobile:
            raise MobileRequiredException()
        common_param = self.common_param('CYS0001')
        return self.__do_post_request('/partner-gateway/points/output/queryCmccBalance', common_param.update(OrderedDict({
            'mobile': mobile,
            'outTokenId': out_token_id,
            'outType': out_type,
            'callbackUrl': callback_url,
            'channelSource': channel_source,
            'reserved1': reserved_1 if reserved_1 is not None else '',
            'reserved2': reserved_2 if reserved_2 is not None else ''
        })))
    
    def query_order(self,
                    order_id: str,
                    order_date: str,
                    out_token_id: str,
                    reserved_1: Union[str, None] = None,
                    reserved_2: Union[str, None] = None) -> QueryOrderResponse:
        try:
            datetime.strptime(order_date, '%Y%m%d')
        except ValueError:
            raise BadRequest(f'{order_date} 格式应为 YYYYMMDD 格式')
        common_param = self.common_param('CYS0002')
        return self.__do_post_request('/partner-gateway/points/output/queryOrder', common_param.update(OrderedDict({
            'orderId': order_id,
            'orderDate': order_date,
            'outTokenId': out_token_id,
            'reserved1': reserved_1 if reserved_1 is not None else '',
            'reserved2': reserved_2 if reserved_2 is not None else ''
        })))

    def place_order(self,
                    out_token_id: str,
                    points: str,
                    goods_info: str,
                    session_id: str,
                    finger_print: str,
                    reserved_1: Union[str, None] = None,
                    reserved_2: Union[str, None] = None,
                    reserved_3: Union[str, None] = None,
                    reserved_4: Union[str, None] = None) -> PlaceOrderResponse:
        common_param = self.common_param('CYS0003')
        return self.__do_post_request('/partner-gateway/points/output/placeOrder', common_param.update(OrderedDict({
            'outTokenId': out_token_id,
            'points': points,
            'goodsInfo': goods_info,
            'reserved1': reserved_1 if reserved_1 is not None else '',
            'reserved2': reserved_2 if reserved_2 is not None else '',
            'reserved3': reserved_3 if reserved_1 is not None else '',
            'reserved4': reserved_4 if reserved_2 is not None else '',
            'sessionId': session_id,
            'fingerprint': finger_print
        })))
    
    def detect_order(self,
                     out_token_id: str,
                     order_id: str,
                     good_order_id: str,
                     sms_code: str,
                     points: str,
                     real_points: str,
                     session_id: str,
                     machine_type: str,
                     finger_print: str,
                     reserved_1: Union[str, None] = None,
                     reserved_2: Union[str, None] = None) -> DetectOrderResponse:
        if machine_type not in ('IOS', 'Android', 'H5', 'MiniProgram'):
            raise BadRequest(f'{machine_type} 必须为：IOS / Android / H5 / MiniProgram')
        common_param = self.common_param('CYS0004')
        return self.__do_post_request('/partner-gateway/points/output/dectOrder', common_param.update(OrderedDict({
            'outTokenId': out_token_id,
            'orderId': order_id,
            'goodOrderId': good_order_id,
            'smsCode': sms_code,
            'points': points,
            'realPoints': real_points,
            'reserved1': reserved_1 if reserved_1 is not None else '',
            'reserved2': reserved_2 if reserved_2 is not None else '',
            'sessionId': session_id,
            'fingerprint': finger_print,
            'machinetype': machine_type
        })))

    def send_cmcc_sms(self,
                      order_id: str,
                      mobile: str,
                      out_token_id: str,
                      reserved_1: Union[str, None] = None,
                      reserved_2: Union[str, None] = None) -> CmccSmsResponse:
        common_param = self.common_param('CYS0005')
        return self.__do_post_request('/partner-gateway/points/output/sendCmccSms', common_param.update(OrderedDict({
            'orderId': order_id,
            'mobile': mobile,
            'outTokenId': out_token_id,
            'reserved1': reserved_1 if reserved_1 is not None else '',
            'reserved2': reserved_2 if reserved_2 is not None else '',
        })))

    def cancel_order(self,
                     good_order_id: str,
                     points: str,
                     out_token_id: str,
                     order_date: str,
                     reserved_1: Union[str, None] = None,
                     reserved_2: Union[str, None] = None) -> CancelOrderResponse:
        common_param = self.common_param('CYS0006')
        return self.__do_post_request('/partner-gateway/points/output/sendCmccSms', common_param.update(OrderedDict({
            'goodOrderId': good_order_id,
            'points': points,
            'outTokenId': out_token_id,
            'orderDate': order_date,
            'reserved1': reserved_1 if reserved_1 is not None else '',
            'reserved2': reserved_2 if reserved_2 is not None else '',
        })))

    def __do_post_request(self, path: str, body: OrderedDict) -> Tuple(dict, int):
        hmac = helper.sign_body(body, self.sign_key)
        body['hmac'] = hmac
        resp = requests.post(f'{self.endpoint}{path}',
                             headers={'AuthToken': self.auth_token, 'X-FORWARDED-FOR': self.public_ip},
                             data=body)
        if resp.code >= 500:
            raise InternalServerError()
        elif 400 <= resp.code < 500:
            raise BadRequest()
        return resp.json()

    @property
    def common_param(self, inter_code: str) -> OrderedDict:
        return OrderedDict({
            'interCode': inter_code,
            'character': '00',
            'ipAddress': self.public_ip,
            'partnerId': self.partener_id,
            'requestId': '1',
            'reqTime': datetime.now().strftime('%Y%m%d%H%M%S'),
            'signType': 'MD5',
            'type': 'web',
            'version': '1.0.0',
        })

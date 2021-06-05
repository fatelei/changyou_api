import asyncio
import json
import requests
import uuid
from base64 import b64encode
from copy import deepcopy
from datetime import datetime
from typing import OrderedDict
from typing import Union
from urllib import parse

from pyppeteer import launch

from .exception import BadRequest
from .exception import InternalServerError
from .exception import MobileRequiredException

from .model import CancelOrderResponse
from .model import CmccSmsResponse
from .model import DetectOrderResponse
from .model import QueryCMCCBalanceResponse
from .model import QueryOrderResponse
from .model import PlaceOrderResponse

from .tongdun import Tongdun

from .utils import helper


class ChangyouClient(object):

    def __init__(self, auth_token: str, sign_key: str, endpoint: str, public_ip: str, partener_id: str, version: str = '1.0.0'):
        self.auth_token = auth_token
        self.sign_key = sign_key
        self.endpoint = endpoint
        self.public_ip = public_ip
        self.partener_id = partener_id
        self.version = version
        self.tongdun_cli = Tongdun()

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
        common_param.update(OrderedDict({
            'mobile': mobile,
            'outTokenId': out_token_id,
            'outType': out_type,
            'callbackUrl': callback_url,
            'channelSource': channel_source,
            'reserved1': reserved_1 if reserved_1 is not None else '',
            'reserved2': reserved_2 if reserved_2 is not None else ''
        }))
        data = self.__do_post_request('/partner-gateway/points/output/queryCmccBalance', common_param)
        if data['resultCode'] != '0000':
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
            loop.run_until_complete(self.transition_page(
                mobile=mobile,
                out_token_id=out_token_id,
                callback_url=callback_url,
                channel_source=channel_source,
                reserved_1=reserved_1,
                reserved_2=reserved_2
            ))

            data = self.__do_post_request('/partner-gateway/points/output/queryCmccBalance', common_param)

        return QueryCMCCBalanceResponse(
            request_id=data['requestId'],
            result_code=data['resultCode'],
            hmac=data['hmac'],
            sign_type=data['signType'],
            partener_id=self.partener_id,
            inter_code=data['interCode'],
            type=data['type'],
            message=data['message'],
            version=data['version'],
            reserved_1=data.get('reversed1', ''),
            reserved_2=data.get('reversed2', ''),
            points=data.get('points', '0')
        )

    async def transition_page(self,
                              mobile: str,
                              out_token_id: str,
                              callback_url: str,
                              channel_source: str,
                              reserved_1: Union[str, None] = None,
                              reserved_2: Union[str, None] = None):
        version = b64encode(self.version.encode('utf8')).decode('utf8')
        ip_address = b64encode(self.public_ip.encode('utf8')).decode('utf8')
        params = OrderedDict({
            'interCode': 'CYS0001',
            'character': '00',
            'ipAddress': ip_address,
            'partnerId': self.partener_id,
            'requestId': '1',
            'reqTime': datetime.now().strftime('%Y%m%d%H%M%S'),
            'signType': 'MD5',
            'type': 'web',
            'version': version,
            'mobile': mobile,
            'outTokenId': out_token_id,
            'outType': '00',
            'callbackUrl': callback_url,
            'channelSource': channel_source,
            'reserved1': reserved_1 if reserved_1 is not None else '',
            'reserved2': reserved_2 if reserved_2 is not None else ''
        })
        params['hmac'] = helper.sign_body(params, self.sign_key)
        params_str = parse.urlencode(params, safe='=')
        browser = await launch(headless=True,
                               handleSIGINT=False,
                               handleSIGTERM=False,
                               handleSIGHUP=False)
        page = await browser.newPage()
        url = f'{self.endpoint}/event/2019/blankPage/index.html?{params_str}'
        print(url)
        await page.goto(url, {'waitUntil': 'networkidle2'})
        await browser.close()
    
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
        common_param.update(OrderedDict({
            'orderId': order_id,
            'orderDate': order_date,
            'outTokenId': out_token_id,
            'reserved1': reserved_1 if reserved_1 is not None else '',
            'reserved2': reserved_2 if reserved_2 is not None else ''
        }))
        data = self.__do_post_request('/partner-gateway/points/output/queryOrder', common_param)
        return QueryOrderResponse(
            request_id=data['requestId'],
            result_code=data['resultCode'],
            hmac=data['hmac'],
            sign_type=data['signType'],
            partener_id=self.partener_id,
            inter_code=data['interCode'],
            type=data['type'],
            message=data['message'],
            version=data['version'],
            reserved_1=data.get('reversed1', ''),
            reserved_2=data.get('reversed2', ''),
            status=data['status'],
            order_id=data['orderId']
        )

    def place_order(self,
                    out_token_id: str,
                    goods_info: str,
                    reserved_1: Union[str, None] = None,
                    reserved_2: Union[str, None] = None,
                    reserved_3: Union[str, None] = None,
                    reserved_4: Union[str, None] = None) -> PlaceOrderResponse:
        common_param = self.common_param('CYS0003')
        session_id = self.tongdun_cli.get_session_id()
        fingerprint = self.tongdun_cli.get_blackbox()

        tmp_goods_info = json.loads(goods_info)
        points = 0
        for item in tmp_goods_info.get('goodslist', []):
            goods_price = int(item['goodsPrice'])
            goods_num = int(item['goodsNum'])
            tmp = goods_price * goods_num * 120
            item['goodsPrice'] = tmp
            points += tmp

        common_param.update(OrderedDict({
            'outTokenId': out_token_id,
            'points': str(points),
            'goodsInfo': json.dumps(tmp_goods_info),
            'reserved1': reserved_1 if reserved_1 is not None else '',
            'reserved2': reserved_2 if reserved_2 is not None else '',
            'reserved3': reserved_3 if reserved_1 is not None else '',
            'reserved4': reserved_4 if reserved_2 is not None else '',
            'sessionid': session_id,
            'fingerprint': fingerprint
        }))

        data = self.__do_post_request('/partner-gateway/points/output/placeOrder', common_param)
        return PlaceOrderResponse(
            request_id=data['requestId'],
            result_code=data['resultCode'],
            hmac=data['hmac'],
            sign_type=data['signType'],
            partener_id=self.partener_id,
            inter_code=data['interCode'],
            type=data['type'],
            message=data['message'],
            version=data['version'],
            reserved_1=data.get('reversed1', ''),
            reserved_2=data.get('reversed2', ''),
            out_token_id=out_token_id,
            order_id=data.get('orderId', ''),
            good_order_id=data.get('goodOrderId', ''),
            points=data.get('points', ''),
            trans_time=data.get('transTime', ''),
            cmcc_mobile=data.get('cmccMobile', '')
        )
    
    def detect_order(self,
                     out_token_id: str,
                     order_id: str,
                     good_order_id: str,
                     sms_code: str,
                     points: str,
                     real_points: str,
                     machine_type: str,
                     reserved_1: Union[str, None] = None,
                     reserved_2: Union[str, None] = None) -> DetectOrderResponse:
        if machine_type not in ('IOS', 'Android', 'H5', 'MiniProgram'):
            raise BadRequest(f'{machine_type} 必须为：IOS / Android / H5 / MiniProgram')
        common_param = self.common_param('CYS0004')
        session_id = self.tongdun_cli.get_session_id()
        fingerprint = self.tongdun_cli.get_blackbox()
        common_param.update(OrderedDict({
            'outTokenId': out_token_id,
            'orderId': order_id,
            'goodOrderId': good_order_id,
            'smsCode': sms_code,
            'points': points,
            'realPoints': real_points,
            'reserved1': reserved_1 if reserved_1 is not None else '',
            'reserved2': reserved_2 if reserved_2 is not None else '',
            'sessionid': session_id,
            'fingerprint': fingerprint,
            'machinetype': machine_type,
            'flag': '1'
        }))
        data = self.__do_post_request('/partner-gateway/points/output/dectOrder', common_param)
        return DetectOrderResponse(
            request_id=data['requestId'],
            result_code=data['resultCode'],
            hmac=data['hmac'],
            sign_type=data['signType'],
            partener_id=self.partener_id,
            inter_code=data['interCode'],
            type=data['type'],
            message=data['message'],
            version=data['version'],
            reserved_1=data.get('reversed1', ''),
            reserved_2=data.get('reversed2', ''),
            out_token_id=out_token_id,
            order_id=data['orderId'],
            good_order_id=data['goodOrderId'],
            mobile=data['mobile'],
            trans_status=data['transStatus'],
            trans_time=data['transTime']
        )

    def send_cmcc_sms(self,
                      order_id: str,
                      mobile: str,
                      out_token_id: str,
                      reserved_1: Union[str, None] = None,
                      reserved_2: Union[str, None] = None) -> CmccSmsResponse:
        common_param = self.common_param('CYS0005')
        common_param.update(OrderedDict({
            'orderId': order_id,
            'mobile': mobile,
            'outTokenId': out_token_id,
            'reserved1': reserved_1 if reserved_1 is not None else '',
            'reserved2': reserved_2 if reserved_2 is not None else '',
        }))
        data = self.__do_post_request('/partner-gateway/points/output/sendCmccSms', common_param)
        return CmccSmsResponse(
            request_id=data['requestId'],
            result_code=data['resultCode'],
            hmac=data['hmac'],
            sign_type=data['signType'],
            partener_id=self.partener_id,
            inter_code=data['interCode'],
            type=data['type'],
            message=data['message'],
            version=data['version'],
            reserved_1=data.get('reversed1', ''),
            reserved_2=data.get('reversed2', ''),
            order_id=data['orderId'],
            sms_status=data['smsStatus'],
            mobile=data['mobile']
        )

    def cancel_order(self,
                     good_order_id: str,
                     points: str,
                     out_token_id: str,
                     order_date: str,
                     reserved_1: Union[str, None] = None,
                     reserved_2: Union[str, None] = None) -> CancelOrderResponse:
        common_param = self.common_param('CYS0006')
        common_param.update(OrderedDict({
            'goodOrderId': good_order_id,
            'points': points,
            'outTokenId': out_token_id,
            'orderDate': order_date,
            'reserved1': reserved_1 if reserved_1 is not None else '',
            'reserved2': reserved_2 if reserved_2 is not None else '',
        }))
        data = self.__do_post_request('/partner-gateway/points/output/cancleOrder', common_param)
        return CancelOrderResponse(
            request_id=data['requestId'],
            result_code=data['resultCode'],
            hmac=data['hmac'],
            sign_type=data['signType'],
            partener_id=self.partener_id,
            inter_code=data['interCode'],
            type=data['type'],
            message=data['message'],
            version=data['version'],
            reserved_1=data.get('reversed1', ''),
            reserved_2=data.get('reversed2', ''),
            good_order_id=data.get('goodOrderId', ''),
            points=data.get('points', '0'),
            status=data.get('status', '')
        )

    def __do_post_request(self, path: str, body: OrderedDict) -> dict:
        hmac = helper.sign_body(body, self.sign_key)
        data = deepcopy(body)
        data['hmac'] = hmac
        resp = requests.post(f'{self.endpoint}{path}',
                             headers={'AuthToken': self.auth_token, 'X-FORWARDED-FOR': self.public_ip},
                             data=data)
        if resp.status_code >= 500:
            raise InternalServerError()
        elif 400 <= resp.status_code < 500:
            raise BadRequest()
        return resp.json()

    @property
    def request_id(self):
        return str(uuid.uuid4())

    def common_param(self, inter_code: str) -> OrderedDict:
        return OrderedDict({
            'interCode': inter_code,
            'character': '00',
            'ipAddress': self.public_ip,
            'partnerId': self.partener_id,
            'requestId': self.request_id,
            'reqTime': datetime.now().strftime('%Y%m%d%H%M%S'),
            'signType': 'MD5',
            'type': 'web',
            'version': '1.0.0',
        })

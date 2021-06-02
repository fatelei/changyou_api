import argparse
import json

from changyou.changyou import ChangyouClient


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='changyou example')
    parser.add_argument('--auto_token', type=str, dest='auth_token', default='123456')
    parser.add_argument('--sign_key', type=str, dest='sign_key', default='123456')
    parser.add_argument('--endpoint', type=str, dest='endpoint', default='https://test-m-stg.ppppoints.com')
    parser.add_argument('--public_ip', type=str, dest='public_ip', default='127.0.0.1')
    parser.add_argument('--partener_id', type=str, dest='partener_id', required=True)
    parser.add_argument('--out_token_id', type=str, dest='out_token_id', required=True)
    args = parser.parse_args()

    cli = ChangyouClient(auth_token=args.auth_token,
                         sign_key=args.sign_key,
                         endpoint=args.endpoint,
                         public_ip=args.public_ip,
                         partener_id=args.partener_id)

    goods_info = json.dumps({
        "reciverMan": "张三",
        "reciverMobile": "15101584911",
        "reciverAddress": "街道XXXXX",
        "deliveryMethos": "配送方式",
        "goodslist": [
            {"goodsNo": "YASHAN0001","goodsName": "心相印抽纸兑换券","goodsBrand": "亚杉","goodsCategory": "","taxRate": "0.06","goodsNum": "1","goodsPrice": "120"},
            {"goodsNo": "YASHAN0002","goodsName": "优酷月度黄金vip会员","goodsBrand": "亚杉","goodsCategory": "","taxRate": "0.06","goodsNum": "1","goodsPrice": "240"}
        ]
    })
    
    res = cli.place_order(out_token_id=args.out_token_id,
                          goods_info=goods_info)
    print(res)

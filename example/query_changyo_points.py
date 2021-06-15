import argparse

from changyou.changyou import ChangyouClient


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='changyou example')
    parser.add_argument('--auto_token', type=str, dest='auth_token', default='123456')
    parser.add_argument('--sign_key', type=str, dest='sign_key', default='123456')
    parser.add_argument('--endpoint', type=str, dest='endpoint', default='https://test-m-stg.ppppoints.com')
    parser.add_argument('--public_ip', type=str, dest='public_ip', default='127.0.0.1')
    parser.add_argument('--partener_id', type=str, dest='partener_id', required=True)
    parser.add_argument('--mobile', type=str, dest='mobile', required=True)
    parser.add_argument('--channel_source', type=str, dest='channel_source', required=True)
    parser.add_argument('--out_token_id', dest='out_token_id', type=str, required=True)
    args = parser.parse_args()

    cli = ChangyouClient(auth_token=args.auth_token,
                         sign_key=args.sign_key,
                         endpoint=args.endpoint,
                         public_ip=args.public_ip,
                         partener_id=args.partener_id)
    res = cli.get_changyo_points(mobile=args.mobile,
                                 channel_source=args.channel_source,
                                 out_token_id=args.out_token_id)
    print(res)

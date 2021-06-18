import argparse
import asyncio

from pyppeteer import launch

from changyou.changyou import ChangyouClient


async def visit_register_page(url):
    browser = await launch(headless=True,
                           handleSIGINT=False,
                           handleSIGTERM=False,
                           handleSIGHUP=False,
                           args=['nosandbox'])
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle2'})
    await browser.close()


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
    res = cli.query_cmcc_balance(mobile=args.mobile,
                                 channel_source=args.channel_source,
                                 out_token_id=args.out_token_id,
                                 callback_url='https://www.baidu.com',
                                 out_type='01')
    if res.result_code != '0000':
        res = cli.transition_page(mobile=args.mobile,
                                  out_token_id=args.out_token_id,
                                  channel_source=args.channel_source,
                                  callback_url='https://www.baidu.com')
        print(res['url'])
        asyncio.get_event_loop().run_until_complete(visit_register_page(res['url']))

        res = cli.query_cmcc_balance(mobile=args.mobile,
                                     channel_source=args.channel_source,
                                     out_token_id=args.out_token_id,
                                     callback_url='https://www.baidu.com',
                                     out_type='01')
    print(res)

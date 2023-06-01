import requests
from binaryencode import image_jpeg_base64


base64_string = image_jpeg_base64("images-input/Image_0002.png")


def get_search_url(base64_string):

    headers = {
        'authority': 'www.bing.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryBIwEjHTjmqg8Qyw0',
        #'cookie': '_IDET=VSNoti2=20230530; MUID=20B02DD20DE56B4D243F3EF20CDB6A32; MUIDB=20B02DD20DE56B4D243F3EF20CDB6A32; _EDGE_V=1; SRCHD=AF=SBIIRP; SRCHUID=V=2&GUID=6A7CC7702AB94916AA499D238DF828F1&dmnchg=1; MMCASM=ID=7E317A33FD3E41119A4CFBA5C64F4A37; BCP=AD=0&AL=0&SM=0; _UR=QS=0&TQS=0; _SS=SID=3E081DD2F46F6A373FB30EF3F5EF6B9C&R=0&RB=0&GB=0&RG=200&RP=0; MicrosoftApplicationsTelemetryDeviceId=7d0ea93d-202a-4ef9-b79b-77757c2fd3d3; _EDGE_S=SID=3E081DD2F46F6A373FB30EF3F5EF6B9C&mkt=pt-br&ui=en-gb; fdfre=o=1; SUID=M; ipv6=hit=1685544553805&t=4; SRCHUSR=DOB=20230529&TPC=1685537084000&T=1685541637000; _HPVN=CS=eyJQbiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMy0wNS0zMVQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6MTZ9; SRCHHPGUSR=SRCHLANG=en&BRW=NOTP&BRH=M&CW=731&CH=821&SCW=731&SCH=821&DPR=2.0&UTC=-180&DM=1&PV=13.0.0&PRVCW=731&PRVCH=821&HV=1685541760&WTS=63821138437; ai_session=lORpdDq2ucQdWoEOK9l4Rv|1685537027723|1685541760073; _RwBf=ilt=24&ihpd=19&ispd=0&rc=0&rb=0&gb=0&rg=200&pc=0&mtu=0&rbb=0&g=0&cid=&clo=0&v=20&l=2023-05-31T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2023-05-31T14:02:40.3594879+00:00&rwred=0&wls=&lka=0&lkt=0&TH=',
        'origin': 'https://www.bing.com',
        'referer': 'https://www.bing.com/',
        #'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        #'sec-ch-ua-arch': '"arm"',
        #'sec-ch-ua-bitness': '"64"',
        #'sec-ch-ua-full-version': '"113.0.5672.126"',
        #'sec-ch-ua-full-version-list': '"Google Chrome";v="113.0.5672.126", "Chromium";v="113.0.5672.126", "Not-A.Brand";v="24.0.0.0"',
        #'sec-ch-ua-mobile': '?0',
        #'sec-ch-ua-model': '""',
        #'sec-ch-ua-platform': '"macOS"',
        #'sec-ch-ua-platform-version': '"13.0.0"',
        #'sec-fetch-dest': 'document',
        #'sec-fetch-mode': 'navigate',
        #'sec-fetch-site': 'same-origin',
        #'sec-fetch-user': '?1',
        #'upgrade-insecure-requests': '1',
        # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    params = {
        'view': 'detailv2',
        'iss': 'sbiupload',
        'FORM': 'SBIHMP',
        'sbisrc': 'ImgPicker',
        'idpbck': '1',
    }

    data = f'------WebKitFormBoundaryBIwEjHTjmqg8Qyw0\r\nContent-Disposition: form-data; name="imgurl"\r\n\r\n\r\n------WebKitFormBoundaryBIwEjHTjmqg8Qyw0\r\nContent-Disposition: form-data; name="cbir"\r\n\r\nsbi\r\n------WebKitFormBoundaryBIwEjHTjmqg8Qyw0\r\nContent-Disposition: form-data; name="imageBin"\r\n\r\n{base64_string}\r\n------WebKitFormBoundaryBIwEjHTjmqg8Qyw0--\r\n'

    response = requests.post('https://www.bing.com/images/search', params=params, headers=headers, data=data)

    return response.url


print(get_search_url(base64_string))



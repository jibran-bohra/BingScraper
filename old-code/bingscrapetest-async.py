import httpx,  requests, json, time, asyncio, os
from urllib.parse import urlparse, parse_qs

async def fetch_content_urls(page, params, headers, data):
    response = httpx.post(
        'https://www.bing.com/images/api/custom/knowledge',
        params=params,
        headers=headers,
        data=data,
        #proxy = 
    )

    try:
        if response.status_code == 200:
            jsondata = response.json()
            content_urls = [item['contentUrl'] for item in jsondata['tags'][0]['actions'][0]['data']['value']]
            return content_urls
        else:
            print(f"Failed to fetch page {page}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


async def gather_content_urls(image_search_url, output_file):
    "Given an Bing search result, gather 1000 direct URLs to images, and export to output file."

    params = {
        'q': '',
        #"rshighlight": "true",
        #"textDecorations": "true",
        #"internalFeatures": "share",
        #"FORM": "SBIIRP",
        #"skey": "00RhsOQh-ASl3WA8x73ZoVq-CPcnHLfxq9FK2YifG-0",
        #"safeSearch": "Moderate",
        #"IG": "746B504FCF954D23A6D27C1568C29F1D",
        #"IID": "idpins",
        #"SFX": "1",
        }

    headers = {
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0',
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        # 'Accept-Encoding': 'gzip, deflate, br',
        "Referer": image_search_url,
        "Content-Type": "multipart/form-data; boundary=---------------------------9660692851014910546208278451",
        "Origin": "https://www.bing.com",
        "Connection": "keep-alive",
        # 'Cookie': '_IDET=VSNoti2=20230528&MIExp=0; MUID=2AF38138B46F644121949227B5BD6557; MUIDB=2AF38138B46F644121949227B5BD6557; _EDGE_S=F=1&SID=0241F1E3FD4465200702E2FCFC96640B&mkt=pt-br&ui=en-gb; _EDGE_V=1; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=E203F9FE6A214F9FB50F7913495BFB48&dmnchg=1; SRCHUSR=DOB=20230528&T=1685386596000; SRCHHPGUSR=SRCHLANG=en&BRW=W&BRH=S&CW=1440&CH=376&SCW=1440&SCH=376&DPR=2.0&UTC=-180&DM=1&HV=1685389349&PRVCW=1440&PRVCH=376&WTS=63820983397; _SS=SID=0241F1E3FD4465200702E2FCFC96640B&R=0&RB=0&GB=0&RG=200&RP=0; _HPVN=CS=eyJQbiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMy0wNS0yOVQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6MTZ9; _UR=QS=0&TQS=0; ipv6=hit=1685390197580&t=4; MicrosoftApplicationsTelemetryDeviceId=0eb2fdb4-cbb7-4dfe-9932-a24c1785a7c7; MMCASM=ID=1F24D211D7FA409EA65BC4E9B81448A3; SUID=M; _RwBf=ilt=12&ihpd=7&ispd=0&rc=0&rb=0&gb=0&rg=200&pc=0&mtu=0&rbb=0&g=0&cid=&clo=0&v=12&l=2023-05-29T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2023-05-29T19:42:28.5905763+00:00&rwred=0&wls=&lka=0&lkt=0&TH=; BCP=AD=0&AL=0&SM=0; ai_session=/VJCvdRDdBP47oaae+QPx7|1685389293211|1685389293211',
        #"Sec-Fetch-Dest": "empty",
        #"Sec-Fetch-Mode": "cors",
        #"Sec-Fetch-Site": "same-origin",
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    parsed_url      = urlparse(image_search_url)
    query_params    = parse_qs(parsed_url.query)
    insights_token  = query_params.get('insightstoken', [''])[0]

    results_per_page = 49
    total_results = 1000
    num_pages = total_results // results_per_page + 1

    all_results = []

    tasks = []

    for page in range(1, num_pages + 1):
        offset = (page - 1) * results_per_page

        data = f'------WebKitFormBoundaryv5aLQy5TxWQ4QiwA\r\nContent-Disposition: form-data; name="knowledgeRequest"\r\n\r\n{{"imageInfo":{{"imageInsightsToken":"{insights_token}","source":"Url"}},"knowledgeRequest":{{"invokedSkills":["SimilarImages"],"offset":{offset},"count":{results_per_page},"index":1}}}}\r\n------WebKitFormBoundaryv5aLQy5TxWQ4QiwA--\r\n'

        tasks.append(fetch_content_urls(page, params, headers, data))

    fetched_results = await asyncio.gather(*tasks)

    for content_urls in fetched_results:
        if content_urls:
            all_results.extend(content_urls)

    return list(set(all_results))




def write_to_json(output_file, results):

    if os.path.exists(output_file):

        print("Output file already exists. Appending to it and then select unique values. ")

        with open(output_file, 'r+') as f:
            existing_data = json.load(f)
            existing_data.extend(results)
            f.seek(0)
            json.dump(list(set(existing_data)), f, indent=4)

    else:

        print("Output file does not exist. Creating it.")

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)

    print(f"Results exported to {output_file} successfully.")

if __name__ == "__main__":
    image_search_url = 'https://www.bing.com/images/search?view=detailV2&insightstoken=bcid_TjXYXWTrL6YF0A*ccid_NdhdZOsv&form=SBIIRP&iss=VSI&sbisrc=ImgPicker&idpbck=1&sbifsz=1906+x+1168+%c2%b7+31.15+kB+%c2%b7+png&sbifnm=Image_0001.png&thw=1906&thh=1168&ptime=97&dlen=42524&expw=766&exph=469&selectedindex=0&id=35269011F5569AB99E51A07EC76492D7CF10FC18&ccid=NdhdZOsv&vt=2&sim=1&pivotparams=insightsToken%3Dbcid_TjXYXWTrL6YFqxcxoNWLuD9SqbotqVTdP8Y'
    output_file_name = 'url-searchresults/Image0001.json'
    results = asyncio.run(gather_content_urls(image_search_url))
    write_to_json(output_file_name, results)



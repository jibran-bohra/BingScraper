import os, time, json, asyncio
import base64
from PIL import Image
import io, requests

class BingScraper:
    def __init__(self):
        self.dir_input = "images-input/"
        self.dir_output = "images-output/"
        self.dir_test = "images-test/"
        self.dir_searchresults = "url-searchresults/"

        self.files_input = os.listdir(self.dir_input)
        self.results_content_urls = [''.join(file.split('.')[:-1]) + '-content_urls' +'.json' for file in os.listdir(self.dir_input)]
        self.results_gps_urls = [''.join(file.split('.')[:-1]) + '-gps_urls' +'.json' for file in os.listdir(self.dir_input)]
    
    def image_jpeg_base64(self, image_path):
        "Bing converts input images to jpeg and then generates a base64 string for search URLs"

        # Open the image file
        image = Image.open(image_path)

        # Convert the image to JPEG format
        jpeg_image = image.convert('RGB')

        # Save the converted image as JPEG to the in-memory file object
        image_file = io.BytesIO()
        jpeg_image.save(image_file, format='JPEG')

        # Retrieve the binary data of the image
        image_binary_data = image_file.getvalue()   

        #Encode in base64
        base64_encoded_data = base64.b64encode(image_binary_data)

        return base64_encoded_data.decode('utf-8')
    
    def get_search_url(self, base64_string):
        "Given image input as a base64 string, get the Bing search result URL."

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

        # Image payload is delivered through the data string. 
        data = f'------WebKitFormBoundaryBIwEjHTjmqg8Qyw0\r\nContent-Disposition: form-data; name="imgurl"\r\n\r\n\r\n------WebKitFormBoundaryBIwEjHTjmqg8Qyw0\r\nContent-Disposition: form-data; name="cbir"\r\n\r\nsbi\r\n------WebKitFormBoundaryBIwEjHTjmqg8Qyw0\r\nContent-Disposition: form-data; name="imageBin"\r\n\r\n{base64_string}\r\n------WebKitFormBoundaryBIwEjHTjmqg8Qyw0--\r\n'

        response = requests.post('https://www.bing.com/images/search', params=params, headers=headers, data=data)

        return response.url

    async def fetch_content_urls(self, page, params, headers, data):
        response = requests.post(
            'https://www.bing.com/images/api/custom/knowledge',
            params=params,
            headers=headers,
            data=data,
        )

        if response.status_code == 200:
            data = response.json()
            content_urls = [item['contentUrl'] for item in data['tags'][0]['actions'][0]['data']['value']]
            return content_urls
        else:
            print(f"Failed to fetch page {page}")


    async def gather_content_urls(self, image_search_url, output_file):
        "Given an Bing search result, gather 1000 direct URLs to images, and export to output file."
        results_per_page = 35
        total_results = 1000
        num_pages = total_results // results_per_page + 1

        all_results = []

        tasks = []

        for page in range(1, num_pages + 1):
            params = {
                'q': '',
                'count': results_per_page,
                'offset': (page - 1) * results_per_page,
                'rshighlight': 'true',
                'textDecorations': 'true',
                'internalFeatures': 'share',
                'FORM': 'SBIIRP',
                'skey': '00RhsOQh-ASl3WA8x73ZoVq-CPcnHLfxq9FK2YifG-0',
                'safeSearch': 'Moderate',
                # 'mkt': 'zh-cn',
                # 'setLang': 'en-gb',
                'IG': '746B504FCF954D23A6D27C1568C29F1D',
                'IID': 'idpins',
                'SFX': '1',
            }

            headers = {
                # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                # 'Accept-Encoding': 'gzip, deflate, br',
                'Referer': image_search_url,
                'Content-Type': 'multipart/form-data; boundary=---------------------------9660692851014910546208278451',
                'Origin': 'https://www.bing.com',
                'Connection': 'keep-alive',
                # 'Cookie': '_IDET=VSNoti2=20230528&MIExp=0; MUID=2AF38138B46F644121949227B5BD6557; MUIDB=2AF38138B46F644121949227B5BD6557; _EDGE_S=F=1&SID=0241F1E3FD4465200702E2FCFC96640B&mkt=pt-br&ui=en-gb; _EDGE_V=1; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=E203F9FE6A214F9FB50F7913495BFB48&dmnchg=1; SRCHUSR=DOB=20230528&T=1685386596000; SRCHHPGUSR=SRCHLANG=en&BRW=W&BRH=S&CW=1440&CH=376&SCW=1440&SCH=376&DPR=2.0&UTC=-180&DM=1&HV=1685389349&PRVCW=1440&PRVCH=376&WTS=63820983397; _SS=SID=0241F1E3FD4465200702E2FCFC96640B&R=0&RB=0&GB=0&RG=200&RP=0; _HPVN=CS=eyJQbiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMy0wNS0yOVQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6MTZ9; _UR=QS=0&TQS=0; ipv6=hit=1685390197580&t=4; MicrosoftApplicationsTelemetryDeviceId=0eb2fdb4-cbb7-4dfe-9932-a24c1785a7c7; MMCASM=ID=1F24D211D7FA409EA65BC4E9B81448A3; SUID=M; _RwBf=ilt=12&ihpd=7&ispd=0&rc=0&rb=0&gb=0&rg=200&pc=0&mtu=0&rbb=0&g=0&cid=&clo=0&v=12&l=2023-05-29T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2023-05-29T19:42:28.5905763+00:00&rwred=0&wls=&lka=0&lkt=0&TH=; BCP=AD=0&AL=0&SM=0; ai_session=/VJCvdRDdBP47oaae+QPx7|1685389293211|1685389293211',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                # Requests doesn't support trailers
                # 'TE': 'trailers',
            }

            data = '-----------------------------9660692851014910546208278451\r\nContent-Disposition: form-data; name="knowledgeRequest"\r\n\r\n{"imageInfo":{"imageInsightsToken":"bcid_TjXYXWTrL6YF0A*ccid_NdhdZOsv","source":"BingImageIndex"},"knowledgeRequest":{"invokedSkills":["ImageById","BestRepresentativeQuery","Offline","ObjectDetection","EntityLinkingFace","EntityLinkingDog","EntityLinkingAnimal","EntityLinkingPlant","EntityLinkingLandmark","EntityLinkingFood","RelatedSearches","TextAds","ProductAds","SponsoredAds","MonetizationSignals","Recipes","Travel","EntityLinkingBook","SimilarImages"],"invokedSkillsRequestData":{"adsRequest":{"textRequest":{"mainlineAdsMaxCount":1}}},"index":1}}\r\n-----------------------------9660692851014910546208278451--\r\n'

            tasks.append(self.fetch_content_urls(page, params, headers, data))

        fetched_results = await asyncio.gather(*tasks)

        for content_urls in fetched_results:
            if content_urls:
                all_results.extend(content_urls)

        if len(all_results) >= total_results:
            output_dir = os.path.dirname(output_file)
            os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
            self.write_to_json(output_file, all_results)
        else:
            print("Not enough results fetched.")
        

    def write_to_json(self, output_file, results):

        if os.path.exists(output_file):

            print("Output file already exists. Appending to it.")

            with open(output_file, 'r+') as f:
                existing_data = json.load(f)
                existing_data.extend(results)
                f.seek(0)
                json.dump(existing_data, f, indent=4)

        else:

            print("Output file does not exist. Creating it.")

            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)

        print(f"Results exported to {output_file} successfully.")


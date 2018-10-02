import requests
import gzip
import json


class CourtOrdersParser:
    def __init__(self, start_page=0, end_page=4603890):
        self.max_pages = 4603890
        self.start_page = start_page
        self.end_page = end_page
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Content-Type": "application/json; charset=UTF-8",
            "Origin": "https://bsr.sudrf.ru",
            "Referer": "https://bsr.sudrf.ru/bigs/portal.html"
        }
        with open('resources/paging.json', encoding='utf8') as f:
            self.paging = json.load(f)
        with open('resources/content.json', encoding='utf8') as f:
            self.content = json.load(f)

    def get_ids(self, current_page):
        payload = self.paging
        payload['request']['start'] = 10 * current_page

        data = None
        try:
            r = requests.post("https://bsr.sudrf.ru/bigs/s.action",
                              json=payload, headers=self.headers, timeout=120)
            data = r.json()
            r.close()
        except requests.exceptions.ConnectionError:
            print(f'get_ids got ConnectionError on page {current_page}')
        result = None
        if data:
            result = [doc['id'] for doc in data['searchResult']['documents']]
        return result

    def get_document(self, doc_id):
        payload = self.content
        payload['request']['id'] = doc_id
        data = None
        try:
            r = requests.post("https://bsr.sudrf.ru/bigs/showDocument.action",
                              json=payload, headers=self.headers, timeout=120)
            data = r.json()
            r.close()
        except requests.exceptions.ConnectionError:
            print(f'get_document got ConnectionError on doc_id {doc_id}')
        return data

    def parse(self):
        current_page = self.start_page
        while current_page <= self.end_page:
            docs = []
            ids = self.get_ids(current_page)
            if ids:
                for doc_id in ids:
                    print(doc_id)
                    doc = self.get_document(doc_id)
                    if doc:
                        docs.append(doc)
                current_page += 1
                yield docs


if __name__ == '__main__':
    parser = CourtOrdersParser()
    data = []
    for i, docs in enumerate(parser.parse()):
        data += docs
        if i % 10 == 0:
            with gzip.GzipFile(f'results/res_{i}.json.gz', 'w') as fout:
                fout.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
                print("f'results/res_{i}.json.gz' saved")
            data = []

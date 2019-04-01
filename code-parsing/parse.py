import re
import json

## Civil_code
# part_pattern = re.compile(r"^ЧАСТЬ (.*)$")
# section_pattern = re.compile(r"^Раздел ([I|V]+)\. (.*)$")
# subsection_pattern = re.compile(r"^Подраздел (\d+)\. (.*)$")
# chapter_pattern = re.compile(r"^Глава (\d+)\. (.*)$")
# paragraph_pattern = re.compile(r"^§ (\d+)\. (.*)$")
# article_pattern = re.compile(r"^Статья ([\d|\.]+)\. (.*)$")

## Criminal code
part_pattern = re.compile(r"^(.*) ЧАСТЬ$")
section_pattern = re.compile(r"^Раздел ([I|V|X]+)\. (.*)$")
chapter_pattern = re.compile(r"^Глава (\d+)\. (.*)$")
article_pattern = re.compile(r"^Статья ([\d|\.]+)\. (.*)$")



def main():
    result = []
    with open('data/criminal_code.txt', 'r', encoding='utf-8') as f:
        data = {}
        data['article'] = ''
        for line in f:
            if re.match(part_pattern, line):
                if data['article']:
                    data = {}
                    data['article'] = ''
                    if data.get('paragraph_number'):
                        del data['paragraph_number'], data['paragraph_name']
                [data['part_name']] = re.findall(part_pattern, line)
            elif re.match(section_pattern, line):
                if data['article']:
                    data['article'] = ''
                    if data.get('paragraph_number'):
                        del data['paragraph_number'], data['paragraph_name']
                [(data['section_number'], data['section_name'])] = re.findall(section_pattern, line)
            # elif re.match(subsection_pattern, line):
            #     if data['article']:
            #         data['article'] = ''
            #         if data.get('paragraph_number'):
            #             del data['paragraph_number'], data['paragraph_name']
            #     [(data['subsection_number'], data['subsection_name'])] = re.findall(subsection_pattern, line)
            elif re.match(chapter_pattern, line):
                if data['article']:
                    if data.get('paragraph_number'):
                        del data['paragraph_number'], data['paragraph_name']
                    data['article'] = ''
                [(data['chapter_number'], data['chapter_name'])] = re.findall(chapter_pattern, line)
            # elif re.match(paragraph_pattern, line):
            #     if data['article']:
            #         data['article'] = ''
            #     [(data['paragraph_number'], data['paragraph_name'])] = re.findall(paragraph_pattern, line)
            elif re.match(article_pattern, line):
                if data['article']:
                    result.append(dict(**data))
                    data['article'] = ''
                [(data['article_number'], data['article_name'])] = re.findall(article_pattern, line)            
            else:
                data['article'] += line
    result.append(dict(**data))
    for d in result:
        d['article'] = ' '.join(d['article'].replace('\n', ' ').split())
    with open('data/criminal_code.json', 'w', encoding='utf8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
if __name__ == '__main__':
    main() 

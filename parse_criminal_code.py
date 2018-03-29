from lxml import etree
import re

root = etree.Element('root')

with open('data/ukrf.txt', 'r') as file:
    lines = file.readlines()

part_iter = iter(range(1,100))
chapter_iter = iter(range(1, 100))


for line in lines:
    line = line.replace('\n', '')
    if (line is '') or ('в ред.' in line) or ('(введена' in line) or ('Утратила силу' in line):
        pass
    elif 'ЧАСТЬ' in line:
        part = etree.SubElement(root, 'part{}'.format(next(part_iter)))
        part.set('name', line)
        section_iter = iter(range(1, 100))
    elif 'Раздел' in line:
        line = re.findall(r'(^\D* )(([A-Z]|[\.]?)+)\. (.*)', line)
        section = etree.SubElement(part, 'section{}'.format(next(section_iter)))
        section.set('number', line[0][1])
        section.set('name', line[0][-1])
        article_iter = iter(range(1, len(lines)))
    elif line.startswith('Глава'):
        line = re.findall(r'(^\D* )(([\d]|[\.]?)+)\. (.*)', line)
        chapter = etree.SubElement(section, 'chapter{}'.format(next(chapter_iter)))
        chapter.set('number', line[0][1])
        chapter.set('name', line[0][-1])
    elif line.startswith('Статья'):
        line = re.findall(r'(^\D* )(([\d]|[\.]?)+)\. (.*)', line)
        article = etree.SubElement(chapter, 'article{}'.format(next(article_iter)))
        body = etree.SubElement(article, 'body')
        article.set('number', line[0][1])
        article.set('name', line[0][-1])
    else:
        try:
            if body.text is not None:
                body.text = body.text + ' '+ line
            else:
                body.text = line
        except NameError:
            pass

with open('RFCriminalCode.xml', 'w') as file:
    file.write(etree.tostring(root, encoding=str,pretty_print=True))
# coding:utf-8
import os
from pdfminer.converter import LTChar, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox
from io import StringIO
from io import open

# 读取pdf文件文本内容

path = '/pdf-txt/pdf'


def read(path):
    parser = PDFParser(path)
    doc = PDFDocument(parser, '')
    parser.set_document(doc)
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        page0 = ''
        for i, page in enumerate(PDFPage.create_pages(doc)):
            print("START PAGE %d\n" % i)
            interpreter.process_page(page)
            print("END PAGE %d\n" % i)
            layout = device.get_result()
            print(layout)
            line0 = ''
            for x in layout:
                if isinstance(x, LTTextBox):
                    line0 = line0 + x.get_text().strip()
            page0 = page0 + line0
        return page0


if __name__ == '__main__':
    path = 'pdf'
    pdfList = os.listdir(path)
    pdf_num = 0
    for li in pdfList:
        try:
            pdffile = open(path + '/' + li, "rb")
            content = read(pdffile)
        except:
            continue
        txt_filename = os.path.splitext(li)[0] + '.txt'
        file1 = os.path.join('txt', txt_filename)
        with open(file1, 'w+', encoding='utf8') as f:
            f.write(content)
        pdf_num += 1
        print("DONE:" + txt_filename)
    print('number of done-article:', end="")
    print(pdf_num)

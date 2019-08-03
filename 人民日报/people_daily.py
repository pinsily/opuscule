

import requests
import time
from scrapy.selector import Selector
from pprint import pprint
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import os
import logging


logging.basicConfig(
    format='%(asctime)s - %(levelname)s * %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)


def get_now_day() -> tuple:
    """获取年月日
    
    [description]
    
    :returns: year, month, day
    """
    localtime = time.localtime(time.time())
    return localtime.tm_year, str(localtime.tm_mon).zfill(2), str(localtime.tm_mday).zfill(2)


def get_pdf_dict() -> dict:
    """获取当前日报的所有pdf链接
    
    [description]
    
    :returns: {filenames: urls}
    """
    year, month, day = get_now_day()

    logging.info("开始获取{0}年{1}月{2}日人民日报pdf......".format(year, month, day))
    
    url = "http://paper.people.com.cn/rmrb/html/{0}-{1}/{2}/nbs.D110000renmrb_01.htm#".format(year,month, day)
    base_url = "http://paper.people.com.cn/rmrb/{0}"

    resp = requests.get(url)
    selector = Selector(text=resp.text)

    # ../../../page/2019-07/30/18/rmrb2019073018.pdf
    pdfs = {url.split("/")[-1]:base_url.format(url[9:]) for url in selector.xpath("//div[@class='right_title-pdf']/a/@href").extract()}

    return pdfs


def merger(output_path: str, input_paths: list) -> None:
    """合并当天的所有PDF为一份
    
    [description]
    :param
        output_path: str, 合并后的文件名
        input_paths: list, 所有当天电子书集合
    """
    logging.info("开始合并电子书......")
    pdf_writer = PdfFileWriter()
    for path in input_paths:
        pdf_reader = PdfFileReader(path, strict=False)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
    with open(output_path, 'wb') as fh:
        pdf_writer.write(fh)


def download_pdf() -> None:
    """下载当前所有电子书PDF
    
    [description]
    """
    logging.info("开始下载当天所有电子书......")
    year, month, day = get_now_day()
    pdfs = get_pdf_dict()

    output_file = "{0}{1}{2}.pdf".format(year, month, day)

    paths = []

    for file_name, url in pdfs.items():
        logging.info("-- 开始下载{0}".format(file_name))
        with open(file_name, 'wb') as f:
            resp = requests.get(url)
            f.write(resp.content)

        logging.info("-- 下载完成: {}".format(file_name))
        paths.append(file_name)

    merger(output_file, paths)
    remove_files(paths)


def remove_files(paths: list) -> None:
    for file in paths:
        os.remove(file)


if __name__ == "__main__":
    download_pdf()

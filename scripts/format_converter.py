import logging
from shutil import Error
from typing import Dict

import requests 
from yattag import Doc
from pathlib import Path
import os
from xhtml2pdf import pisa 

class Converter:
    def __init__(self, data_news: Dict, path_html : str = None , path_pdf : str = None) -> None:
        self.data_news = data_news
        self.path_html = os.path.abspath(path_html) if path_html else path_html
        self.path_pdf = os.path.abspath(path_pdf) if path_pdf else path_pdf
        self.img_folder = None

    def convert_news(self):
        try:
            self.create_image_folder(self.path_html or self.path_pdf)
            html=self.create_html()
        except OSError:
            logging.error('Error : Can\'t create html')
        else:
            if self.path_html:
                self.conver_to_html(html)
            if self.path_pdf:
                self.conver_to_pdf(html)

    def create_image_folder(self, save_path: str) -> None:
        self.img_folder = os.path.join(os.path.dirname(save_path),Path(save_path).resolve(),''.join(f'image'))
        if not os.path.exists(self.img_folder):
            try:
                os.mkdir(self.img_folder)
            except OSError:
                logging.error('Error : Can\'t create directory for image files')

    def download_image(self,link: str,img_number: int) ->str:
        image_path = os.path.join(self.img_folder,''.join(f'image_link{img_number}.jpg'))
        img = requests.get(link)
        recording = open(image_path, "wb")
        recording.write(img.content)
        recording.close()
        return image_path
    
    def create_html(self):
        def add_main_part():
            text('Title:{0}'.format(single_date.get('Title')))
            doc.stag('br')
            text('Date:{0}'.format(single_date.get('Date')))
            doc.stag('br')
            with tag('a', href=single_date.get('Link')):
                text('Link:{0}'.format(single_date.get('Link')))
                doc.stag('br')
        
        def add_explanatory_part():
            if (single_date.get('Text')!='no information'):
                text('Text:{0}'.format(single_date.get('Text')))
                doc.stag('br')
            if(single_date.get('Links')!='no information'):
                with tag('a', href=single_date.get('Link')):
                    text(single_date.get('Link'))
            if(single_date.get('Image')!='no information'):
                image_path=self.download_image(single_date.get('Image'),img_number)
                if not image_path: return
                doc.stag('br')
                doc.stag('img', src=image_path)
                doc.stag('br')

        doc, tag, text = Doc().tagtext()
        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('body'):
                with tag('p'):
                    for img_number,single_date in enumerate(self.data_news, start=1):
                        with tag('b'):
                            add_main_part()
                            add_explanatory_part()
        return doc.getvalue()

    def conver_to_html(self, source_html: str):
        try:
            self.path_html=os.path.join(self.path_html,''.join('rss-reader_file.html'))
            with open(self.path_html, 'w') as file_obj:
                file_obj.write(source_html)
        except OSError:
                logging.error('Error : Can\'t create html file')

    def conver_to_pdf(self, source_html: str):
        try:
            self.path_pdf=os.path.join(self.path_pdf,''.join('rss-reader_file.pdf'))
            with open(self.path_pdf,'w+b') as file_obj:
                pisa_status = pisa.CreatePDF(source_html,dest=file_obj)
        except OSError:
            logging.error('Error : Can\'t create pdf file')
        if pisa_status.err:
            logging.error('Error : Can\'t create pdf file')

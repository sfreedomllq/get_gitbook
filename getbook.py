import time

import pdfkit
import requests
from PyPDF2 import PdfFileMerger
from bs4 import BeautifulSoup



def get_chapter(bookname,url):
    i = 0
    pdfs = []
    html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
        {content}
        </body>
        </html>
        """
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    for cursor in soup.find_all( class_='chapter' ):
        i = i+1
        print(cursor.text)
        pdf_name = 'docker'+ str(i) + '.pdf'
        html_name = 'docker'+ str(i) + '.html'
        link = url+cursor.a.get('href')
        time.sleep(2);
        html = get_chapter_text(link)
        html = html_template.format(content = html)
        html = html.encode("utf-8")
        with open( html_name, 'wb') as f:
            f.write(html)
        save_pdf(html_name,pdf_name )
        pdfs.append(pdf_name)

    merge_pdf(bookname, pdfs)

def merge_pdf(bookname,pdfs):
    merger = PdfFileMerger()
    i = 0
    for pdf in pdfs:
        merger.append(open(pdf, 'rb'), import_bookmarks=False)
        print( "Merging " + str(i) + ' files:' + pdf)

        i = i + 1
    output = open(bookname+".pdf", "wb")
    merger.write(output)
    print("Finished!")


def get_chapter_text(url):
    current_soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    content = current_soup.find(class_='search-noresults')
    return(content)

def save_pdf(htmls, file_name):
  """
  save all .html to .pdf
  :param htmls: name of .html files
  :param file_name: name of .pdf files
  """
  options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'custom-header': [
      ('Accept-Encoding', 'gzip')
    ],
    'cookie': [
      ('cookie-name1', 'cookie-value1'),
      ('cookie-name2', 'cookie-value2'),
    ],
    'outline-depth': 10,
  }
  pdfkit.from_file(htmls, file_name, options=options)

if __name__ == '__main__':
    url = 'https://yeasy.gitbooks.io/docker_practice/content/'
    get_chapter("Docker_all",url)
from bs4 import BeautifulSoup
import os
import html
from config import directory


for filename in os.listdir(directory):
    if filename.endswith(".html"): 
        with open(directory + '/' + filename, 'r') as f:
            html_doc = f.read()
    else:
        continue

class ChatLogFile:
    def __init__(self):
        self.html = ''
        self.data = {'sender': [], 'date': [], 'message': []}

    def make_soup(self):
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.message_soup = self.soup.find_all('div', {'class' : ['message default clearfix', 'message default clearfix joined']})
    
    def __get_sender(self, meta_message):
        if meta_message.find('div', {'class':'from_name'}):
            return meta_message.find('div', {'class':'from_name'}).string.lstrip().rstrip()
        else:
            return False
    
    def __get_message(self, meta_message):
        if meta_message.find('div', {'class':'text'}):
            if meta_message.find('div', {'class':'text'}).string:
                return html.unescape(meta_message.find('div', {'class':'text'}).string.replace('&apos', '&apos;').rstrip().lstrip())
            else:
                temp_list = []
                for sub_tag in meta_message.find('div', {'class':'text'}).contents:
                    if sub_tag.string:
                        temp_list.append(sub_tag.string)
                    else:
                        temp_list.append(' ')
                return html.unescape(''.join(temp_list).replace('&apos', '&apos;').rstrip().lstrip())
        else:
            return 'no message'

    def get_date(self, meta_message):
        return meta_message.find('div', {'class':'pull_right date details'})['title']

    def get_data(self):
        sender = 'no sender'
        for meta_message in self.message_soup:
            if get_sender(meta_message):
                sender = get_sender(meta_message)

            self.data['sender'].append(sender)
            self.data['message'].append(get_message(meta_message))
            self.data['date'].append(get_date(meta_message))

    def add_html_doc(self, html_doc):
        self.html = self.html + '\n' + html_doc
        return 'Presto!'
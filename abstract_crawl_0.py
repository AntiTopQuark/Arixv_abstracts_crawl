import random

import requests
from bs4 import BeautifulSoup
import re


user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64)  Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        ]

def get_html(field,year,month,index):
    user_agent = {'User-Agent' : random.choice(user_agent_list)}
    url = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-%s=y&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date=%s-%s&date-to_date=%s-%s&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&start=%s" %(field,str(year),month,str(year),month,str(index))
    #url = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-physics_archives=all&classification-q_biology=y&classification-include_cross_list=include&date-filter_by=specific_year&date-year=%s&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&start=%s" % (str(year),str(index))
    html = requests.get(url,headers = user_agent)
    return html.content

def parse_html(field,content):
    soup = BeautifulSoup(content, 'lxml')
    abstract_tags = soup.find_all(attrs={"class": "abstract-full has-text-grey-dark mathjax"})
    for tag in abstract_tags:
        abstract = tag.get_text()

        while abstract[0] == " " or abstract[0] == "\n":
            abstract = abstract[1:]
        abstract = abstract[:-16]

        print(abstract)
        write_file(field,abstract)

def write_file(field,abstract):
    if abstract is None:
        pass
    else:

        field = str(field)+".txt"
        file = open(field,"a",encoding="utf-8")
        file.write(abstract+"\n")
        file.close()

if __name__ == '__main__':

    start_year = 2010
    end_year = 2019

    months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    fields = ["computer_science","statistics","q_finance","eess","q_biology","mathematics","economics","physics"]




    field = fields[0]

    for i in range(start_year,end_year+1):
        for month in months:
            for index in range(0,10):
                print("%s %d-%s finished %d %%" %(field,i,month,index*10))

                index = 200 * index
                content = get_html(field,i,month,index)
                parse_html(field,content)

        print("Finished! The year is %d"%i)






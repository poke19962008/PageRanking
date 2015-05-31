__author__ = 'poke19962008'

import re

def remove_html_all_tags(html_doc):
    return re.sub(r'<.*?>', '', html_doc)

def remove_html_tag(html_doc, tag):
    p = re.compile(r'<%s>' % tag)
    return p.sub("", html_doc)

def remove_extra_space(html_doc):
    p = re.compile(r'\s+')
    return p.sub('', html_doc)

# def remove_html_entities(html_doc):
#     p = re.compile("&(#?)(\d{1,5}|\w{1,8});")

def remove_stuff(html_doc):
    html_doc = remove_html_all_tags(html_doc)
    html_doc = remove_extra_space(html_doc)
    return html_doc
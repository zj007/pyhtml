#! /usr/bin/env python
import sys
import re

class Pretty(object):
    def __init__(self, html_str):
        self._html = html_str
        self._initialize()

    def _initialize(self):
        self._p = re.compile(r'([^<>]*?)(<(?P<tag>[\w]+)[^>]*?>)(.*?)(</(?P=tag)>)')
        #xx<html id=1>txt<a></a></html> 
        #[('xx', '<html id=1>', 'html', 'txt<a></a>', '</html>')]
        # 0 father tag content; 1 tag start; 2 tag name; 3 tag content&child 4 tag end
        #print self._p.findall()

    def format(self):
        return self._format_str(self._html, 0)[0]
    
    def _format_str(self, tag_str, space_num):
        tag_list = self._p.findall(tag_str)
        #print tag_list
        if tag_list == []:
            return ' ' * space_num + tag_str, True
        format_str_list = []
        for tag in tag_list:
            if tag[0] != '':
                format_str_list.append(' ' * space_num + tag[0])
            content_child = ('', True)
            if tag[3] != '':
                content_child = self._format_str(tag[3], space_num + 4)
            if content_child[1]:
                format_str_list.append(
                    ' ' * space_num + tag[1] + content_child[0].strip() + tag[4])
            else:
                format_str_list.append(' ' * space_num + tag[1])
                format_str_list.append(content_child[0])
                format_str_list.append(' ' * space_num + tag[4])

        return '\n'.join(format_str_list), False

def main():
    for line in sys.stdin:
        print Pretty(line.strip()).format()

if __name__ == '__main__':
    main()


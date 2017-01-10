#! /usr/bin/env python
"""

author: thinkingCat
"""

import sys
import re
import os
from copy import deepcopy


class Tag(object):
    def __init__(self, tag, content=''):
        self._tag = tag
        self._content = content
        self._attrs = {}
        self._child = ''
        self._initialize()

    def _initialize(self):
        #tag,id,class
        m = re.match(r'(?P<tag>[\w:]+)(\#(?P<id>[\w\-_]+))?(\.(?P<class>[\w\s\-_]+))?(\[(?P<attr>[\w\s:/=;\.\-@]+)\])?', self._tag)
        for k, v in m.groupdict().items():
            if k == 'tag':
                if v is None:
                    raise Exception('tag is empty string')
                self._tag = v
                if v == 'test':
                    print m.groupdict().items()
                continue
            if k == 'attr':
                attr_value_l = [e.split('=') for e in v.split(';')] if v is not None else []
                for attr, value in attr_value_l:
                    self._attrs[attr.strip()] = value.strip()
                continue
            if v is not None:
                self._attrs[k] = v.strip()

    def _attrs2str(self):
        attr_str = ' '.join(['{}="{}"'.format(k, v) for k, v in self._attrs.items()])
        attr_str = ' ' + attr_str if attr_str != '' else ''
        return attr_str

    def name(self):
        return self._tag

    def _recursive_flat_list(self, l):
        _l = []
        for e in l:
            if isinstance(e, list):
                _l.extend(self._recursive_flat_list(e))
            else:
                _l.append(e)
        return _l

    def __gt__(self, child_list):
        _child_list = self._recursive_flat_list(child_list)
        #strip \n in string
        for i, c in enumerate(_child_list):
            if isinstance(c, (str, unicode)):
                _child_list[i] = ''.join([e.strip() for e in c.strip().split('\n')])
        self._child = ''.join(str(e) for e in _child_list)
        return self

    def __str__(self):
        return '<{tag}{attrs}>{content}{child}</{tag}>'.format(
                                                        tag=self._tag,
                                                        attrs=self._attrs2str(),
                                                        content=self._content,
                                                        child=self._child)
    

class load(object):
    def __call__(self, module):
        m_scope =deepcopy(context)
        if module in global_ph_scope_dict:
            m_scope.update(global_ph_scope_dict[module])
            return m_scope
        module_file = self._find_module(module)
        with open(module_file) as fr:
            exec fr.read().strip() in m_scope
        global_ph_scope_dict[module] = m_scope
        return m_scope

    def _find_module(self, module):
        path_str = os.environ.get('PH_PATH', '').strip()
        path_list = path_str.split(';') if path_str != '' else []
        path_list.insert(0, './')
        module_dir = None
        for d in path_list:
            for e in os.listdir(d):
                if not os.path.isfile(os.path.join(d, e)):
                    continue
                try:
                    name, postfix = e.split('.')
                except:
                    continue
                if postfix == 'ph' and name == module:
                    module_dir = d
                    break
        if module_dir is None:
            raise Exception('can not find module<{}>'.format(module))
        return os.path.join(module_dir, '{}.ph'.format(module))


class ddict(dict):
    def __init__(self, **kv):
        self._d = kv
    
    def __getattr__(self, name):
        return self._d[name]
        

context = {'t':Tag,
           'load':load()}

global_ph_scope_dict = {}

def compile(ph_file):
    html = deepcopy(context)
    with open(ph_file) as fr:
        exec fr.read().strip() in html
        print '<!DOCTYPE html>'
        print html['html']

if __name__ == '__main__':
    compile(sys.argv[1])
    

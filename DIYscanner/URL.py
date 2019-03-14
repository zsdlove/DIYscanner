#coding=utf-8
'''
URL.py
url标准化处理
'''
import urlparse
DEFAULT_ENCODING='utf-8'
class URL:
    def __init__(self,url,encoding=DEFAULT_ENCODING):
        self.unicode_url=None
        self._changed=False
        self._encoding=encoding
        if not url.startswith("https://") and not url.startswith("http://"):
            url="http://"+url
        urlres=urlparse.urlparse(url)
        self.scheme=urlres.scheme
        if urlres.port is None:
            self.port=80
        else:
            self.port=urlres.port
        if urlres.netloc.find(":")>1:
            self.netloc=urlres.netloc
        else:
            self.netloc=urlres.netloc+":"+str(self.port)
        self.path=urlres.path
        self.params=urlres.params
        self.qs=urlres.query
        self.fragment=urlres.fragment

    #获取域名
    def get_domain(self):
        return self.netloc.split(':')[0]
    #获取host
    def get_host(self):
        return self.netloc.split(':')[0]

    #获取url中的端口
    def get_port(self):
        return self.port

    #获取url中的路径
    def get_path(self):
        return self.path

    #获取URL中的文件名
    def get_fragment(self):
        return self.fragment

    #获取URL中的文件名
    def get_filename(self):
        return self.path[self.path.rfind('/')+1:]

    #获取URL中的文件扩展名
    def get_ext(self):
        fname=self.get_filename()
        ext=fname[fname.rfind('.')+1:]
        if ext==fname:
            return ''
        else:
            return ext

    #获取URL中的参数
    def get_query(self):
        return self.qs

    #获取URL所对应的完整字符串
    @property
    def url_string(self):
        pass
        u_url=self.unicode_url
        if not self._changed or u_url is None:
            data=(self.scheme,self.netloc,self.path,self.params,self.qs,self.fragment)
            dataurl=urlparse.urlunparse(data)
            try:
                u_url=unicode(dataurl)
            except UnicodeDecodeError:
                u_url=unicode(dataurl,self._encoding,'replace')
            self.unicode_url=u_url
            self._changed=True
        return u_url
if __name__=="__main__":
    url=URL("http://www.moresec.com/book/index.jsp?id=1#top")
    assert url.get_host()=="www.moresec.com"
    assert url.get_port()==80
    assert url.get_path()=="/book/index.jsp"
    assert url.get_filename()=="index.jsp"
    assert url.get_ext()=="jsp"
    assert url.get_query()=="id=1"
    assert url.get_fragment()=="top"
    assert url.url_string()=="http://www.moresec.com/book/index.jsp?id=1#top"
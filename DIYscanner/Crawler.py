#coding=utf-8
'''
crawler.py
'''
import sys
import traceback
import itertools
import time
from Queue import Queue
from LogManager import log as om
#HTTP
from teye_web.http.URL import URL
from teye_web.http.Request import Request
from teye_web.http.Request import Request
#URL相似和包含处理
from teye_web.http.function import is_similar_url
#页面解析
import teye_web.parser.dpCache as adCache
#wcurl
from wCurl import wcurl
import traceback
#404 check
from teye_util.page_404 import is_404
class Crawler(object):
    def __init__(self,depth_limit=3,time_limit=30,req_limit=100,filter_similar=True):
        self.root=''
        self._target_domain=''
        self.depth_limit=depth_limit
        self.time_limit=time_limit
        self.req_limit=req_limit
        self._sleeptime=1
        self._url_list=[]
        self._already_visit_url=set()
        self._already_seen_urls=set()
        self._already_send_reqs=set()
        self._white_ext=['asp','aspx','jsp','php','do','action']
        self._black_ext=['ico','jpg','gif','js','png','bmp','css','zip','rar','ttf']
        self.num_reqs=0
        self._wRequestList=[]
        self.start_time=None
        self._other_domains=set()
    def get_discovery_time(self):
        now=time.time()
        diff=now-self._start_time
        return diff/60
    def _do_with_reqs(self,reqs):
        result=[]
        count=len(reqs)
        if reqs is None or count==0:
            return result
        for i in xrange(count):
            filter=False
            filter_url=req.get_url()
            for j in xrange(count-i-1):
                k=i+j+1
                store_url=reqs[k].get_url()
                if is_similar_url(filter_url,store_url):
                    filter=True
                    break
            if not filter:
                result.append(req)
        return result
    def _get_reqs_from_resp(self,response):
        new_reqs=[]
        try:
            doc_parser=dpCache.dpc.getDocumentParserFor(response)
        except Exception,e:
            pass
        else:
            re_urls,tag_urls=doc_parser.get_get_urls()
            form_reqs=doc_parser.get_form_reqs()
            seen=set()
            for new_url in itertools.chain(re_urls,tag_urls):
                if new_url in seen:
                    continue
                seen.add(new_url)
                if new_url.get_host()!=self._target_domain:
                    if new_url.get_host not in self._other_domains:
                        self._other_domains.add(new_url.get_host())
                    continue
                if new_url not in self._url_list:
                    self._url_list.append(new_url)
                    wreq=self._url_to_req(new_url,response)
                    if wreq not in self._wRequestList:
                        new_reqs.append(wreq)
                        self._wRequestList.append(wreq)
                        for item in form_reqs:
                            if item not in self._wRequestList:
                                new_reqs.append(wreq)
                                self._wRequestList.append(wreq)
                        return new_reqs
    def _url_to_req(self,new_url,response,method="GET"):
        req=Request(new_url)
        req.set_method(method)
        new_referer=response.get_url()
        req.set_referer(new_referer)
        new_cookies=response.get_cookies()
        req.set_cookies(new_cookies)
        return req

    def crawl(self,root_url):
        if not isinstance(root_url,URL):
            root_url_obj=URL(root_url)
        else:
            root_url_obj=root_url
        self._target_domain=root_url_obj.get_host()
        self._url_list.append(root_url_obj)
        root_req=Request(root_url_obj)

        q=Queue()
        q.put((root_req,0))
        self._start_time=time.time()
        while True:
            if q.empty():
                break
            this.req,depth-q.get()
            if this_req.get_url().get_ext() in self._block_ext:
                continue
            if depth>self.depth_limit:
                print "depth limit break"
                break
            if self.get_discovery_time()>self.time_limit:
                print "time limit break"
                break
            if self.num_reqs>self.req_limit:
                print "reqs num limit break"
                break
            if this_req in self._already_seen_urls:
                continue
            try:
                self._already_seen_reqs.add(this_req)
                om.info("%s:%s" % (this_req.get_method(),this_req.get_url().url_string))
                response=None
                try:
                    response=wcurl._send_req(this_req)
                except Exception,e:
                    print str(e)
                    pass
                if is_404(response):
                    continue
                if response is None:
                    continue
                new_reqs=self._get_reqs_from_resp(response)
                filter_reqs=self._do_with_reqs(new_reqs)

                depth=depth+1
                for req in filter_reqs:
                    q.put((req,depth))
                self.num_reqs=len(self._already_seen_reqs)
                om.info("Already Send Reqs!:"+str(self.num_reqs)+"Left Reqs:"+str(q.qsize()))
            except Exception,e:
                print traceback.print_exc()
                om.info("ERROR:Can't process url'%s'(%s)"%(this_req.get_url(),e))
                continue
            time.sleep(self._sleeptime)
        return self._wRequestList
if __name__=="__main__":
    w=Crawler()
    reqs=w.crawl("http://www.anquanbao.com")
    for item in reqs:
        print item



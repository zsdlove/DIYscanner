#coding=utf-8
'''
hooktest
'''
import func
def _hook_show(*args,**kwargs):
    print "hook show func"
    realfun,=args
    return apply(realfun)

def hook():
    _show=func.show
    func.show=lambda :apply(_hook_show,(_show,))#hook

if __name__=="__main__":
    hook()
    func.show()


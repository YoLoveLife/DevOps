from apps.callback.module import BaseModule
class CopyModule(BaseModule):

    def value2Args(self,*args,**kwargs):
        self._size = self._result['size']
        self._own = self._result['own']
        self._group = self._result['group']
        self._md5sum = self._result['md5sum']
        self._dest = self._result['dest']
        self._mode = self._result['mode']

        return super(CopyModule,self).value2Args(*args,**kwargs)




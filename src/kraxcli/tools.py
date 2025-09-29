import sys
import subprocess

def tool_upydev(args,*_,**kwargs):
    sys.argv = ['upydev']+args
    try:
        if getattr(sys, 'frozen', False):
            import _upydev
        else:
            from . import _upydev
    except Exception as e:
        print(f'Ошибка: {e}')
    return

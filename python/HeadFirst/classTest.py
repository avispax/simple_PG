class CountFromBy :
    
    def __init__(self, v:int=0, i:int=1) -> None:
        print('init')

    def __enter__(self):
        print('enter')
        return self

    def myFunc(self):
        print('myFunc')

    def __exit__(self, v,w,x):
        print('exit')

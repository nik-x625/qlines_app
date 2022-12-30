class myclass():
    def __init__(self, par):
        print('the init par is: '+str(par))
        # return 1

    class_param1 = 10
    class_param2 = 20

    def mymethod(self, par2):
        print('the mymethod par is: '+str(par2))
        return 1


a = myclass('x')
a.mymethod('y')

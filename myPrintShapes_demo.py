# Демонстрации возможностей модуля myPrintShapes.ry

#import myPrintShapes
#myPrintShapes.print_rectange()

#from  myPrintShapes import *
from myPrintShapes import print_rectange

def main():
    w = int(input('Ширина? '))
    h = int(input('Высота? '))
    f = int(input('Залить? [y/n] '))
    is_fill = f.lower() =='y'

    print_rectange(w, h, is_fill=is_fill)

if __name__ == "__main__":
    main()
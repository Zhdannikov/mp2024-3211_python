# Модуль для рисования в консоли

def print_rectange(width: int, height: int, symbol: str = "*", is_fill: bool = True):
    """Нарисовать прямоугольник в консолию
    Параметры:
    width - ширина
    height - высотв
    symbol - символ рисования
    is_fill - признак залития фигуры"""

    for r in range(height):
      if r==0 or r == height - 1 or is_fill:
       print(symbol * width)
      else:
       print( symbol + ' ' * (width - 2) + symbol)
print("Модуль myPrintShapes.ry - Загружен")  

if __name__ == "__main__":
  print("Модуль myPrintShapes.ry - Главный")  
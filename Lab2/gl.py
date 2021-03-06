import struct
import random

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h',w)

def dword(d):
    return struct.pack('=l',d)

def color(r,g,b):
    return bytes([b,g,r])

class Render(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = []
        self.clear()
        self.current_color = color(0,0,0)
    def clear(self):
        self.pixels = [[color(255,255,255) for x in range(self.width)]
        for y in range(self.height)]
    def write(self, filename):
      f = open(filename,'bw')

      #file header
      f.write(char('B'))
      f.write(char('M'))
      f.write(dword(14+40+self.width * self.height * 3))
      f.write(dword(0))
      f.write(dword(14+40))
      f.write(dword(40))
      f.write(dword(self.width))
      f.write(dword(self.height))
      f.write(word(1))
      f.write(word(24))
      f.write(dword(0))
      f.write(dword(self.width * self.height * 3))
      f.write(dword(0))
      f.write(dword(0))
      f.write(dword(0))
      f.write(dword(0))

      for x in range(self.height):
          for y in range(self.width):
              f.write(self.pixels[x][y])

      f.close()

    def display(self, filename='out.bmp'):
    
      self.write(filename)

      try:
        from wand.image import Image
        from wand.display import display

        with Image(filename=filename) as image:
          display(image)
      except ImportError:
        pass  # do nothing if no wand is installed

    def set_color(self, color):
      self.current_color = color

    def point(self, x, y, color = None):
      self.pixels[y][x] = color or self.current_color
    def triangle(self, A, B, C, color=None):
      if A.y > B.y:
        A, B = B, A
      if A.y > C.y:
        A, C = C, A
      if B.y > C.y: 
        B, C = C, B

      dx_ac = C.x - A.x
      dy_ac = C.y - A.y
      if dy_ac == 0:
          return
      mi_ac = dx_ac/dy_ac

      dx_ab = B.x - A.x
      dy_ab = B.y - A.y
      if dy_ab != 0:
          mi_ab = dx_ab/dy_ab

          for y in range(A.y, B.y + 1):
              xi = round(A.x - mi_ac * (A.y - y))
              xf = round(A.x - mi_ab * (A.y - y))

              if xi > xf:
                  xi, xf = xf, xi
              for x in range(xi, xf + 1):
                  self.point(x, y, color)

      dx_bc = C.x - B.x
      dy_bc = C.y - B.y
      if dy_bc:
          mi_bc = dx_bc/dy_bc

          # dacx = C.x - A.x
          # dacy = C.y - A.y
          # miac = dacx/dacy  // we have mi_ac already!

          for y in range(B.y, C.y + 1):
              xi = round(A.x - mi_ac * (A.y - y))
              xf = round(B.x - mi_bc * (B.y - y))

              if xi > xf:
                  xi, xf = xf, xi
              for x in range(xi, xf + 1):
                  self.point(x, y, color)
      
    def line(self, start, end, color = None):
     
      x1, y1 = start
      x2, y2 = end

      dy = abs(y2 - y1)
      dx = abs(x2 - x1)
      steep = dy > dx

      if steep:
          x1, y1 = y1, x1
          x2, y2 = y2, x2

      if x1 > x2:
          x1, x2 = x2, x1
          y1, y2 = y2, y1

      dy = abs(y2 - y1)
      dx = abs(x2 - x1)

      offset = 0
      threshold = dx

      y = y1
      for x in range(x1, x2 + 1):
          if steep:
              self.point(y, x, color)
          else:
              self.point(x, y, color)
          
          offset += dy * 2
          if offset >= threshold:
              y += 1 if y1 < y2 else -1
              threshold += dx * 2

#r = Render(800,600)
#r.point(100,200, color(255,255,255))
#r.write('luisa.bmp')

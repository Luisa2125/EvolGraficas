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

    def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), texture=None):
      """
      Loads an obj file in the screen
      Input: 
        filename: the full path of the obj file
        translate: (translateX, translateY) how much the model will be translated during render
        scale: (scaleX, scaleY) how much the model should be scaled
        texture: texture file to use
      """
      model = Obj(filename)
      light = V3(0,0,1)

      for face in model.vfaces:
          vcount = len(face)

          if vcount == 3:
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1

            a = self.transform(model.vertices[f1], translate, scale)
            b = self.transform(model.vertices[f2], translate, scale)
            c = self.transform(model.vertices[f3], translate, scale)

            normal = norm(cross(sub(b, a), sub(c, a)))
            intensity = dot(normal, light)

            if not texture:
              grey = round(255 * intensity)
              if grey < 0:
                continue
              self.triangle(a, b, c, color=color(grey, grey, grey))
            else:
              t1 = face[0][1] - 1
              t2 = face[1][1] - 1
              t3 = face[2][1] - 1
              tA = V3(*model.tvertices[t1])
              tB = V3(*model.tvertices[t2])
              tC = V3(*model.tvertices[t3])

              self.triangle(a, b, c, texture=texture, texture_coords=(tA, tB, tC), intensity=intensity)
            
          else:
            # assuming 4
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1
            f4 = face[3][0] - 1   

            vertices = [
              self.transform(model.vertices[f1], translate, scale),
              self.transform(model.vertices[f2], translate, scale),
              self.transform(model.vertices[f3], translate, scale),
              self.transform(model.vertices[f4], translate, scale)
            ]

            normal = norm(cross(sub(vertices[0], vertices[1]), sub(vertices[1], vertices[2])))  # no necesitamos dos normales!!
            intensity = dot(normal, light)
            grey = round(255 * intensity)

            A, B, C, D = vertices 

            if not texture:
              grey = round(255 * intensity)
              if grey < 0:
                continue
              self.triangle(A, B, C, color(grey, grey, grey))
              self.triangle(A, C, D, color(grey, grey, grey))            
            else:
              t1 = face[0][1] - 1
              t2 = face[1][1] - 1
              t3 = face[2][1] - 1
              t4 = face[3][1] - 1
              tA = V3(*model.tvertices[t1])
              tB = V3(*model.tvertices[t2])
              tC = V3(*model.tvertices[t3])
              tD = V3(*model.tvertices[t4])
              
              self.triangle(A, B, C, texture=texture, texture_coords=(tA, tB, tC), intensity=intensity)
              self.triangle(A, C, D, texture=texture, texture_coords=(tA, tC, tD), intensity=intensity)
              


#r = Render(800,600)
#r.point(100,200, color(255,255,255))
#r.write('luisa.bmp')

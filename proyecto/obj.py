#luisa Arboleda
import struct 


def color(r, g, b):
  return bytes([b, g, r])

class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.tvertices = []
        self.vfaces = []
        self.read()

    def read(self):
        
        for line in self.lines:
            if line:
                
                try:
                    prefix, value = line.split('  ',1)
                    
                except:
                    prefix,value = '',''
                
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                if prefix == 'vt':
                    self.tvertices.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    #print('face',value)
                    to_app = []
                    for face in value.split(' ')[:-1]: 

                        faces = []
                        new_face = face.split('/')
                        
                        for i in new_face:
                            try:
                                faces.append(int(i))
                            except:
                                faces.append(0)
                       #print('faces',faces)
                        to_app.append(faces)

                    self.vfaces.append(to_app)
        #print(self.tvertices)

class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        image = open(self.path, "rb")
        # we ignore all the header stuff
        image.seek(2 + 4 + 4)  # skip BM, skip bmp size, skip zeros
        header_size = struct.unpack("=l", image.read(4))[0]  # read header size
        image.seek(2 + 4 + 4 + 4 + 4)
        
        self.width = struct.unpack("=l", image.read(4))[0]  # read width
        self.height = struct.unpack("=l", image.read(4))[0]  # read width
        self.pixels = []
        image.seek(header_size)
        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                self.pixels[y].append(color(r,g,b))
        image.close()

    def get_color(self, tx, ty, intensity=1):
        x = int(tx * self.width)
        y = int(ty * self.height)
        # return self.pixels[y][x]
        try:
            return bytes(map(lambda b: round(b*intensity) if b*intensity > 0 else 0, self.pixels[y][x]))
        except:
            pass  # what causes this




'''
r = Render(800,600)
model = Obj("./Bigmax_White_OBJ.obj")
co = 1
#print(model.vfaces)
for face in model.vfaces:
    #print(co)
    co+=1
    #print('face',face)
    vcount = len(face)
    for j in range(vcount):
        f1 = face[j][0]
        f2 = face[(j+1)%vcount][0]

        v1 = model.vertices[f1 - 1]
        v2 = model.vertices[f2 - 1]

        scaleX, scaleY = (5,5)
        translateX, translateY = (80,2)

        x1 = round((v1[0] + translateX) * scaleX); 
        y1 = round((v1[1] + translateY) * scaleY); 
        x2 = round((v2[0] + translateX) * scaleX); 
        y2 = round((v2[1] + translateY) * scaleY); 
      
        r.line((x1, y1), (x2, y2))
        #print('line',(x1, y1), (x2, y2))

r.write("model.bmp")
'''
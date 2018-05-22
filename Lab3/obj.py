#luisa Arboleda

from gl import Render

class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.vfaces = []
        self.read()

    def read(self):
        
        for line in self.lines:
            if line:
                
                try:
                    prefix, value = line.split('  ')
                    
                except:
                    prefix,value = '',''
                
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                    
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


r = Render(800,600)
model = Obj("./Luigi_obj.obj")
co = 1
#print("lala ",model.vfaces)
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

        scaleX, scaleY = (4,4)
        translateX, translateY = (130,2)

        x1 = round((v1[0] + translateX) * scaleX); 
        y1 = round((v1[1] + translateY) * scaleY); 
        x2 = round((v2[0] + translateX) * scaleX); 
        y2 = round((v2[1] + translateY) * scaleY); 
      
        r.line((x1, y1), (x2, y2))
        #print('line',(x1, y1), (x2, y2))

r.write("model.bmp")

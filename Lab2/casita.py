from gl import Render
from gl import color
r = Render(600,790)
from collections import namedtuple
#casita
def contorno(r):
	#columnas verticales
	r.line((70,200),(70,320),color(203, 67, 53))#izquierda
	r.line((190,130),(190,250),color(203, 67, 53))#medio
	r.line((530,150),(530,270),color(203, 67, 53))#derecha
	#uniones
	r.line((70,320),(190,250),color(203, 67, 53))#izquierda medio superior
	r.line((70,200),(190,130),color(203, 67, 53))#izquierda medio inferior

	r.line((190,130),(530,150),color(203, 67, 53))#medio derecha inferior

	#puerta
	r.line((310,139),(310,235),color(203, 67, 53))#columna izquierda
	r.line((410,144),(410,240),color(203, 67, 53))#columna derecha
	r.line((310,235),(410,240),color(203, 67, 53))#union superior
	r.line((310,138),(410,143),color(255, 255, 255))
	r.line((310,137),(410,142),color(255, 255, 255))
	r.line((310,136),(410,141),color(255, 255, 255))

	#techo
	r.line((70,320),(260,520),color(203, 67, 53))#diagonal izquierda
	r.line((190,250),(380,450),color(203, 67, 53))#diagonal medio izquierdo
	r.line((380,450),(530,270),color(203, 67, 53))#diagonal medio derecha
	r.line((380,450),(260,520),color(203, 67, 53))#diagonal medio superior

	#chimenea
	r.line((310,490),(310,505),color(203, 67, 53))#columna inferior izquierda
	r.line((296,500),(296,515),color(203, 67, 53))#columna superior izquierda
	r.line((296,515),(310,505),color(203, 67, 53))#union anteriores
	r.line((325,483),(325,510),color(203, 67, 53))#columna derecha
	r.line((310,505),(325,510),color(203, 67, 53))#union anterior con izquierda inferior
	r.line((325,510),(311,520),color(203, 67, 53))#union1
	r.line((311,520),(296,515),color(203, 67, 53))#union2

#fondo
def fondo(r):
	x = 0;
	y = 10

	for __ in range(26):
		x=0
		for _ in range(20):
			print('x ',x,y,_,(x+29,y-10),(x+30,y))
			try:
				r.line((x,y),(x+15,y+5),color(0, 0, 0))
				r.line((x,y+20),(x+15,y+15),color(0,0,0))

			except:
				r.line((x,y),(x+15,y+5),color(0, 0, 0))
				r.line((x,y+19),(x+15,y+15),color(0,0,0))
			r.line((x+15,y+5),(x+15,y+15),color(0,0,0))
			try:
				r.line((x+15,y+5),(x+30,y),color(0, 0, 0))
				r.line((x+15,y+15),(x+30,y+20),color(0, 0, 0))
				r.line((x+30,y-10),(x+30,y),color(0,0,0))
				r.line((x+30,780),(x+30,789),color(0,0,0))
			except:
				r.line((x+15,y+4),(x+29,y),color(0, 0, 0))
				r.line((x+15,y+15),(x+29,y+20),color(0, 0, 0))
				r.line((x+29,y-10),(x+29,y),color(0,0,0))
				r.line((x+29,780),(x+29,789),color(0,0,0))

			#print('x ',x, _)
			x+=30
		y+=30


	#r.line((0,10),(15,15),color(0, 0, 0))
	#r.line((15,15),(30,10),color(0, 0, 0))
V2 = namedtuple('Point2', ['x', 'y'])
def pintar_casa(r):
	#cara izquierda
	r.triangle(V2(70,200),V2(70,320),V2(190,130), color(146, 43, 33))
	r.triangle(V2(70,320),V2(190,130),V2(190,250), color(146, 43, 33))
	#techo
	r.triangle(V2(70,320),V2(260,520),V2(190,250), color(192, 57, 43))
	r.triangle(V2(260,520),V2(190,250),V2(380,450),color(192, 57, 43))
	#techo fromtal
	r.triangle(V2(190,250),V2(380,450),V2(530,270),color(169, 50, 38))
	#enfrente
	r.triangle(V2(190,130),V2(190,250),V2(310,139),color(169, 50, 38))
	r.triangle(V2(530,150),V2(530,270),V2(410,144), color(169, 50, 38))
	#--laterales
	r.triangle(V2(310,139),V2(310,335),V2(190,250),color(169, 50, 38))
	r.triangle(V2(410,144),V2(410,340),V2(530,270),color(169, 50, 38))
	#frontal
	r.triangle(V2(310,335),V2(310,235),V2(410,300),color(169, 50, 38))
	r.triangle(V2(410,300),V2(410,240),V2(310,235),color(169, 50, 38))

	#chimenea
	r.triangle(V2(310,490),V2(310,505),V2(296,500),color(146, 43, 33))
	r.triangle(V2(310,505),V2(296,500),V2(296,515),color(146, 43, 33))

	r.triangle(V2(296,500),V2(296,515),V2(325,483),color(169, 50, 38))
	r.triangle(V2(296,515),V2(325,483),V2(325,510),color(169, 50, 38))

	r.triangle(V2(310,505),V2(296,515),V2(325,510),color(192, 57, 43))
	r.triangle(V2(296,515),V2(325,510),V2(311,520),color(192, 57, 43))


fondo(r)
contorno(r)
pintar_casa(r)
r.write('casita.bmp')
r.display('casita.bmp')

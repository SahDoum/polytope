from polytope import *

def right_120cell(alpha=2.513):  
    phi = (math.sqrt(5)+1)/2
    x_coord = (phi ** 3)

    simp = Simplex()
    simp.add_vert(Point(4, x_coord, 1, 1, 1)) # <-
    simp.add_vert(Point(4, x_coord, 1, 1, -1))
    simp.add_vert(Point(4, x_coord, 1, -1, 1))
    simp.add_vert(Point(4, x_coord, 1, -1, -1))
    simp.add_vert(Point(4, x_coord, -1, 1, 1)) # <-
    simp.add_vert(Point(4, x_coord, -1, 1, -1))
    simp.add_vert(Point(4, x_coord, -1, -1, 1))
    simp.add_vert(Point(4, x_coord, -1, -1, -1))
    simp.add_vert(Point(4, x_coord, 0, phi, 1/phi)) # <-
    simp.add_vert(Point(4, x_coord, 0, phi, -1/phi))
    simp.add_vert(Point(4, x_coord, 0, -phi, 1/phi)) 
    simp.add_vert(Point(4, x_coord, 0, -phi, -1/phi))
    simp.add_vert(Point(4, x_coord, phi, 1/phi, 0))
    simp.add_vert(Point(4, x_coord, phi, -1/phi, 0))
    simp.add_vert(Point(4, x_coord, -phi, 1/phi, 0))
    simp.add_vert(Point(4, x_coord, -phi, -1/phi, 0))
    simp.add_vert(Point(4, x_coord, 1/phi, 0, phi)) # <-
    simp.add_vert(Point(4, x_coord, 1/phi, 0, -phi))
    simp.add_vert(Point(4, x_coord, -1/phi, 0, phi)) # <-
    simp.add_vert(Point(4, x_coord, -1/phi, 0, -phi))
    simp.add_minimal_edges()

    ambda = math.cos(alpha) / math.sqrt(1/4*(1/phi**2+1)) #math.sin(144/180*2*math.pi)
    p = Point(4, math.sin(alpha), 0, ambda/2/phi, ambda/2)
    simp_r = simp.reflect(p, -(p*Point(4, x_coord, 1, 1, 1))) # <-
    doubled_dod = simp.glue(simp_r)
    inthreedim = doubled_dod.stereographic(Point(4, x_coord+100000.4, 0, 0, 0), 0)
    
    return inthreedim   


def dodecahedron():  
    phi = (math.sqrt(5)+1)/2
    x_coord = (phi ** 3)
    simp = Simplex()
    simp.add_vert(Point(3, 1, 1, 1)) # <-
    simp.add_vert(Point(3, 1, 1, -1))
    simp.add_vert(Point(3, 1, -1, 1))
    simp.add_vert(Point(3, 1, -1, -1))
    simp.add_vert(Point(3, -1, 1, 1)) # <-
    simp.add_vert(Point(3, -1, 1, -1))
    simp.add_vert(Point(3, -1, -1, 1))
    simp.add_vert(Point(3, -1, -1, -1))
    simp.add_vert(Point(3, 0, phi, 1/phi)) # <-
    simp.add_vert(Point(3, 0, phi, -1/phi))
    simp.add_vert(Point(3, 0, -phi, 1/phi)) 
    simp.add_vert(Point(3, 0, -phi, -1/phi))
    simp.add_vert(Point(3, phi, 1/phi, 0))
    simp.add_vert(Point(3, phi, -1/phi, 0))
    simp.add_vert(Point(3, -phi, 1/phi, 0))
    simp.add_vert(Point(3, -phi, -1/phi, 0))
    simp.add_vert(Point(3, 1/phi, 0, phi)) # <-
    simp.add_vert(Point(3, 1/phi, 0, -phi))
    simp.add_vert(Point(3, -1/phi, 0, phi)) # <-
    simp.add_vert(Point(3, -1/phi, 0, -phi))
    simp.add_minimal_edges()

    p = Point(3, 0, 1/2/phi, 1/2)
    simp_r = simp.reflect(p, -(p*Point(3, 1, 1, 1))) # <-
    doubled_dod = simp.glue(simp_r)
    #inthreedim = doubled_dod.stereographic(Point(4, 100000, 0, 0, 0), 0) #x_coord+0.4
    
    return doubled_dod

def sliced_cube(alpha=0.1):
    simp = Simplex()
    p1 = Point(3, 0, 0, 0)
    p2_1 = Point(3, 0, 0, 1-alpha)
    p2_2 = Point(3, 0, alpha, 1)
    p3_1 = Point(3, 0, 1-alpha, 0)
    p3_2 = Point(3, alpha, 1, 0)
    p4_1 = Point(3, 0, 1-alpha, 1)
    p4_2 = Point(3, alpha, 1, 1)
    p5_1 = Point(3, 1-alpha, 0, 0)
    p5_2 = Point(3, 1, 0, alpha)
    p6_1 = Point(3, 1, 0, 1-alpha)
    p6_2 = Point(3, 1, alpha, 1)
    p7_1 = Point(3, 1-alpha, 1, 0)
    p7_2 = Point(3, 1, 1, alpha)
    p8 = Point(3, 1, 1, 1)

    simp.add_edge(Edge(p1, p5_1))
    simp.add_edge(Edge(p1, p3_1))
    simp.add_edge(Edge(p1, p2_1))

    simp.add_edge(Edge(p8, p7_2))
    simp.add_edge(Edge(p8, p4_2))
    simp.add_edge(Edge(p8, p6_2))

    simp.add_edge(Edge(p5_1, p7_1))
    simp.add_edge(Edge(p3_1, p4_1))
    simp.add_edge(Edge(p2_1, p6_1))

    simp.add_edge(Edge(p5_2, p7_2))
    simp.add_edge(Edge(p3_2, p4_2))
    simp.add_edge(Edge(p2_2, p6_2))

    simp.add_edge(Edge(p2_1, p2_2))
    simp.add_edge(Edge(p3_1, p3_2))
    simp.add_edge(Edge(p4_1, p4_2))
    simp.add_edge(Edge(p5_1, p5_2))
    simp.add_edge(Edge(p6_1, p6_2))
    simp.add_edge(Edge(p7_1, p7_2))

    simp.add_edge(Edge(p5_2, p6_1))
    simp.add_edge(Edge(p3_2, p7_1))
    simp.add_edge(Edge(p2_2, p4_1))

    return simp


def tesseract():
    simp = Simplex()
    simp.add_vert(Point(4, 1, 1, 1, 1))
    simp.add_vert(Point(4, 1, 1, 1, -1))
    simp.add_vert(Point(4, 1, 1, -1, 1))
    simp.add_vert(Point(4, 1, 1, -1, -1))
    simp.add_vert(Point(4, 1, -1, 1, 1))
    simp.add_vert(Point(4, 1, -1, 1, -1))
    simp.add_vert(Point(4, 1, -1, -1, 1))
    simp.add_vert(Point(4, 1, -1, -1, -1))
    simp.add_vert(Point(4, -1, 1, 1, 1))
    simp.add_vert(Point(4, -1, 1, 1, -1))
    simp.add_vert(Point(4, -1, 1, -1, 1))
    simp.add_vert(Point(4, -1, 1, -1, -1))
    simp.add_vert(Point(4, -1, -1, 1, 1))
    simp.add_vert(Point(4, -1, -1, 1, -1))
    simp.add_vert(Point(4, -1, -1, -1, 1))
    simp.add_vert(Point(4, -1, -1, -1, -1))
    simp.add_minimal_edges()

    simp2 = simp.reflect(Point(4, 0, 1, 0, 0), -1)
    #simp = simp.glue(simp2)
    proj_simp = simp.stereographic(Point(4, 0, 5.5, 0, 0), 1)

    return proj_simp


def icosahedron():  
    phi = (math.sqrt(5)+1)/2
    x_coord = (phi ** 3)
    simp = Simplex()
    simp.add_vert(Point(3, 0, phi, 1)) # <-
    simp.add_vert(Point(3, 0, phi, -1))
    simp.add_vert(Point(3, 0, -phi, 1)) 
    simp.add_vert(Point(3, 0, -phi, -1))
    simp.add_vert(Point(3, phi, 1, 0))
    simp.add_vert(Point(3, phi, -1, 0))
    simp.add_vert(Point(3, -phi, 1, 0))
    simp.add_vert(Point(3, -phi, -1, 0))
    simp.add_vert(Point(3, 1, 0, phi)) # <-
    simp.add_vert(Point(3, 1, 0, -phi))
    simp.add_vert(Point(3, -1, 0, phi)) # <-
    simp.add_vert(Point(3, -1, 0, -phi))
    simp.add_minimal_edges()
    
    return simp


def football():  
    simp = icosahedron()

    c = 2/3
    l = len(simp.vertices)

    for i in range(l):
        v1 = simp.vertices[i]

        for e in simp.edges:
            if v1 is not e.v1 and v1 is not e.v2:
                continue

            v2 = e.v1 if v1 == e.v2 else e.v2
            v_tmp = v2 - v1
            v3 = v1 + 1/math.sqrt(v_tmp*v_tmp)*c*v_tmp
            # v3 = c1*v2 + (1-c1)*v
            print('Hi')
            if v1 == e.v1:
                e.v1 = v3
            else:
                e.v2 = v3
            simp.add_vert(v3)

    #for i in range(l):
    #    simp.vertices.pop()

    simp.vertices = simp.vertices[l:]
    simp.add_minimal_edges()
    
    return simp


if __name__ == '__main__':
    sliced_cube()
    right_120cell()

    '''
    test_simp = Simplex()
    test_simp.add_vert(Point(3, 1, 0, 0))
    test_simp.add_vert(Point(3, 0, 1, 0))
    test_simp.add_vert(Point(3, 0, 0, 1))
    test_simp.add_minimal_edges()
    test_simp.stereographic(Point(3, 2, 0, 0), 0).matrix()
    '''
import math

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class Point:
    def __init__(self, dim, *args):
        self.dim = dim
        self.coords = list(args)
       
    def __repr__(self):
        text = '{}-point: '.format(self.dim)
        for v in self.coords:
            text += '{}, '.format(v)
        return text
   
    def __eq__(p1, p2):
        if p1.dim != p2.dim:
            return False
        for i in range(p1.dim):
            if p1.coords[i] != p2.coords[i]:
                return False
        return True

    def __add__(p1, p2):
        if p1.dim != p2.dim:
            return 0
        new_point = Point(p1.dim)
        for i in range(p1.dim):
            new_point.coords.append(p1.coords[i]+p2.coords[i])
        return new_point

    def __sub__(p1, p2):
        if p1.dim != p2.dim:
            return 0
        new_point = Point(p1.dim)
        for i in range(p1.dim):
            new_point.coords.append(p1.coords[i]-p2.coords[i])
        return new_point
       
    def __mul__(p1, p2):
        if p1.dim != p2.dim:
            return 0
        result = 0
        for i in range(p1.dim):
            result += p1.coords[i]*p2.coords[i]
        return result

    def __rmul__(p1, number):
        new_point = Point(p1.dim)
        for i in range(p1.dim):
            new_point.coords.append(p1.coords[i]*number)
        return new_point
       
    def reflect(p, v, d):
        if v.dim != p.dim:
            return None
        refl_point = Point(v.dim)
        pv = v*p
        vv = v*v
        for i in range(len(p.coords)):
            delta = 2*pv/vv*v.coords[i] + 2*d*v.coords[i]/vv
            refl_point.coords.append(p.coords[i] - delta)
        return refl_point

    def len(p1, p2):
        if p1.dim != p2.dim:
            return -1
        l = 0
        for i in range(p1.dim):
            l += (p1.coords[i] - p2.coords[i])**2
        return math.sqrt(l)

    def stereographic(self, o_point, i_coord):
        if self.dim != o_point.dim:
            return None
        p = Point(self.dim-1)
        k = o_point.coords[i_coord]/(o_point.coords[i_coord] - self.coords[i_coord])
        for i in range(self.dim):
            if i == i_coord:
                continue
            new_coord = o_point.coords[i] + k*(self.coords[i] - o_point.coords[i])
            p.coords.append(new_coord)
           
        return p
           
class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
       
    def __eq__(e1, e2):
        if e1.v1 == e2.v1 and e1.v2 == e2.v2:
            return True
        if e1.v1 == e2.v2 and e1.v2 == e2.v1:
            return True
        return False
       
    def __repr__(self):
        text = 'Edge: {} {}'.format(self.v1, self.v2)
        return text
   
class Simplex:
    def __init__(self):
        self.vertices = []
        self.edges = []
       
    def add_edge(self, e):
        if e in self.edges:
            return
        if e.v1 not in self.vertices:
            self.vertices.append(e.v1)
        if e.v2 not in self.vertices:
            self.vertices.append(e.v2)
        self.edges.append(e)

    def add_vert(self, v):
        if v in self.vertices:
            return
        self.vertices.append(v)
       
    def glue(s1, s2):
        s = Simplex()
        for e in s1.edges:
            s.add_edge(e)
        for e in s2.edges:
            s.add_edge(e)
        return s
       
    def reflect(s, v, d):
        simp = Simplex()
        for e in s.edges:
            re = Edge(e.v1.reflect(v, d), e.v2.reflect(v, d))
            simp.add_edge(re)
        for vert in s.vertices:
            simp.add_vert(vert.reflect(v, d))

        return simp
       
    def stereographic(s, o_point, i_coord):
        simp = Simplex()
        for e in s.edges:
            re = Edge(e.v1.stereographic(o_point, i_coord), 
                      e.v2.stereographic(o_point, i_coord))
            simp.add_edge(re)
        for vert in s.vertices:
            simp.add_vert(vert.stereographic(o_point, i_coord))

        return simp

    def add_minimal_edges(s):
        if len(s.vertices) < 2:
            return
        min_l = s.vertices[0].len(s.vertices[1])
        for v1 in s.vertices:
            for v2 in s.vertices:
                if v1 == v2:
                    continue
                tmp_l = v1.len(v2)

                if min_l > tmp_l:
                    min_l = tmp_l

        for v1 in s.vertices:
            for v2 in s.vertices:
                tmp_l = v1.len(v2)
                if isclose(tmp_l, min_l):
                    e = Edge(v1, v2)
                    s.add_edge(e)

    def matrix(self):
        for i, v in enumerate(self.vertices):
            str = '{}. '.format(i+1)
            for c in v.coords:
                str += '{}; '.format(c)
            print(str+'\n')
        matrix = {}
        for i in range(len(self.vertices)):
            matrix[i] = {}
            str = ''
            for j in range(len(self.vertices)):
                e = Edge(self.vertices[i], self.vertices[j])
                if e in self.edges:
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = 0
                str += '{} '.format(matrix[i][j])
            print(str)

        return matrix
       
    def __repr__(self):
        text = 'Simplex: '
        for v in self.vertices:
            text += '\n{}'.format(v)
        # for e in self.edges:
        #     text += '\n{}'.format(e)
        return text

# 10 января 13:00 Стекловка

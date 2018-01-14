import pygame
from pygame import *
import sys
import math
from pyquaternion import Quaternion

import examples
from polytope import cross_product

class Cam:
    def __init__(self, pos=(0,0,0), rot=(0,0,0)):
        self.pos = list(pos)
        self.rot = list(rot)
        self.quat = Quaternion(axis=[1, 0, 0], degrees=0)

    def update(self, dt, key):
        s = dt / 200

        if key[pygame.K_q]: self.pos[2] -= s
        if key[pygame.K_e]: self.pos[2] += s

        x = s*math.sin(self.rot[1])
        y = s*math.cos(self.rot[1])
        s = 0
        x, y = s, s;

        if key[pygame.K_s]: self.pos[1] += x#; self.pos[1] += y
        if key[pygame.K_w]: self.pos[1] -= x#; self.pos[1] -= y
        if key[pygame.K_d]: self.pos[0] -= y#; self.pos[1] += x
        if key[pygame.K_a]: self.pos[0] += y#; self.pos[1] -= x

    def events(self, event):
        if event.type == pygame.MOUSEMOTION:
            x, y = event.rel
            x /= 1000
            y /= 1000
            #self.rot[0] += y #*math.cos(self.rot[0])-x*math.sin(self.rot[1])
            #self.rot[1] -= x 
            q1 = Quaternion(axis=[1, 0, 0], angle=y)
            q2 = Quaternion(axis=[0, 1, 0], angle=-x)
            self.quat = q2*q1*self.quat


class PolytopeView:
    polytope_list = [examples.right_120cell, examples.right_120cell2, examples.sliced_cube, examples.football]
    params = {examples.right_120cell2: -18/180*math.pi, examples.sliced_cube: 0.2}

    def __init__(self):
        self.alpha = 0
        self.polytope_num = -1
        self.next()

    def get_polytope(self):
        return self.polytope
        pol_func = self.polytope_list[self.polytope_num]
        if pol_func in self.params:
            return pol_func(self.alpha)
        return pol_func()

    def next(self):
        self.polytope_num = (self.polytope_num + 1) % len(self.polytope_list)
        pol_func = self.polytope_list[self.polytope_num]
        if pol_func in self.params:
            self.alpha = self.params[pol_func]
            self.polytope = pol_func(self.alpha)
        else:
            self.polytope = pol_func()
            #self.alpha = self.params[next_pol]

    def change_parameter(self, alpha):
        self.alpha = alpha

        if self.polytope_list[self.polytope_num] in self.params:
            self.polytope = self.polytope_list[self.polytope_num](alpha)



WIN_WIDTH = 1200 
WIN_HEIGHT = 800
cx = WIN_WIDTH//2
cy = WIN_HEIGHT//2   

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#FFFFFF"

clock = pygame.time.Clock()
cam = Cam((0, 0, -25))
pol = PolytopeView()


def rotate2d(pos, rad):
    x, y = pos
    s, c = math.sin(rad), math.cos(rad)
    return x*c-y*s, y*c+x*s

def point_to_screen(point):
    if point.dim != 3:
        return None

    x, y, z = cam.quat.rotate(point.coords)

    x -= cam.pos[0]
    y -= cam.pos[1]
    z -= cam.pos[2]

    z += 5
    f = 200*cam.pos[2]/z
    x, y = x*f, y*f

    return (cx + int(x), cy + int(y))

def main():
    pygame.init() 
    screen = pygame.display.set_mode(DISPLAY) 
    pygame.display.set_caption("polytope_list") 
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) 

    pygame.event.get()
    pygame.mouse.get_rel()
    pygame.mouse.set_visible(0)
    pygame.event.set_grab(1)

    while True: 
        dt = clock.tick()
        for e in pygame.event.get(): 
            if e.type == QUIT or \
               (e.type == KEYDOWN and e.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            cam.events(e)

        simp = pol.get_polytope() #examples.football(alpha=alpha)#right_120cell(alpha)

        screen.fill(Color(BACKGROUND_COLOR))

        '''
        front_vert = []
        l = len(simp.vertices)
        for i in range(l):
            for j in range(i+1, l):
                for k in range(j+1, l):
                    p = cross_product(simp.vertices[i] - simp.vertices[k], 
                                      simp.vertices[j] - simp.vertices[k])
                    d = -1*p*simp.vertices[k]
                    if d > 0:
                    #    print('HGRJDFSJDFJSJ')
                        p = -1*p
                        d *= -1

                    is_front = True
                    for vert in simp.vertices:
                        print('{} {} {}'.format(i, j, k))
                        if p*vert + d < -0.0001:
                    #        print('{}'.format(p*vert+d))
                            is_front = False
                            break

                    if is_front:
                        print('{} {} {}', i, j, k)
                        front_vert.append(simp.vertices[i])
                        front_vert.append(simp.vertices[j])
                        front_vert.append(simp.vertices[k])
        '''
        for vert in simp.vertices:
            coords = point_to_screen(vert)

            pygame.draw.circle(screen, (0, 0, 0), coords, 6)

        for edge in simp.edges:
            v1_coords = point_to_screen(edge.v1)
            v2_coords = point_to_screen(edge.v2)
            pygame.draw.line(screen, (0, 0, 0), v1_coords, v2_coords, 1)
        
        pygame.display.flip()

        key = pygame.key.get_pressed()
        if key[pygame.K_k]:
            pol.change_parameter(pol.alpha + dt/2000)
            print(pol.alpha*180/math.pi+90)
        if key[pygame.K_j]:
            pol.change_parameter(pol.alpha - dt/2000)
            print(pol.alpha*180/math.pi+90)
        if key[pygame.K_RETURN]:
            pol.next()
        cam.update(dt, key)
        

if __name__ == "__main__":
    examples.right_120cell().matrix('examples/120cell_1_inner_cell.txt')
    examples.right_120cell2().matrix('examples/120cell_2_inner_cells.txt')
    examples.football().matrix('examples/sliced_icosahedron.txt')
    examples.sliced_cube().matrix('examples/sliced_cube.txt')
    main()

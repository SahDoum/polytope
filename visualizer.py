import pygame
from pygame import *
import sys
import math
import examples

class Cam:
    def __init__(self, pos=(0,0,0), rot=(0,0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

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
            self.rot[0] += y
            self.rot[1] -= x 


class PolytopeView:
    polytopes = [examples.right_120cell, examples.football, examples.sliced_cube]
    params = {examples.right_120cell: -2.513}

    def __init__(self):
        self.alpha = -2.513
        self.polytope_num = 0

    def get_polytope(self):
        pol_func = self.polytopes[self.polytope_num]
        if pol_func in self.params:
            return pol_func(self.alpha)
        return pol_func()

    def next(self):
        self.polytope_num = (self.polytope_num + 1) % len(self.polytopes)
        next_pol = self.polytopes[self.polytope_num]
        if next_pol in self.params:
            self.alpha = self.params[next_pol]



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

    x, y, z = point.coords

    x, z = rotate2d((x, z), cam.rot[1])
    y, z = rotate2d((y, z), cam.rot[0])

    x -= cam.pos[0]
    y -= cam.pos[1]
    z -= cam.pos[2]

    # z += 5
    f = 100*cam.pos[2]/z
    x, y = x*f, y*f

    return (cx + int(x), cy + int(y))

def main():
    pygame.init() 
    screen = pygame.display.set_mode(DISPLAY) 
    pygame.display.set_caption("Polytopes") 
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
            pol.alpha += dt/1000
            print(pol.alpha*180/6.24318)
        if key[pygame.K_j]:
            pol.alpha -= dt/1000
            print(pol.alpha*180/6.24318)
        if key[pygame.K_RETURN]:
            pol.next()
        cam.update(dt, key)
        

if __name__ == "__main__":
    examples.right_120cell().matrix('examples/120cell.txt')
    examples.football().matrix('examples/football.txt')
    examples.sliced_cube().matrix('examples/sliced_cube.txt')
    main()

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import argparse
import sys
import math

class Quaternion:
    def __init__(self, r, i, j, k):
        self.r = r
        self.i = i
        self.j = j
        self.k = k

    def mag(self):
        return math.sqrt(self.r * self.r + self.i * self.i + self.j * self.j + self.k * self.k)

    def inverse(self):
        mag = self.mag()
        return Quaternion(self.r/mag, -self.i/mag, -self.j/mag, -self.k/mag)

    def unit(self):
        mag = self.mag()
        return Quaternion(self.r/mag, self.i/mag, self.j/mag, self.k/mag)

    def mul(self, q):
        r = self.r * q.r - self.i * q.i - self.j * q.j - self.k * q.k
        i = self.r * q.i + self.i * q.r + self.j * q.k - self.k * q.j
        j = self.r * q.j - self.i * q.k + self.j * q.r + self.k * q.i
        k = self.r * q.k + self.i * q.j - self.j * q.i + self.k * q.r
        return Quaternion(r, i, j, k)

    def show(self):
        return (self.r, self.i, self.j, self.k)


global greencolor
global redcolor
global bluecolor
global blackcolor
global yellowcolor
global q
global ptsRect
global ptsDisk
global ptsLine
global xOrigin
global yOrigin
global xDelta
global yDelta
global diskSize
global diskRadius
global vectorDisk


def init(shape):
    global greencolor 
    global redcolor
    global bluecolor
    global blackcolor
    global yellowcolor
    global ptsRect
    global ptsLine
    global ptsDisk
    global q
    global xDelta
    global yDelta
    global xOrigin
    global yOrigin
    global vectorDisk
    global diskSize
    global diskRadius

    greencolor = (0.0, 1.0, 0.0)
    redcolor = (1.0, 0.0, 0.0)
    bluecolor = (0.0, 0.0, 1.0)
    blackcolor = (0.0, 0.0, 0.0)
    yellowcolor = (1.0, 1.0, 0.0)
    ptsLine = [ (0.0, 0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0, 0.5) ]
    diskSize = 50
    diskRadius = 0.5
    ptsRect = []
    ptsDisk = []
    if shape == "square":
        ptsRect = [(0.0, -0.5, -0.5, 0.0),
                 (0.0, 0.5, -0.5, 0.0), 
                 (0.0, 0.5, 0.5, 0.0),
                 (0.0, -0.5, 0.5, 0.0)]
    elif shape == "rectangle":
        ptsRect = [(0.0, -0.6, -0.4, 0.0),
                 (0.0, 0.6, -0.4, 0.0), 
                 (0.0, 0.6, 0.4, 0.0),
                 (0.0, -0.6, 0.4, 0.0)]
    elif shape == "disk":
        for i in range(diskSize):
            alpha = 2 * math.pi * i / diskSize
            ptsDisk.append((0.0, diskRadius * math.cos(alpha), diskRadius * math.sin(alpha), 0.0))    

        vectorDisk = Quaternion(0.0, 0.0, 0.0, 1.0)
    else:
        raise Exception("wrong argument")
    q = Quaternion(0.0, 1.0, 0.0, 0.0)
    xDelta = 0
    yDelta = 0
    xOrigin = 0
    yOrigin = 0

    glClearColor(0.5, 0.5, 0.5, 1.0)
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0) 
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (1.0, 1.0, 1.0, 1))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (2.0, 2.0, 2.0))


def setQ():
    global xDelta
    global yDelta

    eps = 1
    dist = math.sqrt(xDelta * xDelta + yDelta * yDelta + eps)
    magic = 8e1 
    phi = math.pi / magic
    i = yDelta / dist
    j = xDelta / dist 
    k = 0.0
    cosphi = math.cos(phi / 2.0)
    sinphi = math.sin(phi / 2.0)
    return Quaternion(cosphi, i*sinphi, j*sinphi, k*sinphi).unit()

def drawRectangle():
    global greencolor
    global redcolor
    global bluecolor
    global blackcolor
    global yellowcolor
    global ptsLine
    global ptsRect
    
    q = setQ()
    glClear(GL_COLOR_BUFFER_BIT) 
    glPushMatrix()

    glBegin(GL_QUADS)  # drawing square
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, greencolor)
    p = Quaternion(*ptsRect[0])
    p = q.mul(p.mul(q.inverse()))
    ptsRect[0] = p.show()
    glVertex3f(p.i, p.j, p.k)

    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, redcolor)
    p = Quaternion(*ptsRect[1])
    p = q.mul(p.mul(q.inverse()))
    ptsRect[1] = p.show()
    glVertex3f(p.i, p.j, p.k)

    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, bluecolor)
    p = Quaternion(*ptsRect[2])
    p = q.mul(p.mul(q.inverse()))
    ptsRect[2] = p.show()
    glVertex3f(p.i, p.j, p.k)
    
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, yellowcolor)
    p = Quaternion(*ptsRect[3])
    p = q.mul(p.mul(q.inverse()))
    ptsRect[3] = p.show()
    glVertex3f(p.i, p.j, p.k)
    glEnd()
    
    glLineWidth(3); 
    glBegin(GL_LINES)  # drawing line
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, blackcolor)

    p = Quaternion(*ptsLine[0])
    p = q.mul(p.mul(q.inverse()))
    ptsLine[0] = p.show()
    glVertex3f(p.i, p.j, p.k)
    
    p = Quaternion(*ptsLine[1])
    p = q.mul(p.mul(q.inverse()))
    ptsLine[1] = p.show()
    glVertex3f(p.i, p.j, p.k)
    glEnd()

    glPopMatrix()
    glutSwapBuffers()


def drawDisk():
    global greencolor
    global redcolor
    global bluecolor
    global blackcolor
    global yellowcolor
    global ptsLine
    global ptsDisk
    global diskSize

    q = setQ()
    glClear(GL_COLOR_BUFFER_BIT) 
    glBegin(GL_POLYGON)
    for i in range(diskSize):
        alpha = 2 * math.pi * i / diskSize
        color = (math.cos(alpha), math.sin(alpha), 1.0)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, color)
        p = Quaternion(*ptsDisk[i])
        p = q.mul(p.mul(q.inverse()))
        ptsDisk[i] = p.show()
        glVertex3f(p.i, p.j, p.k)
    glEnd()

    glLineWidth(3); 
    glBegin(GL_LINES)  # drawing line
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, blackcolor)

    p = Quaternion(*ptsLine[0])
    p = q.mul(p.mul(q.inverse()))
    ptsLine[0] = p.show()
    glVertex3f(p.i, p.j, p.k)
    
    p = Quaternion(*ptsLine[1])
    p = q.mul(p.mul(q.inverse()))
    ptsLine[1] = p.show()
    glVertex3f(p.i, p.j, p.k)
    glEnd()

    glutSwapBuffers()


def mouseButton(btn, state, x, y):
    global xOrigin
    global yOrigin
    
    if btn == GLUT_LEFT_BUTTON:
        if state == GLUT_UP:
            xOrigin = -1
            yOrigin = -1
        else:  # state == GLUT_DOWN
            xOrigin = x
            yOrigin = y


def mouseMove(x, y):
    global xOrigin
    global yOrigin
    global xDelta
    global yDelta
    
    if xOrigin >= 0:
        xDelta = x - xOrigin
        yDelta = y - yOrigin
        
        glutPostRedisplay()


parser = argparse.ArgumentParser()
parser.add_argument("shape", type=str, help="shape type")
args = parser.parse_args()

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(900, 900)
glutInitWindowPosition(50, 50)
glutInit(sys.argv)
glutCreateWindow(b"Quaternions Everywhere!")
if args.shape == "disk":
    glutDisplayFunc(drawDisk)
else:
    glutDisplayFunc(drawRectangle)
glutMouseFunc(mouseButton)
glutMotionFunc(mouseMove) 
init(args.shape)
glutMainLoop()


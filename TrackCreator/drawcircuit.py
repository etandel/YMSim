import math

from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtGui
from PyQt4.QtOpenGL import *

class CircuitWidget(QGLWidget):
     '''
     Widget for drawing the circuit.
     '''
    
     def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.max_index = 99

     def paintGL(self):
        '''
        Drawing routine
        '''
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glEnableClientState(GL_VERTEX_ARRAY)
    
        lines = [
            #center strip
            (
                ((p.position.X, p.position.Y) for p in self.window().circuit),
                (0.75, 0.75, 0.75)
            ),

            #left margin
            (
                ((p.X, p.Y) for p in self.window().circuit.left),
                (1.0, 0.0, 0.0),
            ),
            
            #right margin
            (
                ((p.X, p.Y) for p in self.window().circuit.right),
                (1.0, 0.0, 0.0),
            ),
        ]
        for points_g, color in lines:
            points_l = list(points_g)
            glColor(*color)
            glVertexPointerf(list(points_l))
            glDrawArrays(GL_LINE_STRIP, 0, len(points_l))

        glFlush()

     def resizeGL(self, w, h):
         '''
         Resize the GL window 
         '''
         h = h if h != 0 else 1
         
         glViewport(0, 0, w, h)
         glMatrixMode(GL_PROJECTION)
         glLoadIdentity()
         gluPerspective(45.0, w/h, 0.1, 100.0)
     
     def initializeGL(self):
         '''
         Initialize GL
         '''
         # set viewing projection
         glClearColor(0.0, 0.0, 0.0, 1.0)
         glClearDepth(1.0)

         glMatrixMode(GL_PROJECTION)
         glLoadIdentity()
         gluPerspective(45.0, 1.0, 0.1, 100.0)


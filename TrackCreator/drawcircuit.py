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

     def paintGL(self):
        '''
        Drawing routine
        '''
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Draw the circuit as a line in 'immediate mode'
        glBegin(GL_LINE_STRIP)
        glColor(0.75, 0.75, 0.75)
        for point in self.window().circuit:
            glVertex(point.position.X, point.position.Y, 0.0)
        glEnd()
        
        glBegin(GL_LINE_STRIP)
        glColor(1.0, 0.0, 0.0)
        for point in self.window().circuit.left:
            glVertex(point.X, point.Y, 0.0)
        glEnd()

        glBegin(GL_LINE_STRIP)
        glColor(1.0, 0.0, 0.0)
        for point in self.window().circuit.right:
            glVertex(point.X, point.Y, 0.0)
        glEnd()

        ##########****#############

#        glEnableClientState(GL_VERTEX_ARRAY)
#        
#        spiral_array = []
#        
#        # Second Spiral using "array immediate mode" (i.e. Vertex Arrays)
#        radius = 0.8
#        x = radius*math.sin(0)
#        y = radius*math.cos(0)
#        glColor(1.0, 0.0, 0.0)
#        for deg in xrange(820):
#            spiral_array.append([x, y])
#            rad = math.radians(deg)
#            radius -= 0.001
#            x = radius*math.sin(rad)
#            y = radius*math.cos(rad)
#
#        glVertexPointerf(spiral_array)
#        glDrawArrays(GL_LINE_STRIP, 0, len(spiral_array))
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


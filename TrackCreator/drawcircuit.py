import math

from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtGui
from PyQt4.QtOpenGL import *

class CircuitWidget(QGLWidget):
     '''
     Widget for drawing the circuit.
     '''
    
     def __init__(self, circuit, parent):
        QGLWidget.__init__(self, parent)
        self.circuit = circuit

     def paintGL(self):
        '''
        Drawing routine
        '''
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Draw the circuit in 'immediate mode'
        # WARNING: You should not be doing the spiral calculation inside the loop
        # even if you are using glBegin/glEnd, sin/cos are fairly expensive functions
        # I've left it here as is to make the code simpler.
        glColor(0.0, 1.0, 0.0)
        glBegin(GL_LINE_STRIP)
        for point in self.circuit:
            glVertex(point.position.X, point.position.Y, 0.0)
        glEnd()
        
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
         
         glViewport(0, 0, w, h)
         glMatrixMode(GL_PROJECTION)
         glLoadIdentity()
         gluPerspective(40.0, 1.0, 1.0, 30.0)
     
     def initializeGL(self):
         '''
         Initialize GL
         '''
         # set viewing projection
         glClearColor(0.0, 0.0, 0.0, 1.0)
         glClearDepth(1.0)

         glMatrixMode(GL_PROJECTION)
         glLoadIdentity()
         gluPerspective(40.0, 1.0, 1.0, 30.0)


#! /usr/bin/python

from fpdf import FPDF
import sys
import configparser
import io
import math

class Below():
     def __init__(self, width1, width2, folds, foldh_in, foldh_out, material):
          self.d = material*2
          self.bottom = width1 + self.d
          self.up = width2 + self.d
          self.h = folds*(foldh_in + foldh_out + 2*self.d)
          self.fin = foldh_in
          self.fout = foldh_out
          print(self.h)

     def get_edges_coodinates(self):
          left_bottom = (0,self.h)
          right_bottom = (self.bottom, self.h)
          left_up = ((self.bottom-self.up)/2, 0)
          right_up = (self.bottom - (self.bottom-self.up)/2, 0)
          return [left_bottom, right_bottom, right_up, left_up]

     def get_bottom_anges(self):
          return math.atan((self.bottom-self.up)/(2*self.h))

class ImageTransformer():
     def rotate(coordinates, psi, center):
          result=[]
          for i in coordinates:
               x = math.cos(psi)*(i[0] - center[0]) - math.sin(psi)*(i[1] - center[1]) + center[0]
               y = math.sin(psi)*(i[0] - center[0]) + math.cos(psi)*(i[1] - center[1]) + center[1]
               result.append((x,y))
          return result

     def move(coordinates, movex, movey):
          result=[]
          for i in coordinates:
               x = i[0] + movex
               y = i[1] + movey
               result.append((x,y))
          return result

class PDF(FPDF):
     page_w=210
     page_h=297

     def _draw_rect (self, edges):
          self.line(edges[0][0], edges[0][1], edges[1][0], edges[1][1])
          self.line(edges[1][0], edges[1][1], edges[2][0], edges[2][1])
          self.line(edges[2][0], edges[2][1], edges[3][0], edges[3][1])
          self.line(edges[3][0], edges[3][1], edges[0][0], edges[0][1])


     def below(self, bellow1, bellow2):
          offsety = -8
          offsetx = 10
          self.set_line_width(1.0)

          edges = bellow1.get_edges_coodinates()
          edges = ImageTransformer.move(ImageTransformer.rotate(edges, math.pi/2, edges[0]), offsetx, offsety)
          self._draw_rect(edges)
          edges = bellow2.get_edges_coodinates()

          edges = ImageTransformer.move(ImageTransformer.rotate(edges,
                                                                math.pi/2 - bellow1.get_bottom_anges() - bellow2.get_bottom_anges(),
                                                                edges[0]),
                                        offsetx, bellow1.bottom+offsety)
          self._draw_rect(edges)

          edges = bellow2.get_edges_coodinates()
          edges = ImageTransformer.move(ImageTransformer.rotate(edges, math.pi/2, edges[0]), offsetx, -bellow2.bottom+offsety)
          edges = ImageTransformer.rotate(edges, bellow1.get_bottom_anges() + bellow2.get_bottom_anges(), edges[1])
          self._draw_rect(edges)

          base_point = edges[0]
          edges = bellow1.get_edges_coodinates()
          edges = ImageTransformer.move(ImageTransformer.rotate(edges,
                                                                math.pi/2,
                                                                edges[0]),
                                        (base_point[0]-edges[0][0]),
                                        (base_point[1]-edges[0][1])-bellow1.bottom)
          edges = ImageTransformer.rotate(edges,
                                          2*bellow1.get_bottom_anges() + 2*bellow2.get_bottom_anges(),
                                          edges[1])

          self._draw_rect(edges)



def prepare_pdf(below1, below2) :
     pdf = PDF(unit='mm', format='A4')
     pdf.add_page()
     pdf.below(below1, below2)
     pdf.output('test.pdf','F')

def read_config(filename):
     config = configparser.ConfigParser()
     config.read(filename)
     print(config.sections())

def main():
     if len(sys.argv) != 2:
          print("Need configuration file parameter")
          exit(1)

     print(sys.argv[1])
     read_config(sys.argv[1])
     below1 = Below(87, 57, 7, 10, 10, 0.5)
     below2 = Below(57, 57, 7, 10, 10.1, 0.5)
     prepare_pdf(below2, below1)


main()

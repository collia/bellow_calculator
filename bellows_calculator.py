#! /usr/bin/python

from fpdf import FPDF
import sys
import configparser
import io

class PDF(FPDF):
     page_w=210
     page_h=297

     def lines(self):
        self.set_line_width(1.0)
        self.line(0, 0, self.page_h, self.page_w)

def prepare_pdf() :
     pdf = PDF(unit='mm', format='A4')
     pdf.add_page()
     pdf.lines()
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
     prepare_pdf()


main()

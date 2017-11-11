import threading
import subprocess
import sys, os
from machine_learning.attribute_algorithm_main import AttributeAlgorithmMain
from machine_learning.ml_main import MlMain
class Main(object):

      def attr_algorithm_main(self):
               self.obj1 = AttributeAlgorithmMain()
               subprocess.check_call(self.obj1,shell=True)

      def ml_main(self):
              self.obj2 = MlMain()
              subprocess.check_call(self.obj2, shell=True)


      def main(self):
        self.attr_algorithm_main()
        self.ml_main()
        funcs = [self.attr_algorithm_main,self.ml_main]
        for func in funcs:
                func()


obj=Main().main()
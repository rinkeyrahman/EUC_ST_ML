from __future__ import print_function
import sys
import os
import time
import attribute as attr
import algorithm as alg

class AttributeAlgorithmMain:
  """
    This class maintains total procedure of collecting user intention,
    dataset and algorithm selection.

    Parameters
    ----------

    dataset : list
               file to be read.
    learning problem : bool
                       True(if learning problem is supervised)
                       false(if learning problem is unsupervised)

  """

  def __init__(self):
    self.filename=str
    self.learning_problem=bool

  def main(self):
    """
        Call functions for selecting dataset and algorithm.
        :return:
    """
    cached_stamp = 0
    self.filename = 'watch/user_intention.json'
    stamp = os.stat(self.filename).st_mtime
    if stamp != cached_stamp:
      cached_stamp = stamp
      print("user intention file updated",file=sys.stderr)
      obj1=attr.Attribute()
      self.learning_problem=obj1.determine_learning_problem()
      if self.learning_problem is 1:
        obj1.supervised_attribute_set()
      else:
        obj1.unsupervised_attribute_set()
      obj1.generate_attribute_set()
      obj2=alg.Algorithm()
      obj2.generate_algorithm_info(output=self.learning_problem)



obj=AttributeAlgorithmMain().main()
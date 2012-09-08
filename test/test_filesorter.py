import unittest
from random import shuffle
from utilities.filesorter import *


class FileSortingTestCase(unittest.TestCase):

    def test_standardlist(self):
        self.runGeneric([
                "Cblockareabsection1tb291.jpg",
                "Cblockareabsection2tb291.jpg",
                "Cblockareabsection3tb291.jpg",
                "Cblockareabsection4tb291.jpg",
                "Cblockareabsection5tb291.jpg",
                "Cblockareabsection6tb291.jpg",
                "Cblockareabsection7tb291.jpg",
                "Cblockareabsection8tb291.jpg",
                "Cblockareabsection9tb291.jpg",
                "Cblockareabsection10tb291.jpg",
                "Cblockareabsection11tb291.jpg",
                "Cblockareabsection12tb291.jpg"])

    def test_fullnumbering(self):
        self.runGeneric([
                "Cblockareabsection01tb291.jpg",
                "Cblockareabsection02tb291.jpg",
                "Cblockareabsection03tb291.jpg",
                "Cblockareabsection04tb291.jpg",
                "Cblockareabsection05tb291.jpg",
                "Cblockareabsection06tb291.jpg",
                "Cblockareabsection07tb291.jpg",
                "Cblockareabsection08tb291.jpg",
                "Cblockareabsection09tb291.jpg",
                "Cblockareabsection10tb291.jpg",
                "Cblockareabsection11tb291.jpg",
                "Cblockareabsection12tb291.jpg"])

    def runGeneric(self, sortedFileList):
        shuffled = sortedFileList[:]
        shuffle(shuffled)
        for i in range(1000):
            self.assertEqual(sortedFileList,
                             sortByFirstNumber(shuffled))

from __future__ import division, absolute_import, print_function
import unittest
from svgpathtools import *
from io import StringIO
from os.path import join, dirname

from svgpathtools.svg_to_paths import rect2pathd

class TestSVG2Paths(unittest.TestCase):
    def test_svg2paths_polygons(self):

        paths, _ = svg2paths(join(dirname(__file__), 'polygons.svg'))

        # triangular polygon test
        path = paths[0]
        path_correct = Path(Line(55.5+0j, 55.5+50j), 
                            Line(55.5+50j, 105.5+50j), 
                            Line(105.5+50j, 55.5+0j)
                            )
        self.assertTrue(path.isclosed())
        self.assertTrue(len(path)==3)
        self.assertTrue(path==path_correct)

        # triangular quadrilateral (with a redundant 4th "closure" point)
        path = paths[1]
        path_correct = Path(Line(0+0j, 0-100j),
                            Line(0-100j, 0.1-100j),
                            Line(0.1-100j, 0+0j),
                            Line(0+0j, 0+0j)  # result of redundant point
                            )
        self.assertTrue(path.isclosed())
        self.assertTrue(len(path)==4)
        self.assertTrue(path==path_correct)

    def test_svg2paths_ellipses(self):

        paths, _ = svg2paths(join(dirname(__file__), 'ellipse.svg'))

        # ellipse tests
        path_ellipse = paths[0]
        path_ellipse_correct = Path(Arc(50+100j, 50+50j, 0.0, True, False, 150+100j),
                                    Arc(150+100j, 50+50j, 0.0, True, False, 50+100j))
        self.assertTrue(len(path_ellipse)==2)
        self.assertTrue(path_ellipse==path_ellipse_correct)
        self.assertTrue(path_ellipse.isclosed())

        # circle tests
        paths, _ = svg2paths(join(dirname(__file__), 'circle.svg'))

        path_circle = paths[0]
        path_circle_correct = Path(Arc(50+100j, 50+50j, 0.0, True, False, 150+100j),
                                    Arc(150+100j, 50+50j, 0.0, True, False, 50+100j))
        self.assertTrue(len(path_circle)==2)
        self.assertTrue(path_circle==path_circle_correct)
        self.assertTrue(path_circle.isclosed())

    def test_rect2pathd(self):
        non_rounded = {"x":"10", "y":"10", "width":"100","height":"100"}
        self.assertEqual(rect2pathd(non_rounded), 'M10.0 10.0 L 110.0 10.0 L 110.0 110.0 L 10.0 110.0 z')
        rounded = {"x":"10", "y":"10", "width":"100","height":"100", "rx":"15", "ry": "12"}
        self.assertEqual(rect2pathd(rounded), "M 25.0 10.0 L 95.0 10.0 A 15.0 12.0 0 0 1 110.0 22.0 L 110.0 98.0 A 15.0 12.0 0 0 1 95.0 110.0 L 25.0 110.0 A 15.0 12.0 0 0 1 10.0 98.0 L 10.0 22.0 A 15.0 12.0 0 0 1 25.0 10.0 z")

    def test_from_file_path(self):
        """ Test reading svg from file provided as path """
        paths, _ = svg2paths(join(dirname(__file__), 'polygons.svg'))

        self.assertEqual(len(paths), 2)

    def test_from_file_object(self):
        """ Test reading svg from file object that has already been opened """
        with open(join(dirname(__file__), 'polygons.svg'), 'r') as file:
            paths, _ = svg2paths(file)

            self.assertEqual(len(paths), 2)

    def test_from_stringio(self):
        """ Test reading svg object contained in a StringIO object """
        with open(join(dirname(__file__), 'polygons.svg'), 'r') as file:
            # read entire file into string
            file_content: str = file.read()
            # prepare stringio object
            file_as_stringio = StringIO()
            # paste file content into it
            file_as_stringio.write(file_content)
            # reset curser to its beginning
            file_as_stringio.seek(0)

            paths, _ = svg2paths(file_as_stringio)

            self.assertEqual(len(paths), 2)

    def test_from_string_without_svg_attrs(self):
        """ Test reading svg object contained in a string without svg attributes"""
        with open(join(dirname(__file__), 'polygons.svg'), 'r') as file:
            # read entire file into string
            file_content: str = file.read()

            paths, _ = svg_string2paths(file_content)

            self.assertEqual(len(paths), 2)

    def test_from_string_with_svg_attrs(self):
        """ Test reading svg object contained in a string with svg attributes"""
        with open(join(dirname(__file__), 'polygons.svg'), 'r') as file:
            # read entire file into string
            file_content: str = file.read()

            paths, _, _ = svg_string2paths2(file_content)

            self.assertEqual(len(paths), 2)

import unittest
import imageprovider


class SimpleTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_strings_a(self):
        self.assertEqual('a' * 4, 'aaaa')

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_strip(self):
        s = 'geeksforgeeks'
        self.assertEqual(s.strip('geek'), 'sforgeeks')

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        with self.assertRaises(TypeError):
            s.split(2)


class CoordinatesCalculatorTest(unittest.TestCase):
    screen_resolution = 2000, 1000
    window_resolution = 500, 250

    def test_window_coordinates(self):
        calculator = imageprovider.CoordinatesCalculator(self.screen_resolution, self.window_resolution, 1, 10)
        coordinates = calculator.get_window_coordinates()
        self.assertEqual(0, coordinates[0])
        self.assertEqual(10, coordinates[1])
        self.assertEqual(500, coordinates[2])
        self.assertEqual(260, coordinates[3])

    def test_section_coordinates(self):
        calculator = imageprovider.CoordinatesCalculator(self.screen_resolution, self.window_resolution, 1, 10)
        coordinates = calculator.get_region_in_window_coordinates(20, 20, 40, 40)
        self.assertEqual(20, coordinates[0])
        self.assertEqual(30, coordinates[1])
        self.assertEqual(40, coordinates[2])
        self.assertEqual(50, coordinates[3])


if __name__ == '__main__':
    unittest.main()

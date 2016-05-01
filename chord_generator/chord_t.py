import unittest

import chord


class ChordTests(unittest.TestCase):

	def test_getFrequency(self):
	    self.assertEqual('%.3f' % chord.getFrequency('A4'), '440.000')
	    self.assertEqual('%.3f' % chord.getFrequency('A5'), '880.000')
	    self.assertEqual('%.3f' % chord.getFrequency('E4'), '329.628')
	    self.assertEqual('%.3f' % chord.getFrequency('F#3'), '184.997')



unittest.main()
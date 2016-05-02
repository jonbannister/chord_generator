import unittest

import chord


class ChordTests(unittest.TestCase):

	def test_getFrequency(self):
	    self.assertEqual('%.3f' % chord.getFrequency('A4'), '440.000')
	    self.assertEqual('%.3f' % chord.getFrequency('A5'), '880.000')
	    self.assertEqual('%.3f' % chord.getFrequency('E4'), '329.628')
	    self.assertEqual('%.3f' % chord.getFrequency('F#3'), '184.997')
	    self.assertEqual('%.3f' % chord.getFrequency('Gb3'), '184.997')

	def test_getFrequencyErrors(self):
		with self.assertRaises(ValueError):
			chord.getFrequency('Afive')

		with self.assertRaises(ValueError):
			chord.getFrequency('H2')

		with self.assertRaises(ValueError):
			chord.getFrequency('A#b4')

		self.assertIsNone(chord.getFrequency(None))

	def test_getSemitoneShift(self):
		# Test that all notes can be sharpened, flattened, and natural (A#, Ab, A respectively)
		self.assertEqual(chord._getSemitoneShift('Ab'), 8.0)
		self.assertEqual(chord._getSemitoneShift('A'), 9.0)
		self.assertEqual(chord._getSemitoneShift('A#'), 10.0)

		# Test the cases where something went a bit wrong, but we allow it anyway
		self.assertEqual(chord._getSemitoneShift('A##'), 10.0)
		self.assertEqual(chord._getSemitoneShift('A#b'), 10.0)

		# B and Cb are equivalent notes.
		self.assertEqual(chord._getSemitoneShift('B'), 11.0)
		self.assertEqual(chord._getSemitoneShift('Cb'), 11.0)

		# E# and F are equivalent notes.
		self.assertEqual(chord._getSemitoneShift('E#'), 5.0)
		self.assertEqual(chord._getSemitoneShift('F'), 5.0)

		# B# should go from 11 -> 0 since we are base 12
		self.assertEqual(chord._getSemitoneShift('B#'), 0.0)


unittest.main()
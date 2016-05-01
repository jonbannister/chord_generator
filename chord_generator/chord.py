import logging
import math
import re
import struct
import wave

# Set up our logging
logger = logging.getLogger('chord_generator')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def getFrequency(noteName):
    '''
        Returns the frequency of the given note. 
        :param noteName: The note to be translated into a frequency.
                         Notation: Note name + octave e.g. 'A#5', 'Bb2', 'A0', 'G9'
        Reference: https://en.wikipedia.org/wiki/Piano_key_frequencies 
    '''
    
    # In order to get the pitch, we need to shift from C by x semitones
    semitone_shifts = {'A':9.0, 'A#':10.0, 'B':11.0, 'C':0.0, 'C#':1.0, 'D':2.0, 
                       'D#':3.0, 'E':4.0, 'F':5.0, 'F#':6.0, 'G':7.0, 'G#':8.0}

    # This regex splits out the note (e.g. A or D#) from the octave (e.g. 4)
    note, octave = re.match('([A-G](?:#|b)?)(\d+)', noteName).groups()

    try:
        octave = int(octave)
    except ValueError:
        logger.error('The given octave should be an integer (e.g. 2 or 6).')
        raise

    key_number = 4 + semitone_shifts[note] + ((octave-1) * 12.0)
    a_for_octave = math.pow(2, ((key_number-49)/12)) * 440.0
    return a_for_octave

def generateChordsFromFrequencies(chord_frequencies, durations=None, filename=None, weights=None):
    ''' 
        Generates a .wav file with the given frequencies and time.
        
        :param chord_frequencies (iter of iter of floats): 
                            An iterable of iterables with Hz frequencies (must be floats) for each chord in the sequence
                               e.g. C major 5's input could be [[880.0, 1100.0, 1320.0, 1760.0]]
        :param durations (iterable of floats): An array of durations (in seconds) in which the chords should appear
        :param filename (str): The name of the output file. Defaults to my_chord.wav
        :param weights: Allows you to specify how loud you want each note in each chord to sound.
                        Default is balanced (i.e. 1/n for n notes in the chord)
                            e.g. [None, None, [0.1, 0.1, 0.1, 0.4, 0.3], None]
    '''

    # Validate input
    if durations and len(durations) != len(chord_frequencies):
        raise ValueError('If durations are specified, they must be specified for each chord.')
    if weights and len(weights) != len(chord_frequencies):
        raise ValueError('If per-chord weightings are specified, they must be specified for each chord (but they can be None).')

    # After validation, perform some setup with inputs (TODO: maybe these could be arguments too)
    sec_durations = durations or [1.0]*len(chord_frequencies)
    sampleRate = 44100.0
    amplitude = 8000.0
    sample_durations = [int(sampleRate*duration) for duration in sec_durations]
    sine_wave = []
    chord_weights = []
    for (i,fs) in enumerate(chord_frequencies):
        chord_weights.append(weights[i] if (weights and weights[i]) else ([1.0/len(fs)] * len(fs)))

    # Calculate the actual sine wave that creates the chord
    for (freqs, sample_size, weighting) in zip(chord_frequencies, sample_durations, chord_weights):
        for x in range(sample_size):
            sample = 0
            for (freq, coefficient) in zip(freqs, weighting):
                sample += coefficient * math.sin(2*math.pi*freq*(x/sampleRate))
            sine_wave.append(sample)
    logger.debug('Sine wave has been computed, saving to file.')
            
    # Write our sine wave to the .wav file.
    f = wave.open(filename or 'my_chord.wav', 'w')
    channels = 1
    amp_width = 2
    f.setparams((channels, amp_width, sampleRate, sum(sample_durations), 'NONE', 'not compressed'))
    total = float(len(sine_wave))
    for i,frequency in enumerate(sine_wave):
        if i%(total/10.0) == 0:
            logger.debug('Progress: %.2f%% (%d/%d)' % ((i*100.0/total), i, total))
        f.writeframes(struct.pack('h', (frequency*amplitude/2)))
    f.close()
    logger.debug('Save to %s complete.' % filename)


def main():
    generateChordsFromFrequencies(
                    [[880.0, 1100.0, 1320.0, 1760.0], [880.0, 1100.0, 1320.0, 1479.98, 1760.0], [830.609, 987.767, 1320.0, 1661.22]], 
                    durations=[1, 1, 2], 
                    filename='C:/Temp/mychordprogression.wav', 
                    weights=[None, [0.1, 0.1, 0.1, 0.4, 0.3], None])

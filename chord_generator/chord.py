import logging
import math
import struct
import wave

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

    # Some validations
    if durations and len(durations) != len(chord_frequencies):
        raise ValueError('If durations are specified, they must be specified for each chord.')
    if weights and len(weights) != len(chord_frequencies):
        raise ValueError('If per-chord weightings are specified, they must be specified for each chord (but they can be None).')

    sec_durations = durations or [1.0]*len(chord_frequencies)
    sampleRate = 44100.0
    amplitude = 8000.0
    sample_durations = [int(sampleRate*duration) for duration in sec_durations]
    sine_wave = []

    chord_weights = []
    for (i,fs) in enumerate(chord_frequencies):
        chord_weights.append(weights[i] if (weights and weights[i]) else ([1.0/len(fs)] * len(fs)))

    for (freqs, sample_size, weighting) in zip(chord_frequencies, sample_durations, chord_weights):
        for x in range(sample_size):
            sample = 0
            for (freq, coefficient) in zip(freqs, weighting):
                sample += coefficient * math.sin(2*math.pi*freq*(x/sampleRate))
            sine_wave.append(sample)
    logging.debug('Sine wave has been computed, saving to file.')
            
    # Write our sine wave to the file.
    f = wave.open(filename or 'my_chord.wav', 'w')
    channels = 1
    amp_width = 2
    f.setparams((channels, amp_width, sampleRate, sum(sample_durations), 'NONE', 'not compressed'))
    total = float(len(sine_wave))
    for i,frequency in enumerate(sine_wave):
        if i%(total/10.0) == 0:
            logging.debug('Progress: %.2f%% (%d/%d)' % ((i*100.0/total), i, total))
        f.writeframes(struct.pack('h', (frequency*amplitude/2)))
    f.close()
    logging.debug('Save to %s complete.' % filename)
    
def main():
    generateChordsFromFrequencies(
                    [[880.0, 1100.0, 1320.0, 1760.0], [880.0, 1100.0, 1320.0, 1479.98, 1760.0], [830.609, 987.767, 1320.0, 1661.22]], 
                    durations=[1, 1, 2], 
                    filename='C:/Temp/helloworld3.wav', 
                    weights=[None, [0.1, 0.1, 0.1, 0.4, 0.3], None])

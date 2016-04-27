# chord_generator
A small python library to generate musical chords.


# Usage:
``` python
from chord_generator import chord
# A 1.5 second A major chord
chord.generateChordsFromFrequencies([[880.0, 1100.0, 1320.0, 1760.0]], durations=[1.5], filename='C:/Temp/mychord.wav')

# A 4 second 3-chord progression (AC#EA, AC#EF#A, G#BEG#) with a strong weight on the passing note.
chord.generateChordsFromFrequencies(
                    [[880.0, 1100.0, 1320.0, 1760.0], [880.0, 1100.0, 1320.0, 1479.98, 1760.0], [830.609, 987.767, 1320.0, 1661.22]], 
                    durations=[1, 1, 2], 
                    filename='C:/Temp/mychordprogression.wav', 
                    weights=[None, [0.1, 0.1, 0.1, 0.4, 0.3], None])
```

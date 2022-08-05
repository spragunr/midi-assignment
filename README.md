% MIDI

## Python Learning Objectives

* Writing and calling functions with return values
* Using for loops
* Accessing tuples using bracket notation
* Manipulating lists

## Dependencies

*   This activity depends on two Python libraries that will need to be
    installed through the Thonny package manager (or pip, if you you
    aren't using Thonny):
    * pygame
	* mimo
*   Actually playing the MIDI files we will be creating below also
    requires that [FuidSynth](https://www.fluidsynth.org/) and
    possibly [TiMidity++](https://wiki.archlinux.org/title/Timidity++)
    be installed on your computer.

## Files

Download the following Python files and store them in the same folder:

* [synth.py](code/synth.py) FINISHED
* [play_midi.py](code/play_midi.py) FINISHED
* [midi_notes.py](code/midi_notes.py) UNFINISHED


## Introduction: Musical Notation

You may have some experience with standard musical notation like the
following:

<img style="display:block; margin-left:auto; margin-right:auto; width:20em;" src="mary_cropped.svg" alt="mary has a little lamb" >

The vertical position of individual notes corresponds to the pitch,
and different symbols are used to represent the length of the
note. In the example above, the filled notes are quarter notes and the
open note at the end is a half note.

The goal of today's activity is to think about different ways of
representing and manipulating musical information in Python. In
particular, we will be learning a little bit about
[MIDI](https://en.wikipedia.org/wiki/MIDI), the Musical Instrument
Digital Interface.  MIDI is a widely-used standard for representing and
communicating musical information in digital form.

Let's consider some options for representing the musical notes above
using Python. One possibility is to represent the notes as a string
containing the sequence of note names:

```python
mary = "E D C D E E E"
```

This is OK, but it has some weaknesses.  It doesn't tell us anything
about the length of the individual notes, and working with it involves
awkward string manipulation.

As an alternative, let's use a list of tuples, where each tuple
represents a single note. For example, here are the notes above in the
proposed format:

```python
mary = [ (0, 100, 64), 
         (100, 200, 62), 
         (200, 300, 60), 
         (300, 400, 62), 
         (400, 500, 64),
         (500, 600, 64),
         (600, 800, 64)
	]
```

Each tuple contains three numbers: the first is the start time of the
note, the second is the end time of the note and the third is a number
corresponding the pitch of the note. A list of these notes will be
be ordered by the starting time of each note.

One advantage of this representation is that it allows us to represent
multiple notes played at the same time. For example, using standard
musical notation we might see something like this:

<img style="display:block; margin-left:auto; margin-right:auto; width:20em;" src="mary_chord_cropped.svg" alt="mary has a little lamb" >

In this case the two notes at the top are tied together with a line to
indicate that they should be played as one long note at the same time
as the other notes are being played. This overlapping note can be
added as follows:

```python
mary = [ (0, 100, 64), 
         (0, 800, 77),  # THE NEW NOTE!
         (100, 200, 62),
         (200, 300, 60),
         (300, 400, 62),
         (400, 500, 64),
         (500, 600, 64),
         (600, 800, 64)
        ]
```

## Exercise \#1 Validating a Note List

Complete the function named `valid_notes` in `notes.py` so that it
conforms to the provided docstring.  A list of notes is valid if and only if:
* All note values are in the range 0-127.
* All note start times are greater than zero.
* The ending time of every note is greater than or equal to the
  starting time of the note.
* The start time of every note is greater than or equal to the
  starting time of the preceding note.

Here are some sample calls:

```python
a = [ (0, 100, 64) ]
print(valid_notes(a)) # Should print True

b = [ (-1, 100, 64) ]
print(valid_notes(b)) # Should print False, negative start time

c = [ (100, 0, 64) ]
print(valid_notes(c)) # Should print False, end is before start

d = [ (0, 100, 200) ]
print(valid_notes(d)) # Should print False, invalid note number

e = [ (0, 100, 64), (100, 200, 62) ]
print(valid_notes(e)) # Should print True

f = [ (50, 100, 64), (40, 200, 62) ]
print(valid_notes(f)) # Should print False, second start starts before first
```

Think before you code: what style of for loops should you use here?
Should you use a standard for loop, or an indexed for loop using the
`range` function?  Should you use both? Make sure to consider this for
each of the following exercises.

## MIDI

The MIDI protocol takes a different approach from the format described
above.  Rather than representing music as a sequence of *notes*, it
represents music as a sequence of *events*, where the start of a note
is one event and the end of a note is another. This approach makes
sense because MIDI wasn't originally designed to represent musical
scores.  It was designed to connect electronic instruments and other
devices. When a player presses a key on an electric keyboard, we want
to communicate the starting event immediately. There is no way to know
how long the note will be until the finger is lifted.

## Exercise \#2 Converting to Events

Complete the `notes_to_events` function so that it conforms to the
provided docstring. Each event should be represented as a tuple with
three fields: The time of the event, the note number, and the type of
event.  Event types are either `'note_on'` or `'note_off'`.  Each note
should result in exactly two events and the list of events must be
sorted by time. The easiest way to manage this is to create the full
list of events, then sort it by the starting times when the list is
complete.

This can be accomplished by using the `sort` method for Python
lists. For example:

```python
a = [3, 2, 1]
a.sort() # the list now contains [1, 2, 3]
```

When the `sort` method is called on a list of tuples, the list will be
sorted according to the first element in each tuple, which in our case
will be the event times.

Here are some sample calls to `notes_to_events` illustrating the
expected behavior:

```python
a = [ (0, 100, 64) ]
print(notes_to_events(a)) # prints [(0, 64, 'note_on'), (100, 64, 'note_off')]

b = [ (0, 200, 64), (50, 75, 65)]
print(notes_to_events(b)) # prints [(0, 64, 'note_on'), 
                          #         (50, 65, 'note_on'),
                          #         (75, 65, 'note_off'),
                          #         (200, 64, 'note_off')]
```


## Exercise \#3 Calculating Deltas

[Mido](https://mido.readthedocs.io/en/latest/) is a Python library for
reading, manipulating and writing MIDI files. The event lists above
are *almost* in a format that we can use with mido. One remaining
problem is the way time is handled in our events.  In the event lists
generated above, the time field represents the *absolute* time that
the corresponding event occurs. The MIDI protocol actually represents
time in terms of *delta*s between events.  The delta value stored with
each event represents the elapsed time since the previous event.
Complete the `events_to_midi_events` function to convert our event
lists into this representation.  The following code snippet shows an
example of the expected behavior:
```python
events = [(0, 64, 'note_on'), 
          (50, 65, 'note_on'),   # delta is 50
          (75, 65, 'note_off'),  # delta is 25 
          (200, 64, 'note_off')] # delta is 125
		  
print(events_to_midi_events(events)) # prints [(0, 64, 'note_on'), 
                                     #         (50, 65, 'note_on'),
                                     #         (25, 65, 'note_off'),
                                     #         (125, 64, 'note_off')]
```


## Exercise \#4 Using Mido to create MIDI files

We now have all of the tools in place to create MIDI files from a
sequence of notes. Here is an example illustrating how the Mido
library can be used to create a midi file corresponding to the
previous example:

```python
from mido import Message, MidiFile, MidiTrack

outfile = MidiFile()
track = MidiTrack() # MIDI files can have multiple tracks, but we won't.
outfile.tracks.append(track)

track.append(Message('note_on', note=64, velocity=100, time=0))
track.append(Message('note_on', note=65, velocity=100, time=50))
track.append(Message('note_on', note=65, velocity=100, time=25))
track.append(Message('note_on', note=64, velocity=100, time=125))

outfile.save('out.mid')
```

Mido represents a MIDI file using a `MidiFile` object, which can
contain multiple `MidiTrack` objects, which themselves contain a
sequence of `Message` objects corresponding to events.

Complete the unfinished `notes_to_midi` function so that it conforms
to the provided docstring.

## Exercise \#5 Composition

The provided `synth.py` program uses pygame to provide a simple
graphical music composition tool.  If you have successfully completed
the exercises above, you should be able to use the tool to generate
and play MIDI files. The tool accepts the following input:

* The left mouse button activates grid squares indicating that the
  corresponding note should play at the indicated time.
* The right mouse button clears a square.
* Pressing the 'c' key will clear the current composition.
* Pressing the 'p' key will save and play the current composition. The
  file will be saved as `synth.mid` in the same folder where the
  program was executed. If playback doesn't work, you should be able
  to play the saved file using a web-based MIDI player like
  <https://midiplayer.ehubsoft.net/>.

Use this tool to create a beautiful musical composition.

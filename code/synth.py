import subprocess
import pygame
import midi_notes

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def note_to_number(note):
    octave = int(note[-1]) + 1
    number = NOTES.index(note[0:-1])
    number += (len(NOTES) * octave)
    return number

class GridSynth:

    def __init__(self, width, height, duration=100):
        self.square_size = 25
        self.margin = 2
        self.width = width
        self.height = height
        self.duration = duration
        self.grid = [[False]*width for i in range(height)]
        window_size = (width * (self.square_size + self.margin) + self.margin,
                       height * (self.square_size + self.margin) + self.margin)

        pygame.init()
        pygame.key.set_repeat(50)
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.done = False

        while not self.done:
            self.draw()

    def play_notes(self):
        notes = self.get_notes()
        print(notes)
        midi_notes.notes_to_midi(notes, 'synth.mid')
        # Doing it this way because there is a bug that causes pygame
        # to crash after one midi file is played.
        subprocess.call(['python', 'play_midi.py', 'synth.mid'])

    def draw_rect(self, row, column, color, border=0, text=None):

        pygame.draw.rect(self.screen,
                         color,
                         [(self.margin + self.square_size) * column + self.margin,
                          (self.margin + self.square_size) * row + self.margin,
                          self.square_size,
                          self.square_size], border)

        if text is not None:
            font = pygame.font.SysFont(None, 20)
            img = font.render(text, True, (0, 0, 0))
            self.screen.blit(img, ((self.margin + self.square_size) * column + self.margin,
                                   (self.margin + self.square_size) * row + self.margin))

    def row_to_note_name(self, row):
        start_octave = 3
        row = self.height - row - 1
        note = NOTES[row % len(NOTES)]
        note += str(row // len(NOTES) + start_octave)
        return note

    def draw_grid(self):
        self.screen.fill((0, 0, 0))
        for row in range(self.height):
            for column in range(self.width):
                if self.grid[row][column]:
                    color = (0, 0, 0)
                else:
                    color = (255, 255, 255)
                if column == 0:
                    self.draw_rect(row, column, color,
                                   text=self.row_to_note_name(row))
                else:
                    self.draw_rect(row, column, color)
 


    def draw(self):

        for event in pygame.event.get():  # User did something
            pos = pygame.mouse.get_pos()
            column = pos[0] // (self.square_size + self.margin)
            row = pos[1] // (self.square_size + self.margin)
            if event.type == pygame.QUIT:  # If user clicked close
                self.done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.play_notes()
                if event.key == pygame.K_c:
                    for row in range(self.height):
                        for column in range(self.width):
                            self.grid[row][column] = False

            if (row < self.height and row >= 0 and column < self.width
                    and column >= 1):
                if event.type == pygame.MOUSEMOTION:
                    if event.buttons[0] == 1:
                        self.grid[row][column] = True

                    if event.buttons[2] == 1:
                        self.grid[row][column] = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.grid[row][column] = True
                    elif event.button == 3:
                        self.grid[row][column] = False

        self.draw_grid()

        pygame.display.flip()
        self.clock.tick(60)

    def get_notes(self):
        notes = []
        for row in range(self.height):
            in_note = False
            start = -1
            for column in range(1, self.width):
                if self.grid[row][column] and column != self.width-1:
                    if not in_note:
                        start = (column - 1) * self.duration
                        in_note = True
                else:
                    if in_note:
                        end = (column - 1) * self.duration
                        note = self.row_to_note_name(row)
                        number = note_to_number(note)
                        notes.append((start, end, number))
                        in_note = False
        notes.sort()
        return notes


if __name__ == "__main__":
    GridSynth(51, 24)

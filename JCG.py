# ----------------------------------------------------------------------
# Name:       Tim Smaluk & Ryan Stockwell
# Purpose:    GUI Project
#
# Date:       3/30/2019
# ----------------------------------------------------------------------
"""
Homework 8 Module of Josephus Circle game.

The game board consists of blue and yellow circles that represent
soldiers in a circle. Facing execution, they decide to kill themselves
in order to avoid imprisonment. However, you decide that you would
rather face prison than face death. Choose a spot in the circle to
stand where you will avoid death.

Hint: The white circle is the first killer
"""
import tkinter
import argparse
import math
import random

from tkinter import messagebox


def get_arguments():
    """
   Parse and validate the command line arguments.
   :return: tuple containing (int) number of Josephus in the circle,
   (int) number of attempts aka difficulty
   """
    parser = argparse.ArgumentParser()

    parser.add_argument('difficulty',
                        help='Number of Soldiers: easy:6-10, '
                             'normal:11-17, hard:18-22',
                        choices=['easy', 'normal', 'hard'],
                        default='easy')

    parser.add_argument('-v', '--verbose',
                        help='Print details?',
                        action='store_true')

    arguments = parser.parse_args()
    difficulty = arguments.difficulty
    verbose = arguments.verbose

    return difficulty, verbose


def get_count():
    """"
   Generates random solider counts for the game circle
   """
    if get_arguments()[0] == 'easy':
        return random.randint(2, 10)
    elif get_arguments()[0] == 'normal':
        return random.randint(11, 25)
    elif get_arguments()[0] == 'hard':
        return random.randint(50, 100)


def check_verbose():
    """
   Generates verbose statement if verbose arg is invoked
   """
    difficulty, verbose = get_arguments()
    if verbose:
        print(f'Josephus Circle with {get_count()} soldiers and difficulty '
              f'is set to {difficulty.upper()}')


class JosephusCircle:
    """
   GUI puzzle game for solving Josephus Circles

   Argument:
   parent (tkinter.Tk): the root window object

   Attributes:
   count (int): number of solider in the circle
   winner (int): index of winning solider
   coordinates (list): list of graphical coordinates of soldiers
   difficulty (tkinter.Label): the chosen difficulty
   reset (tkinter.Button): resets the game board
   canvas (tkinter.Canvas): the widget where for game board
   """

    attempts = 0

    def __init__(self, parent):
        parent.title('Josephus Circle')
        self.parent = parent
        self.count = get_count()
        #print(self.count)
        self.winner = self.set_winner()
        self.coordinates = []

        # create control frame to align difficulty/attempts/reset
        control_frame = tkinter.Frame(parent)
        control_frame.grid()

        # create difficulty label
        difficulty = tkinter.Label(control_frame, width=25,
                                   text=f'Difficulty: '
                                        f'{self.set_difficulty().upper()}')
        difficulty.grid(column=0, row=0)

        # create reset button
        reset = tkinter.Button(control_frame, width=25, text='RESET',
                               command=self.reset)

        reset.grid(column=2, row=0)

        # create game board canvas
        self.canvas = tkinter.Canvas(parent, width=500, height=500,
                                     background='white')

        self.spartan_image = tkinter.PhotoImage(file='small_spartan.gif')
        self.canvas.create_image(250, 215, image=self.spartan_image)
        self.canvas.create_text(250, 250, text=f'Attempts:{self.attempts}')
        self.canvas.bind("<Button-1>", self.select_solider)
        self.generate_circles()
        self.canvas.grid()

    @staticmethod
    def set_difficulty():
        """
       Sets the game difficulty based on attempts specified in the
       command line arguments
       :return: (string) easy, normal, hard
       """
        return get_arguments()[0]

    @classmethod
    def update_attempts(cls):
        cls.attempts += 1

    def generate_circles(self):
        """
       Generates mini circles around the circumference of a circle
       with radius indicated by the function points_in_circum. Mini
       circles are colored alternating blue/yellow
       :return: (list) of coordinates of the soldiers
       """
        coordinates = []
        count = 0
        for x, y in points_in_circum(200, n=self.count):
            if count == 0:
                self.canvas.create_oval((x + 250,
                                         y + 250,
                                         (x + 250) + 10,
                                         (y + 250) + 10), fill='white',
                                        tags=count)
                count += 1
            elif count % 2 == 0:
                self.canvas.create_oval((x + 250,
                                         y + 250,
                                         (x + 250) + 10,
                                         (y + 250) + 10), fill='blue2',
                                        tags=count)
                count += 1
            else:
                self.canvas.create_oval((x + 250,
                                         y + 250,
                                         (x + 250) + 10,
                                         (y + 250) + 10), fill='goldenrod1',
                                        tags=count)
                count += 1

            coordinates.append((x + 250,
                                y + 250,
                                (x + 250) + 10,
                                (y + 250) + 10))

        self.coordinates = coordinates

    def solider_positions(self):
        """
       Finds the position of all soldiers
       :return: (set) of solider positions
       """
        players = [str(player) for player in range(0, self.count)]

        # dictionary containing soldier number and position(x0,y0,x1,y1)

        player_positions = {players[i]: self.coordinates[i]
                            for i in range(0, self.count)}
        return player_positions

    def distance_between_two_circles(self, killer_circle, casualty_circle):
        """
       Draws a path for the animation to show the trajectory of the kill
       :param killer_circle: (int) The number of the killer
       :param casualty_circle: (int) The number of the casualty
       """
        cords_circle_1 = self.solider_positions()[str(killer_circle)]
        cords_circle_2 = self.solider_positions()[str(casualty_circle)]

        self.canvas.create_line(cords_circle_1[0] + 5,
                                cords_circle_1[1] + 5,
                                cords_circle_2[0] + 5,
                                cords_circle_2[1] + 5,
                                arrow=tkinter.LAST)

    @staticmethod
    def kill(n, k=2):
        """
       Citing rosettacode.org https://bit.ly/2HNtxeP
       Algorithm for order killing of soldiers
       :param n: (int) number of soldiers
       :param k: (int) step
       :return:  (list) of tuples containing order of shooter and casualty
       """
        p, i, casualties, killers = list(range(n)), 0, [], []
        while p:

            i = (i + k - 1) % len(p)
            casualties.append(p.pop(i))
            if len(killers) < n - 1:
                killers.append(p[i - 1])

        casualties = casualties[0:-1]

        # Joins two lists
        sequence = map(lambda shooter, casualty:
                       (shooter, casualty), killers, casualties)
        kill_order = [s for s in sequence]

        return kill_order

    def animate_kills(self):
        """
       Draws lines to indicate the trajectory of the kill
       """
        winners = []
        for x, y in self.kill(self.count, 2):
            self.distance_between_two_circles(x, y)
            self.canvas.update()
            self.canvas.after(250, self.distance_between_two_circles(x, y))
            winners.append(x)
        winner = winners[-1]
        winner_cords = self.solider_positions()[str(winner)]
        self.canvas.create_oval(winner_cords, fill='red')


    def set_winner(self):
        """
       Finds the position of the winning circle (from start circle)
       :return: (int) winner position
       """
        winners = []
        for x, y in self.kill(self.count, 2):
            winners.append(x)
        return winners[-1]

    def select_solider(self, event):
        """
       Selects your solider
       :param event: left mouse button click on canvas
       """
        shape = self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.itemcget(shape, "tags")
        if self.winner == int(tags[0:2]):
            self.animate_kills()
            tkinter.messagebox.showinfo('Congrats', 'You win')
        else:
            if tkinter.messagebox.askyesno('Incorrect', 'You died- Try '
                                                        'Again?'):
                self.update_attempts()
                self.reset()
            else:
                quit()

    def reset(self):
        """
       Clears the canvas and regenerates the circles
       """
        self.canvas.delete("all")
        self.generate_circles()
        self.canvas.create_image(250, 215, image=self.spartan_image)
        self.canvas.create_text(250, 250, text=f'Attempts:'
                                               f'{self.attempts}')


def points_in_circum(r, n=2):
    """
   Citing systech on StackExchange https://bit.ly/2FAIKMt

   :param r: (int) Radius of the circle
   :param n: (int) Number of circles (default = 2)
   :return:  (list) of coordinates for x0,y0 of circle
   """
    pi = math.pi
    return [(int(math.cos(2 * pi / n * x) * r),
             int(math.sin(2 * pi / n * x) * r))
            for x in range(0, n)]


def main():
    check_verbose()
    root = tkinter.Tk()
    josephus_app = JosephusCircle(root)
    # print(josephus_app.winner)
    root.mainloop()


if __name__ == '__main__':
    main()

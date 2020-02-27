"""Array Backed Grid

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.

Note: Regular drawing commands are slow. Particularly when drawing a lot of
items, like the rectangles in this example.

For faster drawing, create the shapes and then draw them as a batch.
See array_backed_grid_buffered.py

If Python and Arcade are installed, this example can be run from the
command line with: python -m arcade.examples.array_backed_grid

"""

import sys
import collections
import arcade
from arcade.color import BLACK

# Set how many rows and columns we will have
ROW_COUNT = Y_LENGTH = 20
COLUMN_COUNT = X_LENGTH = 40

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 1

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Vector racing"

Point = collections.namedtuple("Point", "x y")
Line = collections.namedtuple("Line", "p1 p2")

START_P = Point(x=X_LENGTH // 2, y=1)  # The center of START
START_LINE = Line(p1=Point(x=START_P.x - 1, y=START_P.y),
                  p2=Point(x=START_P.x, y=START_P.y))
GOAL = Point(x=X_LENGTH - 2, y=Y_LENGTH - 1)
GOAL_LINE = Line(p1=Point(x=GOAL.x - 1, y=GOAL.y),
                 p2=Point(x=GOAL.x + 1, y=GOAL.y))


def to_grid(coordinate):
    """Transforms a grid coordinate to a screen point."""
    return coordinate * WIDTH + coordinate * MARGIN


def draw_line(line, color=BLACK, width=1):
    p1 = line.p1
    p2 = line.p2
    arcade.draw_line(to_grid(p1.x), to_grid(p1.y), to_grid(p2.x),
                     to_grid(p2.y), color, width)


def on_segment(p, q, r):
    if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x))
            and (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False


def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r)
    # function returns the following values:
    # 0 : Colinear points
    # 1 : Clockwise points
    # 2 : Counterclockwise

    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
    # for details of below formula.

    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):

        # Clockwise orientation
        return 1
    elif (val < 0):

        # Counterclockwise orientation
        return 2
    else:

        # Colinear orientation
        return 0


def intersect(p1, q1, p2, q2):
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True

    # Special Cases

    # p1 , q1 and p2 are colinear and p2 lies on segment p1q1
    if ((o1 == 0) and on_segment(p1, p2, q1)):
        return True

    # p1 , q1 and q2 are colinear and q2 lies on segment p1q1
    if ((o2 == 0) and on_segment(p1, q2, q1)):
        return True

    # p2 , q2 and p1 are colinear and p1 lies on segment p2q2
    if ((o3 == 0) and on_segment(p2, p1, q2)):
        return True

    # p2 , q2 and q1 are colinear and q1 lies on segment p2q2
    if ((o4 == 0) and on_segment(p2, q1, q2)):
        return True

    # If none of the cases
    return False


class TextButton:
    """ Text-based button """
    def __init__(self,
                 center_x,
                 center_y,
                 width,
                 height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2,
                         self.center_y - self.height / 2,
                         self.center_x + self.width / 2,
                         self.center_y - self.height / 2, color,
                         self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2,
                         self.center_y - self.height / 2,
                         self.center_x + self.width / 2,
                         self.center_y + self.height / 2, color,
                         self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2,
                         self.center_y + self.height / 2,
                         self.center_x + self.width / 2,
                         self.center_y + self.height / 2, color,
                         self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2,
                         self.center_y - self.height / 2,
                         self.center_x - self.width / 2,
                         self.center_y + self.height / 2, color,
                         self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text,
                         x,
                         y,
                         BLACK,
                         font_size=self.font_size,
                         width=self.width,
                         align="center",
                         anchor_x="center",
                         anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


class TimeStepButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 50, 20, "Tic", 12, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class ChangeSpeedButton(TextButton):
    def __init__(self, center_x, center_y, action_function, text):
        super().__init__(center_x,
                         center_y,
                         15,
                         15,
                         text=text,
                         font_size=12,
                         font_face="Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


def check_mouse_press_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def check_mouse_release_for_buttons(_x, _y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()


class VectorRacing(arcade.Window):
    """
    Main application class.
    """
    def __init__(self, width, height, title):
        """
        Set up the application.
        """

        # TODO: Should find out why it's not working OpenGL. Maybe due
        # to my local python compilation.
        super().__init__(width, height, title, antialiasing=False)

        # Create a 2 dimensional array. A two dimensional
        # array is simply a list of lists.
        # TODO: ¿Do I need to store a grid like this?
        self.grid = []

        for row in range(ROW_COUNT):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)  # Append a cell

        arcade.set_background_color(arcade.color.LIGHT_GRAY)

        # Initial speed is zero.
        self.v_x = self.current_v_x = 0
        self.v_y = self.current_v_y = 0

        # the time
        self.t = 0

        self.tip = START_P

        self.game_over = False

        self.winner = False

    def setup(self):
        self.button_list = [
            ChangeSpeedButton(to_grid(2) + 1 * WIDTH // 6,
                              to_grid(Y_LENGTH - 1) - HEIGHT // 2,
                              text="+",
                              action_function=self.speed_v_x),
            ChangeSpeedButton(to_grid(2) + 5 * WIDTH // 6,
                              to_grid(Y_LENGTH - 1) - HEIGHT // 2,
                              text="-",
                              action_function=self.reduce_v_x),
            ChangeSpeedButton(to_grid(2) + 1 * WIDTH // 6,
                              to_grid(Y_LENGTH - 2) - HEIGHT // 2,
                              text="+",
                              action_function=self.speed_v_y),
            ChangeSpeedButton(to_grid(2) + 5 * WIDTH // 6,
                              to_grid(Y_LENGTH - 2) - HEIGHT // 2,
                              text="-",
                              action_function=self.reduce_v_y),
            TimeStepButton(to_grid(3),
                           to_grid(Y_LENGTH - 1) + HEIGHT // 2, self.tic),
        ]

        self.lines = []

    def tic(self):
        self.t += 1
        self.current_v_x = self.v_x
        self.current_v_y = self.v_y

        new_tip = Point(self.tip.x + self.v_x, self.tip.y + self.v_y)

        new_vector = Line(self.tip, new_tip)
        self.lines.append(new_vector)

        if intersect(GOAL_LINE.p1, GOAL_LINE.p2, new_vector.p1, new_vector.p2):
            self.winner = True

        self.tip = new_tip

        if self.out_of_grid():
            self.game_over = True

    def out_of_grid(self):
        if self.tip.x > X_LENGTH:
            return True
        if self.tip.x < 0:
            return True
        if self.tip.y > Y_LENGTH:
            return True
        if self.tip.y < 0:
            return True

        return False

    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        output = "Game Over"
        arcade.draw_text(output, to_grid((X_LENGTH - 8) // 2),
                         to_grid(Y_LENGTH // 2), BLACK, 54)

    def draw_winner(self):
        """
        Draw "winer" across the screen.
        """
        output = "¡You win!"
        arcade.draw_text(output, to_grid((X_LENGTH - 8) // 2),
                         to_grid(Y_LENGTH // 2), BLACK, 54)

    def speed_v_x(self):
        if abs(self.v_x + 1 - self.current_v_x) > 1:
            return
        self.v_x += 1

    def reduce_v_x(self):
        if abs(self.v_x - 1 - self.current_v_x) > 1:
            return
        self.v_x -= 1

    def speed_v_y(self):
        if abs(self.v_y + 1 - self.current_v_y) > 1:
            return
        self.v_y += 1

    def reduce_v_y(self):
        if abs(self.v_y - 1 - self.current_v_y) > 1:
            return

        self.v_y -= 1

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the grid
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # Figure out what color to draw the box
                if self.grid[row][column] == 1:
                    color = arcade.color.GREEN
                else:
                    color = arcade.color.WHITE

                # Do the math to figure out where the box is
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                # Draw the box
                arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

        # The start
        arcade.draw_text("START",
                         to_grid(START_P.x - 1) + WIDTH // 3,
                         to_grid(START_P.y - 1) + HEIGHT // 3, BLACK)

        draw_line(
            Line(p1=Point(x=START_P.x - 1, y=START_P.y),
                 p2=Point(x=START_P.x + 1, y=START_P.y)))

        # The goal
        draw_line(Line(p1=Point(x=GOAL.x - 1, y=GOAL.y),
                       p2=Point(x=GOAL.x + 1, y=GOAL.y)),
                  width=3)

        arcade.draw_text("GOAL",
                         to_grid(GOAL.x - 1) + WIDTH // 3,
                         to_grid(GOAL.y + 1) - HEIGHT, BLACK)

        # Show initial speed
        arcade.draw_text(f"t = {self.t}",
                         to_grid(0) + WIDTH // 3,
                         to_grid(Y_LENGTH) - 2 * HEIGHT // 3, BLACK)
        arcade.draw_text(f"Vx = {self.v_x}",
                         to_grid(0) + WIDTH // 3,
                         to_grid(Y_LENGTH - 1) - 2 * HEIGHT // 3, BLACK)
        arcade.draw_text(f"Vy = {self.v_y}",
                         to_grid(0) + WIDTH // 3,
                         to_grid(Y_LENGTH - 2) - 2 * HEIGHT // 3, BLACK)

        for button in self.button_list:
            button.draw()

        for line in self.lines:
            draw_line(Line(p1=line.p1, p2=line.p2))

        if self.winner:
            self.draw_winner()

        if self.game_over:
            self.draw_game_over()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if self.game_over or self.winner:
            sys.exit(0)
        check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        check_mouse_release_for_buttons(x, y, self.button_list)


def main():
    vector_racing = VectorRacing(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    vector_racing.setup()

    arcade.run()


if __name__ == "__main__":
    main()

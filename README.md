# PGX 1.0 documentation

## PGX is a simple python library for creating 2D games.
## It includes:
   - Many shape widgets
   - A Camera
   - And many predefined functions to make it easy.

## Installation:
You can install PGX by using **pip**. You must do this before writing PGX code:
```
pip install git+https://github.com/FantasticBrain2014/PGX.git
```

## Getting started:
Now, you can get started on PGX.Let's make a simple code where a blank window is opened:
```
import PGX # Get the PGX moudle
win = PGX.GameWindow(800, 600) # Open a window 800 pixels wide and 600 pixels high.
def on_draw(): # Function for drawing.
   PGX.render() # Clear the window. This is the first thing to do in on_draw().

win.bind_draw(on_draw) # Tell the window to draw.
PGX.gameloop() # Start the main loop of PGX.
```
Don't worry that it seems long. You can enhance your typing skills with that!
Now run your code. You should see a white window with the title 'PGX 1.0 Game'. If you don't, 
carefully check the code above.

## Adding objects

Now that we know how to create a window, we want to make objects. We can make text with `PGX.Text()`:
```
import PGX
win = PGX.GameWindow(800, 600)
text = PGX.Text(win.center(), 'Hello, World!') # Create a Text widget at the center of the screen.
def on_draw():
   PGX.render()
   text.draw() # Draw the text.

win.bind_draw(on_draw)
PGX.gameloop()
```
The code should display a medium-sized black text.
Giving style:
- You can change the position of the text by putting a tuple for the xy coords in place of `win.center()` Eg. (200, 400)
- Change the text by changing the string.
- Give it font and color: `PGX.Text(win.center(), 'Hello, World!', col=PGX.col_help.red, font='Courtier 30')` You can make your own colors with PGX.color(red, green, blue, alpha) 
- Alpha makes it transparent and is automaticly set to 255 (Fully visible.)

## More objects

All of these objects have `draw(), moveleft(), moveright(), moveup(), movedown(), move()`, and `teleport()` methods.
`PGX.geometry.Quad(center, width, height, col=PGX.col_help.black, filled=False)` Creates a square or rectangle. You can rotate it.
`PGX.geometry.Circle(center, width, height, col=PGX.col_help.black, filled=False)` Creates a circle or oval. You can also rotate it.
`PGX.geometry.Arc(circle, start_angle, end_angle, col=PGX.col_help.black, filled=False)` Creates an arc. An example of the circle parameter: (200, 400, 50, 50) (center_x, center_y, width, height)
These all have a distort shape method:
`PGX.geometry.Line(start, end, col=PGX.col_help.black, thickness=4)` A line. Start and end are coordinate tuples.
`PGX.geometry.Trio(poi1, poi2, poi3, col=PGX.col_help.black, filled=False)` A triangle. All the points are coordinate tuples.
`PGX.geometry.Poly(points, col=PGX.col_help.black, filled=False)` A polygon. Example of the points parameter: [(400, 200), (340, 450), (560, 560), (120, 190)]

## Events and Game: Hide and Show
PGX can detect input from the user with PGX.Event . Let's see how!
We need to put event handlers, moving and rotating in a function called `update()`; then bind it to the window.
`PGX.Event.getkey()` detects the key pressed and returns various strings.
Let's make a code where we show and hide a square by pressing space:
The algorithim: Set the window -> Create and draw a square -> Space clicked? -yes> Square shown? -yes> Hide it -no> Show it.
Let's start:
```
import PGX
win = PGX.GameWindow(800, 600)
win.set_title('Event Handling') # set_title() gives the window a title.
sq = PGX.geometry.Quad(win.center(), 50, 50, col=PGX.col_help.blue, filled=True) # A blue, filled square.
sq.rotate(45) # Rotate the square.
shown = True
def on_draw():
   PGX.render()
   sq.draw()

def update(delta_time): # delta_time makes a stable speed in all computers.
   global shown
   key = PGX.Event.getkey()
   if key == 'SPACE' and shown:
       shown = False
       sq.hide()
   elif key == 'SPACE' and not shown:
       shown = True
       sq.show()

PGX.Event.bind(win) # Let the window detect key and mouse presses.
win.bind_draw(on_draw)
win.bind_update(update)
PGX.gameloop()
```
The code should run well! Click the spacebar and hide and show!

## All the `PGX.Event.getkey()` Keys:
Use this program to learn the keys by clicking them:
```
import PGX

win = PGX.GameWindow(300, 300) # Just a small window.

def on_draw():
    PGX.render()

def update(delta_time):
    key = PGX.Event.getkey()
    if key != None:
        print('Key pressed: ', key)

PGX.Event.bind(win)
win.bind_update(update)
win.bind_draw(on_draw)
PGX.gameloop()
```
This should show the key name you clicked! Have fun!

## Game: Ball and Bat:
We'll make a ball and bat game with two new functions: `toch()` and `toch_edge()` that detect colloisions. Let's start!
```
import PGX

win = PGX.GameWindow(800, 600)
win.set_title('Bat & Ball')
score = 0 # Set some varibles that move the ball and keep score.
ballx = 3
bally = 3

hexagon = PGX.hexget(300, 400, 20) # Make points for a hexagon.
ball = PGX.geometry.Poly(hexagon, col=PGX.col_help.purple, filled=True) # Make a  purple hexagon as the ball.
bat = PGX.geometry.Quad((400, 75), 60, 20, col=PGX.col_help.blue, filled=True) # Make a rectangle as the bat.
score_txt = PGX.Text((40, 560), 'Score: '+str(score), col=PGX.col_help.white) # Make a text to show the score.

def on_draw():
    PGX.render()
    win.fill(PGX.col_help.dodgerblue4) # Fill the window with dodger blue 4.
    score_txt.draw() # Draw everything.
    ball.draw()
    bat.draw()

def update(delta_time):
    key = PGX.Event.getkey() # Get the key pressed.
    if key == 'LEFT': # Is it the left key?
        bat.moveleft(15) # If so, move left.
    elif key == 'RIGHT': 
        bat.moveright(15)
    edge = PGX.toch_edge(bat, win) Check the edge that the bat is touching.
    if edge == 'LEFT': # Is it the left edge
        bat.moveright(15) # If so, move the opposite direction.
    elif edge == 'RIGHT':
        bat.moveleft(15)
    move_ball()

def move_ball():
    global ballx, bally, score
    edge = PGX.toch_edge(ball, win) # Find the edge the object is toching.
    if edge == 'LEFT' or edge == 'RIGHT':
        ballx = -ballx # Bounce off the left and right sides.
    elif edge == 'TOP':
        bally = -bally # Bounce off the top side.
    elif edge == 'BOTTOM':
        bally = 3 # If the ball touches the bottom side, reset the game.
        ballx = 3
        score = 0
        score_txt.content(newtext='Score: '+str(score)) # Update what the text says.
        ball.teleport(win.center()[0], win.center()[0]) # Teleport to the center of the screen.
    elif PGX.toch(bat, ball) == True: # Is the ball bouncing off the bat?
        bally = -bally # If so ,bounce off the bat.
        score += 1 # And increase the score by one.
        score_txt.content(newtext='Score: '+str(score))
    ball.move(ballx, bally) # Move diagnolly depending on ballx and bally.

PGX.Event.bind(win)
win.bind_draw(on_draw)
win.bind_update(update)
PGX.gameloop() # Start the game.
```
This should work well! You should have learned enough to make your own simple game!


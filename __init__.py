""" PGX, short for Picture GraphiX

A simple 2D game moudle built on top of arcade.
It has lots of easy-to-use widgets and functions.
"""

import arcade
from . import geometry
from .col_help import white, black
from . import Event

import math
from .toch_geo import are_toch, xywhToPoints

from os import path
from pathlib import Path

from PIL import Image
import tempfile
import hashlib
from pyglet import image

_path = path.dirname(__file__)
_ipath = path.join(_path, 'PGXico.png')
# A PGX built-in sprite.
sprite_bobby = path.join(_path, 'bobby.png')

def color(R, G, B, A=255):
    return (R, G, B, A)

class GameWindow:
    def __init__(self, width, height):
        self.win = arcade.Window(dimx, dimy, '  PGX 1.0 Game')
        self.res = (dimx, dimy)
        icon = image.load(_ipath)
        self.win.set_icon(icon)
        self.win.on_close = self._on_close
        
    def fill(self, col):
        arcade.set_background_color(col)

    def close(self):
        self.win.close()

    def set_icon(self, icon):
        try:
            icon = image.load(icon)
            self.win.set_icon(icon)
        except FileNotFoundError as error:
            print('An Error occurred: ' + str(error))

    def set_title(self, title):
        self.win.set_caption('  '+title)

    def _on_close(self):
        print("Window closed")
        self.close()

    def bind_draw(self, func):
        self.win.on_draw = func

    def bind_update(self, func, speed=30):
        arcade.schedule(func, 1/speed)

    def center(self):
        return (self.res[0]/2, self.res[1]/2)

def render():
    arcade.get_window().clear()
    arcade.set_background_color(white)

def sound(soundtoplay, volume=100):
    vol = float(volume/100)
    sound = arcade.load_sound(soundtoplay)
    arcade.play_sound(sound, volume=vol)

class soundOGG:
    def __init__(self, sound):
        self.sound = None
        self.player = None
        self.soundname = sound

    def play(self, volume=100, looping=True):
        vol = float(volume/100)
        self.sound = arcade.Sound(self.soundname, streaming=True)
        self.player = self.sound.play(loop=looping)
        self.player.volume = vol

    def pause(self):
        if self.player != None:
            self.player.pause()

    def resume(self):
        if self.player != None:
            self.player.play()

    def stop(self):
        if self.player:
            self.resume()
            self.player = None
        self.sound = None

def hexget(center_x, center_y, radius):
    points = []
    for i in range(6):
        angle = math.radians(i * 60)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    return points

class Text:
    def __init__(self, center, text, col=black, font="Arial 20"):
        self.center = center
        self.text = text
        self.col = col
        self.font = font.split(" ")
        self.font_name = self.font[0]
        self.font_size = int(self.font[1])
        self.arcade_text = None  
        self.update_text()

    def update_text(self):
        self.arcade_text = arcade.Text(
            self.text,
            self.center[0],
            self.center[1],
            color=self.col,
            font_size=self.font_size,
            font_name=self.font_name,
        )

    def draw(self):
        self.arcade_text.draw()

    def content(self, newtext=None, newfont=None, newcol=None):
        updated = False
        if newtext is not None:
            self.text = newtext
            updated = True
        if newfont is not None:
            self.font = newfont.split(" ")
            self.font_name = self.font[0]
            self.font_size = int(self.font[1])
            updated = True
        if newcol is not None:
            self.col = newcol
            updated = True
        if updated:
            self.update_text()  # Only recreate text if something changed


class Sprite:
    def __init__(self, center, width, height, image):
        self.defaultimage = image
        texture = arcade.load_texture(image)
        self.sprite = arcade.Sprite(texture, 1.0)
        self.sprite.center_x = center[0]
        self.sprite.center_y = center[1]
        self.sprite.width = width
        self.sprite.height = height
        self.sprite.angle = 0
        self.yesdraw = True

    def draw(self):
        if self.yesdraw:
            arcade.draw_sprite(self.sprite) # Please DON'T change this line. It works properly.

    def move(self, dx, dy):
        self.sprite.center_x += dx
        self.sprite.center_y += dy

    def moveleft(self, dx):
        self.sprite.center_x -= dx

    def moveright(self, dx):
        self.sprite.center_x += dx

    def moveup(self, dy):
        self.sprite.center_y += dy

    def movedown(self, dy):
        self.sprite.center_y -= dy

    def teleport(self, dx, dy):
        self.sprite.center_x = dx
        self.sprite.center_y = dy

    def rotate(self, angle):
        if angle + self.sprite.angle < 360:
                self.sprite.angle += angle

    def rotate_set(self, angle):
        if angle < 360:
            self.sprite.angle = angle

    def imag(self, new_image):
        try:
            self.sprite.texture = arcade.load_texture(new_image)
        except FileNotFoundError:
            raise FileNotFoundError('Sorry, the file you requested was not found.')

    def imag_reset(self):
        self.sprite.texture = arcade.load_texture(self.defaultimage)

    def hide(self):
        self.yesdraw = False

    def show(self):
        self.yesdraw = True

    def get_points(self):
        return xywhToPoints(self.sprite.center_x, self.sprite.center_y, self.sprite.width, self.sprite.height)
    
def get_trans(image_path):
    image_path = Path(image_path)
    im = Image.open(image_path).convert("RGBA") # Convert to RGBA format
    datas = im.getdata()
    changed = False
    new_data = []
    for item in datas:
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0)) 
            changed = True
        else:
            new_data.append(item)
    if not changed:
        return str(image_path)
    im.putdata(new_data)
    # Save to a temp file
    hash_name = hashlib.md5(str(image_path).encode()).hexdigest()
    temp_path = Path(tempfile.gettempdir()) / f"pgx_fixed_{hash_name}.png"
    im.save(temp_path)
    return str(temp_path)        

class SpriteGroup:
    def __init__(self):
        self.sprites = []

    def add(self, sprite):
        self.sprites.append(sprite)

    def destroy(self, sprite):
        if sprite in self.sprites:
            sprite.hide()
            self.sprites.remove(sprite)

    def draw_all(self):
        for sprite in self.sprites:
            sprite.draw()        

class Camera:
    def __init__(self, viewarea, zoom=1.0):
        self.zoom = zoom
        self.world = viewarea
        view = arcade.rect.XYWH(0, 0, viewarea[0], viewarea[1])
        self.cam = arcade.Camera2D(viewport=view, zoom=self.zoom)
        self.coords = (0, 0)
        self.set_pos(0, 0)

    def update_view(self):
        self.cam.use()

    def set_pos(self, x, y):
        self.cam.position = arcade.Vec2(x, y)
        self.coords = (x, y)

    def zoom_in(self, value):
        self.zoom += value
        self.cam.zoom = self.zoom

    def zoom_out(self, value):
        self.zoom -= value
        self.cam.zoom = self.zoom

    def getcoords(self):
        return self.coords

def toch(obj, obj2):
    if 'circle' in dir(obj):
        o1list = obj.get_box()
    if 'circle' in dir(obj2):
        o2list = obj2.get_box()
    if 'circle' not in dir(obj):
        o1list = obj.get_points()
    if 'circle' not in dir(obj2):
        o2list = obj2.get_points()
    return are_toch(o1list, o2list)

def toch_group(obj, group):
    istrue = []
    for gobj in group.sprites:
        istoch = toch(obj, gobj)
        if istoch == True:
            istrue.append(0)
    if len(istrue) > 0:
        return True
    return False

def toch_groups(obj, groups):
    istrue = []
    for group in groups:
        istoch = toch_group(obj, gobj)
        if istoch == True:
            istrue.append(0)
    if len(istrue) > 0:
        return True
    return False

def toch_edge(obj, win):
    x, y = win.res  # Window width and height
    if 'circle' in dir(obj):  
        olist = obj.get_box()
    else:
        olist = obj.get_points()
    for px, py in olist:
        if px <= 0:
            return 'LEFT'
        if px >= x:
            return 'RIGHT'
        if py <= 0:
            return 'BOTTOM'
        if py >= y:
            return 'TOP'
    return False

    
    
def gameloop():
    ''' Run the main loop of PGX.'''
    arcade.run()

__all__ = ['Camera', 'Event', 'GameWindow', 'Sprite', 'SpriteGroup', 'Text',
           'col_help', 'color', 'gameloop', 'geometry', 'get_trans', 'hexget',
           'render', 'sound', 'soundOGG', 'sprite_bobby',
           'toch', 'toch_edge', 'toch_group', 'toch_groups']




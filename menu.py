import sys
import termios


class Menu:
  def __init__(self, options, descriptions=None, default_selection=0):
    self.options = options
    self.descriptions = descriptions
    self.selected = default_selection
    self.old_term = None
  
  def __enter__(self):
    self.set_terminal()
    return self
  
  def __exit__(self, *args):
    self.reset_terminal()
  
  def set_terminal(self):
    fd = sys.stdin.fileno()
    self.old_term = termios.tcgetattr(fd)
    new_term = self.old_term.copy()
    new_term[3] &= ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, new_term)
  
  def reset_terminal(self):
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSANOW, self.old_term)

  def draw(self):
    for i, opt in enumerate(self.options):
      desc = self.descriptions[i] if self.descriptions else ''
      if i == self.selected:
        print(f'  \x1b[7m[{i:2}] {opt:40} {desc:30}\x1b[0m')
      else:
        print(f'  [{i:2}] {opt:40} {desc:30}')
  
  def choose(self, title='Choose one of the following:'):
    self.set_terminal()
    while True:
      print('\x1b[0;0H\x1b[2J', end='', flush=True) 
      print(title)
      self.draw()

      c = sys.stdin.read(1)
      
      if c == 'j':
        self.selected += 1
        if self.selected >= len(self.options):
          self.selected = 0

      elif c == 'k':
        self.selected -= 1
        if self.selected < 0:
          self.selected = len(self.options) - 1

      elif c == '\n':
        return self.selected, self.options[self.selected]
          
    self.reset_terminal()

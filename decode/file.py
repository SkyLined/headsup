from Structure import Structure;

class file_(Structure):
  def __init__(self, stream, offset, max_size, parent, name, type_name, \
      structure_class):
    self.type_name = type_name;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    self._contents = self.Member(structure_class, 'used');
    self.Unused();

def ANI(stream, offset, max_size, name):
  from ANI import ANI;
  return file_(stream, offset, max_size, None, name, 'FILE_ANI', ANI);

def BMP(stream, offset, max_size, name):
  from BMP import BMP;
  return file_(stream, offset, max_size, None, name, 'FILE_BMP', BMP);

def GIF(stream, offset, max_size, name):
  from GIF import GIF;
  return file_(stream, offset, max_size, None, name, 'FILE_GIF', GIF);

def ICO(stream, offset, max_size, name):
  from ICON import ICON;
  return file_(stream, offset, max_size, None, name, 'FILE_ICO', ICON);

def PNG(stream, offset, max_size, name):
  from PNG import PNG;
  return file_(stream, offset, max_size, None, name, 'FILE_PNG', PNG);

def WAV(stream, offset, max_size, name):
  from WAV import WAV;
  return file_(stream, offset, max_size, None, name, 'FILE_WAV', WAV);


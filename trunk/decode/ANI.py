import C;
from RIFF_Chunk import RIFF_Chunk;

def ANI(stream, offset, max_size, parent, name):
  result = RIFF_Chunk(stream, offset, max_size, parent, name, {'RIFF': ['ACON']});
  return result;
import C;
from RIFF_Chunk import RIFF_Chunk;

def WAV(stream, offset, max_size, parent, name):
  result = RIFF_Chunk(stream, offset, max_size, parent, name, \
    # TODO: Add structure
  );
  return result;
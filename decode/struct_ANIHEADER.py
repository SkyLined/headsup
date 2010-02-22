
# http://www.gdgsoft.com/anituner/help/aniformat.htm
def struct_ANIHEADER(stream, offset, max_size, parent, name):
  import C;
  result = C.STRUCT(stream, offset, max_size, parent, name, 'ANIHEADER', \
      ('Size',      C.DWORD),    # length of structure, to be set later.
      ('Frames',    C.DWORD),    # cFrames
      ('Steps',     C.DWORD),    # cSteps
      ('X',         C.DWORD),    # cx (must be 0)
      ('Y',         C.DWORD),    # cy (must be 0)
      ('BitCount',  C.DWORD),    # cBitCount
      ('Planes',    C.DWORD),    # cPlanes
      ('JifRate',   C.DWORD),    # JifRate
      ('Flags',     C.DWORD),    # flags (1 = AF_ICON
  );
  max_size -= result.size;
  if result._Size.value != result.size:
    result._Size.warnings.append('expected value to be %d' % result.size);
  if result._Frames.value == 0:
    result._Frames.warnings.append('expected at least 1 frame');
  if result._Steps.value == 0:
    result._Steps.warnings.append('expected at least 1 step');
  # These are reported to be "reserved, must be 0" but it is set to the W*H size
  # of the icons in some valid ani cursors... so ignoring this check.
#  if result._X.value != 0:
#    result._X.warnings.append('expected value to be 0');
#  if result._Y.value != 0:
#    result._Y.warnings.append('expected value to be 0');
  if result._Flags.value != 1:
    result._Flags.warnings.append('expected value to be 1 (AF_ICON)');
  else:
    result._Flags.notes.append('AF_ICON');
  return result;


from Structure import Structure;

# http://www.w3.org/TR/PNG/#11sPLT
class PNG_sPLT(Structure):
  type_name = 'PNG_sPLT';
  def __init__(self, stream, offset, max_size, parent, name):
    import math;
    import C;
    from struct_RGBAQUAD import struct_RGBAQUAD;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    null_seperator_index = self.GetMaxStream().find('\0');
    if null_seperator_index == -1:
      self._palette_name = None;
      self._null_seperator = None;
      self.warnings.append('no null found to seperate palette name from ' \
          'data, assuming data only');
    else:
      self._palette_name = self.Member(C.STRING, 'palette_name', \
          null_seperator_index);
      CheckName(self._palette_name);

      self._null_seperator = self.Member(C.BYTE, 'null_seperator');

    self._sample_depth = self.Member(C.BYTE, 'sample_depth');

    if self._sample_depth.value < 16:
      struct_size = 6;
      struct_definition = (
        ('Red',               C.BYTE),
        ('Green',             C.BYTE),
        ('Blue',              C.BYTE),
        ('Alpha',             C.BYTE),
        ('Frequency',         C.WORD),
      );
      self._sample_depth.notes.append('color/alpha info size = 1 byte');
    else:
      struct_size = 10;
      struct_definition = (
        ('Red',               C.WORD),
        ('Green',             C.WORD),
        ('Blue',              C.WORD),
        ('Alpha',             C.WORD),
        ('Frequency',         C.WORD),
      );
      self._sample_depth.notes.append('color/alpha info size = 2 bytes');

    self._number_of_palette_suggestions = \
        math.floor(self.current_max_size / struct_size);
    self._palette_suggestions = self.Member(C.ARRAY, 'palette_suggestions', \
        self._number_of_palette_suggestions, C.STRUCT, 'PALETTE_SUGGESTION', 
            *struct_definition);
    if self.current_max_size % struct_size != 0:
      self._palette_suggestions.warnings.append(
          'pallete size should be divisible by %d' % struct_size);
    self._palette_suggestions.dump_simplified = True;

    self.Unused();

def CheckName(name):
  if len(name.value) == 0:
    name.warnings.append('expected at least one character');
  elif len(name.value) > 79:
    name.warnings.append('expected at most 79 characters');
  for char in name.value:
    c = ord(char);
    if c < 0x20 or (char > 0x7E and char < 0xA1):
      name.warnings.append('string contains non-printable latin-1 characters');
      break;
  if ' ' in [name.value[0], name.value[-1]]:
    name.warnings.append('string must not start or end with a space');

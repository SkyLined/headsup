from Structure import Structure

VALID_CHUNK_TYPES = [
    'IHDR', 'PLTE', 'IDAT', 'tIME', 'zTXt', 'iTXt', 'pHYs', 'sPLT', \
    'cHRM', 'gAMA', 'iCCP', 'sBIT', 'sRGB', 'bKGD', 'hIST', 'tRNS', 'IEND'];

ALTERNATIVE_CHUNK_NAMES = {
  # X: Y = Chunk X is an alternative name for Chunk Y
  'spAL': 'sPLT',
};

CHUNK_ORDER_BEFORE = {
  # X: None             = No chunks must come before chunk X
  # X: [A, B, C, None]  = chunks A, B, C and any invalid chunks 
  #                       must come before chunk X
  # X can be the name of a valid chunk or None to indicated all invalid
  # chunks
  'IHDR': [],
  'PLTE': ['IHDR', 'cHRM', 'gAMA', 'iCCP', 'sBIT', 'sRGB'],
  'IDAT': ['IHDR', 'PLTE', 'pHYs', 'sPLT', 'cHRM', 'gAMA', 'iCCP', 'sBIT', \
           'sRGB', 'bKGD', 'hIST', 'tRNS'],
  'IEND': ['IHDR', 'PLTE', 'IDAT', 'tIME', 'zTXt', 'iTXt', 'pHYs', 'sPLT', \
           'cHRM', 'gAMA', 'iCCP', 'sBIT', 'sRGB', 'bKGD', 'hIST', 'tRNS',
           None],
  'cHRM': ['IHDR'],
  'gAMA': ['IHDR'],
  'iCCP': ['IHDR'],
  'sBIT': ['IHDR'],
  'sRGB': ['IHDR'],
  'bKGD': ['IHDR', 'PLTE'],
  'hIST': ['IHDR', 'PLTE'],
  'tRNS': ['IHDR', 'PLTE'],
  'pHYs': ['IHDR'],
  'sPLT': ['IHDR'],
  'tIME': ['IHDR'],
  'iTXt': ['IHDR'],
  'tEXt': ['IHDR'],
  'zTXt': ['IHDR'],
  None: ['IHDR'],
};
CHUNK_MIN_MAX_COUNT = {
  # X: (MIN,  None) = Chunk X must appear at least MIN times
  # X: (MIN,  MAX)  = Chunk X must appear between MIN & MAX times, inclusive
  'IHDR': (1,    1),
  'PLTE': (0,    1),
  'IDAT': (1,    None),
  'IEND': (1,    1),
  'cHRM': (0,    1),
  'gAMA': (0,    1),
  'iCCP': (0,    1),
  'sBIT': (0,    1),
  'sRGB': (0,    1),
  'bKGD': (0,    1),
  'hIST': (0,    1),
  'tRNS': (0,    1),
  'pHYs': (0,    1),
  'sPLT': (0,    None),
  'tIME': (0,    1),
  'iTXt': (0,    None),
  'tEXt': (0,    None),
  'zTXt': (0,    None),
};

# http://www.w3.org/TR/PNG/#D-CRCAppendix
class PNG_CHUNK(Structure):
  type_name = 'PNG_CHUNK';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    from PNG_CRC32 import PNG_CRC32;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._length = self.Member(C.DWORD, 'length', little_endian = False);

    self._type = self.Member(C.STRING, 'type', 4);

    if self._type.value in ALTERNATIVE_CHUNK_NAMES:
      self._name = ALTERNATIVE_CHUNK_NAMES[self._type.value];
      self._type.warnings.append( \
          'illegal name interpreted as "%s"' % self._name);
    elif self._type.value in VALID_CHUNK_TYPES:
      self._name = self._type.value;
    else:
      self._name = None;
    
    self._ancillary = None;
    char1 = self._type.value[0];
    if char1 >= 'A' and char1 <= 'Z':
      self._type.notes.append('critical');
      self._ancillary = True;
      if self._type.value not in ['IHDR', 'PLTE', 'IDAT', 'IEND']:
        self._type.warnings.append( \
            'expected critical chunk value to be "IHDR", "PLTE", "IDAT" ' \
            'or "IEND"');
    elif char1 >= 'a' and char1 <= 'z':
      self._type.notes.append('ancillary');
      self._ancillary = True;
    else:
      self._type.warnings.append( \
          'expected first character to be [A-Za-z]');

    self._private = None;
    char2 = self._type.value[1];
    if char2 >= 'A' and char2 <= 'Z':
      self._type.notes.append('public');
      self._private = False;
    elif char2 >= 'a' and char2 <= 'z':
      self._type.notes.append('private');
      self._private = True;
    else:
      self._type.warnings.append( \
          'expected second character to be [A-Za-z]');

    char3 = self._type.value[2];
    if char3 >= 'A' and char3 <= 'Z':
      pass;
    else:
      self._type.warnings.append( \
          'expected third character to be [A-Z]');

    self._safe_to_copy = None;
    char4 = self._type.value[3];
    if char4 >= 'A' and char4 <= 'Z':
      self._type.notes.append('not safe to copy');
      self._safe_to_copy = False;
    elif char1 >= 'a' and char1 <= 'z':
      self._type.notes.append('safe to copy');
      self._safe_to_copy = True;
    else:
      self._type.warnings.append( \
          'expected fourth character to be [A-Za-z]');

    self._data = self.Member(C.STRING, 'data', self._length.value);
    self.ContainStream(self._data.value, self._data.size);

    self._crc = self.Member(C.DWORD, 'crc', little_endian = False);

    crc_stream_size = self._type.size + self._data.size;
    crc_stream = stream[self._type.offset:self._data.offset + self._data.size];
    
    check_crc = PNG_CRC32(crc_stream);
    if check_crc != self._crc.value:
      self._crc.warnings.append('crc over 0x%X|%d bytes is 0x%08X' % \
          (len(crc_stream), len(crc_stream), check_crc));

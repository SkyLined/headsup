from Structure import Structure;

# http://www.w3.org/TR/PNG/#11iTXt
class PNG_iTXt(Structure):
  type_name = 'PNG_iTXt';
  def __init__(self, stream, offset, max_size, parent, name):
    import math;
    import C;
    from ZLIB_BLOCK import ZLIB_BLOCK;
    from struct_RGBAQUAD import struct_RGBAQUAD;
    from PNG_CheckText import PNG_CheckText;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    null_seperator_index = self.GetMaxStream().find('\0');
    if null_seperator_index == -1:
      self._keyword = None;
      self._keyword_seperator = None;
      self.warnings.append('no null found to seperate keyword from ' \
          'remaining data, assuming no keyword present');
    else:
      self._keyword = self.Member(C.STRING, 'keyword', null_seperator_index);
      PNG_CheckText(self._keyword, can_be_empty = False, max_size = 79, \
          no_extra_spaces = True, utf_8 = False, newlines = False, \
          is_keyword = True);
      self._keyword_seperator = self.Member(C.BYTE, 'keyword_seperator');

    self._compression_flag = self.Member(C.BYTE, 'compression_flag');
    self._compression_method = self.Member(C.BYTE, 'compression_method');

    null_seperator_index = self.GetCurrentMaxStream().find('\0');
    if null_seperator_index == -1:
      self._language_tag = None;
      self._language_tag_seperator = None;
      self.warnings.append('no null found to seperate language tag from ' \
          'remaining data, assuming no language tag present');
    else:
      self._language_tag = self.Member(C.STRING, 'language_tag', \
          null_seperator_index);
      PNG_CheckText(self._language_tag, can_be_empty = True, max_size = None, \
          no_extra_spaces = True, utf_8 = False, newlines = False, \
          is_keyword = False);
      # TODO: Extra checks may be in order
      self._language_tag_seperator = self.Member(C.BYTE, \
          'language_tag_seperator');

    null_seperator_index = self.GetCurrentMaxStream().find('\0');
    if null_seperator_index == -1:
      self._translate_keyword = None;
      self._translate_keyword_seperator = None;
      self.warnings.append('no null found to seperate translate keyword from ' \
          'remaining data, assuming no translate keyword present');
    else:
      self._translate_keyword = self.Member(C.STRING, 'translate_keyword', \
          null_seperator_index);
      PNG_CheckText(self._translate_keyword, can_be_empty = True, \
          max_size = None, no_extra_spaces = True, utf_8 = True, \
          newlines = False, is_keyword = False);
      self._translate_keyword_seperator = self.Member(C.BYTE, \
          'translate_keyword_seperator');

    if self.compression_flag.value == 0:
      self.compression_flag.notes.append('not compressed');
      if self._compression_method.value != 0:
        self._compression_method.warnings.append('expected value to be 0');
      self._text = self.Member(C.STRING, 'text', self.current_max_size);
      PNG_CheckText(self._text, can_be_empty = True, max_size = None, \
          no_extra_spaces = False, utf_8 = True, newlines = True, \
          is_keyword = False);
    elif self.compression_flag.value == 1:
      self.compression_flag.notes.append('compressed');
    else:
      self.compression_flag.warnings.append( \
          'expected value to be 0 or 1, assuming 0 (not compressed)');
    if self.compression_flag.value == 1:
      if self._compression_method.value == 0:
        self._compression_method.notes.append('zlib deflate');
      else:
        self._compression_method.warnings.append( \
            'unknown methods, zlib deflate assumed');
  
      self._compressed_text = self.Member(ZLIB_BLOCK, 'compressed_text');
      self._text = self._compressed_text.ContainMember( \
          C.STRING, 'decompressed_text', \
          self._compressed_text.current_contained_max_size);
      PNG_CheckText(self._text, can_be_empty = True, max_size = None, \
          no_extra_spaces = False, utf_8 = False, newlines = True, \
          is_keyword = False);
    else:
      self._text = self.Member(C.STRING, 'text', self.current_max_size);

    self.Unused();


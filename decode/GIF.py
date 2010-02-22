from Structure import Structure;

class GIF(Structure):
  type_name = 'GIF';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    from GIF_COLORTABLE import GIF_COLORTABLE;
    from GIF_EXTENSION import GIF_EXTENSION;
    from GIF_HEADER import GIF_HEADER;
    from GIF_IMAGE import GIF_IMAGE;
    from GIF_SCREEN_DESCRIPTOR import GIF_SCREEN_DESCRIPTOR;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._header = self.Member(GIF_HEADER, 'header');

    self._version = self._header._Version.value;
    self._screen_descriptor = self.Member( \
        GIF_SCREEN_DESCRIPTOR, 'screen_descriptor');

    self._width = self._screen_descriptor._Width.value;
    self._height = self._screen_descriptor._Height.value;
    flags = self._screen_descriptor._Flags;
    self._has_global_color_table = flags._GlobalColorTable.value == 1;
    if self._has_global_color_table:
      self._global_color_table_entries = \
          2 ** (flags._SizeGlobalColorTable.value + 1);
      self._global_color_table_sorted = flags._Sort.value == 1;
      self._bkg_color_index = \
          self._screen_descriptor._BkgColorIndex.value;

    self._bits_per_color = flags._ColorResolution.value + 1;
    aspect_ratio = self._screen_descriptor._PixelAspectRatio.value;
    if aspect_ratio == 0:
      self._aspect_ratio = None;
    else:
      self._aspect_ratio = (aspect_ratio + 15) / 64.0;

    if self._has_global_color_table:
      self._global_color_table = self.Member(GIF_COLORTABLE, \
          'global_color_table', self._global_color_table_entries, \
          self._global_color_table_sorted);
    else:
      self._global_color_table = None;

    self._images = [];
    self._extensions = [];
    blocks = 0;
    while self.DataAvailable():
      blocks += 1;
      block_name = 'block_%d' % blocks;
      id_byte = self.Member(C.BYTE, '%s_id' % block_name);
      if id_byte.value == 0x21:
        id_byte.notes.append('extension');
        block = self.Member(GIF_EXTENSION, '%s_data' % block_name);
        self._extensions.append(block);
      elif id_byte.value == 0x2C:
        id_byte.notes.append('image');
        block = self.Member(GIF_IMAGE, '%s_data' % block_name);
        self._images.append(block);
      elif id_byte.value == 0x3B:
        id_byte.notes.append('trailer');
        break; # End of stream
      else:
        id_byte.warnings.append('unknown type - cannot process');
        break;

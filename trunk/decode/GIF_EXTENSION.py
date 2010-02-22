from Structure import Structure;

# http://www.w3.org/Graphics/GIF/spec-gif89a.txt
class GIF_EXTENSION(Structure):
  type_name = 'EXTENSION';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    from GIF_BLOCK import GIF_BLOCK;
    from GIF_EXTENSION_APPLICATION import GIF_EXTENSION_APPLICATION;
    from GIF_EXTENSION_COMMENT import GIF_EXTENSION_COMMENT;
    from GIF_EXTENSION_GRAPHICS_CONTROL import GIF_EXTENSION_GRAPHICS_CONTROL;
    from GIF_EXTENSION_PLAIN_TEXT import GIF_EXTENSION_PLAIN_TEXT;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    
    self._label = self.Member(C.BYTE, 'label');
    if self._label.value == 0x01:
      self._label.notes.append('plain text extension');
      self._data = self.Member( \
          GIF_EXTENSION_PLAIN_TEXT, 'plain_text_extension');
    elif self._label.value == 0xF9:
      self._label.notes.append('graphice control extension');
      self._data = self.Member( \
          GIF_EXTENSION_GRAPHICS_CONTROL, 'graphice_control_extension');
    elif self._label.value == 0xFE:
      self._label.notes.append('comment extension');
      self._data = self.Member( \
          GIF_EXTENSION_COMMENT, 'comment_extension');
    elif self._label.value == 0xFF:
      self._label.notes.append('application extension');
      self._data = self.Member( \
          GIF_EXTENSION_APPLICATION, 'application_extension');
    else:
      self._label.warnings.append('unknown extension');
      self._data = self.Member(GIF_BLOCK, 'data');
      self._data.ContainUnused();

from Structure import Structure;

# http://www.w3.org/Graphics/GIF/spec-gif89a.txt
class GIF_EXTENSION_COMMENT(Structure):
  type_name = 'COMMENT_EXTENSION';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    from GIF_BLOCK import GIF_BLOCK;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._data = self.Member(GIF_BLOCK, 'data');

    self._comment = self._data.ContainMember(C.STRING, \
        'comment', self._data.contained_current_max_size);

    self._data.ContainUnused(); # Should always be 0.
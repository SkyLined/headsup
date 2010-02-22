from Structure import Structure;

# http://www.w3.org/Graphics/GIF/spec-gif89a.txt
class GIF_EXTENSION_APPLICATION(Structure):
  type_name = 'GIF_APPLICATION_EXTENSION';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    from GIF_BLOCK import GIF_BLOCK;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._data = self.Member(GIF_BLOCK, 'data');

    self._application_header = self._data.ContainMember(C.STRUCT, \
        'application_header', 'APPLICATION_EXTENSION_HEADER', \
        ('Identifier',          {C.STRING: 8}),
        ('AuthenticationCode',  {C.ARRAY: (3, C.BYTE)}),
    );

    self._application_data = self._data.ContainMember(C.STRING, \
        'application_data', self._data.contained_current_max_size);

    self._data.ContainUnused(); # Should always be 0

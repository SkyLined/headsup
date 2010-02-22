
def struct_RGBTRIPPLE(stream, offset, max_size, parent, name):
  import C;
  return C.STRUCT(stream, offset, max_size, parent, name, 
      'RGBTRIPPLE', \
      ('Red',               C.BYTE),
      ('Green',             C.BYTE),
      ('Blue',              C.BYTE),
    );

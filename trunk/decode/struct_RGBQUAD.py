
# http://msdn.microsoft.com/en-us/library/aa922960.aspx
def struct_RGBQUAD(stream, offset, max_size, parent, name):
  import C;
  return C.STRUCT(stream, offset, max_size, parent, name, 
      'RGBQUAD', \
      ('Red',               C.BYTE),
      ('Green',             C.BYTE),
      ('Blue',              C.BYTE),
      ('Reserved',          C.BYTE),
    );

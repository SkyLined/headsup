
# http://msdn.microsoft.com/en-us/library/aa922960.aspx
def struct_RGBAQUAD(stream, offset, max_size, parent, name):
  import C;
  return C.STRUCT(stream, offset, max_size, parent, name, 
      'RGBQUAD', \
      ('Red',               C.BYTE),
      ('Green',             C.BYTE),
      ('Blue',              C.BYTE),
      ('Alpha',          C.BYTE),
    );

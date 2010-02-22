
# http://en.wikipedia.org/wiki/BMP_file_format
def struct_BMPHEADER(stream, offset, max_size, parent, name):
  import C;
  result = C.STRUCT(stream, offset, max_size, parent, name, \
      'BMPHEADER', \
      ('MagicNumber',       {C.STRING: 2}),
      ('FileSize',          C.DWORD),
      ('Reserved',          {C.ARRAY: (2, C.WORD)}),
      ('Offset',            C.DWORD),
  );
  if result._MagicNumber.value not in ["BM", "BA", "CI", "CP", "IC", "PT"]:
    result._MagicNumber.warnings.append('invalid magic number');

  return result;
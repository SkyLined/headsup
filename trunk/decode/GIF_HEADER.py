import C;

# http://www.w3.org/Graphics/GIF/spec-gif89a.txt
def GIF_HEADER(stream, offset, max_size, parent, name):
  result = C.STRUCT(stream, offset, max_size, parent, name, \
      'GIF_HEADER', \
      ('Signature',     {C.STRING: 3}),
      ('Version',       {C.STRING: 3}),
  );
  if result._Signature.value != 'GIF':
    result._Signature.warnings.append('expected value to be "GIF"');
  if result._Version.value not in ['87a', '89a']:
    result._Version.warnings.append('expected value to be "87a" or "89a"');

  return result;


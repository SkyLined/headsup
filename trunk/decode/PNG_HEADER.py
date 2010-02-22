import C;

# http://www.w3.org/Graphics/GIF/spec-gif89a.txt
def PNG_HEADER(stream, offset, max_size, parent, name):
  result = C.STRUCT(stream, offset, max_size, parent, name, \
      'PNG_HEADER', \
      ('0x89',            C.BYTE),
      ('Signature',       {C.STRING: 3}),
      ('CR_LF',           {C.STRING: 2}),
      ('ESC',             {C.STRING: 1}),
      ('LF',              {C.STRING: 1}),
  );
  max_size -= result.size;
  if result._Signature.value != 'PNG':
    result._Signature.warnings.append('expected value to be "PNG"');
  if result._CR_LF.value != '\x0D\x0A':
    result._CR_LF.warnings.append('expected value to be "\\x0D\\x0A"');
  if result._ESC.value != '\x1A':
    result._ESC.warnings.append('expected value to be "\\x1A"');
  if result._LF.value not in ['\x0A', '\x0A']:
    result._LF.warnings.append('expected value to be "\\x0A"');

  return result;


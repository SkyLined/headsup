
# http://msdn.microsoft.com/en-us/library/ms997538.aspx
def struct_ICONDIR(stream, offset, max_size, parent, name):
  import C;
  result = C.STRUCT(stream, offset, max_size, parent, name, \
      'ICONDIR', \
      ('Reserved',        C.WORD),   # idReserved
      ('Type',            C.WORD),   # idType (1=.ICO, 2=.CUR)
      ('Count',           C.WORD),   # idCount (number of images)
  );
  if result._Reserved.value != 0:
    result._Reserved.warnings.append('expected value to be 0');
  if result._Type.value not in [1, 2]:
    result._Type.warnings.append('expected value to be 1 or 2');
  else:
    result._Type.notes.append( \
        {1:'ICON', 2:'CURSOR'}[result._Type.value]);
  if result._Count.value == 0:
    result._Count.warnings.append('expected at least one image');
  return result;


# http://msdn.microsoft.com/en-us/library/ms997538.aspx
def struct_ICONDIRENTRY(stream, offset, max_size, parent, name, \
    image_type = None):
  import C;
  if image_type != 2: # Default to icon if unknown
    result = C.STRUCT(stream, offset, max_size, parent, name, \
        'ICONDIRENTRY', \
        ('Width',           C.BYTE),   # bWidth
        ('Height',          C.BYTE),   # bHeight
        ('ColorCount',      C.BYTE),   # bColorCount
        ('Reserved',        C.BYTE),   # bReserved (must be 0)
        ('Planes',          C.WORD),   # wPlanes (color planes)
        ('BitCount',        C.WORD),   # wBitCount (bits per pixel)
        ('BytesInRes',      C.DWORD),  # dwBytesInRes (bitmap resource size)
        ('ImageOffset',     C.DWORD),  # dwImageOffset (bitmap offset in strream)
    );
  else:
    result = C.STRUCT(stream, offset, max_size, parent, name, \
        'ICONDIRENTRY', \
        ('Width',           C.BYTE),   # bWidth
        ('Height',          C.BYTE),   # bHeight
        ('ColorCount',      C.BYTE),   # bColorCount
        ('Reserved',        C.BYTE),   # bReserved (must be 0)
        ('HotspotHCoords',  C.WORD),   # Horizontal hotspot coordinates
        ('HotspotVCoords',  C.WORD),   # Vertical hotspot coordinates
        ('BytesInRes',      C.DWORD),  # dwBytesInRes (bitmap resource size)
        ('ImageOffset',     C.DWORD),  # dwImageOffset (bitmap offset in strream)
    );
  w = result._Width.value;
  h = result._Height.value;
  if w * h > 0xFFFFFFFF:
    result.warnings.append('W*H overflows => 0x%X`%08X|%d' % \
        (w * h >> 32, w * h & 0xFFFFFFFF, w * h & 0xFFFFFFFF));
  elif w * h > 0x01000000:
    result.warnings.append('W*H is large => 0x%X|%d' % \
        (w * h, w * h));
  else:
    result._Width.notes.append('W*H => 0x%X|%d' % (w * h, w * h));
  if result._ColorCount.value == 0:
    result._ColorCount.notes.append('image is truecolor');

  if result._Reserved.value != 0:
    result._Reserved.warnings.append('expected value to be 0');
  if image_type == 1:
    if result._Planes.value not in [0,1]:
      result._Planes.warnings.append('expected value to be 0 or 1');
    result._Planes.notes.append('color depth = %d' % \
        (result._Planes.value * result._BitCount.value));
  elif image_type == 2:
    if result._HotspotHCoords.value > result._Width.value:
      result._HotspotHCoords.warnings.append( \
          'value is larger than width of image');
    if result._HotspotVCoords.value > result._Height.value:
      result._HotspotVCoords.warnings.append( \
          'value is larger than height of image');

  image_offset_from_current = result._ImageOffset.value - \
      (result._ImageOffset.offset + result._ImageOffset.size);
  if image_offset_from_current < 0:
    result._ImageOffset.notes.append('-0x%X|-%d from current' % \
        (-image_offset_from_current, -image_offset_from_current));
  else:
    result._ImageOffset.notes.append('+0x%X|+%d from current' % \
        (image_offset_from_current, image_offset_from_current));

  return result;


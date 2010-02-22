from Structure import Structure;

# http://msdn.microsoft.com/en-us/library/ms997538.aspx
class struct_ICONIMAGE(Structure):
  type_name = 'struct ICONIMAGE'
  def __init__(self, stream, offset, max_size, parent, name):
    import math;
    import C;
    from struct_BITMAPINFO import struct_BITMAPINFO;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._bitmapinfo = self.Member(struct_BITMAPINFO, \
        'bitmapinfo', height_div_2 = True);

    mask_w = self._bitmapinfo._header._Width.value;
    # Height is split in two for XOR and AND mask:
    mask_h = int(math.floor( \
        self._bitmapinfo._header._Height.value / 2.0));
    if self._bitmapinfo._header._Height.value % 2 == 1:
      self._bitmapinfo._header._Height.warnings.append( \
          'expected an even value');
    bits_per_pixel = self._bitmapinfo._header._BitCount.value;
    # Calculate size in bytes of masks:
    xor_mask_pixels_row_bits = bits_per_pixel * mask_w;
    if xor_mask_pixels_row_bits % 32 != 0:
      # Make each row 32 bit alligned.
      xor_mask_pixels_row_bits += 32 - (xor_mask_pixels_row_bits % 32);
    xor_mask_pixels_row_bytes = int(math.ceil(xor_mask_pixels_row_bits / 8.0));
    xor_mask_pixels_bytes = xor_mask_pixels_row_bytes * mask_h;

    and_mask_pixels_row_bits = mask_w;
    if mask_w % 32 != 0:
      # Make each row 32 bit alligned.
      and_mask_pixels_row_bits += 32 - (mask_w % 32);
    and_mask_pixels_row_bytes = int(math.ceil(and_mask_pixels_row_bits / 8.0));
    and_mask_pixels_bytes = and_mask_pixels_row_bytes * mask_h; # mask=1bpp;

    if xor_mask_pixels_bytes >= 0 and and_mask_pixels_bytes >= 0:
      image_size = self._bitmapinfo._header._SizeImage.value;
      off_by = image_size - xor_mask_pixels_bytes - and_mask_pixels_bytes;
      if image_size == 0 and off_by:
        self._bitmapinfo._header._SizeImage.warnings.append( \
            'expected value to be 0x%X|%d bytes' % (-off_by, -off_by));
      elif off_by > 0:
        self._bitmapinfo._header._SizeImage.warnings.append( \
            'icon masks use 0x%X|%d bytes less than this value' % \
            (off_by, off_by));
      elif off_by < 0:
        self._bitmapinfo._header._SizeImage.warnings.append( \
            'icon masks use 0x%X|%d bytes more than this value' % \
            (-off_by, -off_by));

    if xor_mask_pixels_bytes >= 0:
      self._xor_mask = self.Member(C.STRING, 'xor_mask', xor_mask_pixels_bytes);
    else:
      self.warnings.append('cannot show XOR mask because it is reported to ' \
          'have a negative size');
      self._xor_mask = None;

    if and_mask_pixels_bytes >= 0:
      self._and_mask = self.Member(C.STRING, 'and_mask', and_mask_pixels_bytes);
    else:
      self.warnings.append('cannot show AND mask because it is reported to ' \
          'have a negative size');
      self._and_mask = None;

from Structure import Structure;

class PNG_sRGB(Structure):
  type_name = 'PNG_sRGB';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._intent = self.Member(C.BYTE, 'intent');
    
    if self._intent.value == 0:
      self._intent.notes.append('perceptual');
    elif self._intent.value == 1:
      self._intent.notes.append('relative colorimetric');
    elif self._intent.value == 2:
      self._intent.notes.append('saturation');
    elif self._intent.value == 3:
      self._intent.notes.append('absolute colorimetric');
    else:
      self._intent.warnings.append('expected value to be 0, 1, 2 or 3');

    self.Unused();

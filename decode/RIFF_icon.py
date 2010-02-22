from Structure import Structure;

class RIFF_icon(Structure):
  type_name = 'RIFF_icon'
  def __init__(self, stream, offset, max_size, parent, name):
    from ICON import ICON;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._icon = self.Member(ICON, 'icon_data');
    self.Unused();

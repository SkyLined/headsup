# Copyright 2010 Google Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math;
from Structure import Structure;

class RIFF_WAVE_DISP(Structure):
  type_name = 'RIFF_WAVE_DISP'
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    from BITMAP import BITMAP;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._Type = self.Member(C.DWORD, 'Type');

    CLIPBOARD_FORMATS = {
        0x0001: ('TEXT',                            None),
        0x0002: ('BITMAP',                          None),
        0x0003: ('METAFILEPICT',                    None),
        0x0004: ('SYLK',                            'Symbolic link'),
        0x0005: ('DIF',                             'Data Interchange Format'),
        0x0006: ('TIFF',                            None),
        0x0007: ('OEMTEXT',                         None),
        0x0008: ('DIB',                             None),
        0x0009: ('PALETTE',                         None),
        0x000A: ('PENDATA',                         None),
        0x000B: ('RIFF(audio)',                     None),
        0x000C: ('WAVE',                            None),
        0x000D: ('UNICODETEXT',                     None),
        0x000E: ('ENHMETAFILE',                     None),
        0x000F: ('HDROP',                           'list of file handles'),
        0x0010: ('LOCALE',                          None),
        0x0011: ('DIBV5',                           'struct BITMAPV5HEADER'),
        0x0080: ('OWNERDISPLAY',                    None),
        0x0081: ('DSPTEXT',                         'private'),
        0x0082: ('DSPBITMAP',                       'private'),
        0x0083: ('DSPMETAFILEPICT',                 'private'),
        0x008E: ('DSPENHMETAFILE',                  'private'),
        0xBF00: ('Link',                            None),
    };
    t = self._Type.value;
    if t in CLIPBOARD_FORMATS:
      format, details = CLIPBOARD_FORMATS[t];
      self.format_details = 'DISP(%s)' % format;
      if details != None:
        self._Type.notes.append('%s(%s)' % (format, details));
      else:
        self._Type.notes.append(format);
    elif t >= 0x200 and t <= 0x2FF:
      t &= 0xFF;
      self.format_details = 'DISP(private %d|0x%02X)' % (t, t);
      self._Type.notes.append('private format %d|%08X' % (t, t));
    elif t >= 0x300 and t <= 0x3FF:
      t &= 0xFF;
      self.format_details = 'DISP(private GDI %d|0x%02X)' % (t, t);
      self._Type.notes.append('private GDI object format %d|%08X' % (t, t));
    else:
      self.format_details = 'DISP(unknown %d|0x%08X)' % (t, t);
      self._Type.warnings.append('unknown type');
    if t == 8:
      self._bitmapinfo = self.Member(BITMAP, 'bitmapinfo');
    else:
      self._data = self.Member(C.STRING, 'data', self.current_max_size);

    self.Unused();

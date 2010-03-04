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

from Structure import Structure;

# http://www.w3.org/Graphics/GIF/spec-gif89a.txt
class GIF_EXTENSION(Structure):
  type_name = 'EXTENSION';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    from GIF_BLOCK import GIF_BLOCK;
    from GIF_EXTENSION_APPLICATION import GIF_EXTENSION_APPLICATION;
    from GIF_EXTENSION_COMMENT import GIF_EXTENSION_COMMENT;
    from GIF_EXTENSION_GRAPHICS_CONTROL import GIF_EXTENSION_GRAPHICS_CONTROL;
    from GIF_EXTENSION_PLAIN_TEXT import GIF_EXTENSION_PLAIN_TEXT;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    
    self._label = self.Member(C.BYTE, 'label');
    if self._label.value == 0x01:
      self._label.notes.append('plain text extension');
      self._data = self.Member( \
          GIF_EXTENSION_PLAIN_TEXT, 'plain_text_extension');
    elif self._label.value == 0xF9:
      self._label.notes.append('graphice control extension');
      self._data = self.Member( \
          GIF_EXTENSION_GRAPHICS_CONTROL, 'graphice_control_extension');
    elif self._label.value == 0xFE:
      self._label.notes.append('comment extension');
      self._data = self.Member( \
          GIF_EXTENSION_COMMENT, 'comment_extension');
    elif self._label.value == 0xFF:
      self._label.notes.append('application extension');
      self._data = self.Member( \
          GIF_EXTENSION_APPLICATION, 'application_extension');
    else:
      self._label.warnings.append('unknown extension');
      self._data = self.Member(GIF_BLOCK, 'data');
      self._data.ContainUnused();

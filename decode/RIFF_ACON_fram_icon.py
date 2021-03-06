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

class RIFF_ACON_fram_icon(Structure):
  type_name = 'RIFF_icon'
  def __init__(self, stream, offset, max_size, parent, name):
    from ICON import ICON;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._icon = self.Member(ICON, 'icon_data');

    self.format_details = self._icon.format_details;

    self.Unused();

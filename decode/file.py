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

class __file(Structure):
  def __init__(self, stream, offset, max_size, parent, name, type_name, \
      structure_class):
    self.type_name = type_name;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    self._contents = self.Member(structure_class, 'used');
    if hasattr(self._contents, 'format_details'):
      self.format_details = self._contents.format_details;
    self.Unused();

def ANI(stream, offset, max_size, name):
  from ANI import ANI;
  return __file(stream, offset, max_size, None, name, 'FILE_ANI', ANI);

def BMP(stream, offset, max_size, name):
  from BMP import BMP;
  return __file(stream, offset, max_size, None, name, 'FILE_BMP', BMP);

def GIF(stream, offset, max_size, name):
  from GIF import GIF;
  return __file(stream, offset, max_size, None, name, 'FILE_GIF', GIF);

def ICO(stream, offset, max_size, name):
  from ICON import ICON;
  return __file(stream, offset, max_size, None, name, 'FILE_ICO', ICON);

def LNK(stream, offset, max_size, name):
  from LNK import LNK;
  return __file(stream, offset, max_size, None, name, 'FILE_LNK', LNK);

def PNG(stream, offset, max_size, name):
  from PNG import PNG;
  return __file(stream, offset, max_size, None, name, 'FILE_PNG', PNG);

def WAV(stream, offset, max_size, name):
  from WAV import WAV;
  return __file(stream, offset, max_size, None, name, 'FILE_WAV', WAV);


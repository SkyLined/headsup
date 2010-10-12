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

# http://www.stdlib.com/art6-1-Shortcut-File-Format-lnk.html
KNOWN_DRIVE_TYPES = {
  0: 'DRIVE_UNKNOWN',
  1: 'DRIVE_NO_ROOT_DIR',
  2: 'DRIVE_REMOVABLE',
  3: 'DRIVE_FIXED',
  4: 'DRIVE_REMOTE',
  5: 'DRIVE_CDROM',
  6: 'DRIVE_RAMDISK',
};

class struct_VOLUME_ID(Structure):
  type_name = 'VOLUME_ID';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    
    # UINT VolumeIDSize
    self._VolumeIDSize = self.Member(C.UINT, 'VolumeIDSize');
    if self._VolumeIDSize.value <= 0x10:
      self._VolumeIDSize.warnings.append(
          'Expected value to be larger than 0x10|16');
    # UINT DriveType
    self._DriveType = self.Member(C.UINT, 'DriveType');
    if self._DriveType.value in KNOWN_DRIVE_TYPES:
      self._DriveType.notes.append(KNOWN_DRIVE_TYPES[self._DriveType.value]);
    else:
      self._DriveType.warnings.append('Unknown type value');
    # UINT DriveSerialNumber
    self._DriveSerialNumber = self.Member(C.UINT, 'DriveSerialNumber');
    # UINT VolumeLabelOffset
    self._VolumeLabelOffset = self.Member(C.UINT, 'VolumeLabelOffset');
    data_ascii = True;
    if self._VolumeLabelOffset.value == 0x10:
      self._Data = self.Member(C.STRING, 'Data');
    elif self._VolumeLabelOffset.value == 0x14:
      self._VolumeLabelOffset.notes.append( \
          'Ignored in favor of VolumeLabelOffsetUnicode');
      # UINT VolumeLabelOffsetUnicode
      self._VolumeLabelOffsetUnicode = self.Member(C.UINT, \
          'VolumeLabelOffsetUnicode');
      if self._VolumeLabelOffsetUnicode.value != 0x14:
        self._VolumeLabelOffsetUnicode.warnings.append( \
            'Expected value to be 0x14|20');
      self._Data = self.Member(C.UNICODE_STRING, 'Data');
    else:
      self._VolumeLabelOffset.warnings.append( \
          'Expected value to be 0x10|16 or 0x14|20');
      if self._VolumeIDSize.value - 0x10 > 0:
        self._Data = self.Member(C.ARRAY, 'Data', C.BYTE, \
            self._VolumeIDSize.value - 0x10);
      else:
        self._Data = None;

class struct_COMMON_NETWORK_RELATIVE_LINK(Structure):
  type_name = 'COMMON_NETWORK_RELATIVE_LINK';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    
    # UINT CommonNetworkRelativeLinkSize
    self._CommonNetworkRelativeLinkSize = self.Member(C.UINT, \
        'CommonNetworkRelativeLinkSize');
    if self._CommonNetworkRelativeLinkSize.value < 0x14:
      self._CommonNetworkRelativeLinkSize.warnings.append(
          'Expected value to be larger than or equal to 0x14|20');
    # 32 BITS CommonNetworkRelativeLinkFlags
    self._CommonNetworkRelativeLinkFlags = self.Member(C.BITFIELD, \
      'CommonNetworkRelativeLinkFlags', 
      ('Unused',                                  30),
      ('ValidNetType',                            1),
      ('ValidDevice',                             1)
    );
    # UINT NetNameOffset
    self._NetNameOffset = self.Member(C.UINT, 'NetNameOffset');
    # UINT DeviceNameOffset
    self._DeviceNameOffset = self.Member(C.UINT, 'DeviceNameOffset');
    if self._CommonNetworkRelativeLinkFlags._ValidDevice.value == 0 \
        and self._DeviceNameOffset.value != 0:
      self._DeviceNameOffset.warnings.append('Expected value to be 0');
    # UINT NetworkProviderType
    self._NetworkProviderType = self.Member(C.UINT, 'NetworkProviderType');
    if self._CommonNetworkRelativeLinkFlags._ValidNetType.value == 0 \
        and self._NetworkProviderType.value != 0:
      self._NetworkProviderType.warnings.append('Expected value to be 0');
# This was never finished
#    if self._NetworkProviderType.value > 0:
#      if self._NetworkProviderType.value in KNOWN_NETWORK_PROVIDER_TYPES:
#        self._NetworkProviderType.notes.append( \
#            KNOWN_NETWORK_PROVIDER_TYPES[self._NetworkProviderType.value]);
#      else:
#        self._NetworkProviderType.warnings.append( \
#        

class struct_LINK_INFO(Structure):
  type_name = 'LINK_INFO';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    
    # UINT LinkInfoSize
    self._LinkInfoSize = self.Member(C.UINT, 'LinkInfoSize');
    if self._LinkInfoSize.value == 0:
      self._LinkInfoSize.notes.append('No LinkInfo present');
    else:
      # UINT LinkInfoHeaderSize
      self._LinkInfoHeaderSize = self.Member(C.UINT, 'LinkInfoHeaderSize');
      if self._LinkInfoHeaderSize.value == 0x1C:
        self._LinkInfoHeaderSize.notes.append( \
            'Offsets to optional fields are not specified');
      elif self._LinkInfoHeaderSize.value >= 0x24:
        self._LinkInfoHeaderSize.notes.append( \
            'Offsets to optional fields are specified');
      # 32 BITS LinkInfoFlags
      self._LinkInfoFlags = self.Member(C.BITFIELD, 'LinkInfoFlags', 
        ('Unused',                                  30),
        ('CommonNetworkRelativeLinkAndPathSuffix',  1),
        ('VolumeIDAndLocalBasePath',                1)
      );
      # UINT VolumeIDOffset
      self._VolumeIDOffset = self.Member(C.UINT, 'VolumeIDOffset');
      if self._LinkInfoFlags._VolumeIDAndLocalBasePath.value == 0 \
          and self._VolumeIDOffset.value != 0:
        self._VolumeIDOffset.warnings.append('Expected value to be 0');
      # UINT LocalBasePathOffset
      self._LocalBasePathOffset = self.Member(C.DWORD, 'LocalBasePathOffset');
      if self._LinkInfoFlags._VolumeIDAndLocalBasePath.value == 0 \
          and self._LocalBasePathOffset.value != 0:
        self._LocalBasePathOffset.warnings.append('Expected value to be 0');
      # UINT CommonNetworkRelativeLinkOffset
      self._CommonNetworkRelativeLinkOffset = self.Member(C.UINT, \
          'CommonNetworkRelativeLinkOffset');
      if self._LinkInfoFlags._CommonNetworkRelativeLinkAndPathSuffix.value == 0 \
          and self._CommonNetworkRelativeLinkOffset.value != 0:
        self._CommonNetworkRelativeLinkOffset.warnings.append( \
            'Expected value to be 0');
      # UINT CommonPathSuffixOffset
      self._CommonPathSuffixOffset = self.Member(C.UINT, 'CommonPathSuffixOffset');

      if self._LinkInfoHeaderSize.value >= 0x24:
        # UINT LocalBasePathOffsetUnicode
        self._LocalBasePathOffsetUnicode = self.Member(C.UINT, \
            'LocalBasePathOffsetUnicode');
        # UINT CommonPathSuffixOffsetUnicode
        self._CommonPathSuffixOffsetUnicode = self.Member(C.UINT, \
            'CommonPathSuffixOffsetUnicode');
  
      if self._LinkInfoFlags._VolumeIDAndLocalBasePath.value == 1:
        # struct VOLUME_ID VolumeId
        self._VolumeID = self.Member(struct_VOLUME_ID, 'VolumeID');
        # string LocalBasePath
        self._LocalBasePath = self.Member(C.STRING, 'LocalBasePath');
  
      if self._LinkInfoFlags._CommonNetworkRelativeLinkAndPathSuffix.value == 1:
        # struct COMMON_NETWORK_RELATIVE_LINK
        self._CommonNetworkRelativeLink = self.Member( \
            struct_COMMON_NETWORK_RELATIVE_LINK, 'CommonNetworkRelativeLink');
        # string CommonPathSuffix
        self._CommonPathSuffix = self.Member(C.STRING, 'CommonPathSuffix');
  
      if self._LinkInfoHeaderSize.value >= 0x24:
        # unicode string LocalBasePathUnicode
        self._LocalBasePathUnicode = self.Member(C.UNICODE_STRING, \
            'LocalBasePathUnicode');
        # unicode string CommonPathSuffixUnicode
        self._CommonPathSuffixUnicode = self.Member(C.UNICODE_STRING, \
            'CommonPathSuffixUnicode');
  
        
      if self._LinkInfoHeaderSize.value >= self._LinkInfoSize.value:
        self._LinkInfoHeaderSize.warnings.append( \
            'Expected value to be smaller than value of LinkInfoSize');

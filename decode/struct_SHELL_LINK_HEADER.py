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

import C;
LINK_CLSID = '{00021401-0000-0000-C000-000000000046}';

VALID_SHOW_COMMAND_VALUES = {
  1: 'SW_SHOWNORMAL',
  3: 'SW_SHOWMAXIMIZED',
  7: 'SW_SHOWMINNOACTIVE',
};

VALID_HOTKEY_LOWBYTE_VALUES = {
  0x90: 'NumLock',
  0x91: 'ScrollLock',
};
for i in range(0x30, 0x3A):
  VALID_HOTKEY_LOWBYTE_VALUES[i] = chr(i); # 0 - 9
for i in range(0x41, 0x5B):
  VALID_HOTKEY_LOWBYTE_VALUES[i] = chr(i); # A - Z
for i in range(1, 25):
  VALID_HOTKEY_LOWBYTE_VALUES[i + 0x6F] = 'F%d' % i; # F1 - F24 (!)

# bitflags_LinkFlags
def bitflags_LinkFlags(stream, offset, max_size, parent, name):
  result = C.BITFIELD(stream, offset, max_size, parent, name, \
      ('Reserved',                                5),
      ('KeepLocalIDListForUNCTarget',             1),
      ('PreferEnvironmentPath',                   1),
      ('UnaliasOnSave',                           1),
      ('AllowLinkToLink',                         1),
      ('DisableKnownFolderAlias',                 1),
      ('DisableKnownFolderTracking',              1),
      ('DisableLinkPathTracking',                 1),
      ('EnableTargetMetadata',                    1),
      ('ForceNoLinkTrack',                        1),
      ('RunWithShimLayer',                        1),
      ('Unused2',                                 1),
      ('NoPidlAlis',                              1),
      ('HasExpIcon',                              1),
      ('RunAsUser',                               1),
      ('HasDarwinID',                             1),
      ('Unused1',                                 1),
      ('RunInSeperateProcess',                    1),
      ('HasExpString',                            1),
      ('ForceNoLinkInfo',                         1),
      ('IsUnicode',                               1),
      ('HasIconLocation',                         1),
      ('HasArguments',                            1),
      ('HasWorkingDir',                           1),
      ('HasRelativePath',                         1),
      ('HasName',                                 1),
      ('HasLinkInfo',                             1),
      ('HasLinkTargetIDList',                     1)
  );
  result.dump_simplified = True;
  if result._Unused1.value != 0:
    result._Unused1.warnings.append('Expected value to be 0');
  if result._Unused2.value != 0:
    result._Unused2.warnings.append('Expected value to be 0');
  if result._Reserved.value != 0:
    result._Reserved.warnings.append('Expected value to be 0');
  return result;

# bitflags_FileAttributes
def bitflags_FileAttributes(stream, offset, max_size, parent, name):
  result = C.BITFIELD(stream, offset, max_size, parent, name, \
      ('Unused',                                  17),
      ('FILE_ATTRIBUTE_ENCRYPTED',                1),
      ('FILE_ATTRIBUTE_NOT_CONTENT_INDEXED',      1),
      ('FILE_ATTRIBUTE_OFFLINE',                  1),
      ('FILE_ATTRIBUTE_COMPRESSED',               1),
      ('FILE_ATTRIBUTE_REPARSE_POINT',            1),
      ('FILE_ATTRIBUTE_SPARSE_FILE',              1),
      ('FILE_ATTRIBUTE_TEMPORARY',                1),
      ('FILE_ATTRIBUTE_NORMAL',                   1),
      ('Reserved2',                               1),
      ('FILE_ATTRIBUTE_ARCHIVE',                  1),
      ('FILE_ATTRIBUTE_DIRECTORY',                1),
      ('Reserved1',                               1),
      ('FILE_ATTRIBUTE_SYSTEM',                   1),
      ('FILE_ATTRIBUTE_HIDDEN',                   1),
      ('FILE_ATTRIBUTE_READONLY',                 1)
  );
  result.dump_simplified = True;
  if result._Reserved1.value != 0:
    result._Reserved1.warnings.append('Expected value to be 0');
  if result._Reserved2.value != 0:
    result._Reserved2.warnings.append('Expected value to be 0');
  return result;

# struct_HotKeyFlags
def struct_HotKeyFlags(stream, offset, max_size, parent, name):
  result = C.STRUCT(stream, offset, max_size, parent, name, \
      'HotKeyFlags', \
      ('LowByte',          C.BYTE),
      ('HighByte',         {C.BITFIELD: (
          ('Reserved',             5),
          ('HOTKEYF_ALT',          1),
          ('HOTKEYF_CONTROL',      1),
          ('HOTKEYF_SHIFT',        1),
      )})
  );
  if results._LowByte.value in VALID_HOTKEY_LOWBYTE_VALUES:
    result._LowByte.notes.append( \
        VALID_HOTKEY_LOWBYTE_VALUES[result._LowByte.value]);
  else:
    result._LowByte.warnings.append('Unrecognized value');
  if results._HighByte._Reserved.value > 0:
    results._HighByte._Reserved.warnings.append('Expected value to be 0');
  return result;

# http://download.microsoft.com/download/B/0/B/B0B199DB-41E6-400F-90CD-C350D0C14A53/%5BMS-SHLLINK%5D.pdf
def struct_SHELL_LINK_HEADER(stream, offset, max_size, parent, name):
  import C;
  from struct_GUID import struct_GUID;
  result = C.STRUCT(stream, offset, max_size, parent, name, \
      'LNK_HEADER', \
      ('HeaderSize',          C.DWORD),
      ('LinkCLSID',           struct_GUID),
      ('LinkFlags',           bitflags_LinkFlags),
      ('FileAttributes',      bitflags_FileAttributes),
      ('CreationTime',        C.QWORD),
      ('AccessTime',          C.QWORD),
      ('WriteTime',           C.QWORD),
      ('FileSize',            C.UINT),
      ('IconIndex',           C.INT),
      ('ShowCommand',         C.UINT),
      ('HotKey',              C.WORD),
      ('Reserved1',           C.WORD),
      ('Reserved2',           C.DWORD),
      ('Reserved3',           C.DWORD)
  );
  if result._HeaderSize.value != 0x4C:
    result._HeaderSize.warnings.append(
        'expected value to be 0x4C');
  if result._LinkCLSID.string_value != LINK_CLSID:
    result._LinkCLSID.warnings.append('expected value to be "%s"' % LINK_CLSID);

  if result._ShowCommand.value in VALID_SHOW_COMMAND_VALUES:
    result._ShowCommand.notes.append( \
        VALID_SHOW_COMMAND_VALUES[result._ShowCommand.value]);
  else:
    valid_values = VALID_SHOW_COMMAND_VALUES.keys()
    valid_values = '%s or %s' % \
        (', '.join(valid_values[:-1]), valid_values[-1]);
    result._ShowCommand.warnings.append( \
        'Expected value to be %s' % valid_values);

  if result._Reserved1.value != 0:
    result._Reserved1.warnings.append('Expected value to be 0');
  if result._Reserved2.value != 0:
    result._Reserved2.warnings.append('Expected value to be 0');
  return result;


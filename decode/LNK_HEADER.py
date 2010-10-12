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
LINK_GUID = '{00021401-0000-0000-C000-000000000046}';

# http://www.stdlib.com/art6-Shortcut-File-Format-lnk.html
def LNK_HEADER(stream, offset, max_size, parent, name):
  from struct_GUID import struct_GUID;
  result = C.STRUCT(stream, offset, max_size, parent, name, \
      'LNK_HEADER', \
      ('Signature',           C.DWORD),
      ('GUID',                struct_GUID),
      ('ShortcutFlags',       {C.BITFIELD: (
          ('Unused',                    25),
          ('HasCustomIcon',             1),
          ('HasCommandLineArgs',        1),
          ('HasWorkingDir',             1),
          ('HasRelativePath',           1),
          ('HasDescription',            1),
          ('TargetIsFileOrDir',         1),
          ('ShellItemIdListPresent',    1),
      )}),
      ('TargetFileFlags',     {C.BITFIELD: (
          ('Unused',                    19),
          ('TargetIsOffline',           1),
          ('TargetIsCompressed',        1),
          ('TargetHasReparsePointData', 1),
          ('TargetIsSparseFile',        1),
          ('TargetIsTemporary',         1),
          ('TargetIsNormal',            1),
          ('TargetIsEncrypted',         1),
          ('TargetIsModified',          1),
          ('TargetIsDir',               1),
          ('TargetIsVolumeLabel',       1),
          ('TargetIsSystemFile',        1),
          ('TargetIsHidden',            1),
          ('TargetIsReadOnly',          1),
      )}),
      ('CreationTime',        C.QWORD),
      ('LastAccessTime',      C.QWORD),
      ('ModificationTime',    C.QWORD),
      ('FileLength',          C.DWORD),
      ('IconNumber',          C.DWORD),
      ('ShowWindow',          C.DWORD),
      ('HotKey',              C.DWORD),
      ('Reserved1',           C.DWORD),
      ('Reserved2',           C.DWORD),
  );
  if result._Signature.value != 0x4C:
    result._Signature.warnings.append(
        'expected value to be 0x0000004C ("L\\0\\0\\0")');
  if result._GUID.string_value != LINK_GUID:
    result._GUID.warnings.append('expected value to be "%s"' % LINK_GUID);
  
  result._ShortcutFlags.dump_simplified = True;
  result._TargetFileFlags.dump_simplified = True;

  if result._Reserved1.value != 0:
    result._Reserved1.warnings.append('Expected value to be 0');
  if result._Reserved2.value != 0:
    result._Reserved2.warnings.append('Expected value to be 0');
  return result;


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

import os, re, sys;
import decode;

HANDLED_FILETYPES = [
    # Could use a separate file_ANIMATED_CURSOR and some more checks:
    (['ani'], r'RIFF[\s\S]{4}ACON',       decode.file.ANI, 'animated_cursor'), 
    (['bmp'], r'BM',                      decode.file.BMP, 'bitmap'),
    (['gif'], r'GIF',                     decode.file.GIF, 'gif_image'),
    (['ico'], None,                       decode.file.ICO, 'icon'),
    (['png'], r'\\x89PNG\\r\\n\\x1A\\n',  decode.file.PNG, 'png_image'),
    (['wav'], r'RIFF[\s\S]{4}WAVE',       decode.file.WAV, 'waveform'),
];

def Help():
  print 'Usage:';
  print '    headsup [file name] [switch]';
  print 'Switches:';
  print '    -h, --help       - Output this information and quit';
  print '    -q, --quiet      - Do not dump file contents information';
  print '    -f, --format     - Show the files format description';
  print '    -r, --rename     - Rename the file according to the format ' \
                                                                  'description';

def MakeValidFileName(string):
  file_name = '';
  for char in string:
    if char.upper() in ' !()-.,;#0123456789=@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]_{}~':
      file_name += char;
    else:
      file_name += '.';
  return file_name;

if __name__ == "__main__":
  file_name = None;
  rename_switch = False;
  format_switch = False;
  quiet_switch = False;
  for arg in sys.argv[1:]:
    if not arg[0] in ['-', '/']:
      if file_name is None:
        file_name = arg;
      else:
        print 'Found two file names in arguments: %s and %s' % \
            (repr(file_name), repr(arg));
        exit(-1);
    else:
      if arg.lower() in ['-h', '--help', '/h', '-?', '/?']:
        Help();
        exit();
      elif arg.lower() in ['-r', '--rename']:
        rename_switch = True;
      elif arg.lower() in ['-q', '--quiet']:
        quiet_switch = True;
      elif arg.lower() in ['-f', '--format']:
        format_switch = True;
  if file_name is None:
    print 'Expected a file name in the arguments';
    Help();
    exit(-1);
  try:
    input_file = open(file_name, 'rb');
    try:
      stream = input_file.read();
    finally:
      input_file.close();
  except Exception, e:
    print 'Cannot open file "%s":' % sys.argv[1];
    print '    %s' % repr(e);
    exit(-1);

  ext_file_type_handling = None;
  sniff_file_type_handling = None;
  for exts, sniff, extractor, name in HANDLED_FILETYPES:
    for ext in exts:
      if file_name.lower().endswith('.' + ext):
        ext_file_type_handling = ext, extractor, name;
        break;
    if sniff is not None and re.match('^' + sniff, stream):
      sniff_file_type_handling = exts[0], extractor, name;
  if sniff_file_type_handling:
    ext, extractor, name = sniff_file_type_handling;
  elif ext_file_type_handling:
    ext, extractor, name = ext_file_type_handling;
  else:
    print 'Unknown file extension and type cannot be sniffed from data.';
    exit(-1);

  contents = extractor(stream, 0, len(stream), file_name);
  unused_size = len(stream) - contents.size;
  if unused_size > 0:
    unused = extract.C.STRING(stream, contents.size, unused_size, \
        'unused', unused_size);
  else:
    unused = None;

  if not quiet_switch:
    contents.Dump();
    if unused:
      unused.Dump();
  if format_switch:
    if hasattr(contents, 'format_details'):
      print 'Format: %s' % contents.format_details;

  if rename_switch:
    if not hasattr(contents, 'format_details'):
      print 'Cannot rename file; format_details not available for this type';
      exit(-1);
    new_file_name = MakeValidFileName('%s.%s' % (contents.format_details, ext));
    counter = 1;
    while os.path.exists(new_file_name) and file_name != new_file_name:
      counter += 1;
      new_file_name = MakeValidFileName('%s #%d.%s' % \
          (contents.format_details, counter, ext));
    if file_name == new_file_name:
      print 'Name already %s.' % repr(new_file_name);
    else:
      print 'Renaming to %s.' % repr(new_file_name);
      os.rename(file_name, new_file_name);
    
import sys;
import decode;

if __name__ == "__main__":
  assert len(sys.argv) == 2, 'Syntax: %s "input file name"' % sys.argv[0];
  file_name = sys.argv[1];
  try:
    input_file = open(file_name, 'rb');
    try:
      stream = input_file.read();
    finally:
      input_file.close();
  except:
    print 'Cannot open file "%s":' % sys.argv[1];
    raise;
  handled_filetypes = {
    # Could use a separate file_ANIMATED_CURSOR and some more checks:
    '.ani': (decode.file.ANI, 'animated_cursor'), 
    '.bmp': (decode.file.BMP, 'bitmap'),
    '.gif': (decode.file.GIF, 'graphics_interchange_format'),
    '.ico': (decode.file.ICO, 'icon'),
    '.png': (decode.file.PNG, 'portable_network_graphics'),
    '.wav': (decode.file.WAV, 'waveform'),
  }
  for (ext, (extractor, name)) in handled_filetypes.items():
    if file_name.lower().endswith(ext):
      contents = extractor(stream, 0, len(stream), file_name);
      unused_size = len(stream) - contents.size;
      if unused_size > 0:
        unused = extract.C.STRING(stream, contents.size, unused_size, \
            'unused', unused_size);
      else:
        unused = None;
      contents.Dump();
      if unused:
        unused.Dump();
      break;
  else:
    print 'Unknown filetype';
    
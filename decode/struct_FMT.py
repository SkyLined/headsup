# http://www.gdgsoft.com/anituner/help/aniformat.htm
def struct_FMT(stream, offset, max_size, parent, name):
  import C;
  result = C.STRUCT(stream, offset, max_size, parent, name, \
      'FMT', \
      ('AudioFormat',   C.WORD),
      ('NumChannels',   C.WORD),
      ('SampleRate',    C.DWORD),
      ('ByteRate',      C.DWORD),
      ('BlockAlign',    C.WORD),
      ('BitsPerSample', C.WORD),
  );
  max_size -= result.size;
  if result._AudioFormat.value == 1:
    result._AudioFormat.notes.append('format = PCM');
  else:
    result._AudioFormat.notes.append('format = unknown');

  num_channels = result._NumChannels.value;
  bits_per_sample = result._BitsPerSample.value;

  if num_channels == 0:
    result._NumChannels.warnings.append('expected at least 1 channel');
  if bits_per_sample == 0:
    result._NumChannels.warnings.append('expected at least 1 bit per sample');

  bit_rate = result._SampleRate.value * num_channels * bits_per_sample;
  if result._ByteRate.value * 8 != bit_rate:
    result._ByteRate.warnings.append( \
        'expected value to be %f' % (BitRate / 8.0));

  expected_block_align = num_channels * bits_per_sample / 8.0;
  if result._BlockAlign.value != expected_block_align:
    result._BlockAlign.warnings.append( \
        'expected value to be %f' % expected_block_align);

  return result;


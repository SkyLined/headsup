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


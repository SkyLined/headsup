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

def RIFF_WAVE_Checks(WAVE_block):
  fmt_chunk = None;
  fact_chunk = None;
  data_chunk = None;
#  format_description = 'WAVE - Unknown format';
  if 'fmt ' not in WAVE_block._named_chunks:
    WAVE_block.warnings.append('expected one "fmt " block, found none');
  else:
    fmt_chunk = WAVE_block._named_chunks['fmt '][0];
#    format_description = 'WAVE - %s' % fmt_chunk._data.format_description;
  if 'fact' not in WAVE_block._named_chunks:
    if not fmt_chunk._data.is_PCM:
      WAVE_block.warnings.append('expected one "fact" block, found none');
  else:
    fact_chunk = WAVE_block._named_chunks['fact'][0];
  if 'data' not in WAVE_block._named_chunks:
    WAVE_block.warnings.append('expected one "data" block, found none');
  else:
    data_chunk = WAVE_block._named_chunks['data'][0];

#  d_chunks = set();
#  d_blocks = set();
#  for chunk_name in WAVE_block._named_chunks.keys():
#    if chunk_name == 'LIST':
#      for chunk in WAVE_block._named_chunks[chunk_name]:
#        for block_name in chunk._named_blocks.keys():
#          d_blocks.add(block_name.strip());
#    elif chunk_name not in ['fmt ', 'data']:
#      d_chunks.add(chunk_name.strip());
#  if d_chunks:
#    format_description += ' + chunks=' + ','.join(d_chunks);
#  if d_blocks:
#    format_description += ' + blocks=' + ','.join(d_blocks);

  for name, chunks in WAVE_block._named_chunks.items():
    if name == 'fmt ':
      for chunk in chunks:
        if len(chunks) > 1:
          chunk._name.warnings.append( \
              'expected only one "fmt " chunk, found %d' % len(chunks));
        RIFF_WAVE_fmt_Checks(WAVE_block, chunk);
    if name == 'fact':
      for chunk in chunks:
        if len(chunks) > 1:
          chunk._name.warnings.append( \
              'expected only one "fact" chunk, found %d' % len(chunks));
        RIFF_WAVE_fact_Checks(WAVE_block, chunk);
    if name == 'cue ':
      for chunk in chunks:
        if len(chunks) > 1:
          chunk._name.warnings.append( \
              'expected only one "cue " chunk, found %d' % len(chunks));
        RIFF_WAVE_cue_Checks(WAVE_block, chunk);
    if name == 'PEAK':
      for chunk in chunks:
        RIFF_WAVE_PEAK_Checks(WAVE_block, chunk);
    if name == 'data':
      for chunk in chunks:
        if len(chunks) > 1:
          chunk._name.warnings.append( \
              'expected only one "data" chunk, found %d' % len(chunks));
        RIFF_WAVE_data_Checks(WAVE_block, chunk);
#  WAVE_block.notes.append(format_description);

def RIFF_WAVE_fmt_Checks(WAVE_block, fmt_chunk):
  pass;

def RIFF_WAVE_fact_Checks(WAVE_block, fact_chunk):
  pass;

def RIFF_WAVE_cue_Checks(WAVE_block, cue_chunk):
  pass;

def RIFF_WAVE_PEAK_Checks(WAVE_block, PEAK_chunk):
  # Check if peak positions are valid?
  pass;

def RIFF_WAVE_data_Checks(WAVE_block, data_chunk):
  pass;

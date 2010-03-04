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

def RIFF_ACON_Checks(acon_block):
  if 'anih' not in acon_block._named_chunks:
    acon_block.warnings.append('expected one "anih" block, found none');
  for name, chunks in acon_block._named_chunks.items():
    if name == 'anih':
      for chunk in chunks:
        if len(chunks) > 1:
          chunk._name.warnings.append( \
              'expected only one "anih" chunk, found %d' % len(chunks));
        RIFF_anih_Checks(acon_block, chunk);
    if name == 'rate':
      for chunk in chunks:
        if len(chunks) > 1:
          chunk._name.warnings.append( \
              'expected only one "rate" block, found %d' % len(chunks));
        RIFF_rate_Checks(acon_block, chunk);
    if name == 'LIST':
      for chunk in chunks:
        if len(chunk._named_blocks) != 1 \
            or chunk._named_blocks.keys()[0] not in ['fram', 'INFO']:
          chunk.warnings.append(
              'expected only one "fram" or "INFO" blocks in LIST chunk');
        if 'fram' in chunk._named_blocks:
          RIFF_LIST_fram_Checks(acon_block, chunk);
        if 'INFO' in chunk._named_blocks:
          RIFF_LIST_INFO_Checks(acon_block, chunk);

def RIFF_anih_Checks(acon_block, anih_chunk):
  pass;

def RIFF_rate_Checks(acon_block, rate_chunk):
  anih_steps = GetAnihSteps(acon_block);
  if anih_steps is None:
    if len(rate_chunk._data._rates._items) == 0:
      rate_chunk._data.warnings.append( \
          'expected at least one rate entry, found none');
  elif len(rate_chunk._data._rates._items) != anih_steps:
    rate_chunk._data.warnings.append( \
        'expected %d rate entries, found %d' % \
        (anih_steps, len(rate_chunk._data._rates._items)));

def RIFF_LIST_fram_Checks(acon_block, fram_list_chunk):
  for name, blocks in fram_list_chunk._named_blocks.items():
    if name == 'fram':
      for block in blocks:
        if len(blocks) > 1:
          block._name.warnings.append( \
              'expected only one "fram" block, found %d' % len(blocks));
        RIFF_fram_Checks(acon_block, block);
    else:
      for block in blocks:
        block._name.warnings.append('expected value to be "fram"');

def RIFF_fram_Checks(acon_block, fram_block):
  anih_steps = GetAnihSteps(acon_block);
  if 'icon' not in fram_block._named_chunks:
    if anih_steps is not None:
      fram_block.warnings.append( \
          'expected %d "ICON" blocks, found none' % anih_steps);
    else:
      fram_block.warnings.append( \
          'expected at least one "ICON" block, found none');
  for name, chunks in fram_block._named_chunks.items():
    if name == 'icon':
      if anih_steps is not None and len(chunks) != anih_steps:
        fram_block.warnings.append( \
            'expected %d "ICON" blocks, found %d' % (anih_steps, len(blocks)));
    else:
      for chunk in chunks:
        chunk._name.warnings.append('expected value to be "ICON"');

def RIFF_LIST_INFO_Checks(acon_block, info_list_chunk):
  for name, blocks in info_list_chunk._named_blocks.items():
    if name == 'INFO':
      for block in blocks:
        RIFF_INFO_Checks(acon_block, block);
    else:
      for block in blocks:
        block._name.warnings.append('expected value to be "INFO"');

def RIFF_INFO_Checks(acon_block, INFO_block):
  for name, chunks in INFO_block._named_chunks.items():
    if name not in ['INAM', 'IART']:
      for chunk in chunks:
        chunk._name.warnings.append('expected value to be "INAM" or "IART"');

def GetAnihSteps(acon_block):
  if 'anih' not in acon_block._named_chunks:
    return None;
  steps_max = None;
  for anih_chunk in acon_block._named_chunks['anih']:
    if steps_max is None or steps_max < anih_chunk._data._anih._Steps.value:
      steps_max = anih_chunk._data._anih._Steps.value;
  return steps_max;
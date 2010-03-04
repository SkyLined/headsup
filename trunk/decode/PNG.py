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

from Structure import Structure

# http://www.w3.org/TR/PNG/
class PNG(Structure):
  type_name = 'PNG';
  def __init__(self, stream, offset, max_size, parent, name):
    import math;
    import C;
    from PNG_HEADER import PNG_HEADER;
    from PNG_CHUNK import PNG_CHUNK, VALID_CHUNK_TYPES, CHUNK_ORDER_BEFORE, \
                          CHUNK_MIN_MAX_COUNT;
    from PNG_IHDR import PNG_IHDR;
    from PNG_PLTE import PNG_PLTE;
    from PNG_IDAT import PNG_IDAT;
    from PNG_tRNS import PNG_tRNS;
    from PNG_IEND import PNG_IEND;
    from PNG_sRGB import PNG_sRGB;
    from PNG_gAMA import PNG_gAMA;
    from PNG_cHRM import PNG_cHRM;
    from PNG_pHYs import PNG_pHYs;
    from PNG_tEXt import PNG_tEXt;
    from PNG_sBIT import PNG_sBIT;
    from PNG_bKGD import PNG_bKGD;
    from PNG_hIST import PNG_hIST;
    from PNG_tIME import PNG_tIME;
    from PNG_sPLT import PNG_sPLT;
    from PNG_iCCP import PNG_iCCP;
    from PNG_zTXt import PNG_zTXt;
    from PNG_iTXt import PNG_iTXt;
    from ZLIB_BLOCK import ZLIB_BLOCK;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._header = self.Member(PNG_HEADER, 'header');

    self._chunks = [];
    self._named_chunks = {};
    
    while self.DataAvailable():
      chunk = self.Member(PNG_CHUNK, 'chunk_%d' % (len(self._chunks) + 1));
      chunk._chunk_index = len(self._chunks);
      self._chunks.append(chunk);
      if chunk._name not in self._named_chunks:
        self._named_chunks[chunk._name] = [chunk];
      else:
        self._named_chunks[chunk._name].append(chunk);

    # Check order (A must come after B):
    for upper_index in range(0, len(self._chunks) - 1):
      upper_chunk = self._chunks[upper_index];
      chunks_that_must_come_before_upper = \
          CHUNK_ORDER_BEFORE[upper_chunk._name];
      incorrectly_ordered_chunks = set();
      for lower_index in range(upper_index + 1, len(self._chunks)):
        lower_chunk = self._chunks[lower_index];
        if lower_chunk._name in chunks_that_must_come_before_upper:
          incorrectly_ordered_chunks.add(lower_chunk._name);
      incorrectly_ordered_chunks = list(incorrectly_ordered_chunks);
      if len(incorrectly_ordered_chunks) == 1:
        upper_chunk.warnings.append( \
            'expected chunk to come after "%s" chunk' % \
            incorrectly_ordered_chunks);
      elif incorrectly_ordered_chunks:
        and_chunk = incorrectly_ordered_chunks.pop();
        upper_chunk.warnings.append( \
            'expected chunk to come after "%s" and "%s" chunks' % \
            '", "'.join(incorrectly_ordered_chunks), and_chunk);
    # Check order (A must come before B):
    for lower_index in range(1, len(self._chunks)):
      lower_chunk = self._chunks[lower_index];
      incorrectly_ordered_chunks = set();
      for upper_index in range(0, lower_index - 1):
        upper_chunk = self._chunks[upper_index];
        chunks_that_must_come_before_upper = \
            CHUNK_ORDER_BEFORE[upper_chunk._name];
        if lower_chunk._name in chunks_that_must_come_before_upper:
          incorrectly_ordered_chunks.add(lower_chunk._name);
      incorrectly_ordered_chunks = list(incorrectly_ordered_chunks);
      if len(incorrectly_ordered_chunks) == 1:
        lower_chunk.warnings.append( \
            'expected chunk to come before "%s" chunk' % \
            incorrectly_ordered_chunks);
      elif incorrectly_ordered_chunks:
        and_chunk = incorrectly_ordered_chunks.pop();
        lower_chunk.warnings.append( \
            'expected chunk to come before "%s" and "%s" chunks' % \
            '", "'.join(incorrectly_ordered_chunks), and_chunk);

    # Check the number of occurances of each chunk type:
    for chunk_type, (min, max) in CHUNK_MIN_MAX_COUNT.items():
      if chunk_type not in self._named_chunks:
        count = 0;
      else:
        count = self._named_chunks[chunk_type];
      if min > count:
        if min == 1:
          self.warnings.append( \
              'expected at least one "%s" chunk' % chunk_type);
        else:
          self.warnings.append( \
              'expected at least %d "%s" chunks' % (min, chunk_type));
        if max is not None and count > max:
          self.warnings.append( \
              'expected at most %d "%s" chunks' % (max, chunk_type));

    self._IHDR = None;
    self._IHDRs = [];
    if 'IHDR' in self._named_chunks:
      for chunk in self._named_chunks['IHDR']:
        self._IHDR = chunk.ContainMember(PNG_IHDR, chunk.name + '_data');
        self._IHDRs.append(self._IHDR);
    if self._IHDR:
      w = self._IHDR._data._Width.value;
      h = self._IHDR._data._Height.value;
      color_type = self._IHDR._data._ColorType.value;
      bit_depth = self._IHDR._data._BitDepth.value;
      interlaced = self._IHDR._data._Interlace.value;
      filter = self._IHDR._data._Filter.value;
      if color_type == 3: # indexed-color
        sample_depth = 8;
      else:
        sample_depth = bit_depth;
    else:
      w = None;
      h = None;
      color_type = None;
      bit_depth = None;
      interlaced = None;
      sample_depth = None;
      filter = None;

    self._PLTE = None;
    self._PLTEs = [];
    if 'PLTE' in self._named_chunks:
      for chunk in self._named_chunks['PLTE']:
        self._PLTE = chunk.ContainMember(PNG_PLTE, chunk.name + '_data');
        self._PLTEs.append(self._PLTE);
    if self._PLTE:
      palette_entries = self._PLTE._number_of_rgb_tripples;
    else:
      palette_entries = None;

    self._IDATs = [];
    self.ContainStream('', 0);
    if 'IDAT' in self._named_chunks:
      for chunk in self._named_chunks['IDAT']:
        IDAT = chunk.ContainMember(PNG_IDAT, chunk.name + '_data');
        self._IDATs.append(IDAT);
        self.ContainStream(IDAT._compressed_pixel_data.GetUsedStream());

    self._compressed_image_data = self.ContainMember( \
        ZLIB_BLOCK, 'compressed_image_data');
    if self._IHDR:
      if color_type in [0, 3]:
        samples = 1; # greyscale or index
      elif color_type == 2:
        samples = 3; # RGB tripple
      elif color_type == 4:
        samples = 2; # greyscale + alpha
      elif color_type == 6:
        samples = 4; # RGBA quad
      bytes_per_pixel = samples * bit_depth / 8.0;
      # scanlines are byte aligned:
      image_data_bytes = 0;
      filters = {0:'None', 1:'Sub', 2:'Up', 3: 'Average', 4: 'Paeth'};
      if interlaced == 1:
        # http://www.w3.org/TR/PNG/#8Interlace
        self._image_data = [];
        for (left, pixel_width, top, pixel_height) in [ 
            (0, 8, 0, 8), (4, 8, 0, 8), (0, 4, 4, 8), (2, 4, 0, 4), \
            (0, 2, 2, 4), (1, 2, 0, 2), (0, 1, 1, 2)]:
          pixels_per_scanline = int(math.ceil(1.0 * (w-left) / pixel_width));
          scanlines_per_image = int(math.ceil(1.0 * (h-top) / pixel_height));

          bytes_per_scanline = \
              int(math.ceil(bytes_per_pixel * pixels_per_scanline));

          bytes_per_image = bytes_per_scanline * scanlines_per_image;

          if bytes_per_image != 0 and filter == 0:
            # One filter byte per scanline:
            bytes_per_image += scanlines_per_image;

          image_data_bytes += bytes_per_image;
          self._image_data.append(
              self._compressed_image_data.ContainMember( \
              C.STRING, 'decompressed_image_%d_data' % \
              (len(self._image_data) + 1), bytes_per_image));
      else:
        bytes_per_scanline = int(math.ceil(w * bytes_per_pixel));
        bytes_per_image = bytes_per_scanline * h;
        if bytes_per_image != 0 and filter == 0:
          # One filter byte per scanline:
          bytes_per_image += h;
        image_data_bytes += bytes_per_image;
        self._image_data = self._compressed_image_data.ContainMember( \
            C.STRING, 'decompressed_image_data', bytes_per_image);
      self._compressed_image_data.ContainUnused();

    self._IEND = None;
    self._IENDs = [];
    if 'IEND' in self._named_chunks:
      for chunk in self._named_chunks['IEND']:
        self._IEND = chunk.ContainMember(PNG_IEND, chunk.name + '_data');
        if chunk._length.value != 0:
          chunk._length.warnings.append('expected value to be 0');
        self._IENDs.append(self._IEND);

    self._tRNSs = [];
    if 'tRNS' in self._named_chunks:
      for chunk in self._named_chunks['tRNS']:
        tRNS = chunk.ContainMember(PNG_tRNS, chunk.name + '_data', \
            color_type, bit_depth, palette_entries);
        self._tRNSs.append(tRNS);

    self._cHRM = None;
    self._cHRMs = [];
    if 'cHRM' in self._named_chunks:
      for chunk in self._named_chunks['cHRM']:
        self._cHRM = chunk.ContainMember(PNG_cHRM, chunk.name + '_data');
        self._cHRMs.append(self._cHRM);

    self._gAMA = None;
    self._gAMAs = [];
    if 'gAMA' in self._named_chunks:
      for chunk in self._named_chunks['gAMA']:
        self._gAMA = chunk.ContainMember(PNG_gAMA, chunk.name + '_data');
        self._gAMAs.append(self._gAMA);


    self._iCCP = None;
    self._iCCPs = [];
    if 'iCCP' in self._named_chunks:
      for chunk in self._named_chunks['iCCP']:
        self._iCCP = chunk.ContainMember(PNG_iCCP, chunk.name + '_data');
        self._iCCPs.append(self._iCCP);
        if 'sRGB' in self._named_chunks:
          self._iCCP.warnings.append( \
              'expected either an "iCCP" or an "sRGB" block, not both');

    self._sBIT = None;
    self._sBITs = [];
    if 'sBIT' in self._named_chunks:
      for chunk in self._named_chunks['sBIT']:
        self._sBIT = chunk.ContainMember(PNG_sBIT, chunk.name + '_data', \
            color_type, sample_depth);
        self._sBITs.append(self._sBIT);

    self._sRGB = None;
    self._sRGBs = [];
    if 'sRGB' in self._named_chunks:
      for chunk in self._named_chunks['sRGB']:
        self._sRGB = chunk.ContainMember(PNG_sRGB, chunk.name + '_data');
        self._sRGBs.append(self._sRGB);
        if 'iCCP' in self._named_chunks:
          self._sRGB.warnings.append( \
              'expected either an "iCCP" or an "sRGB" block, not both');

    self._tEXt = None;
    self._tEXts = [];
    if 'tEXt' in self._named_chunks:
      for chunk in self._named_chunks['tEXt']:
        self._tEXt = chunk.ContainMember(PNG_tEXt, chunk.name + '_data');
        self._tEXts.append(self._tEXt);

    self._zTXt = None;
    self._zTXts = [];
    if 'zTXt' in self._named_chunks:
      for chunk in self._named_chunks['zTXt']:
        self._zTXt = chunk.ContainMember(PNG_zTXt, chunk.name + '_data');
        self._zTXts.append(self._zTXt);

    self._iTXt = None;
    self._iTXts = [];
    if 'iTXt' in self._named_chunks:
      for chunk in self._named_chunks['iTXt']:
        self._iTXt = chunk.ContainMember(PNG_iTXt, chunk.name + '_data');
        self._iTXts.append(self._iTXt);

    self._bKGD = None;
    self._bKGDs = [];
    if 'bKGD' in self._named_chunks:
      for chunk in self._named_chunks['bKGD']:
        self._bKGD = chunk.ContainMember(PNG_bKGD, chunk.name + '_data', \
            color_type, bit_depth, palette_entries);
        self._bKGDs.append(self._bKGD);

    self._hIST = None;
    self._hISTs = [];
    if 'hIST' in self._named_chunks:
      for chunk in self._named_chunks['hIST']:
        self._hIST = chunk.ContainMember(PNG_hIST, chunk.name + '_data', \
            palette_entries);
        self._hISTs.append(self._hIST);

    self._pHYs = None;
    self._pHYss = [];
    if 'pHYs' in self._named_chunks:
      for chunk in self._named_chunks['pHYs']:
        self._pHYs = chunk.ContainMember(PNG_pHYs, chunk.name + '_data');
        self._pHYss.append(self._pHYs);

    self._sPLT = None;
    self._sPLTs = [];
    if 'sPLT' in self._named_chunks:
      for chunk in self._named_chunks['sPLT']:
        self._sPLT = chunk.ContainMember(PNG_sPLT, chunk.name + '_data');
        self._sPLTs.append(self._sPLT);

    self._tIME = None;
    self._tIMEs = [];
    if 'tIME' in self._named_chunks:
      for chunk in self._named_chunks['tIME']:
        self._tIME = chunk.ContainMember(PNG_tIME, chunk.name + '_data');
        self._tIMEs.append(self._tIME);

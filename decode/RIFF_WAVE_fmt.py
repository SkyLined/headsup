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
from twocc import TWOCC_FORMATS;

# twocc formats codes for formats that do not use an extended "fmt" structure.
NOT_EXTENDED_FORMATS = [0x0001, 0x0008, 0x0092]; # PCM, MS DTS, 

VALID_SPEAKER_LOCATIONS = [
  # http://msdn.microsoft.com/en-us/library/ms713496(VS.85).aspx
  'Front L', 'Front R', 'Front C', 'LowFreq', 'Back L', 'Back R',
  'Front LC', 'Front RC', 'Back C', 'Side L', 'Side R', 'Top C',
  'Top front L', 'Top front C', 'Top front R', 
  'Top back L', 'Top back C', 'Top back R',
];

SPEAKER_LOCATION_PRESETS = {
  0x00000003: 'Front stereo',
  0x00000033: 'Front+back stereo',
  0x0000003F: 'Dolby 5.1',
  0x00000107: 'Front stereo, front+back central',
  0x0000073F: 'Dolby 8.1',
};


class RIFF_WAVE_fmt(Structure):
  type_name = 'RIFF_WAVE_fmt'
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    # http://msdn.microsoft.com/en-us/library/ms713497(VS.85).aspx
    self._AudioFormat = self.Member(C.WORD, 'AudioFormat');
    self._NumChannels = self.Member(C.WORD, 'NumChannels');
    self._SampleRate = self.Member(C.DWORD, 'SampleRate');
    self._ByteRate = self.Member(C.DWORD, 'ByteRate');
    self._BlockAlign = self.Member(C.WORD, 'BlockAlign');
    self._BitsPerSample = self.Member(C.WORD, 'BitsPerSample');


    if self._AudioFormat.value in TWOCC_FORMATS.keys():
      format, ext_fmt, ext_fmt_size = TWOCC_FORMATS[self._AudioFormat.value];
      self._AudioFormat.notes.append('format = %s' % format);
    elif self._AudioFormat.value == 0xFFFE:
      format = 'Extended'; ext_fmt = True; ext_fmt_size = 0x16;
      self._AudioFormat.notes.append('format = %s' % format);
    else:
      format = 'Unknown'; ext_fmt = False, ext_fmt_size = None;
      self._AudioFormat.warnings.append('Unknown format');

    sample_rate = self._SampleRate.value;
    sample_rate_member = self._SampleRate;
    bit_rate = self._ByteRate.value * 8;
    byte_rate_member = self._ByteRate;
    num_channels = self._NumChannels.value;
    if num_channels == 0:
      channels = 'none';
      self._NumChannels.warnings.append('expected at least 1 channel');
    else:
      channels = num_channels;

    self.bits_per_sample = self._BitsPerSample.value;
    self.is_PCM = self._AudioFormat.value == 1;
    format_extended_details = [];
    if not ext_fmt:
      bit_rate = self._SampleRate.value * num_channels * self.bits_per_sample;
      if self._ByteRate.value * 8 != bit_rate:
        self._ByteRate.warnings.append( \
            'expected value to be %s' % (bit_rate / 8.0));
  
      expected_block_align = num_channels * self.bits_per_sample / 8.0;
      if self._BlockAlign.value != expected_block_align:
        self._BlockAlign.warnings.append( \
            'expected value to be %s' % expected_block_align);
      if self.bits_per_sample == 0:
        self._BitsPerSample.warnings.append( \
            'expected at least 1 bit per sample');
    else:
      self._ExtensionSize = self.Member(C.WORD, 'ExtensionSize');
      if ext_fmt_size is not None and self._ExtensionSize.value != ext_fmt_size:
        self._ExtensionSize.warnings.append( \
            'expected value to be %d|0x%X' % (ext_fmt_size, ext_fmt_size));
      if self._AudioFormat.value == 0x0002: #ADPCM
        self._SamplesPerBlock = self.Member(C.WORD, 'SamplesPerBlock');
        self._NumCoefs = self.Member(C.WORD, 'NumCoefs');
        self._Coefs = self.Member(C.ARRAY, self._NumCoefs.value, C.SHORT, \
            'Coefs');
        self.__CheckADPCM();
      elif self._AudioFormat.value in [0x0006, 0x0007]: #A-Law, mu-law
        if self._ExtensionSize.value == 2:
          self._Dummy = self.Member(C.WORD, 'Dummy');
        elif self._ExtensionSize.value != 0:
          self._ExtensionSize.warnings.append('expected value to be 0 or 2');
      elif self._AudioFormat.value == 0x0010: #OKI ADPCM
        self._Pole = self.Member(C.WORD, 'Pole');
        self.__CheckOKI_ADPCM();
      elif self._AudioFormat.value == 0x0011: #Intel DVI ADPCM
        self._SamplesPerBlock = self.Member(C.WORD, 'SamplesPerBlock');
        self.__CheckIntelDVI_ADPCM();
      elif self._AudioFormat.value == 0x0012: #Videologic MediaSpace ADPCM
        self._Revision = self.Member(C.WORD, 'Revision');
        format += ' rev %s' % self._Revision.value;
      elif self._AudioFormat.value == 0x0013: #Sierra ADPCM
        self._Revision = self.Member(C.WORD, 'Revision');
        if self._Revision.value != 0x100:
          self._Revision.warnings.append('expected value to be 0x100');
        format += ' rev %s' % self._Revision.value;
      elif self._AudioFormat.value == 0x0014: #G.723 ADPCM
        self._AuxBlockSize = self.Member(C.WORD, 'AuxBlockSize');
      elif self._AudioFormat.value == 0x0021: #Speech Compression Sonarc
        self._CompType = self.Member(C.WORD, 'CompType');
        format += ' type %s' % self._CompType.value;
      elif self._AudioFormat.value == 0x0022: #DSP Group TrueSpeech
        # http://neo.dmcs.p.lodz.pl/tm/pdf/ct8020d.pdf
        self._Revision = self.Member(C.WORD, 'Revision');
        self._SamplesPerBlock = self.Member(C.WORD, 'SamplesPerBlock');
        self._Reserved = self.Member(C.ARRAY, 'Reserved', 28, C.BYTE);
        self._Reserved.dump_simplified = True;
        if self._Revision.value == 1:
          format += ' 8.5';
        else:
          format += ' rev %s' % self._Revision.value;
        if self._SamplesPerBlock.value != 240:
          self._SamplesPerBlock.warnings.append( \
              'expected value to be 240|0xF0');
      elif self._AudioFormat.value == 0x0031: #GSM 6.10
        self._SamplesPerBlock = self.Member(C.WORD, 'SamplesPerBlock');
        if self._BlockAlign.value != 65:
          self._BlockAlign.warnings.append('expected value to be 65|0x41');
        if self._SamplesPerBlock.value != 320:
          self._SamplesPerBlock.warnings.append( \
              'expected value to be 320|0x140');
        self.bits_per_sample = 16;
      elif self._AudioFormat.value == 0x0034: #Control Res VQLPC
        self._CompType = self.Member(C.WORD, 'CompType');
        if self._CompType.value != 1:
          self._CompType.warnings.append('expected value to be 1');
      elif self._AudioFormat.value == 0x0040: #G.721 ADPCM
        self._AuxBlockSize = self.Member(C.WORD, 'AuxBlockSize');
      elif self._AudioFormat.value == 0x0050: #MPEG
        # http://msdn.microsoft.com/en-us/library/dd390701(VS.85).aspx
        if self._ExtensionSize.value < 0x16:
          self._ExtensionSize.warnings.append( \
              'expected value to be at least 22|0x16');
        self._HeadLayer = self.Member(C.WORD, 'HeadLayer');
        self._HeadBitrate = self.Member(C.DWORD, 'HeadBitrate');
        self._HeadMode = self.Member(C.WORD, 'HeadMode');
        self._HeadModeExt = self.Member(C.WORD, 'HeadModeExt');
        self._HeadEmphasis = self.Member(C.WORD, 'HeadEmphasis');
        self._HeadFlags = self.Member(C.WORD, 'HeadFlags');
        self._PTSLow = self.Member(C.DWORD, 'PTSLow');
        self._PTSHigh = self.Member(C.DWORD, 'PTSHigh');
        self.__CheckMPEG();
      elif self._AudioFormat.value == 0x0055: #MP3
        # http://msdn.microsoft.com/en-us/library/dd390710(VS.85).aspx
        self._ID = self.Member(C.WORD, 'ID');
        self._Flags = self.Member(C.DWORD, 'Flags');
        self._BlockSize = self.Member(C.WORD, 'BlockSize');
        self._FramesPerBlock = self.Member(C.WORD, 'FramesPerBlock');
        self._CodecDelay = self.Member(C.WORD, 'CodecDelay');
        if self._ID.value != 1:
          self._ID.warnings.append('expected value to be 1');
        flags_values = {0:'iso', 1: 'on', 2: 'off'};
        if self._Flags.value in flags_values:
          self._Flags.notes.append('padding=%s' % \
              flags_values[self._Flags.value]);
        else:
          self._Flags.warnings.append('expected value to be 0, 1 or 2');
        self.bits_per_sample = None;
      elif self._AudioFormat.value == 0x0200: #Creative ADPCM
        self._Revision = self.Member(C.WORD, 'Revision');
        format += ' rev %s' % self._Revision.value;
      elif self._AudioFormat.value in [0x0202, 0x0203]: # Creative FastSpeech*
        self._Revision = self.Member(C.WORD, 'Revision');
        if self._Revision.value != 1:
          self._Revision.warnings.append('expected value to be 1');
        format += ' rev %s' % self._Revision.value;
      elif self._AudioFormat.value == 0x1610: #HE-ACC
        self._PayloadType = self.Member(C.WORD, 'PayloadType');
        self._AudioProfileLevelIndication = self.Member(C.WORD, \
            'AudioProfileLevelIndication');
        self._StructType = self.Member(C.WORD, 'StructType');
        self._Reserved1 = self.Member(C.WORD, 'Reserved1');
        self._Reserved2 = self.Member(C.DWORD, 'Reserved2');
        payload_type_values = {0: 'raw', 1: 'ADTS', 2: 'ADIF', 3: 'MPEG-4'};
        if self._PayloadType.value in payload_type_values:
          self._PayloadType.notes.append( \
              payload_type_values[self._PayloadType.value]);
        else:
          self._PayloadType.warnings.append( \
              'expected value to be 0, 1, 2 or 3');
        if self._StructType.value == 0:
          self._StructType.notes.append('ISO/IEC 14496-3');
          config_size = self._ExtensionSize.value - 12;
          self._AudioSpecificConfig = self.Member(C.ARRAY, config_size, \
              C.BYTE, 'AudioSpecificConfig');
        else:
          self._StructType.warnings.append('expected value to be 0');
          
      elif self._AudioFormat.value == 0xFFFE: #Extended
        # http://msdn.microsoft.com/en-us/library/ms713496(VS.85).aspx
        self._ValidBitsPerSample = self.Member(C.WORD, 'ValidBitsPerSample');
        self._ChannelMask = self.Member(C.DWORD, 'ChannelMask');
        self._ExtendedAudioFormat = self.Member(C.WORD, 'ExtendedAudioFormat');
        self._GUID = self.Member(C.ARRAY, 'GUID', 14, C.BYTE);
        self._GUID.dump_simplified = True;

        format, channels = self.__CheckExtensible(format, channels);
      elif self._ExtensionSize.value == 0:
        self._ExtensionSize.notes.append('no extension data');
      else:
        self._ExtensionData = self.Member(C.ARRAY, 'ExtensionData', \
            self._ExtensionSize.value, C.BYTE);
        self._ExtensionData.warnings.append(
            'Contents unknown');

    format_details = [];
    sample_rate = ApplyUnits(sample_rate, 'Hz', 'kHz', 'MHz', 'GHz', 'Thz');
    if sample_rate_member:
      sample_rate_member.notes.append(sample_rate);
    format_details.append(sample_rate);

    if bit_rate is not None:
      bit_rate = ApplyUnits(bit_rate, 'bps', 'kbps', 'Mbps', 'Gbps', 'Tbps');
      if byte_rate_member:
        byte_rate_member.notes.append(bit_rate);
      format_details.append(bit_rate);

    format_details.append('ch=%s' % channels);

    if self.bits_per_sample is not None:
      format_details.append('%s bit' % self.bits_per_sample);
    format_details.extend(format_extended_details);

    self.format_details = 'fmt(%s, %s)' % (format, ', '.join(format_details));

    self.Unused();

  def __CheckADPCM(self):
    expected_size = 4 + 2 * self._CoefficientsCount.value;
    if self._ExtensionSize.value != expected_size:
      self._ExtensionSize.warnings.append( \
          'expected value to be %d|0x%X' % (expected_size, expected_size));
# Read somewhere that the first 7 coefs should have certain values, but not
# enough information about how this is encoded:
#    ExpectedCoefs = [(256, 0), (512, -256), (0, 0), (192, 64), (240, 0), \
#        (460, -208), (392, -232)];
#    for index in range(len(ExpectedCoefs));
#      if self._NumCoefs.value < index:
#        break;
#      coef1, coef2 = ExpectedCoefs[index];
    bytes_per_block = 7 * self._NumChannels.value;
    if self._SamplesPerBlock.value > 2:
      x = (self._SamplesPerBlock.value - 2) * self._NumChannels.value;
      bytes_per_block += int(ceil(x / 2.0));
    self._SamplesPerBlock.notes.append( \
        '%d|0x%X bytes per block' % (bytes_per_block, bytes_per_block));
    ba = self._BlockAlign.value;
    if bytes_per_block > ba:
      self._SamplesPerBlock.warnings.append( \
          'expected value to be < %d|0x%X (BlockAlign)' % (ba, ba));
    self.bits_per_sample = bytes_per_block * 8.0 / self._SamplesPerBlock;
    
    if self.BlockAlign.value not in [256, 512, 1024]:
      self.BlockAlign.warnings.append('expected value to be 256, 512 or 1024');
# This check would be nice, but I am not sure if k refers to 1000 or 1024...
#    total_samples_per_sec = self._SamplesPerSec.value * self._NumChannels.value;
#    total_samples_per_sec       BlockAlign
#    8k                          256
#    11k                         256
#    22k                         512
#    44k                         1024

  def __CheckOKI_ADPCM(self):
    ba = self._BlockAlign.value;
    if self._NumChannels.value in [1, 2] \
        and self._BitsPerSample.value in [3, 4]:
      if self._BitsPerSample.value == 3:
        expected_ba = self._NumChannels.value * 3;
      else:
        expected_ba = 1;
      if ba != expected_ba:
        self._BlockAlign.warnings.append( \
            'expected value to be %s' % expected_ba);

  def __CheckIntelDVI_ADPCM(self):
    if self._SamplesPerBlock.value % 8 != 1:
      self._SamplesPerBlock.warnings.append( \
          'expected value modulus 8 to be 1');
    # per channel, ima has blocks of len 4, the 1st has 1st sample, the
    # others up to 8 samples per block, so number of later blocks is 
    # (nsamp-1 + 7)/8, total blocks/chan is (nsamp-1+7)/8 + 1 = (nsamp+14)/8
    bytes_per_block = (self._SamplesPerBlock.value + 14) / \
        (8 * 4 * self._NumChannels.value);
    self._SamplesPerBlock.notes.append( \
        '%d|0x%X bytes per block' % (bytes_per_block, bytes_per_block));
    ba = self._BlockAlign.value;

    if self._NumChannels.value in [1, 2] \
        and self._BitsPerSample.value in [3, 4]:
      if self._BitsPerSample.value == 3:
        expected_ba = self._NumChannels.value * 3;
      else:
        expected_ba = 1;
      if ba != expected_ba:
        self._BlockAlign.warnings.append( \
            'expected value to be %s' % expected_ba);
    if bytes_per_block > ba:
      self._SamplesPerBlock.warnings.append( \
          'expected value to be < %d|0x%X (BlockAlign)' % (ba, ba));
    self.bits_per_sample = \
        round(bytes_per_block * 8.0 / self._SamplesPerBlock.value, 2);

  def __CheckMPEG(self):
    if self._HeadLayer.value == 0 or self._HeadLayer.value > 7:
      self._HeadLayer.warnings.append( \
          'expected value to be between 1 and 7, inclusive');
    layer_bits = {1: '1', 2: '2', 4: '3'};
    layers = [];
    for bit, layer in layer_bits.items():
      if self._HeadLayer.value & bit:
        layers.append(layer);
    if len(layers) == 0:
      format += ' (unknown layers)';
    elif len(layers) == 1:
      format += ' layer-%s' % layers[0];
    else:
      format += ' layers-%s&%s' % (','.join(layers[:-1]), layers[-1]);
    mode_bits = {1: 'stereo', 2: 'joint stereo', 4: 'dual channel', \
                 8: 'single channel'}
    modes = []
    for bit, mode in mode_bits.items():
      if self._HeadMode.value & bit:
        modes.append(mode);
    format_extended_details = ['mode=' + ','.join(modes)];
    if self._HeadMode.value & 2: # Joint stereo
      pass; # Found no clear information on what to do here
    else:
      if self._HeadModeExt.value != 0:
        self._HeadModeExt.warnings.append('expected value to be 0');
    emphasis_values = {1: 'none', 2: '50/15 ms', 3: 'reserved', \
                      4: 'CCITT J.17'};
    for value, emphasis in emphasis_values.items():
      if self._HeadEmphasis.value == value:
        self._HeadEmphasis.notes.append('emphasis=%s' % emphasis);
        break;
    else:
      self._HeadEmphasis.warnings.append( \
          'expected value between 1 and 4, inclusive');
    flag_bits = {1: 'private', 2: 'copyright', 4: 'original/home', \
       8: 'error protection', 0x10: 'id mpeg1'};
    flags = [];
    for bit, flag in flag_bits.items():
      if self._HeadFlags.value & bit:
        flags.append(flag);
    format_extended_details = ['flags=' + ','.join(flags)];
    if self._HeadFlags.value & 0x10 == 0:
      self._HeadFlags.warnings.append('expected bit 5 (16|0x10) to be set');
    pts = self._PTSLow.value + ((self._PTSHigh.value & 1) << 32);
    self._PTSLow.notes.append('PTS=%d|%09X' % (pts, pts));
    if self._PTSHigh.value > 1:
      self._PTSHigh.warnings.append('expected value to be 0 or 1');

  def __CheckExtensible(self, format, channels):
    self.is_PCM = self._ExtendedAudioFormat.value == 1;

    if self._ExtendedAudioFormat.value in TWOCC_FORMATS:
      ext_format, fmt_ext, fmt_ext_size = \
          TWOCC_FORMATS[self._ExtendedAudioFormat.value];
      self._ExtendedAudioFormat.notes.append('format=%s' % ext_format);
      format += ' ' + ext_format;
    else:
      format += ' Unknown';
      self._ExtendedAudioFormat.warnings.append('Unknown format');

    self.bits_per_sample = self._ValidBitsPerSample.value;
    if self._ChannelMask.value in SPEAKER_LOCATION_PRESETS:
      channels = SPEAKER_LOCATION_PRESETS[self._ChannelMask.value];
      self._ChannelMask.notes.append(channels);
    else:
      speaker_locations = [];
      specified_channels = 0;
      for bit_nr in range(len(VALID_SPEAKER_LOCATIONS)):
        location = VALID_SPEAKER_LOCATIONS[bit_nr];
        bit = 2 ** bit_nr;
        if self._ChannelMask.value & bit:
          speaker_locations.append(location);
          specified_channels += 1;
      if speaker_locations:
        self._ChannelMask.notes.append(','.join(speaker_locations));
        if specified_channels != num_channels:
          self._ChannelMask.warnings.append( \
              'expected %d channels to be specified, found %s' % \
              (num_channels, specified_channels));
        else:
          channels = ','.join(speaker_locations);
      else:
        self._ChannelMask.notes.append('unspecified');

    guid = [byte.value for byte in self._GUID.value if 1];
    expected_guid = [0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x80, \
                     0x00, 0x00, 0xAA, 0x00, 0x38, 0x9B, 0x71];
    index = 0;
    for byte in self._GUID.value:
      if byte.value != expected_guid[index]:
        byte.warnings.append('expected value to be %d|0x%02X' % \
            (expected_guid[index], expected_guid[index]));
        self._GUID.dump_simplified = False;
      index += 1;
    return format, channels;

def ApplyUnits(value, *units):
  value = float(value);
  unit_index = 0;
  while value > 1000 and unit_index < len(units) - 1:
    value /= 1000;
    unit_index += 1;
  if int(value) == value:
    value = int(value);
  else:
    value = round(value, 3);
  return '%s %s' % (value, units[unit_index]);



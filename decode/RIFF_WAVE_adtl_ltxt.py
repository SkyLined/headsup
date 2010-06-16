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

VALID_COUNTRY_CODES = {
    0: 'None (ignore this field)',
    1: 'USA',
    2: 'Canada',
    3: 'Latin America',
   30: 'Greece',
   31: 'Netherlands',
   32: 'Belgium',
   33: 'France',
   34: 'Spain',
   39: 'Italy',
   41: 'Switzerland',
   43: 'Austria',
   44: 'United Kingdom',
   45: 'Denmark',
   46: 'Sweden',
   47: 'Norway',
   49: 'West Germany',
   52: 'Mexico',
   55: 'Brazil',
   61: 'Australia',
   64: 'New Zealand',
   81: 'Japan',
   82: 'Korea',
   86: 'People\'s Republic of China',
   88: 'Taiwan',
   90: 'Turkey',
  351: 'Portugal',
  352: 'Luxembourg',
  354: 'Iceland',
  358: 'Finland',
};
VALID_LANGUAGE_AND_DIALECT_CODES = {
  0: {'lang': 'None', 0: 'None (ignore these fields)'},
  1: {'lang': 'Arabic', 1: 'Arabic'},
  2: {'lang': 'Bulgarian', 1: 'Bulgarian'},
  3: {'lang': 'Catalan', 1: 'Catalan'},
  4: {'lang': 'Chinese', 1: 'Traditional Chinese', 2: 'Simplified Chinese'},
  5: {'lang': 'Czech', 1: 'Czech'},
  6: {'lang': 'Danish', 1: 'Danish'},
  7: {'lang': 'German', 1: 'German', 2: 'Swiss German'},
  8: {'lang': 'Greek', 1: 'Greek'},
  9: {'lang': 'English', 1: 'US English', 2: 'UK English'},
  10: {'lang': 'Spanish', 1: 'Spanish', 2: 'Spanish Mexican'},
  11: {'lang': 'Finnish', 1: 'Finnish'},
  12: {'lang': 'French', 1: 'French', 2: 'Belgian French', 3: 'Canadian French', \
       4: 'Swiss French'},
  13: {'lang': 'Hebrew', 1: 'Hebrew'},
  14: {'lang': 'Hungarian', 1: 'Hungarian'},
  15: {'lang': 'Icelandic', 1: 'Icelandic'},
  16: {'lang': 'Italian', 1: 'Italian', 2: 'Swiss Italian'},
  17: {'lang': 'Japanese', 1: 'Japanese'},
  18: {'lang': 'Korean', 1: 'Korean'},
  19: {'lang': 'Dutch', 1: 'Dutch', 2: 'Belgian Dutch'},
  20: {'lang': 'Norwegian', 1: 'Norwegian - Bokmal', 2: 'Norwegian - Nynorsk'},
  21: {'lang': 'Polish', 1: 'Polish'},
  22: {'lang': 'Portuguese', 1: 'Brazilian Portuguese', 2: 'Portuguese'},
  23: {'lang': 'Rhaeto-Romanic', 1: 'Rhaeto-Romanic'},
  24: {'lang': 'Romanian', 1: 'Romanian'},
  25: {'lang': 'Russian', 1: 'Russian'},
  26: {'lang': 'Serbo-Croatian', 1: 'Serbo-Croatian (Latin)', 2: 'Serbo-Croatian (Cyrillic)'},
  27: {'lang': 'Slovak', 1: 'Slovak'},
  28: {'lang': 'Albanian', 1: 'Albanian'},
  29: {'lang': 'Swedish', 1: 'Swedish'},
  30: {'lang': 'Thai', 1: 'Thai'},
  31: {'lang': 'Turkish', 1: 'Turkish'},
  32: {'lang': 'Urdu', 1: 'Urdu'},
  33: {'lang': 'Bahasa', 1: 'Bahasa'},
};

class RIFF_WAVE_adtl_ltxt(Structure):
  type_name = 'RIFF_WAVE_adtl_ltxt'
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._CuePointName = self.Member(C.DWORD, 'CuePointName');
    self._SampleLength = self.Member(C.DWORD, 'SampleLength');
    self._PurposeId = self.Member(C.STRING, 4, 'PurposeId');
    self._CountryCode = self.Member(C.WORD, 'CountryCode');
    self._Language = self.Member(C.WORD, 'Language');
    self._Dialect = self.Member(C.WORD, 'Dialect');
    self._CodePage = self.Member(C.WORD, 'CodePage');
    self._Text = self.Member(C.STRING, 'Text');

    if self._SampleLength.value == 0:
      self._SampleLength.warnings.append('expected value to be at least 1');
    if self._PurposeId.value == 'scrp':
      self._PurposeId.notes.append('script text');
    elif self._PurposeId.value == 'capt':
      self._PurposeId.notes.append('close-caption');
    else:
      self._PurposeId.warnings.append('unknown purpose');
    lang = '%d,%d' % (self._Language.value, self._Dialect.value);
    if self._Language.value in VALID_LANGUAGE_AND_DIALECT_CODES:
      valid_dialect_codes = \
          VALID_LANGUAGE_AND_DIALECT_CODES[self._Language.value];
      self._Language.notes.append(valid_dialect_codes['lang']);
      if self._Dialect.value in valid_dialect_codes:
        self._Dialect.notes.append(valid_dialect_codes[self._Dialect.value]);
      else:
        valid_codes = valid_dialect_codes.keys();
        valid_codes.remove('lang');
        self._Dialect.warnings.append('expected value to be %s or %s' % \
            (', '.join(valid_codes[:-1]), valid_codes[-1]));
    else:
      self._Language.warnings.append( \
          'expected value to be in range 0-33, inclusive');
    if self.CountryCode.value in VALID_COUNTRY_CODES:
      self.CountryCode.notes.append( \
          VALID_COUNTRY_CODES[self.CountryCode.value]);
    else:
      self.CountryCode.warnings.append('unknown code');
    self.format_details = 'ltxt';
    self.Unused();

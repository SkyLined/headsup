
# http://www.w3.org/TR/PNG/#D-CRCAppendix
CRC_TABLE = [];
for n in range(0x100):
  c = n;
  for k in range(8):
    if c & 1:
      c = 0xEDB88320 ^ (c >> 1);
    else:
      c >>= 1;
  CRC_TABLE.append(c);

def PNG_CRC32(string):# == zlib.crc32
  crc = 0xFFFFFFFF;
  for char in string:
    crc = CRC_TABLE[(crc & 0xFF) ^ ord(char)] ^ (crc >> 8);
  return crc ^ 0xFFFFFFFF;


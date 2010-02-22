def PNG_CheckText(text, can_be_empty = False, max_size = None, \
    no_extra_spaces = True, utf_8 = False, newlines = False, \
    is_keyword = False):
  string = text.value;
  if not can_be_empty and len(string) == 0:
    name.warnings.append('expected at least one character');
  elif max_size is not None and len(string) > max_size:
    name.warnings.append('expected at most 79 characters');
  illegal_charcodes = set();
  if utf_8:
    try:
      string = string.decode('utf-8', 'strict');
    except Exception, e:
      text.warnings.append('utf-8 decoding error: %s' % e);
      string = '';
  for char in string:
    charcode = ord(char);
    if not newlines:
      if charcode == 0x0A:
        illegal_charcodes.add(charcode);
    elif (charcode < 0x20 and charcode != 0x0A) \
        or (charcode > 0x7E and charcode < 0xA1):
      illegal_charcodes.add(charcode);

  if illegal_charcodes:
    illegal_chars = ['%02X' % charcode for charcode in illegal_charcodes if 1];
    text.warnings.append( \
        'string contains illegal characters: %s' % ', '.join(illegal_chars));

  if no_extra_spaces and ' ' in [string[0], string[-1]]:
    text.warnings.append('string must not start or end with a space');

  if is_keyword and string not in [
      'Title', 'Author', 'Description', 'Copyright', 'Creation Time', 
      'Software', 'Disclaimer', 'Warning', 'Source', 'Comment']:
    text.warnings.append('unknown keyword');

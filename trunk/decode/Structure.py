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

g_debug_output = False;

class Structure():
  def __init__(self, stream, offset, max_size, parent, name):
    if g_debug_output:
      print 'Create Structure %s %s @%08X' % (self.type_name, name, offset);
    self.stream = stream;
    self.offset = offset;
    self.max_size = max_size;
    self.name = name;
    self.parent = parent;
    self.check_offset_and_max_size = True;

    self.warnings = [];
    self.notes = [];
    self.value = [];
    self.size = 0;
    self.current_offset = offset;
    self.current_max_size = max_size;
    self.dump_simplified = False;
    self.unused = None;

    self.contained_stream = None;

    self.CheckOffsetAndMaxSize(start=True);

  def CheckOffsetAndMaxSize(self, start = False, end = False):
    if not self.check_offset_and_max_size \
        or (self.parent and not self.parent.check_offset_and_max_size):
      return;
    if start:
      if self.current_offset > len(self.stream):
        off_by = self.current_offset - len(self.stream);
        self.warnings.append( \
            'start is 0x%X|%d bytes beyond end of stream' % (off_by, off_by));
        self.check_offset_and_max_size = False;
      elif self.current_max_size == 0:
        self.warnings.append('start is at end of container');
        self.check_offset_and_max_size = False;
      elif self.current_max_size < 0:
        off_by = -self.current_max_size;
        self.warnings.append( \
            'start is 0x%X|%d bytes beyond end of container' % (off_by, off_by));
        self.check_offset_and_max_size = False;
    if end:
      if self.current_offset > len(self.stream):
        off_by = self.current_offset - len(self.stream);
        self.warnings.append( \
            'end is 0x%X|%d bytes beyond end of stream' % (off_by, off_by));
        self.check_offset_and_max_size = False;
      elif self.current_max_size < 0:
        off_by = -self.current_max_size;
        self.warnings.append( \
            'end is 0x%X|%d bytes beyond end of container' % (off_by, off_by));
        self.check_offset_and_max_size = False;

  def DataAvailable(self, how_much = 1):
    return self.current_max_size >= how_much and \
        self.current_offset + how_much <= len(self.stream);

  def Member(self, structure_class, name, *args, **nargs):
    if g_debug_output:
      print 'Create Member %s %s -> %s @%08X' % \
          (self.type_name, self.name, name, self.current_offset);
    member = structure_class(self.stream, self.current_offset, \
        self.current_max_size, self, name, *args, **nargs);
    self.value.append(member);
    self.size += member.size;
    self.current_offset += member.size;
    self.current_max_size -= member.size;
    member.CheckOffsetAndMaxSize(end=True);
    return member;

  def GetMaxStream(self):
    return self.stream[self.offset : self.offset + self.max_size];
  def GetUsedStream(self):
    return self.stream[self.offset : self.offset + self.size];

  def Unused(self):
    import C;
    if self.current_max_size > 0:
      self.unused = self.Member(C.STRING, 'unused', self.current_max_size);
      self.unused.warnings.append('unexpected unused bytes');
    return self.unused;

  def GetUnusedStream(self):
    if self.unused:
      return self.unused.GetStream();
    return '';

  def ContainStream(self, name, source, stream, max_size = None):
    if max_size is None:
      max_size = len(stream);
    if self.contained_stream is None:
      self.contained_name = name;
      if source:
        self.contained_sources = [source];
      else:
        self.contained_sources = [];
      self.contained_stream = stream;
      self.contained_max_size = max_size;
      self.contained_current_offset = 0;
      self.contained_current_max_size = max_size;
      self.contained_value = [];
      self.contained_unused = None;
    else:
      assert self.contained_name == name, \
          'Expected only one containing stream name, got %s and %s' % \
          (self.contained_name, name);
      if source:
        self.contained_sources.append(source);
      self.contained_stream += stream;
      self.contained_max_size += max_size;
      self.contained_current_max_size += max_size;

  def ContainedDataAvailable(self, how_much = 1):
    # ContainStream needs to be called to create a stream before it can contain
    # anything.
    assert self.contained_stream is not None, \
        'ContainedDataAvailable called before ContainStream';
    return self.contained_current_max_size >= how_much \
        and self.contained_current_offset + how_much <= \
            len(self.contained_stream);

  def ContainMember(self, structure_class, name, *args):
    # ContainStream needs to be called to create a stream before it can contain
    # anything.
    assert self.contained_stream is not None, \
        'ContainMember called before ContainStream';
    contained_member = structure_class(self.contained_stream, \
        self.contained_current_offset, self.contained_current_max_size, \
        self, name, *args);
    self.contained_value.append(contained_member);
    self.contained_current_offset += contained_member.size;
    self.contained_current_max_size -= contained_member.size;
    contained_member.CheckOffsetAndMaxSize(end=True);
    return contained_member;

  def ContainUnused(self):
    # ContainStream needs to be called to create a stream before it can contain
    # anything.
    assert self.contained_stream is not None, \
        'ContainUnused called before ContainStream';
    import C;
    if self.contained_current_max_size > 0:
      self.contained_unused = C.STRING(self.contained_stream, \
          self.contained_current_offset, self.contained_current_max_size, \
          self, 'unused', self.contained_current_max_size);
      self.contained_unused.warnings.append('unexpected unused bytes');
      self.contained_value.append(self.contained_unused);
      self.contained_current_offset += self.contained_unused.size;
      self.contained_current_max_size -= self.contained_unused.size;
    return self.contained_unused;

  def Dump(self, indent_header = ' ', indent_body = ''):
    header_size = 18;
    if self.notes:
      notes = ' // ' + ', '.join(self.notes);
    else:
      notes = '';

    if self.dump_simplified:
      if hasattr(self, 'SimplifiedValue'):
        dump_value = self.SimplifiedValue();
      else:
        dump_value = '%s (0x%X|%d members)' % \
            (self.type_name, len(self.value), len(self.value));
      brackets = False
    else:
      dump_value = self.type_name;
      brackets = True;
      
    if brackets:
      open_bracket = ' {';
    else:
      open_bracket = '';
    print indent_header + \
        ('%08X+%08X ' % (self.offset, self.size)).ljust(header_size) + \
        indent_body + '%s = %s%s' % (self.name, dump_value, open_bracket) + \
        notes;

    for warning in self.warnings:
      print indent_header + ''.ljust(header_size) + \
          indent_body + '// *** Heads up! ' + warning;

    if not self.dump_simplified:
      for member in self.value:
        member.Dump(indent_header, indent_body + '  ');
      off_by = self.offset + self.size - self.current_offset;
      if off_by > 0:
        print indent_header + ''.ljust(header_size) + indent_body + \
            '// *** Heads up! 0x%X|%d more bytes have not been assigned any ' \
            'use!' % (off_by, off_by);
        

    if self.contained_stream and self.contained_value:
      print indent_header;
      print indent_header + ('  +- 00000000 -- contents of %s ---' % \
          self.contained_name).ljust(80, '-');
      if len(self.contained_sources) == 1:
        print indent_header + '  | // Source: %s' % self.contained_sources[0];
      elif len(self.contained_sources) > 1:
        print indent_header + '  | // Sources: %s' % \
            ', '.join(self.contained_sources);
      for contained_member in self.contained_value:
        contained_member.Dump(indent_header + '  | ');
      if self.contained_current_max_size > 0:
        print indent_header + '  | // *** Heads up! 0x%X|%d more bytes have ' \
            'not been assigned any use!' % (self.contained_current_max_size,
            self.contained_current_max_size);
      print indent_header + \
          ('  +- %08X --- end contents %s ---' % \
          (self.contained_max_size, self.contained_name)).ljust(80, '-');
      print indent_header;

    if brackets:
      print indent_header + \
          ('%08X' % (self.offset + self.size)).ljust(header_size) + \
          indent_body + '} // end %s %s' % (self.type_name, self.name);
  

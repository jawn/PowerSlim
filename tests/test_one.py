from nose.tools import ok_, eq_

import clr
clr.AddReference( "System.Management.Automation" )
from System.Management.Automation import PowerShell

def setup():

  global p
  p = PowerShell.Create()

  s = open( "slim.ps1" ).read()
  i_( s )

script = lambda s: p.AddScript(s)

def i_(s):

  script(s)
  global res

  res = p.Invoke()

  if (len(res)):
    res = res[0]

  p.Commands.Clear()

def print_errors():
 
  print len(p.Streams.Error)
  for i in p.Streams.Error:
    print i

def make_stream(s):
  
  i_( "$stream = New-Object System.IO.MemoryStream" )
  i_( "$writer = New-Object System.IO.StreamWriter $stream" )

  i_( "$writer.WriteLine('%s')" % s )
  i_( "$writer.Flush()" )
  i_( "$stream.Seek(0, 'Begin')" )  
  i_( "Write-Error $stream.Position" )

def test_stream():

  p.Streams.Error.Clear()
  make_stream( "Wow" )

  i_( "$buff = new-object byte[] 3" )
  i_( "$stream.Read($buff,0,3)" )
  i_( "[text.encoding]::utf8.getstring($buff);$buff" )

  print_errors()

  eq_(res, "Wow" )

def test_powershell():
  
  i_( "$a=12;$a" )
  eq_(res, 12)

def test_one_row_table():
  
  i_( "$a = 1, 2, 3" )
  i_( "Test-OneRowTable( $a )" )

  eq_(res, True)
  
  i_( "$a = (1,2,3), 2, 3" )
  i_( "Test-OneRowTable( $a )" )
  
  eq_(res, False)

def test_is_chunk():

  i_( "$a='not chunk'" )
  i_( "ischunk($a)" )

  eq_(res, False)

  i_( "$a='[chunk]'" )
  i_( "ischunk($a)" )

  eq_(res, True)

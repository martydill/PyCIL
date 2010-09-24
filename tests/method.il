  .method private hidebysig static int32 
          testmethod() cil managed
  {
    // Code size       7 (0x7)
    .maxstack  1
    .locals init ([0] int32 CS$1$0000)
    IL_0000:  nop
    IL_0001:  ldc.i4.5
    IL_0002:  stloc.0
    IL_0003:  br.s       IL_0005

    IL_0005:  ldloc.0
    IL_0006:  ret
  } // end of method Program::testmethod

  .method private hidebysig static int32 
          Main(string[] args) cil managed
  {
    .entrypoint
    // Code size       15 (0xf)
    .maxstack  2
    .locals init ([0] int32 a,
             [1] int32 CS$1$0000)
    IL_0000:  nop
    IL_0001:  ldc.i4.5
    IL_0002:  stloc.0
    IL_0003:  ldloc.0
    IL_0004:  call       int32 ConsoleApplication1.Program::testmethod()
    IL_0009:  add
    IL_000a:  stloc.1
    IL_000b:  br.s       IL_000d

    IL_000d:  ldloc.1
    IL_000e:  ret
  } // end of method Program::Main

.method private hidebysig static int32  Main(string[] args) cil managed
{
  .entrypoint
  // Code size       13 (0xd)
  .maxstack  2
  .locals init ([0] int32 a,
           [1] int32 b,
           [2] int32 CS$1$0000)
  IL_0000:  nop
  IL_0001:  ldc.i4.5
  IL_0002:  stloc.0
  IL_0003:  ldc.i4.2
  IL_0004:  stloc.1
  IL_0005:  ldloc.0
  IL_0006:  ldloc.1
  IL_0007:  add
  IL_0008:  stloc.2
  //IL_0009:  br.s       IL_000b
  IL_000b:  ldloc.2
  IL_000c:  ret
} // end of method Program::Main


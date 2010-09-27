.method private hidebysig static int32  Main(string[] args) cil managed
{
  .entrypoint
  // Code size       18 (0x12)
  .maxstack  2
  .locals init ([0] int32 a,
           [1] int32 CS$1$0000)
  IL_0000:  nop
  IL_0001:  ldc.i4.1
  IL_0002:  stloc.0
  IL_0003:  ldloc.0
  IL_0004:  ldc.i4.s   13
  IL_0006:  mul
  IL_0007:  stloc.0
  IL_0008:  ldloc.0
  IL_0009:  ldc.i4.2
  IL_000a:  mul
  IL_000b:  stloc.0
  IL_000c:  ldloc.0
  IL_000d:  stloc.1
  IL_000e:  br.s       IL_0010
  IL_0010:  ldloc.1
  IL_0011:  ret
} // end of method Program::Main


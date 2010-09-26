.method private hidebysig static int32  Main(string[] args) cil managed
{
  .entrypoint
  // Code size       24 (0x18)
  .maxstack  2
  .locals init ([0] int32 a,
           [1] int32 CS$1$0000,
           [2] bool CS$4$0001)
  IL_0000:  nop
  IL_0001:  ldc.i4.0
  IL_0002:  stloc.0
  IL_0003:  br.s       IL_0009
  IL_0005:  ldloc.0
  IL_0006:  ldc.i4.1
  IL_0007:  add
  IL_0008:  stloc.0
  IL_0009:  ldloc.0
  IL_000a:  ldc.i4.s   10
  IL_000c:  clt
  IL_000e:  stloc.2
  IL_000f:  ldloc.2
  IL_0010:  brtrue.s   IL_0005
  IL_0012:  ldloc.0
  IL_0013:  stloc.1
  IL_0014:  br.s       IL_0016
  IL_0016:  ldloc.1
  IL_0017:  ret
} // end of method Program::Main


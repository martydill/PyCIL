.method private hidebysig static int32  Main(string[] args) cil managed
{
  .entrypoint
  // Code size       29 (0x1d)
  .maxstack  2
  .locals init ([0] int32 a,
           [1] int32 i,
           [2] int32 CS$1$0000,
           [3] bool CS$4$0001)
  IL_0000:  nop
  IL_0001:  ldc.i4.0
  IL_0002:  stloc.0
  IL_0003:  ldc.i4.0
  IL_0004:  stloc.1
  IL_0005:  br.s       IL_000f
  IL_0007:  ldloc.0
  IL_0008:  ldloc.1
  IL_0009:  add
  IL_000a:  stloc.0
  IL_000b:  ldloc.1
  IL_000c:  ldc.i4.1
  IL_000d:  add
  IL_000e:  stloc.1
  IL_000f:  ldloc.1
  IL_0010:  ldc.i4.4
  IL_0011:  clt
  IL_0013:  stloc.3
  IL_0014:  ldloc.3
  IL_0015:  brtrue.s   IL_0007
  IL_0017:  ldloc.0
  IL_0018:  stloc.2
  IL_0019:  br.s       IL_001b
  IL_001b:  ldloc.2
  IL_001c:  ret
} // end of method Program::Main


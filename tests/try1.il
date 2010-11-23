.method private hidebysig static int32  Main(string[] args) cil managed
{
  .entrypoint
  // Code size       19 (0x13)
  .maxstack  1
  .locals init ([0] int32 CS$1$0000)
  IL_0000:  nop
  .try
  {
    IL_0001:  nop
    IL_0002:  ldc.i4     0x4d2
    IL_0007:  stloc.0
    IL_0008:  leave.s    IL_0010
  }  // end .try
  catch [mscorlib]System.Object 
  {
    IL_000a:  pop
    IL_000b:  nop
    IL_000c:  ldc.i4.0
    IL_000d:  stloc.0
    IL_000e:  leave.s    IL_0010
  }  // end handler
  IL_0010:  nop
  IL_0011:  ldloc.0
  IL_0012:  ret
} // end of method Program::Main


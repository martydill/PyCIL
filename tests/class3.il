
//  Microsoft (R) .NET Framework IL Disassembler.  Version 3.5.30729.1
//  Copyright (c) Microsoft Corporation.  All rights reserved.



// Metadata version: v2.0.50727
.assembly extern mscorlib
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 )                         // .z\V.4..
  .ver 2:0:0:0
}
.assembly ConsoleApplication1
{
  .custom instance void [mscorlib]System.Reflection.AssemblyTitleAttribute::.ctor(string) = ( 01 00 13 43 6F 6E 73 6F 6C 65 41 70 70 6C 69 63   // ...ConsoleApplic
                                                                                              61 74 69 6F 6E 31 00 00 )                         // ation1..
  .custom instance void [mscorlib]System.Reflection.AssemblyDescriptionAttribute::.ctor(string) = ( 01 00 00 00 00 ) 
  .custom instance void [mscorlib]System.Reflection.AssemblyConfigurationAttribute::.ctor(string) = ( 01 00 00 00 00 ) 
  .custom instance void [mscorlib]System.Reflection.AssemblyCompanyAttribute::.ctor(string) = ( 01 00 09 4D 69 63 72 6F 73 6F 66 74 00 00 )       // ...Microsoft..
  .custom instance void [mscorlib]System.Reflection.AssemblyProductAttribute::.ctor(string) = ( 01 00 13 43 6F 6E 73 6F 6C 65 41 70 70 6C 69 63   // ...ConsoleApplic
                                                                                                61 74 69 6F 6E 31 00 00 )                         // ation1..
  .custom instance void [mscorlib]System.Reflection.AssemblyCopyrightAttribute::.ctor(string) = ( 01 00 1B 43 6F 70 79 72 69 67 68 74 20 C2 A9 20   // ...Copyright .. 
                                                                                                  4D 69 63 72 6F 73 6F 66 74 20 32 30 31 30 00 00 ) // Microsoft 2010..
  .custom instance void [mscorlib]System.Reflection.AssemblyTrademarkAttribute::.ctor(string) = ( 01 00 00 00 00 ) 
  .custom instance void [mscorlib]System.Runtime.InteropServices.ComVisibleAttribute::.ctor(bool) = ( 01 00 00 00 00 ) 
  .custom instance void [mscorlib]System.Runtime.InteropServices.GuidAttribute::.ctor(string) = ( 01 00 24 62 30 38 33 66 32 30 36 2D 37 63 66 64   // ..$b083f206-7cfd
                                                                                                  2D 34 65 61 32 2D 62 64 31 39 2D 66 38 37 64 30   // -4ea2-bd19-f87d0
                                                                                                  35 62 39 31 38 30 31 00 00 )                      // 5b91801..
  .custom instance void [mscorlib]System.Reflection.AssemblyFileVersionAttribute::.ctor(string) = ( 01 00 07 31 2E 30 2E 30 2E 30 00 00 )             // ...1.0.0.0..

  // --- The following custom attribute is added automatically, do not uncomment -------
  //  .custom instance void [mscorlib]System.Diagnostics.DebuggableAttribute::.ctor(valuetype [mscorlib]System.Diagnostics.DebuggableAttribute/DebuggingModes) = ( 01 00 07 01 00 00 00 00 ) 

  .custom instance void [mscorlib]System.Runtime.CompilerServices.CompilationRelaxationsAttribute::.ctor(int32) = ( 01 00 08 00 00 00 00 00 ) 
  .custom instance void [mscorlib]System.Runtime.CompilerServices.RuntimeCompatibilityAttribute::.ctor() = ( 01 00 01 00 54 02 16 57 72 61 70 4E 6F 6E 45 78   // ....T..WrapNonEx
                                                                                                             63 65 70 74 69 6F 6E 54 68 72 6F 77 73 01 )       // ceptionThrows.
  .hash algorithm 0x00008004
  .ver 1:0:0:0
}
.module ConsoleApplication1.exe
// MVID: {5BEEDC97-E77E-4CB9-9C9B-84440DC551FD}
.imagebase 0x00400000
.file alignment 0x00000200
.stackreserve 0x00100000
.subsystem 0x0003       // WINDOWS_CUI
.corflags 0x00000001    //  ILONLY
// Image base: 0x00D10000


// =============== CLASS MEMBERS DECLARATION ===================

.class private auto ansi beforefieldinit ConsoleApplication1.foo
       extends [mscorlib]System.Object
{
  .field public int32 z
  .method public hidebysig specialname rtspecialname 
          instance void  .ctor() cil managed
  {
    // Code size       7 (0x7)
    .maxstack  8
    IL_0000:  ldarg.0
    IL_0001:  call       instance void [mscorlib]System.Object::.ctor()
    IL_0006:  ret
  } // end of method foo::.ctor

} // end of class ConsoleApplication1.foo

.class private auto ansi beforefieldinit ConsoleApplication1.Program
       extends [mscorlib]System.Object
{
  .method private hidebysig static int32 
          Main(string[] args) cil managed
  {
    .entrypoint
    // Code size       52 (0x34)
    .maxstack  2
    .locals init ([0] int32 counter,
             [1] int32 i,
             [2] class ConsoleApplication1.foo f,
             [3] int32 CS$1$0000,
             [4] bool CS$4$0001)
    IL_0000:  nop
    IL_0001:  ldc.i4.0
    IL_0002:  stloc.0
    IL_0003:  ldc.i4.0
    IL_0004:  stloc.1
    IL_0005:  br.s       IL_0023

    IL_0007:  nop
    IL_0008:  newobj     instance void ConsoleApplication1.foo::.ctor()
    IL_000d:  stloc.2
    IL_000e:  ldloc.2
    IL_000f:  ldloc.1
    IL_0010:  stfld      int32 ConsoleApplication1.foo::z
    IL_0015:  ldloc.0
    IL_0016:  ldloc.2
    IL_0017:  ldfld      int32 ConsoleApplication1.foo::z
    IL_001c:  add
    IL_001d:  stloc.0
    IL_001e:  nop
    IL_001f:  ldloc.1
    IL_0020:  ldc.i4.1
    IL_0021:  add
    IL_0022:  stloc.1
    IL_0023:  ldloc.1
    IL_0024:  ldc.i4.s   10
    IL_0026:  clt
    IL_0028:  stloc.s    CS$4$0001
    IL_002a:  ldloc.s    CS$4$0001
    IL_002c:  brtrue.s   IL_0007

    IL_002e:  ldloc.0
    IL_002f:  stloc.3
    IL_0030:  br.s       IL_0032

    IL_0032:  ldloc.3
    IL_0033:  ret
  } // end of method Program::Main

  .method public hidebysig specialname rtspecialname 
          instance void  .ctor() cil managed
  {
    // Code size       7 (0x7)
    .maxstack  8
    IL_0000:  ldarg.0
    IL_0001:  call       instance void [mscorlib]System.Object::.ctor()
    IL_0006:  ret
  } // end of method Program::.ctor

} // end of class ConsoleApplication1.Program


// =============================================================

// *********** DISASSEMBLY COMPLETE ***********************
// WARNING: Created Win32 resource file C:\Users\Marty\Documents\Visual Studio 2008\Projects\ConsoleApplication1\ConsoleApplication1\bin\Debug\test.res

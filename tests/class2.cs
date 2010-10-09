using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApplication1
{
   class foo
   {
      public int z;
   }

   class Program
   {
      // returns 684870
      static int Main(string[] args)
      {
         foo f = new foo();
         f.z = 1234;
         foo f2 = new foo();
         f2.z = 555;
         return f.z * f2.z;
      }
   }
}

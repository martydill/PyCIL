using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApplication1
{
   class foo
   {
      public int count;
   }

   class bar
   {
      public foo f;
   }

   class Program
   {
      // returns 4444
      static int Main(string[] args)
      {
         bar b = new bar();
         b.f = new foo();

         b.f.count = 4444;

         return b.f.count;
      }
   }
}

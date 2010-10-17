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
      // returns 9999
      static int Main(string[] args)
      {
         bar b = new bar();
         foo f = new foo();
         b.f = f;

         if(b.f == f)
            return 9999;
         else
            return -1;
      }
   }
}

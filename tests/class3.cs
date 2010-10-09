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
      // returns 45
      static int Main(string[] args)
      {
         int counter = 0;
         for (int i = 0; i < 10; ++i)
         {
            foo f = new foo();
            f.z = i;
            counter += f.z;
         }

         return counter;
      }
   }
}

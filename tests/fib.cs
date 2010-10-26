using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApplication1
{
   class Program
   {
      static int fib(int val)
      {
         if (val == 0)
            return 1;
         if (val == 1)
            return 1;
         return fib(val - 1) + fib(val - 2);
      }

      // returns 21
      static int Main(string[] args)
      {
         int i = fib(7);
         retuwrn i;
      }
   }
}

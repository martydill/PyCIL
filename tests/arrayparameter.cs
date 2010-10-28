using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApplication1
{
   class Program
   {
      static int readarrayvalue(int[] foo)
      {
         return foo[9];
      }

      // returns 232232
      static int Main(string[] args)
      {
         int[] arr = new int[100];
         arr[9] = 232232;
         return readarrayvalue(arr);
      }
   }
}

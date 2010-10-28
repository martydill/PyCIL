using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApplication1
{
   class Program
   {
      // returns 987987
      static int Main(string[] args)
      {
         int[] arr = new int[100];
         arr[5] = 987987;
         return arr[5];
      }
   }
}

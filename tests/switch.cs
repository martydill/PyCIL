using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApplication1
{
   class Program
   {
      // returns 555
      static int Main(string[] args)
      {
         int x = 1234;
         int ret = 1;
         switch (x)
         {
            case 111:
               ret = 2;
               break;
            case 1234:
               ret = 555;
               break;
            default:
               ret = -1;
               break;
         }
         return ret;
      }
   }
}

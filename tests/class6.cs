using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApplication1
{
   class foo
   {
      private int count = 987654;

      public int GetCount()
      {
         return count - 1;
      }
   }

   class Program
   {
      // returns 987653
      static int Main(string[] args)
        {
            foo f = new foo();
            return f.GetCount();
        }
   }
}

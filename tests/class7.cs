using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApplication1
{
   class foo
   {
      private int count = 987654;

      public void SetCount(int c)
      {
         count = c;
      }

      public int GetCount()
      {
         return count - 1;
      }
   }

   class Program
   {
        // returns 999
        static int Main(string[] args)
        {
            foo f = new foo();
            f.SetCount(1000);
            return f.GetCount();
        }
   }
}

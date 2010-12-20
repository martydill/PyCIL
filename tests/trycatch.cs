using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApplication1
{
    class Program
    {
		  // returns 1234
       static int Main(string[] args)
       {
          try
          {
             throw new Exception();
          }
          catch
          {
             return 1234;
          }

          return 0;
       }
    }
}

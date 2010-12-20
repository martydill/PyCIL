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
              try
              {
                 return 1234;
              }
              catch
              {
                 return 1;
              }
           }
           catch
           {
              return 0;
           }
        }
    }
}

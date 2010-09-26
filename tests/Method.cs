using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApplication1
{
    class Program
    {
        static int testmethod()
        {
            return 5;
        }

        static int Main(string[] args)
        {
            int a = 0;

            return a + testmethod();
        }
    }
}

using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApplication1
{
    class Program
    {
        // returns 6
        static int Main(string[] args)
        {
            int a = 0;
            for (int i = 0; i < 4; ++i)
                a += i;

            return a;
        }
    }
}

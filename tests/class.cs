using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApplication1
{
    class foo
    {
        public int z;
    }

    class Program
    {
        // returns 1234
        static int Main(string[] args)
        {
            foo f = new foo();
            f.z = 1234;
            return f.z;
        }
    }
}

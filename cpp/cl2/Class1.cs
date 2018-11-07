using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace cl2
{
    public class Class1
    {

        public int Cl2Int { get; set; } = 0;
        public String Cs_s { get; set; }

        public void hello()
        {
            Console.WriteLine("hello, world.C#");
        }

        public int myInt()
        {
            return 123;
        }

        public void displayCs_s()
        {
            Console.WriteLine(this.Cs_s);
        }
    }
}

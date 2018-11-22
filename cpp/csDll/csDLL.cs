using System;
using System.Text;
using System.Threading;

namespace csDll
{
    public class csDLL
    {
        public String testString { get; set; }

        public void helloDLL()
        {
            Console.WriteLine("C# Hello DLL");

            WebReference.Subscriber s = new WebReference.Subscriber();
            s.subscriberId = "111";
            Console.WriteLine("subscriber : " + s.subscriberId);

        }

        public void show_String()
        {
            //Thread.Sleep(5000);
            Console.WriteLine(this.testString);
        }

    }
}

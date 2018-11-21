using System;
using System.Text;

namespace csDll
{
    public class csDLL
    {
        public void helloDLL()
        {
            Console.WriteLine("C# Hello DLL");

            WebReference.Subscriber s = new WebReference.Subscriber();
            s.subscriberId = "111";
            Console.WriteLine("subscriber : " + s.subscriberId);

        }
    }
}

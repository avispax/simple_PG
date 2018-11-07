using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.ServiceModel;
using testForm.testLocal;

namespace testForm
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            localhost.sono1 c = new localhost.sono1();
            Console.WriteLine(c.method_test("#"));

            Subscriber s = new testLocal.Subscriber();
            PSXAPIService a = new PSXAPIService();
            a.Timeout
            SubscriberKey k = new SubscriberKey();
            k.subscriberId = "12345";
            k.countryId = "81";
            k.owningCarrierId = null;
            Subscriber sub = (Subscriber)a.retrieve("aaa", k);

            
            NumberTranslation n = new NumberTranslation();
            
            EndPointLocationProfileKey eplpk = new EndPointLocationProfileKey();

            a.create("sss", s);
            
            
        }
    }

}

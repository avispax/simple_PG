using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace t1
{
    public class Ball
    {
        public event EventHandler BallInPlay;
        public void OnBallInPlay(BallEventArgs e)
        {
            if ( BallInPlay != null )
            {
                BallInPlay(this, e);
            }
        }
    }

    public class BallEventArgs : EventArgs
    {
        public int Trajectory { get; private set; }
        public int Distance { get; private set; }
        public BallEventArgs (int Trajectory, int Distance)
        {
            this.Trajectory = Trajectory;
            this.Distance = Distance;
        }

    }

}

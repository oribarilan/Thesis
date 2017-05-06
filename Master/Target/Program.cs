using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using InvariantSynthesis.Utility;

[assembly:
    CsvLogMethod(AttributePriority = 0, AttributeTargetAssemblies = "TargetSample", AttributeTargetTypes = "TargetSample.*")]

namespace TargetSample
{
    /// <summary>
    /// This is an example of target class for the Invariant Synthesis framework.
    /// Follow these steps:
    ///     1. Add a reference to InvariantSynthesis
    ///     2. Add the following attribute above the namespace declaration:
    ///         [assembly: CsvLogMethod(AttributePriority = 0, AttributeTargetAssemblies = "Target", AttributeTargetTypes = "Target.*")]
    ///     3. Add a UnitTest class (or edit the existing UnitTest class) and use InvAssert class from InvariantSynthesis project
    ///         (Follow instructions inside TargetTest)
    ///
    /// </summary>
    public class Program
    {
        static void Main(string[] args)
        {
            Fibonacci(5);
        }

        public static int Fibonacci(int n)
        {
            if (n < 0)
                throw new ArgumentOutOfRangeException();
            if (n == 0)
                return 0;
            if (n == 1)
                return 1;

            return Fibonacci(n - 1) + Fibonacci(n - 2);
        }

        public static bool Go(bool throwException, bool returnThis)
        {
            if (throwException)
            {
                throw new Exception();
            }
            else
            {
                return returnThis;
            }
        }

        public static bool Go(int i)
        {
            if (i == 0)
            {
                return true;
            }
            if (i == 1)
            {
                Go(i - 1);
                throw new Exception();
            }
            else
            {
                return Go(i-1);
            }
        }
    }
}

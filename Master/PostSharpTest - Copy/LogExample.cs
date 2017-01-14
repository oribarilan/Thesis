using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using InvariantSynthesis.Utility;

// Add logging to every method in the assembly.
[assembly: CsvLogMethod(AttributePriority = 0)]

//// Remove logging from the Aspects namespace to avoid infinite recursions (logging would log itself).
[assembly: CsvLogMethod(AttributePriority = 1, AttributeExclude = true, AttributeTargetTypes = "InvariantSynthesis.Utility.*")]


namespace InvariantSynthesis
{
    class LogExample
    {
        [LogSetValue]
        private static int Value;

        public static void Main(string[] args)
        {
            // Demonstrate that we can create a nice hierarchical log including parameter and return values.
            Value = Fibonacci(5);

            // Demonstrate how exceptions are logged.
            try
            {
                Fibonacci(-1);
            }
            catch
            {
            }

            // Demonstrate that we can add logging to system methods, too.
            Console.WriteLine(Math.Sin(5));

            Console.ReadLine();
        }


        private static int Fibonacci(int n)
        {
            if (n < 0)
                throw new ArgumentOutOfRangeException();
            if (n == 0)
                return 0;
            if (n == 1)
                return 1;

            return Fibonacci(n - 1) + Fibonacci(n - 2);
        }
    }
}

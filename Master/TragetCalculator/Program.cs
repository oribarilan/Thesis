using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TragetCalculator
{
    class Program
    {
        static void Main(string[] args)
        {
            //Get the input values from the console, and initiaze the answer to zero
            int num1 = 0;
            Console.WriteLine("Enter the value for Number 1:");
            int.TryParse(Console.ReadLine(), out num1);
            int num2 = 0;
            Console.WriteLine("Enter the value for Number 2:");
            int.TryParse(Console.ReadLine(), out num2);
            string op = "";
            Console.WriteLine("Enter the Operator (+,-,*,/):");
            op = Console.ReadLine();
            int answer = 0;

            //Depending on which operator the user selected, call the approparite calculator method.
            //Store the result int the answer variable
            switch (op)
            {
                case "+":
                    answer = Calculator.Add(num1, num2);
                    break;
                case "-":
                    answer = Calculator.Subtract(num1, num2);
                    break;
                case "*":
                    answer = Calculator.Multiply(num1, num2);
                    break;
                case "/":
                    answer = Calculator.Divide(num1, num2);
                    break;
            }

            //Show the answer
            Console.WriteLine("{0} {1} {2} = {3}{4}{4}Press [ENTER] to continue...", num1, op, num2, answer, System.Environment.NewLine);
            Console.ReadLine();


        }
    }
}

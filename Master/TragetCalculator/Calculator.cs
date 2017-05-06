using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using InvariantSynthesis.Utility;

[assembly:
    CsvLogMethod(AttributePriority = 0, AttributeTargetAssemblies = "TragetCalculator", AttributeTargetTypes = "TragetCalculator.*")]

namespace TragetCalculator
{
    public class Calculator
    {
        //Create a method to add the two numbers
        public static int Add(int num1, int num2)
        {
            return num1 + num2;
        }

        //Create a method to subtract the two numbers
        public static int Subtract(int num1, int num2)
        {
            return num1 - num2;
        }

        //Create a method to multiply the two numbers
        public static int Multiply(int num1, int num2)
        {
            var sign = 1;
            if (num1 < 0)
            {
                sign = Calculator.Negative(sign);
            }
            // BUG: Missing concideration to the 2nd multiplier
            //if (num2 < 0)
            //{
            //    sign = Calculator.Negative(sign);
            //}

            num1 = Math.Abs(num1);
            num2 = Math.Abs(num2);
            var res = 0;
            while (num2 > 0)
            {
                res = Calculator.Add(res, num1);
                num2 = Calculator.Subtract(num2, 1);
            }

            return res * sign;
        }

        //Create a method to divide the two numbers
        public static int Divide(int num1, int num2)
        {
            var a = num1;
            var b = num2;

            if (b == 0)
            {
                throw new DivideByZeroException();
            }
            var sign = 1;
            if (a < 0)
            {
                a = Calculator.Negative(a);
                sign = Calculator.Negative(sign);
            }
            if (b < 0)
            {
                b = Calculator.Negative(b);
                sign = Calculator.Negative(sign);
            }
            var res = 0;
            while (a >= 0)
            {
                a = Calculator.Subtract(a, b);
                res = Calculator.Add(res, 1);
            }

            var ans = Calculator.Subtract(res, 1);
            ans = Calculator.Multiply(ans, sign);

            return ans;
        }

        public static int Pow(int num1, int num2)
        {
            var sign = 1;
            if (num1 < 0 && num2 % 2 == 1)
            {
                sign = Calculator.Negative(sign);
            }
            if (num2 < 0)
            {
                throw new ArithmeticException();
            }

            num1 = Math.Abs(num1);
            num2 = Math.Abs(num2);
            var res = 1;
            while (num2 > 0)
            {
                res = Calculator.Multiply(res, num1);
                num2 = Calculator.Subtract(num2, 1);
            }

            return res * sign;
        }

        public static int Negative(int num)
        {
            return Calculator.Subtract(0, num);
        }

        public static int Modulo(int num1, int num2)
        {
            var a = num1;
            var b = num2;

            if (b == 0)
            {
                throw new DivideByZeroException();
            }
            var sign = 1;
            if (a < 0)
            {
                a = Calculator.Negative(a);
                sign = Calculator.Negative(sign);
            }
            if (b < 0)
            {
                b = Calculator.Negative(b);
                sign = Calculator.Negative(sign);
            }
            var res = 0;
            while (a >= 0)
            {
                a = Calculator.Subtract(a, b);
                res = Calculator.Add(res, 1);
            }

            var div = Calculator.Subtract(res, 1);
            div = Calculator.Multiply(div, sign);

            div = Calculator.Multiply(div, num2);

            return Calculator.Subtract(num1, div);
        }
    }
}

using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using InvariantSynthesis.Utility;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using TragetCalculator;
using Assert = InvariantSynthesis.LoggedUtility.Assert;

[assembly:
    CsvLogMethod(AttributePriority = 0, AttributeExclude = true, AttributeTargetAssemblies = "TargetCalculatorTest", AttributeTargetTypes = "TargetCalculatorTest.*")]

namespace TargetCalculatorTest
{
    [TestClass]
    public class CalculatorTests
    {
        [TestInitialize]
        public void TestInit()
        {
            Assert.Restart();
        }

        [TestCleanup]
        public void TestClean()
        {
            Assert.Inv_AssertAll();
            Assert.Restart();
        }

        [TestMethod]
        public void TestCsAddition()
        {
            var testData = new[]
            {
                new {Num1 = 0, Num2 = 0, Result = 0},
                new {Num1 = 10, Num2 = 10, Result = 20},
                new {Num1 = 10, Num2 = 20, Result = 30},
                new {Num1 = -0, Num2 = -0, Result = 0},
                new {Num1 = -5, Num2 = -5, Result = -10},
                new {Num1 = -5, Num2 = 5, Result = 0},
                new {Num1 = -10, Num2 = -5, Result = -15},
                new {Num1 = -5, Num2 = -10, Result = -15},
                new {Num1 = -5, Num2 = 10, Result = 5},
            };

            foreach (var test in testData)
            {
                var answer = Calculator.Add(test.Num1, test.Num2);
                Assert.AreEqual(test.Result, answer);
            }
        }

        [TestMethod]
        public void TestCsSubtraction()
        {
            var testData = new[]
            {
                new {Num1 = 0, Num2 = 0, Result = 0},
                new {Num1 = 10, Num2 = 10, Result = 0},
                new {Num1 = 10, Num2 = 20, Result = -10},
                new {Num1 = 20, Num2 = 10, Result = 10},
                new {Num1 = -0, Num2 = -0, Result = 0},
                new {Num1 = -5, Num2 = -5, Result = 0},
                new {Num1 = -5, Num2 = 5, Result = -10},
                new {Num1 = -10, Num2 = -5, Result = -5},
                new {Num1 = -5, Num2 = -10, Result = 5},
                new {Num1 = -5, Num2 = 10, Result = -15},
            };

            foreach (var test in testData)
            {
                var answer = Calculator.Subtract(test.Num1, test.Num2);
                Assert.AreEqual(test.Result, answer);
            }
        }

        [TestMethod]
        public void TestCsMultiplication()
        {
            var testData = new[]
            {
                new {Num1 = 10, Num2 = 20, Result = 200},
                new {Num1 = 0, Num2 = 0, Result = 0},
                new {Num1 = 10, Num2 = 10, Result = 100},
                new {Num1 = 20, Num2 = 10, Result = 200},
                new {Num1 = -0, Num2 = -0, Result = 0},
                new {Num1 = -5, Num2 = -5, Result = 25},
                new {Num1 = -5, Num2 = 5, Result = -25},
                new {Num1 = -10, Num2 = -5, Result = 50},
                new {Num1 = -5, Num2 = -10, Result = 50},
                new {Num1 = -5, Num2 = 10, Result = -50},
            };

            foreach (var test in testData)
            {
                var answer = Calculator.Multiply(test.Num1, test.Num2);
                Assert.AreEqual(test.Result, answer);
            }
        }

        [TestMethod]
        public void TestCsDivision()
        {
            var testData = new[]
            {
                new {Num1 = 10, Num2 = 10, Result = 1},
                new {Num1 = 20, Num2 = 10, Result = 2},
                new {Num1 = -5, Num2 = -5, Result = 1},
                new {Num1 = -5, Num2 = 5, Result = -1},
                new {Num1 = -10, Num2 = -5, Result = 2},
            };

            foreach (var test in testData)
            {
                var answer = Calculator.Divide(test.Num1, test.Num2);
                Assert.AreEqual(test.Result, answer);
            }
        }

        //[TestMethod]
        //[ExpectedException(typeof(DivideByZeroException))]
        //public void TestCsDivisionByZero()
        //{
        //    Calculator.Divide(5, 0);
        //}

        [TestMethod]
        public void TestCsPow()
        {
            var testData = new[]
            {
                new {Num1 = 1, Num2 = 10, Result = 1},
                new {Num1 = 10, Num2 = 5, Result = 100000},
                new {Num1 = -5, Num2 = 2, Result = 25},
                new {Num1 = -5, Num2 = 3, Result = -125},
                new {Num1 = 1, Num2 = 1, Result = 1},
                new {Num1 = 0, Num2 = 100, Result = 0},
                new {Num1 = 0, Num2 = 0, Result = 1},
            };

            foreach (var test in testData)
            {
                var answer = Calculator.Pow(test.Num1, test.Num2);
                Assert.AreEqual(test.Result, answer);
            }
        }

        //[TestMethod]
        //[ExpectedException(typeof(ArithmeticException))]
        //public void TestCsPowException()
        //{
        //    Calculator.Pow(5, -5);
        //    Calculator.Pow(5, -1);
        //    Calculator.Pow(1, -1);

        //    Calculator.Pow(-5, -5);
        //    Calculator.Pow(-5, -1);
        //    Calculator.Pow(-1, -1);
        //}

        [TestMethod]
        public void TestCsNegative()
        {
            var testData = new[]
            {
                new {Num = 0, Result = 0},
                new {Num = 1, Result = -1},
                new {Num = -1, Result = 1},
                new {Num = 20, Result = -20},
                new {Num = -7, Result = 7},
            };

            foreach (var test in testData)
            {
                var answer = Calculator.Negative(test.Num);
                Assert.AreEqual(test.Result, answer);
            }
        }

        [TestMethod]
        public void TestCsModulo()
        {
            var testData = new[]
            {
                new {Num1 = 1, Num2 = 1, Result = 0},
                new {Num1 = 20, Num2 = 1, Result = 0},
                new {Num1 = 20, Num2 = 5, Result = 0},
                new {Num1 = 20, Num2 = 3, Result = 2},
                new {Num1 = 5, Num2 = 2, Result = 1},
                new {Num1 = 10, Num2 = 8, Result = 2},
                new {Num1 = 100, Num2 = 3, Result = 1},
            };

            foreach (var test in testData)
            {
                var answer = Calculator.Modulo(test.Num1, test.Num2);
                Assert.AreEqual(test.Result, answer);
            }
        }
    }
}

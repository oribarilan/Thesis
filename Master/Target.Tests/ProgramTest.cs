// <copyright file="ProgramTest.cs">Copyright ©  2017</copyright>
using System;
using Microsoft.Pex.Framework;
using Microsoft.Pex.Framework.Validation;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Target;

namespace Target.Tests
{
    /// <summary>This class contains parameterized unit tests for Program</summary>
    [PexClass(typeof(Program))]
    [PexAllowedExceptionFromTypeUnderTest(typeof(InvalidOperationException))]
    [PexAllowedExceptionFromTypeUnderTest(typeof(ArgumentException), AcceptExceptionSubtypes = true)]
    [TestClass]
    public partial class ProgramTest
    {
        /// <summary>Test stub for Sqrt(Int32)</summary>
        [PexMethod]
        public double SqrtTest(int n)
        {
            double result = Program.Sqrt(n);
            return result;
            // TODO: add assertions to method ProgramTest.SqrtTest(Int32)
        }
    }
}

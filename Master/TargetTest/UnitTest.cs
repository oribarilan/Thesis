using System;
using InvariantSynthesis.Utility;
using InvariantSynthesis.LoggedUtility;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Assert = InvariantSynthesis.LoggedUtility.Assert;

[assembly:
    CsvLogMethod(AttributePriority = 0, AttributeExclude = true, AttributeTargetAssemblies = "TargetTest", AttributeTargetTypes = "TargetTest.*")]

namespace TargetTest
{
    /// <summary>
    /// This is an example of test class for the target class for Invariant Synthesis framework.
    /// This will generate the dataset for each method to be later learned and made into an invariant.
    /// Follow these steps:
    ///     1. Add a reference to InvariantSynthesis
    ///     2. Add the following line above the namespace declaration:
    ///         [assembly: CsvLogMethod(AttributePriority = 0, AttributeExclude = true, AttributeTargetAssemblies = "TargetTest", AttributeTargetTypes = "TargetTest.*")]
    ///     3. Use InvAssert class instead of Assert. Add the following using statement for convenience:
    ///         using Assert = InvariantSynthesis.LoggedUtility.Assert;
    ///     4. Make sure you group all asserts together (using Inv_AssertAll), to prevent the testing from stopping when the test fails.    
    /// </summary>
    [TestClass]
    public class UnitTest
    {
        [TestMethod]
        public void Test_Method1()
        {
            Assert.Inv_AssertAll(
                () => Assert.Inv_AreEqual(3, Target.Program.Fibonacci(5)),
                () => Assert.Inv_AreEqual(5, Target.Program.Fibonacci(5))
                );
            
            
        }

    }


}

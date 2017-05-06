using System;
using System.Collections.Generic;
using InvariantSynthesis.Utility;
using InvariantSynthesis.LoggedUtility;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Assert = InvariantSynthesis.LoggedUtility.Assert;

[assembly:
    CsvLogMethod(AttributePriority = 0, AttributeExclude = true, AttributeTargetAssemblies = "TargetTestSample", AttributeTargetTypes = "TargetTestSample.*")]
namespace TargetTestSample
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
            var asserts = new List<Action>() {};
            {
                //asserts.Add(() => Assert.Inv_isTrue(Target.Program.Go(false, false))); //should log: false,false,false,0
                //asserts.Add(() => Assert.Inv_isTrue(Target.Program.Go(false,true))); //should log: false,true,true,1
                //asserts.Add(() => Assert.Inv_ThrowsException(() => Target.Program.Go(true,true))); //should log true,true,NaN,1
                //asserts.Add(() => Assert.Inv_isTrue(Target.Program.Go(true, true))); //should log true,true,NaN,0

                /* should log:
                 * 3, NaN, 0
                 * 2, NaN, 0
                 * 1, NaN, 0
                 * 0, true, 0
                 */
                //asserts.Add(() => Assert.Inv_isFalse(() => TargetSample.Program.Go(3)));

                /* should log:
                 * 3, NaN, 1
                 * 2, NaN, 1
                 * 1, NaN, 1
                 * 0, true, 1
                 */
                //asserts.Add(() => Assert.Inv_ThrowsException(() => TargetSample.Program.Go(3)));

            }
            //Assert.Inv_AssertAll(asserts);
        }

    }


}

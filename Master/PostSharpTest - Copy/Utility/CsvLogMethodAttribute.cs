using System.Collections.Generic;
using System.Text;
using PostSharp.Aspects;
using PostSharp.Serialization;

namespace InvariantSynthesis.Utility
{
    /// <summary>
    ///     Aspect that, when applied to a method, appends a record to the <see cref="Logger" /> class whenever this method is
    ///     executed.
    /// </summary>
    [PSerializable]
    [LinesOfCodeAvoided(6)]
    public sealed class CsvLogMethodAttribute : OnMethodBoundaryAspect
    {
        private const bool Success = true;
        private const bool Failure = false;
        private const char Separator = ',';

        private static List<Trace> buffer = new List<Trace>(); 
            
        /// <summary>
        ///     Method invoked before the target method is executed.
        /// </summary>
        /// <param name="args">Method execution context.</param>
        public override void OnEntry(MethodExecutionArgs args)
        {
        }


        /// <summary>
        ///     Method invoked after the target method has successfully completed.
        /// </summary>
        /// <param name="args">Method execution context.</param>
        public override void OnSuccess(MethodExecutionArgs args)
        {
            var methodName = args.Method.Name;
            if (!IsAssertMethod(methodName)) //normal method, sample it
            {
                var sb = GetInputsOutputString(args);
                buffer.Add(new Trace(GetMethodFullName(args), sb.ToString()));
            }
            else //successful test method, mark all samples with success
            {
                FlushBufferWithClass(methodName, Success);
            }
        }

        /// <summary>
        ///     Method invoked when the target method has failed.
        /// </summary>
        /// <param name="args">Method execution context.</param>
        public override void OnException(MethodExecutionArgs args)
        {
            var methodName = args.Method.Name;
            if (!IsAssertMethod(methodName)) //normal method, sample it with failure
            {
                var sb = GetInputsOutputString(args);
                sb.Append(Failure.ToString());
                CsvLogger.WriteLine(GetMethodFullName(args), sb.ToString());
            }
            else //successful test method, mark all samples with failure
            {
                FlushBufferWithClass(methodName, Failure);
            }


        }

        private static string GetMethodFullName(MethodExecutionArgs args)
        {
            return args.Method.DeclaringType + "." + args.Method.Name;
        }

        private static StringBuilder GetInputsOutputString(MethodExecutionArgs args)
        {
            var c = args.Arguments.Count;
            var sb = new StringBuilder();
            for (var i = 0; i < c; i++)
            {
                sb.Append(args.Arguments.GetArgument(i).ToString() + Separator);
            }
//            sb.Append(args.ReturnValue);
            return sb;
        }

        private static bool IsAssertMethod(string methodName)
        {
            return methodName.StartsWith("Inv_");
        }

        private static void FlushBufferWithClass(string methodName, bool _class)
        {
            foreach (var trace in buffer)
            {
                CsvLogger.WriteLine(trace.MethodFullName, trace.Line + _class);
            }
            buffer = new List<Trace>();
        }
    }

    class Trace
    {
        public Trace(string methodFullName , string line)
        {
            MethodFullName = methodFullName;
            Line = line;
        }
        public string MethodFullName { get; set; }
        public string Line { get; set; }
    }
}
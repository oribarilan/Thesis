using System.Collections.Generic;
using System.Diagnostics;
using System.Reflection;
using System.Security.Policy;
using System.Text;
using InvariantSynthesis.LoggedUtility;
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
        private const char Success = '1';
        private const char Failure = '0';
        private const char Separator = ',';
        private static List<string> _testMethodNames = new List<string>(); 

        private static List<Trace> buffer = new List<Trace>(); 
            
        /// <summary>
        ///     Method invoked before the target method is executed.
        /// </summary>
        /// <param name="args">Method execution context.</param>
        public override void OnEntry(MethodExecutionArgs args)
        {
        }

        public override void OnExit(MethodExecutionArgs args)
        {
        }

        /// <summary>
        ///     Method invoked after the target method has successfully completed.
        /// </summary>
        /// <param name="args">Method execution context.</param>
        public override void OnSuccess(MethodExecutionArgs args)
        {
            Tracer.WriteLine($"OnSuccess: {GetMethodFullName(args)}, Arguments and output: {GetInputsOutputString(args)}");
            var methodName = args.Method.Name;
            if (IsFlushMethod(methodName))
            {
                Tracer.WriteLine($"OnSuccess: {GetMethodFullName(args)} is flush method, flushing buffer");
                FlushBufferWithClass(methodName);
            }
            else if (!IsAssertMethod(methodName)) //normal method, sample it
            {
                Tracer.WriteLine($"OnSuccess: {GetMethodFullName(args)} is not assert method");
                var sb = GetInputsOutputString(args);
                var trace = new Trace(GetMethodFullName(args), sb.ToString());
                buffer.Add(trace);
                Tracer.WriteLine($"OnSuccess: added to buffer: {trace}");
            }
            else //successful test method, mark all samples with success
            {
                Tracer.WriteLine($"OnSuccess: {GetMethodFullName(args)} is assert method, do nothing");
            }
        }

        /// <summary>
        ///     Method invoked when the target method has failed.
        /// </summary>
        /// <param name="args">Method execution context.</param>
        public override void OnException(MethodExecutionArgs args)
        {
            Tracer.WriteLine($"OnException: {GetMethodFullName(args)}, Arguments and output: {GetInputsOutputString(args)}");
            var methodName = args.Method.Name;
            if (IsFlushMethod(methodName))
            {
                Tracer.WriteLine($"OnException: {GetMethodFullName(args)} is flush method, flushing buffer");
                FlushBufferWithClass(methodName);
            }
            else if (!IsAssertMethod(methodName)) //normal method, sample it
            {
                Tracer.WriteLine($"OnException: {GetMethodFullName(args)} is not assert method");
                var sb = GetInputsOutputString(args, triggeredOnException: true);
                var trace = new Trace(GetMethodFullName(args), sb.ToString());
                buffer.Add(trace);
                Tracer.WriteLine($"OnException: added to buffer: {trace}");
            }
            else //Is an assert method, do nothing
            {
                Tracer.WriteLine($"OnException: {GetMethodFullName(args)} is assert method, do nothing");
            }
        }

        private static string GetMethodFullName(MethodExecutionArgs args)
        {
            return args.Method.DeclaringType + "." + args.Method.Name;
        }

        private static StringBuilder GetInputsOutputString(MethodExecutionArgs args, bool triggeredOnException = false)
        {
            var c = args.Arguments.Count;
            var sb = new StringBuilder();
            for (var i = 0; i < c; i++)
            {
                sb.Append(args.Arguments.GetArgument(i).ToString() + Separator);
            }
            if (!triggeredOnException) //log output value normally, void for a void method
            {
                sb.Append(args.ReturnValue);
            }
            else //exception was thrown, log NaN
            {
                sb.Append("NaN");
            }
            return sb;
        }

        private static bool IsAssertMethod(string methodName)
        {
            if (_testMethodNames.Count == 0)
            {
                var t = (typeof(InvariantSynthesis.LoggedUtility.Assert));
                MethodInfo[] methods = t.GetMethods();
                foreach (var method in methods)
                {
                    _testMethodNames.Add(method.Name);
                }
            }
            return _testMethodNames.Contains(methodName);
        }

        private static bool IsFlushMethod(string methodName)
        {
            return methodName.StartsWith("Inv_AssertAll");
        }

        private static void FlushBufferWithClass(string methodName)
        {
            foreach (var trace in buffer)
            {
                Tracer.WriteLine($"FlushBufferWithClass: {methodName} flushing buffer with class: {trace.Cluster}");
                CsvLogger.WriteLine(trace.MethodFullName, trace.Line + ',' + trace.Cluster);
            }
            Tracer.WriteLine($"FlushBufferWithClass: {methodName} finished flushing");
            buffer = new List<Trace>();
        }

        public static List<Trace> CollectFreeTraces()
        {
            List<Trace> traces = new List<Trace>();
            foreach (var trace in buffer)
            {
                if (!trace.Occupied)
                {
                    traces.Add(trace);
                    trace.Occupied = true;
                }
            }
            return traces;
        }

        public static void ClassifyTraces(List<Trace> traces, char _class)
        {
            foreach (var trace in traces)
            {
                trace.Cluster = _class;
            }
        }
    }

    public class Trace
    {
        public readonly char MissingCluster= 'm';
        public Trace(string methodFullName , string line)
        {
            MethodFullName = methodFullName;
            Line = line;
            Cluster = MissingCluster;
            Occupied = false;
        }
        public string MethodFullName { get; set; }
        public string Line { get; set; }
        public char Cluster { get; set; }
        public bool Occupied { get; set; }
        public override string ToString()
        {
            return $"Name: {MethodFullName}, Line: {Line}, Cluster: {Cluster}";
        }
    }
}
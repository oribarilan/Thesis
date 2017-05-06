using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using InvariantSynthesis.Utility;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace InvariantSynthesis.LoggedUtility
{
    public class Assert
    {
        private const char Success = '1';
        private const char Failure = '0';

        private static List<Action> _assertions;

        public Assert()
        {
            _assertions = new List<Action>();
        }

        public static void Restart()
        {
            _assertions = new List<Action>();
        }

        public static void AreEqual(int a, int b)
        {
            List<Utility.Trace> traces = CsvLogMethodAttribute.CollectFreeTraces();
            Action act = delegate
            {
                if (!a.Equals(b))
                {
                    CsvLogMethodAttribute.ClassifyTraces(traces, Failure);
                    throw new AssertFailedException();
                }
                CsvLogMethodAttribute.ClassifyTraces(traces, Success);
            };
            _assertions.Add(act);
        }

        public static void IsTrue(bool a)
        {
            List<Utility.Trace> traces = CsvLogMethodAttribute.CollectFreeTraces();
            Action act = delegate
            {
                if (!a)
                {
                    CsvLogMethodAttribute.ClassifyTraces(traces,Failure);
                    throw new AssertFailedException();
                }
                CsvLogMethodAttribute.ClassifyTraces(traces, Success);
            };
            _assertions.Add(act);
        }

        public static void IsFalse(bool a)
        {
            IsTrue(!a);
        }

        public static void Inv_ThrowsException(Action act)
        {
            try
            {
                act();
                // exception was not thrown, this is invalid
                throw new AssertFailedException();
            }
            catch
            {
                // exception was thrown, this is valid
            }
        }

        public static void Inv_AssertAll()
        {
            var errors = new List<Exception>();

            foreach (var assertion in _assertions)
            {
                try
                {
                    assertion();
                }
                catch (Exception ex)
                {
                    errors.Add(ex);
                }                
            }

            if (errors.Any())
            {
                var ex = new AssertFailedException(
                    string.Join(Environment.NewLine, errors.Select(e => e.Message)),
                    errors.First());
                
                // Use stack trace from the first exception to ensure first
                // failed Assert is one click away
                ReplaceStackTrace(ex, errors.First().StackTrace);

                throw ex;
            }
        }

        static void ReplaceStackTrace(Exception exception, string stackTrace)
        {
            var remoteStackTraceString = typeof(Exception)
                .GetField("_remoteStackTraceString",
                    BindingFlags.Instance | BindingFlags.NonPublic);

            remoteStackTraceString.SetValue(exception, stackTrace);
        }
    }
}
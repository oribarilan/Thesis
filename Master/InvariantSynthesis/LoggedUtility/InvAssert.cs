using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace InvariantSynthesis.LoggedUtility
{
    public static class Assert
    {
        public static void Inv_AreEqual(int a, int b)
        {
            if (!a.Equals(b))
            {
                throw new AssertFailedException();
            }
        }

        public static void Inv_AssertAll(params Action[] assertions)
        {
            var errors = new List<Exception>();

            foreach (var assertion in assertions)
                try
                {
                    assertion();
                }
                catch (Exception ex)
                {
                    errors.Add(ex);
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
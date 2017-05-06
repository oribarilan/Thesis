using System;
using System.Collections.Generic;
using System.IO;
using System.Text;


namespace InvariantSynthesis.Utility
{
    /// <summary>
    ///     A logger that writes to a CSV file. This class is a singelton.
    /// </summary>
    public class CsvLogger
    {
        private const string Path = "C:/UniGit/Thesis/";
        private static CsvLogger _instance;

        private CsvLogger()
        {
        }

        public static CsvLogger Instance
        {
            get
            {
                if (_instance == null)
                {
                    _instance = new CsvLogger();
                }
                return _instance;
            }
        }

        public static void WriteLine(string methodName, string line)
        {
            Tracer.WriteLine($"Entered Csv Logger WriteLine. methodName: {methodName}, line: {line}");
            var p = GetPathForMethod(methodName);
            var f = new FileInfo(p);
            f.Directory.Create();
            using (var swr = new StreamWriter(new FileStream(p, FileMode.Append, FileAccess.Write), Encoding.UTF8))
            {
                swr.WriteLine(line);
            }
            Tracer.WriteLine($"Left Csv Logger WriteLine. methodName: {methodName}, line: {line}");
        }

        private static string GetPathForMethod(string methodName)
        {
            return (Path + "MethodsData/" + GetDateFolderName() + "/" + methodName).Replace(".", "_") + ".txt";
        }

        private static string GetDateFolderName()
        {
            return DateTime.Now.ToString("dd-MM-yyyy");
        }
    }
}

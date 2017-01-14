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
        private const string Path = "C:/Users/t-orbar/Documents/Visual Studio 2015/Projects/Masters/";
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
            var p = GetPathForMethod(methodName);
            var f = new FileInfo(p);
            f.Directory.Create();
            using (var swr = new StreamWriter(new FileStream(p, FileMode.Append, FileAccess.Write), Encoding.UTF8))
            {
                swr.WriteLine(line);
            }
        }

        private static string GetPathForMethod(string methodName)
        {
            return (Path + "MethodsData/" + GetDateFolderName() + "/" + methodName).Replace(".", "_") + ".txt";
        }

        private static string GetDateFolderName()
        {
            return DateTime.Now.ToString("dd-MM-yyyy");
        }

        private static void AddClassToAboveRows(string methodName, int count, string _class)
        {
            var p = GetPathForMethod(methodName);
            var f = new FileInfo(p);
            if (!f.Directory.Exists)
            {
                return;
            }
            var swr = new ReverseLineReader(GetPathForMethod(methodName));
            foreach(var line in swr)
            {
                if (line.EndsWith(","))
                {
                    
                }
            }
        }
    }
}

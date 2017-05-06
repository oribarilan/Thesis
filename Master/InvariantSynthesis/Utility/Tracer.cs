using System;
using System.Collections.Generic;
using System.IO;
using System.Text;


namespace InvariantSynthesis.Utility
{
    /// <summary>
    ///     A logger that writes to a CSV file. This class is a singelton.
    /// </summary>
    public class Tracer
    {
        private const string Path = "C:/UniGit/Thesis/";
        private static Tracer _instance;

        private Tracer()
        {
        }

        public static Tracer Instance
        {
            get
            {
                if (_instance == null)
                {
                    _instance = new Tracer();
                }
                return _instance;
            }
        }

        public static void WriteLine(string line)
        {
            var p = GetPathForMethod();
            var f = new FileInfo(p);
            if (f == null)
            {
                throw new NullReferenceException($"Can't open file: {f}");
            }
            f.Directory.Create();
            using (var swr = new StreamWriter(new FileStream(p, FileMode.Append, FileAccess.Write), Encoding.UTF8))
            {
                swr.WriteLine(GetTimestamp() + ":: " + line);
            }
        }

        private static string GetPathForMethod()
        {
            return (Path + "Traces/" + GetDateFolderName()) + ".txt";
        }

        private static string GetDateFolderName()
        {
            return DateTime.Now.ToString("dd-MM-yyyy");
        }

        private static string GetTimestamp()
        {
            return DateTime.Now.ToShortTimeString();
        }
    }
}

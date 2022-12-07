using System.Text;

string LoadInput(string path)
{
    using FileStream fs = File.OpenRead("input.txt");
    using StreamReader sr = new StreamReader(fs);
    return sr.ReadToEnd();
}

string input = LoadInput("input.txt");

Solver solver = new Solver();
foreach (char c in input)
{
    solver.ReceiveChar(c);
}
Console.WriteLine(solver.StartOfPacketLoc);
Console.WriteLine(solver.StartOfMessageLoc);


class Solver
{
    private readonly StringBuilder ReceiveBuffer = new StringBuilder();

    public int CharsProcessed { get => ReceiveBuffer.Length; }

    public int StartOfPacketLoc { get; private set; } = -1;
    private bool FoundPacketStart { get => StartOfPacketLoc != -1; }

    public int StartOfMessageLoc { get; private set; } = -1;
    private bool FoundMessageStart { get => StartOfMessageLoc != -1; }

    public void ReceiveChar(char input)
    {
        if (FoundPacketStart && FoundMessageStart)
        {
            return;
        }

        ReceiveBuffer.Append(input);
        if (!FoundPacketStart && ReceiveBuffer.Length >= 4)
        {
            string marker = ReceiveBuffer.ToString(ReceiveBuffer.Length - 4, 4);
            if (marker.Distinct().ToArray().Length == 4)
            {
                //Console.WriteLine(marker);
                StartOfPacketLoc = ReceiveBuffer.Length;
            }
        }

        if (!FoundMessageStart && ReceiveBuffer.Length >= 14)
        {
            string marker = ReceiveBuffer.ToString(ReceiveBuffer.Length - 14, 14);
            if (marker.Distinct().ToArray().Length == 14)
            {
                //Console.WriteLine(marker);
                StartOfMessageLoc = ReceiveBuffer.Length;
            }
        }
    }
}

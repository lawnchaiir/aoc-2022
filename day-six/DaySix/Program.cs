using System.Collections;

static string LoadInput(string path)
{
    using FileStream fs = File.OpenRead(path);
    using StreamReader sr = new StreamReader(fs);
    return sr.ReadToEnd();
}

string input = LoadInput("input.txt");

Solver solver = new Solver();
foreach (char c in input)
{
    solver.ReceiveChar(c);
    if (solver.DoneProcessing())
    {
        Console.WriteLine("Done!");
        break;
    }
}

Console.WriteLine(solver.StartOfPacketLoc);
Console.WriteLine(solver.StartOfMessageLoc);


class CircularBuffer<T> : IEnumerable<T>
{
    public int Count { get; private set; }

    private readonly T[] Buffer;
    public readonly int Capacity = 0;

    private int Head = 0;

    public CircularBuffer(int capacity)
    {
        Buffer = new T[capacity];
        Capacity = capacity;
    }

    public void Add(T item)
    {
        Buffer[Head] = item;
        Head = (Head + 1) % Capacity;
        Count = Math.Min(Count, Capacity);
    }

    public IEnumerator<T> GetEnumerator()
    {
        return ((IEnumerable<T>)Buffer).GetEnumerator();
    }

    IEnumerator IEnumerable.GetEnumerator()
    {
        return Buffer.GetEnumerator();
    }
}


class Solver
{
    public int CharsProcessed { get; private set; } = 0;
    public int StartOfPacketLoc { get; private set; } = -1;
    public int StartOfMessageLoc { get; private set; } = -1;

    private readonly CircularBuffer<char> PacketBuffer = new CircularBuffer<char>(4);
    private readonly CircularBuffer<char> MessageBuffer = new CircularBuffer<char>(14);

    // Not very robust for buffer sizes > 32, obviously, but for these problems,
    // I'm a little inclined to just optimize for the known case for fun
    private static bool IsBufferUnique(CircularBuffer<char> buffer)
    {
        int bitFlag = 0;
        foreach (char c in buffer)
        {
            int pos = c & 31; // ordinal alphabet position
            int flag = 1 << pos;
            if ((bitFlag & flag) != 0)
            {
                return false;
            }
            bitFlag |= flag;
        }
        return true;
    }

    public bool DoneProcessing()
    {
        return StartOfPacketLoc != -1 && StartOfMessageLoc != -1;
    }

    public void ReceiveChar(char input)
    {
        CharsProcessed += 1;

        PacketBuffer.Add(input);
        MessageBuffer.Add(input);

        if (StartOfPacketLoc == -1 && CharsProcessed >= PacketBuffer.Capacity && IsBufferUnique(PacketBuffer) )
        {
            StartOfPacketLoc = CharsProcessed;
        }

        if (StartOfMessageLoc == -1 && CharsProcessed >= MessageBuffer.Capacity && IsBufferUnique(MessageBuffer))
        {
            StartOfMessageLoc = CharsProcessed;
        }
    }
}

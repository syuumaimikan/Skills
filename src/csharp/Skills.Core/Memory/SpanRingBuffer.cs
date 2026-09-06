namespace Skills.Core.Memory
{
    using System;
    using System.Runtime.CompilerServices;
    using System.Threading;

    /// <summary>
    /// High-Performance Zero-Allocation Ring Buffer leveraging ReadOnlySpan and MemoryMarshal.
    /// </summary>
    public sealed class SpanRingBuffer<T> where T : struct
    {
        private readonly T[] _buffer;
        private readonly int _mask;
        private long _head;
        private long _tail;

        public SpanRingBuffer(int capacity)
        {
            if (capacity <= 0)
                throw new ArgumentOutOfRangeException(nameof(capacity));

            int powerOfTwo = 1;
            while (powerOfTwo < capacity)
                powerOfTwo <<= 1;

            _buffer = new T[powerOfTwo];
            _mask = powerOfTwo - 1;
            _head = 0;
            _tail = 0;
        }

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public bool TryEnqueue(in T item)
        {
            long currentTail = Volatile.Read(ref _tail);
            long currentHead = Volatile.Read(ref _head);

            if (currentTail - currentHead >= _buffer.Length)
                return false; // Full

            _buffer[currentTail & _mask] = item;
            Volatile.Write(ref _tail, currentTail + 1);
            return true;
        }

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public bool TryDequeue(out T item)
        {
            long currentHead = Volatile.Read(ref _head);
            long currentTail = Volatile.Read(ref _tail);

            if (currentHead >= currentTail)
            {
                item = default;
                return false; // Empty
            }

            item = _buffer[currentHead & _mask];
            Volatile.Write(ref _head, currentHead + 1);
            return true;
        }

        public int Count => (int)(Volatile.Read(ref _tail) - Volatile.Read(ref _head));
    }
}

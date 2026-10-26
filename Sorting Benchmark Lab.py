import random
import time
import matplotlib.pyplot as plt


def insertion_sort(a):
    a = a[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    result = []
    while left and right:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    return result + left + right


def quick_sort(a):
    if len(a) <= 1:
        return a
    pivot = a[len(a) // 2]
    less = [x for x in a if x < pivot]
    equal = [x for x in a if x == pivot]
    more = [x for x in a if x > pivot]
    return quick_sort(less) + equal + quick_sort(more)


algorithms = {
    "Insertion": insertion_sort,
    "Merge": merge_sort,
    "Quick": quick_sort,
    "sorted()": sorted,
}

sizes = [100, 1000, 10000]   # kept small so it runs fast
types = ["Sorted", "Reversed", "Random"]


def make_data(kind, n):
    if kind == "Sorted":
        return list(range(n))
    if kind == "Reversed":
        return list(range(n, 0, -1))
    return [random.randint(0, n) for _ in range(n)]


plt.figure(figsize=(14, 4))

for i, kind in enumerate(types):
    plt.subplot(1, 3, i + 1)
    for name, func in algorithms.items():
        times = []
        for n in sizes:
            data = make_data(kind, n)
            start = time.perf_counter()
            func(data)
            times.append(time.perf_counter() - start)
        print(kind, name, times)
        plt.plot(sizes, times, marker="o", label=name)
    plt.title(kind + " data")
    plt.xlabel("n")
    plt.ylabel("time (s)")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()

plt.tight_layout()
plt.savefig("result.png")
plt.show()

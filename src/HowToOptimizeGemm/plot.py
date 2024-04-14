import sys
import matplotlib.pyplot as plt
import numpy as np

# Indicate the number of floating point operations that can be executed
# per clock cycle
nflops_per_cycle = 16

# Indicate the number of processors being used (in case you are using a
# multicore or SMP)
nprocessors = 1

# Indicate the clock speed of the processor.  On a Linux machine this info
# can be found in the file /proc/cpuinfo
#
# Note: some processors have a "turbo boost" mode, which increases
# the peak clock rate...
#
GHz_of_processor = 3.22


class Parser:
    def __init__(self, file_name) -> None:
        self.attrs = {}
        with open(file_name) as file:
            self.toks = file.read().split()
            self.toksi = 0
            file.close()
            self.attrs = self.parse()

    def next(self):
        tok = self.toks[self.toksi]
        self.toksi += 1
        return tok

    def get_var_name(self):
        return self.next()

    def get_symbol(self, sym):
        tok = self.next()
        assert(tok == sym)
        return tok

    def get_value(self):
        value = None
        tok = self.next()
        if tok == '[':
            # list
            value = []
            tok = self.next()
            while not tok.startswith(']'):
                value.append(float(tok))
                tok = self.next()
        elif tok.startswith("'"):
            value = tok[1:-2]

        assert value != None
        return value

    def parse(self):
        res = {}
        while self.toksi < len(self.toks):
            var = self.get_var_name()
            self.get_symbol('=')
            val = self.get_value()
            res[var] = val
        return res

    def __getattr__(self, name):
        return self.attrs[name]


BASIC_FILENAMES = [
    "MMult0",
    "MMult1",
    "MMult2",
]

SINGLE_DOUBLE_FILENAMES = [
    "MMult_1x4_3",
    "MMult_1x4_4",
    "MMult_1x4_5",
    "MMult_1x4_6",
    "MMult_1x4_7",
    "MMult_1x4_8",
    "MMult_1x4_9",
]

BLOCK_DOUBLE_FILENAMES = [
    "MMult_4x4_3",
    "MMult_4x4_4",
    "MMult_4x4_5",
    "MMult_4x4_6",
    "MMult_4x4_7",
    "MMult_4x4_8",
    "MMult_4x4_9",
]

BLOCK_VECTOR_FILENAMES = [
    "MMult_4x4_10",
    "MMult_4x4_11",
    "MMult_4x4_12",
    "MMult_4x4_13",
    "MMult_4x4_14",
    "MMult_4x4_15",
]

if sys.argv[1] == "basic":
    title = "Basic"
    filenames = BASIC_FILENAMES
elif sys.argv[1] == "1block":
    title = "1d double blocks"
    filenames = SINGLE_DOUBLE_FILENAMES
elif sys.argv[1] == "basic1block":
    title = "Basic and 1d double blocks"
    filenames = BASIC_FILENAMES + SINGLE_DOUBLE_FILENAMES
elif sys.argv[1] == "2blockd":
    title = "2d double blocks"
    filenames = BLOCK_DOUBLE_FILENAMES
elif sys.argv[1] == "2blockv":
    title = "2d vector blocks"
    filenames = BLOCK_VECTOR_FILENAMES
elif sys.argv[1] == "2block":
    title = "All 2d blocks"
    filenames = BLOCK_DOUBLE_FILENAMES + BLOCK_VECTOR_FILENAMES
elif sys.argv[1] == "all":
    title = "All"
    filenames = BASIC_FILENAMES   \
        + SINGLE_DOUBLE_FILENAMES \
        + BLOCK_DOUBLE_FILENAMES  \
        + BLOCK_VECTOR_FILENAMES

max_gflops = nflops_per_cycle * nprocessors * GHz_of_processor;

fig, ax = plt.subplots()

for filename in filenames:
    results = Parser(f"output_{filename}.m")
    data = np.array(results.MY_MMult).reshape(-1, 3)
    x_limits = (data[0, 0], data[-1, 0])
    ax.plot(data[:, 0], data[:, 1], label=results.version, marker=".")

ax.set(xlabel='m = n = k', ylabel='GFLOPS',
       title=title)
ax.grid()
ax.legend(fontsize=8, loc="center right", bbox_to_anchor=(1.315, 0.5))
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])

ax.set_xlim(x_limits)
ax.set_ylim([0, max_gflops])

fig.savefig(f"result-chart-{sys.argv[1].lower()}.png")
plt.show()

from __future__ import print_function

import os
import shutil
import sys
import time
import math
import pickle
from collections import defaultdict
from heapq import heappush, heappop

INF = float('inf')

try:
   user_input = raw_input
except NameError:
   user_input = input

def int_ceil(f):
    return int(math.ceil(f))

##################################################

def get_python_version():
    return sys.version_info[0]


def read(filename):
    with open(filename, 'r') as f:
        return f.read()


def write(filename, string):
    with open(filename, 'w') as f:
        f.write(string)


def write_pickle(filename, data):
    # TODO: cannot pickle lambda or nested functions
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def read_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def safe_remove(p):
    if os.path.exists(p):
        os.remove(p)


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def safe_rm_dir(d):
    if os.path.exists(d):
        shutil.rmtree(d)

def clear_dir(d):
    safe_rm_dir(d)
    ensure_dir(d)

def get_file_path(file, rel_path):
    directory = os.path.dirname(os.path.abspath(file))
    return os.path.join(directory, rel_path)

def open_pdf(filename):
    import subprocess
    # import os
    # import webbrowser
    subprocess.Popen('open {}'.format(filename), shell=True)
    # os.system(filename)
    # webbrowser.open(filename)
    user_input('Display?')
    # safe_remove(filename)

##################################################

def elapsed_time(start_time):
    return time.time() - start_time

def get_length(sequence):
    if sequence is None:
        return INF
    return len(sequence)

def safe_zip(sequence1, sequence2):
    assert len(sequence1) == len(sequence2)
    return zip(sequence1, sequence2)

def get_mapping(sequence1, sequence2):
    return dict(safe_zip(sequence1, sequence2))

def invert_test(test):
    return lambda *args: not test(*args)

def flatten(iterable_of_iterables):
    return (item for iterables in iterable_of_iterables for item in iterables)

def find(test, sequence):
    for item in sequence:
        if test(item):
            return item
    return None

def find_unique(test, sequence):
    found, value = False, None
    for item in sequence:
        if test(item):
            if found:
                raise RuntimeError('Both elements {} and {} satisfy the test'.format(value, item))
            found, value = True, item
    if not found:
        raise RuntimeError('Unable to find an element satisfying the test')
    return value

def implies(a, b):
    return not a or b

def irange(start, end=None, step=1):
    if end is None:
        end = start
        start = 0
    n = start
    while n < end:
        yield n
        n += step

def argmin(function, sequence):
    values = list(sequence)
    scores = [function(x) for x in values]
    return values[scores.index(min(scores))]

def argmax(function, sequence):
    values = list(sequence)
    scores = [function(x) for x in values]
    return values[scores.index(max(scores))]

def invert_dict(d):
    return dict((v, k) for k, v in d.items())

##################################################

def print_solution(solution):
    plan, cost, evaluations = solution
    solved = plan is not None
    print()
    print('Solved: {}'.format(solved))
    print('Cost: {}'.format(cost))
    print('Length: {}'.format(get_length(plan)))
    print('Evaluations: {}'.format(len(evaluations)))
    if not solved:
        return
    for i, (name, args) in enumerate(plan):
        print('{}) {} {}'.format(i+1, name, ' '.join(map(str_from_object, args))))
    #    print('{}) {}{}'.format(i+1, name, str_from_object(tuple(args))))

##################################################

class Verbose(object): # TODO: use DisableOutput
    def __init__(self, verbose):
        self.verbose = verbose
    def __enter__(self):
        if not self.verbose:
            self.stdout = sys.stdout
            self.devnull = open(os.devnull, 'w')
            sys.stdout = self.devnull
            #self.stderr = sys.stderr
            #self.devnull = open(os.devnull, 'w')
            #sys.stderr = self.stderr
        return self
    def __exit__(self, type, value, traceback):
        if not self.verbose:
            sys.stdout = self.stdout
            self.devnull.close()
            #sys.stderr = self.stderr
            #self.devnull.close()

class TmpCWD(object):
    def __init__(self, temp_cwd):
        self.tmp_cwd = temp_cwd
    def __enter__(self):
        self.old_cwd = os.getcwd()
        os.chdir(self.tmp_cwd)
        return self
    def __exit__(self, type, value, traceback):
        os.chdir(self.old_cwd)

##################################################

class MockSet(object):
    def __init__(self, test=lambda item: True):
        self.test = test
    def __contains__(self, item):
        return self.test(item)

class HeapElement(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value
    def __lt__(self, other):
        return self.key < other.key
    def __iter__(self):
        return iter([self.key, self.value])

##################################################

def str_from_object(obj):  # str_object
    if type(obj) in [list]: #, np.ndarray):
        return '[{}]'.format(', '.join(str_from_object(item) for item in obj))
    if type(obj) == tuple:
        return '({})'.format(', '.join(str_from_object(item) for item in obj))
    if type(obj) == dict:
        return '{{{}}}'.format(', '.join('{}: {}'.format(str_from_object(key), str_from_object(obj[key])) \
                                  for key in sorted(obj.keys(), key=lambda k: str_from_object(k))))
    if type(obj) in (set, frozenset):
        return '{{{}}}'.format(', '.join(sorted(str_from_object(item) for item in obj)))
    #if type(obj) in (float, np.float64):
    #    obj = round(obj, 3)
    #    if obj == 0: obj = 0  # NOTE - catches -0.0 bug
    #    return '%.3f' % obj
    #if isinstance(obj, types.FunctionType):
    #    return obj.__name__
    return str(obj)

def str_from_tuple(tup):
    return str_from_object(tup)

def str_from_action(action):
    name, args = action
    return '{}{}'.format(name, str_from_object(tuple(args)))

def str_from_plan(plan):
    if plan is None:
        return str(plan)
    return str_from_object(list(map(str_from_action, plan)))

##################################################

def neighbors_from_orders(orders):
    incoming_edges = defaultdict(set)
    outgoing_edges = defaultdict(set)
    for v1, v2 in orders:
        incoming_edges[v2].add(v1)
        outgoing_edges[v1].add(v2)
    return incoming_edges, outgoing_edges


def topological_sort(vertices, orders, priority_fn=lambda v: 0):
    # Can also do a DFS version
    incoming_edges, outgoing_edges = neighbors_from_orders(orders)
    ordering = []
    queue = []
    for v in vertices:
        if not incoming_edges[v]:
            heappush(queue, HeapElement(priority_fn(v), v))
    while queue:
        v1 = heappop(queue).value
        ordering.append(v1)
        for v2 in outgoing_edges[v1]:
            incoming_edges[v2].remove(v1)
            if not incoming_edges[v2]:
                heappush(queue, HeapElement(priority_fn(v2), v2))
    return ordering

##################################################

def is_hashable(value):
    #return isinstance(value, Hashable) # TODO: issue with hashable and numpy 2.7.6
    try:
        hash(value)
    except TypeError:
        return False
    return True


def hash_or_id(value):
    #return id(value)
    try:
        hash(value)
        return value
    except TypeError:
        return id(value)
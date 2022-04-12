from typing import *
from dataclasses import dataclass
from collections import deque


@dataclass
class GenTask:
    generator: Generator


@dataclass
class GenResult:
    result: Any


class GenDriver:
    def __init__(self, generator: Generator):
        self.stack: Deque[Generator] = deque()
        self.stack.append(generator)
        self.consumed: bool = False

    def iter(self):
        if self.consumed:
            raise ReferenceError

        self.consumed = True

        currentGenerator: Generator = self.stack.pop()

        try:
            yieldedValue = next(currentGenerator)
        except StopIteration:
            return

        while True:
            try:
                while True:
                    if type(yieldedValue) == GenResult:
                        if not self.stack:
                            yield yieldedValue.result

                        else:
                            currentGenerator = self.stack.pop()
                            yieldedValue = currentGenerator.send(yieldedValue)
                            continue

                    elif type(yieldedValue) == GenTask:
                        self.stack.append(currentGenerator)
                        currentGenerator = yieldedValue.generator

                    else:
                        if not self.stack:
                            yield yieldedValue

                        else:
                            currentGenerator = self.stack.pop()
                            yieldedValue = currentGenerator.send(yieldedValue)
                            continue

                    yieldedValue = next(currentGenerator)

            except StopIteration:
                while True:
                    try:
                        if not self.stack:
                            return

                        currentGenerator = self.stack.pop()
                        yieldedValue = currentGenerator.send(StopIteration)
                        break

                    except StopIteration:
                        continue

    def run(self, result: bool = False):
        if result == True:
            return [x for x in self.iter()]

        elif result == False:
            for _ in self.iter():
                pass

        else:
            raise TypeError

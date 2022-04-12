from typing import *
from dataclasses import dataclass


@dataclass
class GenTask:
    generator: Generator


@dataclass
class GenResult:
    result: Any


class GenDriver:
    def __init__(self, generator: Generator):
        self.stack: List[Generator] = [generator]
        self.consumed: bool = False

    def iter(self):
        if self.consumed:
            raise ReferenceError

        self.consumed = True

        currentGenerator: Generator = self.stack[-1]

        try:
            yieldedValue = next(currentGenerator)
        except StopIteration:
            return

        while True:
            try:
                while True:
                    if type(yieldedValue) == GenResult:
                        if len(self.stack) > 1:
                            yieldedValue = self.stack[-2].send(yieldedValue)
                            self.stack.pop()
                            currentGenerator = self.stack[-1]
                            continue

                        else:
                            yield yieldedValue

                    elif type(yieldedValue) == GenTask:
                        currentGenerator = yieldedValue.generator
                        self.stack.append(currentGenerator)

                    else:
                        if len(self.stack) > 1:
                            yieldedValue = self.stack[-2].send(yieldedValue)
                            self.stack.pop()
                            currentGenerator = self.stack[-1]
                            continue

                        else:
                            yield yieldedValue

                    yieldedValue = next(currentGenerator)

            except StopIteration:
                while True:
                    try:
                        if len(self.stack) == 1:
                            return

                        self.stack.pop()
                        currentGenerator = self.stack[-1]
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

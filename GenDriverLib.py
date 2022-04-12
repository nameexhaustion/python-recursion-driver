from typing import *
from dataclasses import dataclass


@dataclass
class Result:
    result: Any


@dataclass
class GenTask:
    generator: Generator
    resultMode: str = "iter"
    externalGenerator: bool = False


@dataclass
class InternalTask:
    generator: Generator
    resultMode: str = "iter"
    resultList: List = None
    prevTask: "InternalTask" = None
    externalGenerator: bool = False

    def __post_init__(self):
        if self.resultMode == "list":
            self.resultList = []


@dataclass
class GenDriverLib:
    task: InternalTask
    consumed: bool = False

    @classmethod
    def fromTask(cls, task: GenTask) -> "GenDriverLib":
        return cls(task=(InternalTask(**task.__dict__)))

    def iter(self):
        if self.consumed:
            raise ReferenceError

        self.consumed = True

        try:
            yieldedValue = next(self.task.generator)

            while True:
                try:
                    if type(yieldedValue) == Result or self.task.externalGenerator:
                        if self.task.externalGenerator:
                            result = yieldedValue
                        else:
                            result = yieldedValue.result

                        if self.task.resultMode == "list":
                            self.task.resultList.append(result)

                        elif self.task.resultMode == "iter":
                            if self.task.prevTask is not None:
                                yieldedValue = self.task.prevTask.generator.send(
                                    yieldedValue
                                )
                                self.task = self.task.prevTask
                                continue

                            yield yieldedValue

                        elif self.task.resultMode == "none":
                            pass

                        else:
                            raise TypeError

                    elif type(yieldedValue) == GenTask:
                        newTask: InternalTask = InternalTask(
                            **yieldedValue.__dict__, prevTask=self.task
                        )
                        self.task = newTask

                    else:
                        raise TypeError

                    yieldedValue = next(self.task.generator)
                except StopIteration:
                    done = False
                    while True:
                        try:
                            if self.task.prevTask is not None:
                                if self.task.resultMode == "iter":
                                    yieldedValue = self.task.prevTask.generator.send(
                                        StopIteration
                                    )

                                elif self.task.resultMode == "list":
                                    yieldedValue = self.task.prevTask.generator.send(
                                        Result(result=self.task.resultList)
                                    )

                                else:
                                    yieldedValue = next(self.task.prevTask.generator)

                                self.task = self.task.prevTask
                            else:
                                done = True

                            break

                        except StopIteration:
                            continue

                    if done:
                        raise StopIteration

        except StopIteration:
            return

    def runSilently(self):
        for _ in self.iter():
            pass

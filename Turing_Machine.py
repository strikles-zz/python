#!/usr/bin/env python2

BLANK_SYMBOL = '0'
ZERO, ONE = '0', '1'
DIR_LEFT, DIR_RIGHT = 'l','r'
HALT = 'H'
A,B,C,D,E,F = 'A','B','C','D','E','F'

class Tape(object):
    def __init__(self, blank_symbol, dir_left, dir_right):
        self.blank_symbol, self.dir_left, self.dir_right = blank_symbol, dir_left, dir_right
        self.tape = [blank_symbol]
        self.index = 0

    def __repr__(self):
        return ''.join(symbol for symbol in self.tape)

    def read(self):
        return self.tape[self.index]

    def write(self, symbol):
        self.tape[self.index] = symbol

    def wind(self, direction):
        if direction == self.dir_left:
            self.index -= 1
            if self.index < 0:
                self.index = 0
                self.tape.insert(0, self.blank_symbol)
        elif direction == self.dir_right:
            self.index += 1
            if self.index >= len(self.tape):
                self.tape.append(self.blank_symbol)

class Transition(object):
    def __init__(self, transition):
        self.transition = transition

    def __repr__(self):
        return self.transition.__repr__()

    def get_write_symbol(self):
        return self.transition[0]

    def get_next_direction(self):
        return self.transition[1]

    def get_next_state(self):
        return self.transition[2]

class TransitionTable(object):
    def __init__(self, *args):
        self.ttable = dict(args)

    def __repr__(self):
        return self.ttable.__repr__()

    def lookup(self, state, read_symbol):
        return Transition(self.ttable[state+read_symbol])

class TuringMachine(object):
    def __init__(self, tape, transition_table, state, halt_state):
        self.tape = tape
        self.ttable = transition_table
        self.state = state
        self.halt_state = halt_state
        self.steps = 0

    def __repr__(self):
        return self.tape.__repr__()

    def update_state(self):
        transition = self.ttable.lookup(self.state, self.tape.read())
        self.tape.write(transition.get_write_symbol())
        self.state = transition.get_next_state()
        self.tape.wind(transition.get_next_direction())
        self.steps += 1

    def run(self, halt_state):
        print self
        while self.state != self.halt_state:
            self.update_state()
            print self
        print "Completed in %d steps." % self.steps

def busy_beaver_table(n):
    if n == 1:
        return TransitionTable(tuple([A+ZERO,ONE+DIR_RIGHT+HALT]))
    elif n == 2:
        return TransitionTable(
                tuple([A+ZERO,ONE+DIR_RIGHT+B]),
                tuple([B+ZERO,ONE+DIR_LEFT+A]),
                tuple([A+ONE,ONE+DIR_LEFT+B]),
                tuple([B+ONE,ONE+DIR_RIGHT+HALT]))
    elif n == 3:
        return TransitionTable(
                tuple([A+ZERO, ONE+DIR_RIGHT+B]),
                tuple([B+ZERO, ZERO+DIR_RIGHT+C]),
                tuple([C+ZERO, ONE+DIR_LEFT+C]),
                tuple([A+ONE, ONE+DIR_RIGHT+HALT]),
                tuple([B+ONE, ONE+DIR_RIGHT+B]),
                tuple([C+ONE, ONE+DIR_LEFT+A]))
    elif n == 4:
        return TransitionTable(
                tuple([A+ZERO, ONE+DIR_RIGHT+B]),
                tuple([B+ZERO, ONE+DIR_LEFT+A]),
                tuple([C+ZERO, ONE+DIR_RIGHT+HALT]),
                tuple([D+ZERO, ONE+DIR_RIGHT+D]),
                tuple([A+ONE, ONE+DIR_LEFT+B]),
                tuple([B+ONE, ZERO+DIR_LEFT+C]),
                tuple([C+ONE, ONE+DIR_LEFT+D]),
                tuple([D+ONE, ZERO+DIR_RIGHT+A]))
    elif n == 5:
        return TransitionTable(
                tuple([A+ZERO, ONE+DIR_LEFT+B]),
                tuple([B+ZERO, ONE+DIR_RIGHT+C]),
                tuple([C+ZERO, ONE+DIR_LEFT+A]),
                tuple([D+ZERO, ONE+DIR_LEFT+A]),
                tuple([E+ZERO, ONE+DIR_RIGHT+HALT]),
                tuple([A+ONE, ONE+DIR_LEFT+A]),
                tuple([B+ONE, ONE+DIR_RIGHT+B]),
                tuple([C+ONE, ONE+DIR_RIGHT+D]),
                tuple([D+ONE, ONE+DIR_RIGHT+E]),
                tuple([E+ONE, ZERO+DIR_RIGHT+C]))

def main():
    tape = Tape(BLANK_SYMBOL, DIR_LEFT, DIR_RIGHT)
    n = 4
    ttable = busy_beaver_table(n)
    print "Running the busy beaver for %d states." % n
    tm = TuringMachine(tape, ttable, A, HALT)
    tm.run(HALT)

if __name__ == '__main__':
    main()

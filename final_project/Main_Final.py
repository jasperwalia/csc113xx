import string
from turtle import Turtle, Screen
from tkinter import *

fileList = []
probDic = {}
printDic = {}

class Category(object):
    def __init__(self, name=''):
        self.name = name
        self.freq = 0
        self.prob = 0.00

    def getName(self):
        return self.name

    def getFreq(self):
        return self.freq

    def getProb(self):
        return self.prob

    def countFreq(self):
        freq = 0
        for line in fileList:
            for char in line:
                self.freq += 1

    def readFile(self):
        with open("Words.txt", 'r') as file:
            fileList.extend(file.readlines())
            file.close()


    def print(self):
        print('{0:25} {1:20} {2}'.format("Character", "Frequency", "Probability"))
        print('{0:31} {1}'.format(self.name, self.getFreq()))


class LetterCategory(Category):
    def setName(self, name):
        self.name = name

    def getProb(self):
        return self.prob

    def calculateProb(self, totalFreq):
         self.prob = self.freq / totalFreq

    def countFreq(self):
        for line in range(len(fileList)):
            for char in range(len(fileList[line])):
                character = fileList[line][char].lower()
                if character == self.name:
                    self.freq += 1

    def putInProbDic(self):
        if self.prob != 0.0:
            probDic[self.name] = self.prob
        else:
            pass

    def print(self):
        print('{0} \t \t \t \t {1}  \t \t{2:3f} '.format(self.name, self.getFreq(), self.getProb()))


class NumberCategory(LetterCategory):
    def countFreq(self):
        count = 0
        for line in range(len(fileList)):
            for char in range(len(fileList[line])):
                character = fileList[line][char]
                if character.isdigit():
                    count += 1
        self.freq = count

    def print(self):
        print('{0:10}{1:10}{2:3f}'.format(self.name, self.getFreq(), self.getProb()))

class SymbolCategory(LetterCategory):
    def countFreq(self):
        count = 0
        for line in range(len(fileList)):
            for char in range(len(fileList[line])):
                character = fileList[line][char]
                if character in string.punctuation:
                    count += 1
        self.freq = count

    def print(self):
       print('{0:10}{1:20}{2:3f}'.format(self.name, self.getFreq(), self.getProb()))


class SpaceCategory(LetterCategory):
    def countFreq(self):
        count = 0
        for line in range(len(fileList)):
            for char in range(len(fileList[line])):
                character = fileList[line][char]
                if character in string.whitespace:
                    count += 1
        self.freq = count

    def print(self):
       print('{0:10}{1:10}{2:3f}'.format(self.name, self.getFreq(), self.getProb()))


class OtherLettersCategory(LetterCategory):
    def setFreq(self, freq):
        self.freq = freq

    def calculateProb(self, ptotalvalue):
        self.prob = abs(1.00 - ptotalvalue)

    def print(self):
       print('{0:10}{1:10}{2:3f}'.format(self.name, self.getFreq(), self.getProb()))

totalProb = 0.00
# total frequency
total = Category('total')
total.readFile()
total.countFreq()
total.print()
totalFreq = total.getFreq()

# probability of each appeared alphabet in the file
letterList = [LetterCategory() for char in string.ascii_lowercase]
count = 0
for letter in letterList:
    letter.setName(string.ascii_lowercase[count])
    letter.countFreq()
    letter.calculateProb(totalFreq)
    letter.putInProbDic()
    letter.print()
    count += 1
    totalProb += letter.getProb()

# probability of numeral
number = NumberCategory('numeral')
number.countFreq()
number.calculateProb(totalFreq)
number.putInProbDic()
totalProb += number.getProb()

# probability of symbol
symbol = SymbolCategory('symbol')
symbol.countFreq()
symbol.calculateProb(totalFreq)
symbol.putInProbDic()
totalProb += symbol.getProb()

# probability of whitespace
space = SpaceCategory('whitespace')
space.countFreq()
space.calculateProb(totalFreq)
space.putInProbDic()
totalProb += space.getProb()

# print the status
print('%r' % number.name,'%24r' % number.getFreq(),'%32r' % number.getProb())
print('%r' % symbol.name,'%25r' % symbol.getFreq(),'%33r' % symbol.getProb())
print('%r' % space.name,'%21r' % space.getFreq(),'%32r' % space.getProb())


# draw the pie chart by the number that user input
def enter():
    # get user input from the entry box
    string = entry_box.get().strip()
    amount=int(string)
    ptotalvalue = 0
    for number in range(amount):
        key_max = max(probDic.keys(), key=(lambda k: probDic[k]))
        printDic[key_max] = probDic[key_max]
        ptotalvalue += probDic[key_max]
        del probDic[key_max]

    # probability of other letters
    other = OtherLettersCategory('Other Letters')
    other.calculateProb(ptotalvalue)
    other.putInProbDic()
    printDic['Other Letter'] = probDic['Other Letters']

    # function to cycle colors for piechart
    def cycle(iterable):
        # cycle('ABCD') --> A B C D A B C D A B C D ...
        saved = []
        for element in iterable:
            yield element
            saved.append(element)
        while saved:
            for element in saved:
                yield element

    # colors to use
    PALETTE = ['#B1B5C8', '#BFD5E2', '#C7EBF0', '#B0D0D3', '#C08497',
               '#F7AF9D', '#F7E3AF', '#FF70A6', '#FF9770', '#FFD670',
               '#E9FF70', '#D6FFF6', '#87D68D', '#FFBE0B', '#FF006E',
               '#4F6D7A', '#947EB0', '#F9DEC9', '#4DCCBD', '#2374AB',
               '#FF8484', '#FFB8D1', '#FCA17D', '#BCEBCB']

    PALETTE = cycle(PALETTE)

    # pie chart properties
    LENGTH = 310
    LABEL_LENGTH = LENGTH * 1.15

    # the pie slices
    LetterFreq = printDic.items()
    total = sum(fraction for _, fraction in LetterFreq)

    # commands for turtle
    piechart = Turtle()
    piechart.penup()
    piechart.sety(-LENGTH)

    # set speed to max
    piechart.speed(0)

    # window properties
    screen = Screen()
    screen.screensize()
    screen.setup(width = 1.0, height = 1.0)
    screen.title("Probability of letter n in Words.txt")

    # create pie slices
    for _, fraction in LetterFreq:
        piechart.fillcolor(next(PALETTE))
        piechart.begin_fill()
        piechart.circle(LENGTH, fraction * 360 / total)
        position = piechart.position()
        piechart.goto(0, 0)
        piechart.end_fill()
        piechart.setposition(position)

    # create labels
    piechart.sety(-LABEL_LENGTH)

    for char, count in LetterFreq:
        piechart.circle(LABEL_LENGTH, count * 360 / total / 2)
        piechart.write((char, round(count, 4)), align="center", font=("Times New Roman", 10, "normal"))
        #continue slice
        piechart.circle(LABEL_LENGTH, count * 360 / total / 2)

    screen.exitonclick()


# create a window to get user input
root = Tk()
root.title("Pie Chart")
root.geometry("500x200")
heading = Label(root,text="Enter a number to show the n highest element in the pie chart", font=("arial", 12, "bold"),fg="black")
heading.pack()
entry_box = Entry(root)
entry_box.pack()
work = Button(root, text="Enter",width=5,bg="white",command=enter).place(x=220,y=50)
root.mainloop()

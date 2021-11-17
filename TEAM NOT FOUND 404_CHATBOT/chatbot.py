from fuzzywuzzy import fuzz
import csv
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

bot = ChatBot("Chat Bot")

trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english.greetings", "chatterbot.corpus.english.conversations")


class CafeteriaBot(object):
    def __init__(self):
        self.dataset = []
        self.orderList = []

        self.functionality = dict({
            "Introduce": self.introduce,
            "Tell me about": self.introduce,
            "What do you have": self.introduce,
            "Menu" : self.introduce,
            "How much": self.price,
            "Price" : self.price,
            "Order": self.order,
            "Buy" : self.order,
            "Purchase": self.order,
            "Help": self.help,
            "Assist": self.help,
            "Aid" : self.help,
            "Question" : self.help,
            "Enquiry" : self.help,
            "Recipe": self.receipt,
            "That's all": self.receipt
        })

        self.id = 0

        with open("food_list.csv") as csvfile:
            content = csv.reader(csvfile)
            
            for entry in content:
                self.dataset.append(entry)

        with open('order.csv', 'r') as orderCsv:
            content = csv.reader(orderCsv)
            header = next(content)
            if header != None:
                for entry in content:
                    if self.id <= int(entry[0]):
                        self.id = int(entry[0]) + 1


        self.question = "Help"
        self.response = ""
        self.data = []

    def getInput(self, question):
        temp = 0
        
        for i in self.functionality:
            similarity = fuzz.WRatio(i, question)
            if similarity > temp:
                self.question = i
                temp = similarity

        self.confidence = temp

        print("Match (%s) with (%s): %d\n" % (self.question, question, temp))
        if self.confidence > 50:
            self.getData(question)

    def getData(self, question):
        temp = 0
        for i in self.dataset:
            food = i[1]
            similarity = fuzz.token_set_ratio(food, question)
            if similarity > temp:
                    self.data = i
                    temp = similarity

        print("Match (%s) with (%s): %d\n" % (self.data[1], question, temp))

        print(self.data)

        self.confidence = (self.confidence + temp) / 2
        
    def getResponse(self):
        print(self.question)
        if self.confidence > 50:
            response = self.functionality[self.question]()
        else:
            response = str(bot.get_response(self.question))
        return response

    # Below are the functionalities of the chatbot
    def introduce(self):
        if self.data[-1] == "yes":
            delivery = "available"
        else:
            delivery = "not available"

        message = "The %s from %s stall cost RM %s and the delivery service is %s\n" % (self.data[1], self.data[0], self.data[2], delivery)
        response = message
        return response

    def price(self):
        message = "The %s from %s stall cost RM %s\n" % (self.data[1], self.data[0], self.data[2])
        response = message
        return response
    
    def order(self):
        number = 1
        message = "Ok, I have added your order: %d %s - RM %s <br>What else would you like to order?" % (number, self.data[1], number * float(self.data[2]))
        response = message
        data = [self.id, self.data[1], number, self.data[0], number * float(self.data[2])]
        with open('order.csv', 'a') as orderCsv:
            orderWriter = csv.writer(orderCsv, lineterminator='\n') 
            orderWriter.writerow(data)
        self.orderList.append(data)
        return response

    def help(self):
        message = "Help: I am a chatbot for you to take food order <br> I know the details of food in our cafeteria so you can ask 'How much' or 'Introduce' <br> I can also help you to take order so try 'Order' when you have decided what to eat"
        return message 

    def receipt(self):
        counter = 0
        message = "Here is your receipt: <br>No. Stall Item Number Price<br>"
        for i in self.orderList:
            line = "%d. %s Stall %s %s %s <br>" % (counter, i[3], i[1], i[2], i[-1])
            message = message + line
            counter += 1
        return message
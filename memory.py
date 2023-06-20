class Memory:
    def __init__(self, messages=[], data = None):
        self.messages = messages
        self.data = data

    def initMemory(self, messages, data):
        self.messages = messages
        self.data = data

    def replaceData(self, data):
        self.data = data

    def appendMessages(self, messages):
        self.messages.append(messages)

    def getData(self):
        return self.data
    
    def getMessages(self):
        return self.messages


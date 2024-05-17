class Message:
    def __init__(self, sender, receiver, content):
        self.sender = sender
        self.receiver = receiver
        self.content = content

    def get_sender(self):
        return self.sender

    def get_receiver(self):
        return self.receiver

    def get_content(self):
        return self.content

    def set_sender(self, sender):
        self.sender = sender

    def set_receiver(self, receiver):
        self.receiver = receiver

    def set_content(self, content):
        self.content = content

    def __str__(self):
        s = "from " + self.sender.get_id() + " to " + self.receiver.get_id()
        return s

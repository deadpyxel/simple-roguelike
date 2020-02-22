import textwrap

import tcod as libtcod


class Message:
    """Message class. Holds game message definitions
    """

    def __init__(self, text: str, color: libtcod.Color = libtcod.white):
        """MEssage initializer
        
        Arguments:
            text {str} -- The text for the message
        
        Keyword Arguments:
            color {libtcod.Color} -- Color to be used in rendering (default: {libtcod.white})
        """
        self.text = text
        self.color = color


class MessageLog:
    """MessageLog class. Holds UI message log definitions
    """

    def __init__(self, x: int, width: int, height: int):
        """MessageLog intializer
        
        Arguments:
            x {int} -- x position to start rendering message log
            width {int} -- width for the message log
            height {int} -- height for the message log
        """
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message: Message):
        """Adds new function to the log
        
        Arguments:
            message {Message} -- Message object to be added to the log
        """        
        # Auto split text in case it overflows width attribute
        new_msg_lines = textwrap.wrap(message.text, width=self.width)

        for line in new_msg_lines:
            # If the buffer is full, use FIFO strategy to clear the buffer
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))

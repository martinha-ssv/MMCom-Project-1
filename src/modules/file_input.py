import parser
import numpy as np

class InputFile():
    def __init__(self, file: str) -> None:
        self.full_text = ''
        with open(file) as f:
            self.full_text = f.readlines()

    def contentToDict(self):
        headings = [i for i in range(len(self.full_text)) if parser.isHeading(self.full_text[i])]
        for i in range(len(headings)):
            heading_index = headings[i]
            next_heading_index = headings[i+1] if i+1 < len(headings) else len(self.full_text)
            heading = parser.getHeading(self.full_text[heading_index])
            heading_content = self.full_text[heading_index+1:next_heading_index]
        


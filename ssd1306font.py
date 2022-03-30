

class Display_font():
    def __init__(self, file):
        try:
            f = open(file, "r")
        except OSError:
            self.font = None
            return
        # Bypass lines where 1st char is space. These are comment lines.
        line = f.readline()
        while line[0] == " ":
            line = f.readline()
            
        char = line[0]    # a non-space character
        font = {" ": [" ", " ", " "]}   # insert a space character to start
        more = True
        self.font_height = 0

        while more:
            new_char, char_list, more = self._gather_lines(f)
            font[char] = char_list
            char = new_char
        self.font = font        
        
    def _gather_lines(self, f):
        char_list = []
        
        while True:
            line = f.readline()
            if len(line) == 0:                # EOF, return char_list only.
                return None, char_list, False

            if line[0] == " ": # font "pixel" line
                font_line = line[1:-1]   # trim off leading space & last \n character
                self.font_height = max(self.font_height, len(font_line))
                char_list.append(font_line) 
            else:              # new char in col 1
                return line[0], char_list, True # we have new font char in col 1.
    
if __name__ == "__main__":
    display = Display_font("font28.txt")
    if display.font is None:
        print("File not found. Abandoning!")
    print(display.font_height)
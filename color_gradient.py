class ColorGradient:
    def __init__(self, start_color, end_color):
        self.start_color = start_color
        self.end_color = end_color

    def get_blended_color(self, scalar):
        # Calculate the RGB values for the blended color
        blended_red = self.start_color[0] + (self.end_color[0] - self.start_color[0]) * scalar
        blended_green = self.start_color[1] + (self.end_color[1] - self.start_color[1]) * scalar
        blended_blue = self.start_color[2] + (self.end_color[2] - self.start_color[2]) * scalar

        blended_red = int(blended_red)
        blended_green = int(blended_green)
        blended_blue = int(blended_blue)

        # Return the blended color as a tuple
        return (blended_red, blended_green, blended_blue)
    
    def to_hex(self, color):
        return '#%02x%02x%02x' % color
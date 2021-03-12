class TextSpaceLimit:
    def __init__(self, font_size, horizontal_scale, line_length_limits):
        self.font_size = font_size
        self.horizontal_scale = horizontal_scale
        self.line_length_limits = line_length_limits
        self.line_count = len(line_length_limits)

import numpy
# import quad

class Integrate:
    def __init__(self, function):
        self.function = function
        self.error = 0
        self.sign = 0
    
    def integral(self, lower, upper, precision=10000):
        if lower > upper:
            lower, upper, = upper, lower
            self.sign = -1
        number_of_points = (upper - lower) * precision
        xs = np.linspace(lower, upper, int(number_of_points))
        integral = 0
        super_sum = 0
        sub_sum = 0
        for index in tqdm(range(len(xs) - 1)):
            delta = xs[index + 1] - xs[index]
            try:
                y1 = self.function(xs[index])
                sub_area = y1 * delta
                y2 = self.function(xs[index + 1])
                super_area = y2 * delta

                area = (y2 + y1) / 2 * delta
                integral += area
                sub_sum += sub_area
                super_sum += super_area
            except ZeroDivisionError:
                print(f"\nAvoided pole")

        self.error = super_sum - sub_sum
        return self.sign * integral
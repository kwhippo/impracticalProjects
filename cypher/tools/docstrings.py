import math


class SimpleEquation:
    """
    A class to define a simple equation.

    """
    def demo(self, a, b, c):
        """
        Accept 3 integers and return result of mathematical equation.

        :return: two roots
        :param int a: a quadratic coefficient
        :param int b: linear coefficient
        :param int c: free term
        """
        d = math.sqrt(abs(b ** 2 - 4 * a * c))
        root1 = (-b + d) / (2 * a)
        root2 = (-b - d) / (2 * a)
        return root1, root2


def main():
    """Takes no arguments and print hello world."""
    print('Hello world')


if __name__ == '__main__':
    main()

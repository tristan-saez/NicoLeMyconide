"""

Bar class used to display Nico' status

"""

from math import ceil
import pygame as pg
from src.item import Item


class Bar(Item):
    """

    Class is used for creating bar item, for loading screen or stats

    :param coordinates: location on the screen of the bar item
    :param size: the size of bar item
    :param img: the image of bar item
    :param value: maximum value for the bar item
    """

    def __init__(self, coordinates: list, size: list, img: str, value: int = 3) -> None:
        super().__init__(coordinates, size)

        # fill_value is a float between 0 and 3 which
        self.fill_value = value
        # Special state able "visual bar change"
        # like lightning (0) -> moon (1) when Nico is sleeping
        self.special_state = 0
        self.bar_img = "assets/" + img + "0.png"
        # color bar able the game to have special bar fill texture not only simple color
        # This one is preloaded because the color bar is updated a lot more than image bar
        self.color_bar = pg.image.load(
            "assets/bar_lvl_" + str(round(value)) + ".png"
        ).convert_alpha()

    def display(self, screen: pg.display) -> None:
        """

        Display the bar item on the screen

        :param screen: the pygame.display element for the game
        """
        screen.blit(pg.image.load(self.bar_img).convert_alpha(), self.coordinates)
        pg.display.flip()

        self.update(screen, (self.fill_value, self.special_state))

    def update(self, screen: pg.display, args: tuple = (None, -1)) -> None:
        """

        Update the bar item on the screen

        :param screen: the pygame.display element for the game
        :param args: used to update state,
        value or both (state change bar visual, value change visual pourcentage)
        """
        if args[0]:
            self.update_values(args[0])
        if args[1] != -1:
            self.update_state(args[1])
        self.update_on_screen(screen)

    def update_values(self, value: float) -> None:
        """

        Update bar value to passed value

        :param value: the new bar value
        """
        self.fill_value = value
        self.color_bar = pg.image.load(
            "assets/bar_lvl_"
            + str(3 if ceil(value) > 3 else (1 if ceil(value) < 1 else ceil(value)))
            + ".png"
        ).convert_alpha()

    def update_state(self, state: int) -> None:
        """

        Update bar state to passed state (e.g change lightning to moon for energy)

        :param state: new bar state
        """
        self.bar_img = self.bar_img.replace(str(self.special_state) + ".png", str(state) + ".png")
        self.special_state = state

    def update_on_screen(self, screen: pg.display) -> None:
        """

        Update bar on the screen

        :param screen: the pygame.screen element for the game
        """
        cropped_region = (1, 1, (self.fill_value / 3 * 120), 32)

        screen.blit(self.color_bar, self.coordinates, cropped_region)

        screen.blit(pg.image.load(self.bar_img).convert_alpha(), self.coordinates)
        pg.display.flip()

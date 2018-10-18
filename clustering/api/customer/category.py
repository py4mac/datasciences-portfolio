# -*- coding: utf-8 -*-
"""

This module is in charge of category mapping for customer segmentation.
It provides API to get class 'real name' from a class number.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""


class Category:
    """Category class definition
    """

    CATEGORY_UNKNOWN = "unknown"

    def __init__(self):
        self.__cat_mapping = [
                        'discrete',
                        self.CATEGORY_UNKNOWN,
                        self.CATEGORY_UNKNOWN,
                        'gold',
                        self.CATEGORY_UNKNOWN,
                        'loyal',
                        self.CATEGORY_UNKNOWN,
                        'cold',
                    ]
        """array: Category mapping.

        The category is composed of the 4 'real name'.
        """

    def get_name(self, index):
        # Sanity check for index value.
        if (index < 0) or (index > (len(self.__cat_mapping) - 1)):
            return self.CATEGORY_UNKNOWN
        return self.__cat_mapping[index]

"""Reference weights for the empirical dietary inflammatory index (EDII).

Primary source:
Tabung FK, Smith-Warner SA, Chavarro JE, et al. Development and Validation of
an Empirical Dietary Inflammatory Index. J Nutr. 2016;146(8):1560-1570.

Implementation note:
The published EDII is formed by summing 18 weighted food-group intakes and
dividing the total by 1000 to keep the final score on an interpretable scale.
Inputs are expected as servings per day aligned to the paper's food-group
definitions.
"""

from __future__ import annotations


EDII_REFERENCE = {
    "processed_meat": {"weight": 165.03, "direction": "pro"},
    "red_meat": {"weight": 140.19, "direction": "pro"},
    "organ_meat": {"weight": 144.61, "direction": "pro"},
    "other_fish": {"weight": 252.45, "direction": "pro"},
    "other_vegetables": {"weight": 136.14, "direction": "pro"},
    "refined_grains": {"weight": 81.21, "direction": "pro"},
    "high_energy_beverages": {"weight": 156.85, "direction": "pro"},
    "low_energy_beverages": {"weight": 94.77, "direction": "pro"},
    "tomatoes": {"weight": 167.92, "direction": "pro"},
    "beer": {"weight": -136.99, "direction": "anti"},
    "wine": {"weight": -249.70, "direction": "anti"},
    "tea": {"weight": -42.25, "direction": "anti"},
    "coffee": {"weight": -83.18, "direction": "anti"},
    "dark_yellow_vegetables": {"weight": -165.37, "direction": "anti"},
    "leafy_green_vegetables": {"weight": -190.29, "direction": "anti"},
    "snacks": {"weight": -45.08, "direction": "anti"},
    "fruit_juice": {"weight": -58.95, "direction": "anti"},
    "pizza": {"weight": -1175.21, "direction": "anti"},
}

EDII_VARIABLE_ORDER = tuple(EDII_REFERENCE.keys())

EDII_COMPONENT_OUTPUT_NAMES = {
    "processed_meat": "PROCESSED_MEAT",
    "red_meat": "RED_MEAT",
    "organ_meat": "ORGAN_MEAT",
    "other_fish": "OTHER_FISH",
    "other_vegetables": "OTHER_VEGETABLES",
    "refined_grains": "REFINED_GRAINS",
    "high_energy_beverages": "HIGH_ENERGY_BEVERAGES",
    "low_energy_beverages": "LOW_ENERGY_BEVERAGES",
    "tomatoes": "TOMATOES",
    "beer": "BEER",
    "wine": "WINE",
    "tea": "TEA",
    "coffee": "COFFEE",
    "dark_yellow_vegetables": "DARK_YELLOW_VEGETABLES",
    "leafy_green_vegetables": "LEAFY_GREEN_VEGETABLES",
    "snacks": "SNACKS",
    "fruit_juice": "FRUIT_JUICE",
    "pizza": "PIZZA",
}


__all__ = [
    "EDII_COMPONENT_OUTPUT_NAMES",
    "EDII_REFERENCE",
    "EDII_VARIABLE_ORDER",
]

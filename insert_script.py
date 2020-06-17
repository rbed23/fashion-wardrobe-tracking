from fashion_wardrobe_tracker.users.models import User
from fashion_wardrobe_tracker.users.models import User
from fashion_wardrobe_tracker.wardrobe.models import Color
from fashion_wardrobe_tracker.wardrobe.models import Fit
from fashion_wardrobe_tracker.wardrobe.models import ShoesFit
from fashion_wardrobe_tracker.wardrobe.models import LowerPattern
from fashion_wardrobe_tracker.wardrobe.models import UpperPattern
from fashion_wardrobe_tracker.wardrobe.models import LowerStyle
from fashion_wardrobe_tracker.wardrobe.models import UpperStyle
from fashion_wardrobe_tracker.wardrobe.models import Material
from fashion_wardrobe_tracker.wardrobe.models import ShoesMaterial
from fashion_wardrobe_tracker.wardrobe.models import ShoesPattern
from fashion_wardrobe_tracker.wardrobe.models import ShoesStyle
from fashion_wardrobe_tracker.wardrobe.models import Size
###

from fashion_wardrobe_tracker import app, db
from fashion_wardrobe_tracker.logger import ROOT_LOGGER_CONFIG


if __name__ == "__main__":

    add_list = [
        'XXS',
        'XS',
        'S',
        'M',
        'L',
        'XL',
        'XXL',
        'XXXL'
    ]

    with app.app_context():
        print('in app')
        for each in add_list:
            print(each)
            fit = Size.create(size=each)

from functools import partial

round_ = partial(round, ndigits=2)


class SpaceAge(object):
    def __init__(self, seconds):
        self.seconds = seconds

    def earth_year(self):
        return self.seconds / 31557600

    def on_earth(self):
        return round_(self.earth_year())

    def on_mercury(self):
        return round_(self.earth_year() / 0.2408467)

    def on_venus(self):
        return round_(self.earth_year() / 0.61519726)

    def on_mars(self):
        return round_(self.earth_year() / 1.8808158)

    def on_jupiter(self):
        return round_(self.earth_year() / 11.862615)

    def on_saturn(self):
        return round_(self.earth_year() / 29.447498)

    def on_uranus(self):
        return round_(self.earth_year() / 84.016846)

    def on_neptune(self):
        return round_(self.earth_year() / 164.79132)


'''Another good solution:使用此解决方案时，IDE不能自动补全
class SpaceAge(object):

    PLANET_RATIOS = [(k, v * 31557600) for k, v in (
        ('earth', 1.0),
        ('mercury', 0.2408467),
        ('venus', 0.61519726),
        ('mars', 1.8808158),
        ('jupiter', 11.862615),
        ('saturn', 29.447498),
        ('uranus', 84.016846),
        ('neptune', 164.79132)
    )]

    def __init__(self, seconds):
        self.seconds = seconds
        for planet, ratio in self.PLANET_RATIOS:
            setattr(self, 'on_' + planet, self._planet_years(ratio))

    def _planet_years(self, ratio):
        return lambda ratio=ratio: round(self.seconds / ratio, 2)
'''

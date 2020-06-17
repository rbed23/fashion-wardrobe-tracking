from fashion_wardrobe_tracker.data import CRUDMixin, db


class Site(CRUDMixin, db.Model):
    __tablename__ = 'tracking_site'

    base_url = db.Column(db.String(120))
    visits = db.relationship('Visit', backref='site', lazy='select')
    user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))

    def __repr__(self):
        return f'<Site {self.id}: {self.base_url}>'

    def __str__(self):
        return self.base_url


class Visit(CRUDMixin, db.Model):
    __tablename__ = 'tracking_visit'

    browser = db.Column(db.String(120))
    date = db.Column(db.DateTime)
    event = db.Column(db.String(120))
    url = db.Column(db.String(120))
    ip_address = db.Column(db.String(120))
    location = db.Column(db.String(120))
    latitude = db.Column(db.String(120))
    longitude = db.Column(db.String(120))
    site_id = db.Column(db.Integer, db.ForeignKey('tracking_site.id'))

    def __repr__(self):
        r = f'<Visit for site ID {self.site_id}: {self.url} on {self.date}>'
        return r




class Wardrobe(db.Model, CRUDMixin):
    __tablename__ = "wardrobe"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProfileID = db.Column(db.Integer, db.ForeignKey('users_profile.id'))
    name = db.Column(db.String(120))

    profile = db.relationship("Profile", back_populates='wardrobe')
    uppers = db.relationship('Upper', back_populates='wardrobe')
    lowers = db.relationship('Lower', back_populates='wardrobe')
    footers = db.relationship('Shoes', back_populates='wardrobe')

    def __repr__(self):
        return f"<Wardrobe ID: {self.id}>"


class Upper(CRUDMixin, db.Model):
    __tablename__ = "wardrobe_upper"

    id = db.Column(db.Integer, primary_key=True)
    WardrobeID = db.Column(db.Integer, db.ForeignKey('wardrobe.id'))
    wardrobe = db.relationship("Wardrobe", back_populates='uppers')

    brand = db.Column(db.String(120))
    style = db.Column(db.String(120))
    collar = db.Column(db.Boolean)
    size = db.Column(db.String(10))
    year = db.Column(db.Integer)
    pattern = db.Column(db.String(120))
    color_1 = db.Column(db.String(120))
    color_2 = db.Column(db.String(120))
    color_3 = db.Column(db.String(120))
    fit = db.Column(db.String(120))
    material = db.Column(db.String(120))
    stretch = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Upper ID: {self.id}>"

    def __iter__(self):
        yield 'brand', self.brand
        yield 'style', self.style
        yield 'collar', self.collar
        yield 'size', self.size
        yield 'year', self.year
        yield 'pattern', self.pattern
        yield 'colors:', [self.color1, self.color2, self.color3]
        yield 'fit', self.fit
        yield 'material', self.material
        yield 'stretch', self.stretch


class UpperStyle(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(120))


class UpperPattern(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    pattern = db.Column(db.String(120))



class Lower(CRUDMixin, db.Model):
    __tablename__ = "wardrobe_lower"

    id = db.Column(db.Integer, primary_key=True)
    WardrobeID = db.Column(db.Integer, db.ForeignKey('wardrobe.id'))
    wardrobe = db.relationship("Wardrobe", back_populates='lowers')

    brand = db.Column(db.String(120))
    style = db.Column(db.String(120))
    waist = db.Column(db.Integer)
    inseam = db.Column(db.Integer)
    year = db.Column(db.Integer)
    pattern = db.Column(db.String(120))
    color_1 = db.Column(db.String(120))
    color_2 = db.Column(db.String(120))
    color_3 = db.Column(db.String(120))
    fit = db.Column(db.String(120))
    material = db.Column(db.String(120))
    stretch = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Lower ID: {self.id}>"

    def __iter__(self):
        yield 'brand', self.brand
        yield 'style', self.style
        yield 'waist', self.waist
        yield 'inseam', self.inseam
        yield 'year', self.year
        yield 'pattern', self.pattern
        yield 'colors:', [self.color1, self.color2, self.color3]
        yield 'fit', self.fit
        yield 'material', self.material
        yield 'stretch', self.stretch


class LowerStyle(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(120))


class LowerPattern(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    pattern = db.Column(db.String(120))



class Color(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(120))


class Fit(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    fit = db.Column(db.String(120))


class Material(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String(120))


class Size(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(120))



class Shoes(CRUDMixin, db.Model):
    __tablename__ = "wardrobe_shoes"

    id = db.Column(db.Integer, primary_key=True)
    WardrobeID = db.Column(db.Integer, db.ForeignKey('wardrobe.id'))
    wardrobe = db.relationship("Wardrobe", back_populates='footers')

    brand = db.Column(db.String(120))
    style = db.Column(db.String(120))
    size = db.Column(db.Float(10))
    year = db.Column(db.Integer)
    pattern = db.Column(db.String(120))
    color_1 = db.Column(db.String(120))
    color_2 = db.Column(db.String(120))
    color_3 = db.Column(db.String(120))
    fit = db.Column(db.String(120))
    material = db.Column(db.String(120))

    def __repr__(self):
        return f"<Shoes ID: {self.id}>"

    def __iter__(self):
        yield 'brand', self.brand
        yield 'style', self.style
        yield 'size', self.size
        yield 'year', self.year
        yield 'pattern', self.pattern
        yield 'colors:', [self.color1, self.color2, self.color3]
        yield 'fit', self.fit
        yield 'material', self.material


class ShoesStyle(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(120))


class ShoesPattern(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    pattern = db.Column(db.String(120))

class ShoesFit(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    fit = db.Column(db.String(120))

class ShoesMaterial(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String(120))


'''
class Underwear(CRUDMixin, db.Model):
'''

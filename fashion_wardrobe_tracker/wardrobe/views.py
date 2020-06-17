from flask import abort, Blueprint, current_app, flash, jsonify, Markup, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..data import query_to_list
from ..helpers import generate_selection
from .forms import WardrobeForm
from .models import Wardrobe, Upper, Lower, Shoes
from .models import UpperStyle, UpperPattern
from .models import LowerStyle, LowerPattern
from .models import ShoesStyle, ShoesPattern, ShoesFit, ShoesMaterial
from .models import Color, Fit, Material, Size
from ..users.models import Profile
from .geodata import get_geodata


wardrobe = Blueprint("wardrobe", __name__)


@wardrobe.route("/")
def index():
    current_app.logger.info('welcome home')
    return render_template("index.html")


@wardrobe.route("/wardrobe", methods=("POST", "GET"))
def landing(user_id=None):
    if current_user.is_anonymous:
        return render_template('users/login.html')

    wardrobe_form = WardrobeForm()
    wardrobe_form.uppers.style.choices = generate_selection(UpperStyle, 'style')
    wardrobe_form.uppers.pattern.choices = generate_selection(UpperPattern, 'pattern')
    wardrobe_form.uppers.color1.choices = generate_selection(Color, 'color')
    wardrobe_form.uppers.color2.choices = generate_selection(Color, 'color')
    wardrobe_form.uppers.color3.choices = generate_selection(Color, 'color')
    wardrobe_form.uppers.fit.choices = generate_selection(Fit, 'fit')
    wardrobe_form.uppers.material.choices = generate_selection(Material, 'material')
    wardrobe_form.uppers.size.choices = generate_selection(Size, 'size')
        
    wardrobe_form.lowers.style.choices = generate_selection(LowerStyle, 'style')
    wardrobe_form.lowers.pattern.choices = generate_selection(LowerPattern, 'pattern')
    wardrobe_form.lowers.color1.choices = generate_selection(Color, 'color')
    wardrobe_form.lowers.color2.choices = generate_selection(Color, 'color')
    wardrobe_form.lowers.color3.choices = generate_selection(Color, 'color')
    wardrobe_form.lowers.fit.choices = generate_selection(Fit, 'fit')
    wardrobe_form.lowers.material.choices = generate_selection(Material, 'material')
    wardrobe_form.lowers.size.choices = generate_selection(Size, 'size')
    
    wardrobe_form.footers.style.choices = generate_selection(ShoesStyle, 'style')
    wardrobe_form.footers.pattern.choices = generate_selection(ShoesPattern, 'style')
    wardrobe_form.footers.color1.choices = generate_selection(Color, 'color')
    wardrobe_form.footers.color2.choices = generate_selection(Color, 'color')
    wardrobe_form.footers.color3.choices = generate_selection(Color, 'color')
    wardrobe_form.footers.fit.choices = generate_selection(ShoesFit, 'fit')
    wardrobe_form.footers.material.choices = generate_selection(ShoesMaterial, 'material')


    if request.method == 'GET' and wardrobe_form.validate():
        print(wardrobe_form.name)
        return redirect('index')
    if wardrobe_form.validate_on_submit():
        wardrobe = Wardrobe.create(**wardrobe_form.data)
        flash(f"Added Wardrobe: {wardrobe.id}")
        return redirect(url_for("wardrobe_form.user", user_id=current_user.id))

    print(wardrobe_form.errors)

    return render_template("validation_error.html",
                                form=wardrobe_form)


@wardrobe.route("/wardrobe/<int:user_id>")
@login_required
def wardrobe_user(user_id=None):
    if not user_id:
        return redirect(url_for('landing', user_id=user_id))
    profile = Profile.query.filter(Profile.UserID==user_id).first()
    if not profile:
        abort(401)
    wardrobe = Wardrobe.query.filter(Wardrobe.ProfileID==profile.id).first()
    if not wardrobe:
        return redirect(url_for('landing', user_id=user_id))
    if not wardrobe.ProfileID == profile.id and\
            not profile.UserID == current_user.id:
        abort(401)

    
    query = Wardrobe.query.filter(Wardrobe.ProfileID == profile.id).first()
    data = query_to_list(query)
    print(data)
    return render_template("wardrobe/wardrobe.html",
                                visits=data,
                                site=data,
                                title=data)


@wardrobe.route("/visit", methods=("POST", ))
@wardrobe.route("/site/<int:site_id>/visit", methods=("GET", "POST",))
def add_visit(site_id=None):
    if site_id is None:
        # This is only used by the visit_form on the index page.
        form = VisitForm()
    else:
        site = Site.query.get_or_404(site_id)
        
        browser = request.headers.get("User-Agent")
        url = request.values.get('url') or request.headers.get("Referer")
        event = request.values.get('event')
        ip_addr = request.access_route[0] or request.remote_addr
        geodata = get_geodata(ip_addr)
        location = f"{geodata.get('city')}, {geodata.get('zipcode')}, {geodata.get('country')}"


        # WTForms does not coerce obj or keyword arguments
        # (otherwise, we could just pass in `site=site_id`)
        # CSRF is disabled in this case because we will *want*
        # users to be able to hit the /site/:id endpoint from other sites.

        form = VisitForm(
            csrf_enabled=False,
            site=site,
            browser=browser,
            url=url,
            ip_address=ip_addr,
            latitude=geodata.get('latitude'),
            longitude=geodata.get('longitude'),
            location=location,
            event=event)

    if form.validate():
        visit = Visit.create(**form.data)
        flash(f"Added visit for site {visit}")
        return '', 204

    return jsonify(errors=form.errors), 400


@wardrobe.route("/sites", methods=("GET", "POST"))
@login_required
def view_sites():

    form = SiteForm()

    if form.validate_on_submit():
        Site.create(owner=current_user, **form.data)
        flash("Added Site")
        return redirect(url_for(".view_sites"))

    query = Site.query.filter(Site.user_id == current_user.id)
    data = query_to_list(query)
    results = []

    # The header row should not be linked
    try:
        results = [next(data)]
        for row in data:
            row = [_make_link(cell) if i == 0 else cell
                for i, cell in enumerate(row)]
            results.append(row)

    except StopIteration:
        pass # no sites registered

    return render_template("tracking/sites.html", sites=results, form=form)


_LINK = Markup('<a href="{url}">{name}</a>')


def _make_link(site_id):
    url = url_for(".view_site_visits", site_id=site_id)
    return _LINK.format(url=url, name=site_id)

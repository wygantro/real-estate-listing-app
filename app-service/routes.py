from app import app, db, login_manager
from flask import request, render_template, flash, redirect, url_for, session
from models import *
from forms import *
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
#from flask_cachecontrol import cache#, cache_for, dont_cache, Always
#https://pypi.org/project/Flask-CacheControl/

@app.route('/')
#@cache_for(hours=10)
def index():
  #favorite listing count side bar
  if current_user.is_authenticated:
    user_id = current_user.id
    favorite_len = len(User_listing.query.filter(User_listing.user_id==user_id).all())
  else:
    favorite_len = False
  return render_template('landing_page.html',
                         favorite_len=favorite_len)

@app.route('/contact')
def contact():
  #favorite listing count side bar
  if current_user.is_authenticated:
    user_id = current_user.id
    favorite_len = len(User_listing.query.filter(User_listing.user_id==user_id).all())
  else:
    favorite_len = False
  return render_template('contact.html',
                         favorite_len=favorite_len)

@app.route('/terms_disclaimer')
def terms_disclaimer():
  #favorite listing count side bar
  if current_user:
    user_id = current_user.id
    favorite_len = len(User_listing.query.filter(User_listing.user_id==user_id).all())
  return render_template('terms_disclaimer.html',
                         favorite_len=favorite_len)

@app.route('/privacy')
def privacy():
  #favorite listing count side bar
  if current_user:
    user_id = current_user.id
    favorite_len = len(User_listing.query.filter(User_listing.user_id==user_id).all())
  return render_template('privacy.html',
                         favorite_len=favorite_len)

@app.route('/reset_password')
def reset_password():
  #favorite listing count side bar
  if current_user:
    user_id = current_user.id
    favorite_len = len(User_listing.query.filter(User_listing.user_id==user_id).all())
  return render_template('reset_password.html',
                         favorite_len=favorite_len)

@app.route('/manage_subscription/<user_id>', methods=['GET', 'POST'])
@login_required
def manage_subscription(user_id):  
  available_counties = County.query.filter(County.ACTIVE == True).all()
  forms = []
  for county in available_counties:
    form = CountySelectionForm(prefix=county.CTYNAME)
    form.county_selection.label = (str(county.CTYNAME) + ': ' + str(county.id))
    form.county_selection.data = bool(User_county.query.filter(User_county.user_id == current_user.id,
                                                               User_county.county_id == county.id).first())
    forms.append(form)

  for i, form in enumerate(forms):
    if form.submit.data and not form.county_selection.data:
      form.county_selection.data = True
      u_c = User_county(user_id = current_user.id,
                        county_id = available_counties[i].id)
      db.session().expire_on_commit = False
      db.session.add(u_c)
      try:
        db.session.commit()
      except:
        db.session.rollback()
        print('rollback@80')
      #db.session.close()
    elif form.submit.data and form.county_selection.data:
      form.county_selection.data = False   
      User_county.query.filter(User_county.user_id == current_user.id, 
                               User_county.county_id == available_counties[i].id).delete()
      db.session().expire_on_commit = False
      try:
        db.session.commit()
      except:
        db.session.rollback()
        print('rollback@90')
      #db.session.close()
  #subscription logic
  counties_selected = User_county.query.filter(User_county.user_id == current_user.id).all()
  user_counties_selected = []
  user_total_monthly = 0
  user_total_annual_monthly = 0
  for county in counties_selected:
    county_id = county.county_id
    county = db.session.get(County, county_id) 
    user_counties_selected.append(county)
    user_total_monthly += county.monthly_price
    user_total_annual_monthly += county.annual_monthly_price
  #yearly totals
  user_total_monthly_yearly = user_total_monthly * 12
  user_total_annual_yearly = user_total_annual_monthly * 12
  #initial user subscription option
  annual_payment_option=False
  monthly_payment_option=False
  forms_payment_selection = PaymentSelectionForm()
  #set and submit subscription selection to db
  if forms_payment_selection.validate_on_submit():
    if forms_payment_selection.payment_selection.data == 'annual':
      annual_payment_option=True
      for county in counties_selected:
        db.session().expire_on_commit = False
        county.yearly_subscribed = 1
        try:
          db.session.commit()
        except:
          db.session.rollback()
        county.monthly_subscribed = 0
        try:
          db.session.commit()
        except:
          db.session.rollback()
    if forms_payment_selection.payment_selection.data == 'monthly':
      monthly_payment_option=True
      for county in counties_selected:
        db.session().expire_on_commit = False
        county.monthly_subscribed = 1
        try:
          db.session.commit()
        except:
          db.session.rollback()
        county.yearly_subscribed = 0
        try:
          db.session.commit()
        except:
          db.session.rollback()
  #payment submit
  forms_payment = PaymentForm()
  #set and submit subscription selection to db
  if forms_payment.validate_on_submit():
    for county in counties_selected:
      #db.session().expire_on_commit = False
      county.payment_agreement = 1
      try:
        db.session.commit()
      except:
        db.session.rollback()
      county.subscribed_at_date = datetime.utcnow()
      try:
        db.session.commit()
      except:
        db.session.rollback()
    return redirect(url_for('listings', user_id=current_user.id))
  #favorite listing count side bar
  favorite_len = len(User_listing.query.filter(User_listing.user_id==user_id).all())
  return render_template('manage_subscription.html', 
                         forms=forms, 
                         available_counties=available_counties, 
                         user_counties_selected=user_counties_selected,
                         user_total_monthly=user_total_monthly,
                         user_total_annual_monthly=user_total_annual_monthly,
                         user_total_monthly_yearly=user_total_monthly_yearly,
                         user_total_annual_yearly=user_total_annual_yearly,
                         annual_payment_option=annual_payment_option,
                         monthly_payment_option=monthly_payment_option,
                         forms_payment_selection=forms_payment_selection,
                         forms_payment=forms_payment,
                         favorite_len=favorite_len)

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(user_name=form.user_name.data,
                email=form.email.data,
                occupation=form.occupation.data)
    user.set_password(form.password.data)
    db.session.add(user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
    #db.session.close()
    #flash('Thanks for registering')
    user = User.query.filter_by(email=form.email.data).first()
    if user and user.check_password_hash(form.password.data):
      login_user(user)
      return redirect(url_for('welcome'))
  return render_template('register.html', form=form)

@app.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
  user_id = current_user.id
  favorite_len = len(User_listing.query.filter(User_listing.user_id==user_id).all())
  return render_template('welcome.html',
                         favorite_len=favorite_len)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and user.check_password_hash(form.password.data):
      login_user(user, remember=form.remember_me.data)
      return redirect(url_for('listings', user_id=current_user.id))
    else:
      return redirect(url_for('login'))
  return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))

@app.route('/listings/<user_id>', methods=['GET', 'POST'])
@login_required
def listings(user_id):
  user_available_counties = User_county.query.filter(User_county.user_id == current_user.id).all() 
  available_listings_dict = {}
  for user_county in user_available_counties:
    county = db.session.get(County, user_county.county_id)
    if request.args.get('sort_listing'):
      sort_by = eval('Listing.' + str(request.args.get('sort_listing')))
      county_listings = Listing.query.filter(Listing.county_id == county.id).order_by(sort_by).all()
      #sort = True
    else:
      county_listings = Listing.query.filter(Listing.county_id == county.id).order_by(Listing.date_relisted_formatted).all()
    available_listings_dict[county] = county_listings
  listing_id = request.args.get('listing_id')
  if listing_id:
    listing_info = db.session.get(Listing, listing_id)   
  else:
    listing_info = False
  
  #favorite listing count side bar
  favorite_len = len(User_listing.query.filter(User_listing.user_id==user_id).all())
  return render_template('listings.html', 
                         available_listings_dict=available_listings_dict,
                         listing_info=listing_info,
                         favorite_len=favorite_len)

@app.route('/add_listing/<user_id>/<listing_id>', methods=['GET'])
@login_required
def add_listing(user_id, listing_id):
    listing_id=listing_id
    if User_listing.query.filter(User_listing.user_id==user_id, User_listing.listing_id==listing_id).all():
      return redirect(url_for('listings', user_id=current_user.id))
    else:
      u_l = User_listing(user_id = user_id,
                         listing_id = listing_id)
      db.session().expire_on_commit = False
      db.session.add(u_l)
    try:
      db.session.commit()
    except:
      db.session.rollback()
      #db.session.close()
    return redirect(url_for('listings', 
                            user_id=current_user.id,
                            listing_id=listing_id))

@app.route('/remove_listing/<user_id>/<listing_id>', methods=['GET'])
@login_required
def remove_listing(user_id, listing_id):
  User_listing.query.filter(User_listing.user_id == user_id, User_listing.listing_id == listing_id).delete()
  db.session().expire_on_commit = False
  try:
    db.session.commit()
  except:
    db.session.rollback()
    #db.session.close()
  return redirect(url_for('favorites', 
                          user_id=current_user.id))

@app.route('/favorites/<user_id>', methods=['GET', 'POST'])
@login_required
def favorites(user_id):
  user_available_listings = User_listing.query.filter(User_listing.user_id==user_id).all()
  favorite_len = len(user_available_listings)
  favorite_listings_lst = []
  for favorite_listing in user_available_listings:
    listing = db.session.get(Listing, favorite_listing.listing_id)
    favorite_listings_lst.append(listing)
  listing_id = request.args.get('listing_id')
  if listing_id:
    listing_info = db.session.get(Listing, listing_id)   
  else:
    listing_info = False
  
  if request.args.get('sort_listing'):
    sort_attribute = request.args.get('sort_listing')
  else:
    sort_attribute = ''
  return render_template('favorites.html',
                         favorite_len=favorite_len,
                         favorite_listings_lst=favorite_listings_lst, 
                         listing_info=listing_info,
                         sort_attribute=sort_attribute)

@app.route('/user_account/<user_id>', methods=['GET', 'POST'])
@login_required
def user_account(user_id):
  form = User_AccountForm()
  if form.validate_on_submit():
    current_user.user_name = form.user_name.data
    current_user.email = form.email.data
    current_user.email_weekly = form.email_weekly.data
    current_user.user_setting_option1 = form.user_setting_option1.data
    current_user.user_setting_option2 = form.user_setting_option2.data
    try:
        db.session.commit()
    except:
        db.session.rollback()
    #db.session.close()
    return redirect(url_for('index'))
  form.user_name.data = current_user.user_name
  form.email.data = current_user.email
  form.email_weekly.data = current_user.email_weekly
  form.user_setting_option1.data = current_user.user_setting_option1
  form.user_setting_option2.data = current_user.user_setting_option2
  #favorite listing count side bar
  favorite_len = len(User_listing.query.filter(User_listing.user_id==user_id).all())
  return render_template('user_account.html', 
                         form=form,
                         favorite_len=favorite_len)
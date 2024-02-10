from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
  __table_args__ = {'extend_existing': True}

  id = db.Column(db.Integer, primary_key=True)
  user_name = db.Column(db.String(64), index=True)
  email = db.Column(db.String(120), index=True, unique=True)
  occupation = db.Column(db.String(64), index=True)
  password_hash = db.Column(db.String(128))
  joined_at_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
  # account settings
  email_weekly = db.Column(db.Boolean, default=False, server_default="false", index=True)
  user_setting_option1 = db.Column(db.Boolean, default=False, server_default="false", index=True)
  user_setting_option2 = db.Column(db.Boolean, default=False, server_default="false", index=True)
  # relationships
  user_listings = db.relationship('User_listing', backref='user', lazy='dynamic', cascade = 'all, delete, delete-orphan')
  user_counties = db.relationship('User_county', backref='user', lazy='dynamic', cascade = 'all, delete, delete-orphan')

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
  
  def check_password_hash(self, password):
    return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

class Listing(db.Model):
  __table_args__ = {'extend_existing': True}

  id = db.Column(db.Integer, primary_key=True)
  property_address = db.Column(db.String(1000), index = True, unique = False)
  formatted_address = db.Column(db.String(1000), index = True, unique = False)
  street = db.Column(db.String(1000), index = True, unique = False)
  city = db.Column(db.String(1000), index = True, unique = False)
  zip_code = db.Column(db.String(1000), index = True, unique = False)
  lat = db.Column(db.String(100), index = False, unique = False)
  lng = db.Column(db.String(100), index = False, unique = False)
  FIPS_county = db.Column(db.Integer, index = False, unique = False)
  county_name = db.Column(db.String(70), index = False, unique = False)
  FIPS_state = db.Column(db.Integer, index = False, unique = False)
  state = db.Column(db.String(70), index = False, unique = False)
  confidence_api = db.Column(db.String(70), index = False, unique = False)
  estimated_value = db.Column(db.String(80), index = True, unique = False)
  equity = db.Column(db.String(80), index = False, unique = False)
  published_debt = db.Column(db.String(80), index = True, unique = False)
  date_debt_published = db.Column(db.String(150), index = False, unique = False)
  foreclosure_sale_date = db.Column(db.String(150), index = False, unique = False)
  redemption_period = db.Column(db.String(150), index = False, unique = False) # replace with date type later
  mortgagor_name = db.Column(db.String(150), index = False, unique = False) # replace with date type later
  foreclosing_assignee_mortgagee = db.Column(db.String(150), index = False, unique = False) # replace with date type later
  date_of_mortgage = db.Column(db.String(150), index = False, unique = False)
  foreclosing_attorney = db.Column(db.String(150), index = False, unique = False)
  listing_active = db.Column(db.Boolean, default=False, server_default="false", index=True)
  date_relisted_uploaded = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
  date_relisted_formatted = db.Column(db.String(150), index = False, unique = False)
  n_clicks = db.Column(db.Integer, index = False, unique = False)
  # relationships
  user_listings = db.relationship('User_listing', backref='listing', lazy='dynamic', cascade = 'all, delete, delete-orphan')
  image_files = db.relationship('Image_files', backref='listing', lazy='dynamic', cascade = 'all, delete, delete-orphan')
  county_id = db.Column(db.Integer, db.ForeignKey('county.id'), index=True)

class County(db.Model):
   __table_args__ = {'extend_existing': True}
   id = db.Column(db.Integer, primary_key=True)
   FIPS = db.Column(db.String(150), index = True, unique = False)
   STNAME = db.Column(db.String(150), index = True, unique = False)
   CTYNAME = db.Column(db.String(150), index = True, unique = False)
   LISTINGS_AVAILABLE = db.Column(db.Boolean, default=False, server_default="false", index=True)
   APPROVAL = db.Column(db.Boolean, default=False, server_default="false", index=True)
   ACTIVE = db.Column(db.Boolean, default=False, server_default="false", index=True)
   monthly_price = db.Column(db.Integer, index = False, unique = False)
   annual_monthly_price = db.Column(db.Integer, index = False, unique = False)
   # relationships
   listings = db.relationship('Listing', backref='county', lazy='dynamic', cascade = 'all, delete, delete-orphan')
   user_counties = db.relationship('User_county', backref='county', lazy='dynamic', cascade = 'all, delete, delete-orphan')

class User_listing(db.Model):
  #__table_args__ = {'extend_existing': True}
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)# primary_key=True)
  listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), index=True)# primary_key=True)

class User_county(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)# primary_key=True)
  county_id = db.Column(db.Integer, db.ForeignKey('county.id'), index=True)
  monthly_subscribed = db.Column(db.Boolean, default=False, server_default="false", index=True)
  #monthly_subscribed_at_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
  yearly_subscribed = db.Column(db.Boolean, default=False, server_default="false", index=True)
  payment_agreement = db.Column(db.Boolean, default=False, server_default="false", index=True)
  subscribed_at_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)

class Image_files(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))
   image_file_name = db.Column(db.String(100), index = True, unique = False)
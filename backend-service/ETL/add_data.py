# add_data.py

from app import db
from models import *
import pandas as pd
from datetime import datetime

current_datetime = datetime.now()

# add mock users
u1 = User(user_name='Rob Wygant',
          email='rob_55@example.com',
          occupation='Investor',
          password_hash='pw_test1')
db.session.add(u1)

u2 = User(user_name='Tom Harris',
          email='the_stranger@example.com',
          occupation='Home Buyer',
          password_hash='pw_test2')
db.session.add(u2)

u3 = User(user_name='Ann Addams',
          email='ann.adams@example.com',
          occupation='Lender',
          password_hash='pw_test3')
db.session.add(u3)

u4 = User(user_name='Sam Hill',
          email='sam.adams@example.com',
          occupation='Investor',
          password_hash='pw_test4')
db.session.add(u4)
db.session.commit()
print("mock users committed")

# add US country data from df_use_counties.csv
df_usa_counties = pd.read_csv('./dataframes/df_usa_counties.csv')

county_info_list = []
# iterate over each row
for i, rows in df_usa_counties.iterrows():
    # create list for the current row
    county_info = [rows.FIPS,
                   rows.STNAME,
                   rows.CTYNAME,
                   rows.LISTINGS_AVAILABLE,
                   rows.APPROVAL,
                   rows.ACTIVE]
    county_info_list.append(county_info)

for i in range(len(county_info_list)):
    c_i = County(id=county_info_list[i][0],
                 FIPS=county_info_list[i][0],
                 STNAME=county_info_list[i][1],
                 CTYNAME=county_info_list[i][2],
                 LISTINGS_AVAILABLE=county_info_list[i][3],
                 APPROVAL=county_info_list[i][4],
                 ACTIVE=county_info_list[i][5])
    db.session.add(c_i)
db.session.commit()
print("country data committed")


# add mock listing data from df_listings.csv
df_listings = pd.read_csv('./dataframes/df_listings.csv')
listings_info_list = []
# iterate over each row
for i, rows in df_listings.iterrows():
    # create list for the current row
    listing_info = [rows.property_address,  # property location info
                    rows.formatted_address,
                    rows.street,
                    rows.city,
                    rows.zip_code,
                    rows.lat,
                    rows.lng,
                    rows.FIPS_county,
                    rows.county_name,  # rows.county_name
                    rows.FIPS_state,
                    rows.state,
                    rows.confidence_api,
                    rows.estimated_value,  # financial info
                    rows.equity,
                    rows.published_debt,
                    rows.date_debt_published,
                    rows.foreclosure_sale_date,
                    rows.redemption_period,
                    rows.mortgagor_name,  # ownership info
                    rows.foreclosing_assignee_mortgagee,
                    rows.date_of_mortgage,
                    rows.foreclosing_attorney,
                    # rows.picture_url,
                    rows.listing_active,
                    rows.date_relisted,
                    rows.date_relisted_formatted]
    listings_info_list.append(listing_info)

for i in range(len(listings_info_list)):
    l_i = Listing(property_address=listings_info_list[i][0],
                  formatted_address=listings_info_list[i][1],
                  street=listings_info_list[i][2],
                  city=listings_info_list[i][3],
                  zip_code=listings_info_list[i][4],
                  lat=listings_info_list[i][5],
                  lng=listings_info_list[i][6],
                  county_id=listings_info_list[i][7],
                  FIPS_county=listings_info_list[i][7],
                  county_name=listings_info_list[i][8],
                  FIPS_state=listings_info_list[i][9],
                  state=listings_info_list[i][10],
                  confidence_api=listings_info_list[i][11],
                  estimated_value=listings_info_list[i][12],
                  equity=listings_info_list[i][13],
                  published_debt=listings_info_list[i][14],
                  date_debt_published=listings_info_list[i][15],
                  foreclosure_sale_date=listings_info_list[i][16],
                  redemption_period=listings_info_list[i][17],
                  mortgagor_name=listings_info_list[i][18],
                  foreclosing_assignee_mortgagee=listings_info_list[i][19],
                  date_of_mortgage=listings_info_list[i][20],
                  foreclosing_attorney=listings_info_list[i][21],
                  listing_active=listings_info_list[i][22],
                  date_relisted_formatted=current_datetime\
                    .strftime('%Y-%m-%d'),
                  n_clicks=0)
    db.session.add(l_i)
db.session.commit()
print("listing data committed")


# add mock image file data
i_f1 = Image_files(listing_id=3,
                   image_file_name='photo_file_3_1')
db.session.add(i_f1)

i_f2 = Image_files(listing_id=3,
                   image_file_name='photo_file_3_2')
db.session.add(i_f2)

i_f3 = Image_files(listing_id=3,
                   image_file_name='photo_file_3_3')
db.session.add(i_f3)

i_f4 = Image_files(listing_id=3,
                   image_file_name='photo_file_3_4')
db.session.add(i_f4)

i_f5 = Image_files(listing_id=5,
                   image_file_name='photo_file_5_1')
db.session.add(i_f5)

i_f6 = Image_files(listing_id=5,
                   image_file_name='photo_file_5_2')
db.session.add(i_f6)

i_f7 = Image_files(listing_id=26,
                   image_file_name='photo_file_26_1')
db.session.add(i_f7)

i_f8 = Image_files(listing_id=26,
                   image_file_name='photo_file_26_2')
db.session.add(i_f8)

i_f9 = Image_files(listing_id=26,
                   image_file_name='photo_file_26_3')
db.session.add(i_f9)
db.session.commit()
print("mock photo data committed")

# oakland county = 26125
oakland_county_update = db.session.get(County, 26125)
oakland_county_update.LISTINGS_AVAILABLE = 1
oakland_county_update.APPROVAL = 1
oakland_county_update.ACTIVE = 1
oakland_county_update.monthly_price = 100
oakland_county_update.annual_monthly_price = 90
try:
    db.session.commit()
except BaseException:
    db.session.rollback()

# st clair county = 26147
st_clair_county_update = db.session.get(County, 26147)
st_clair_county_update.LISTINGS_AVAILABLE = 1
st_clair_county_update.APPROVAL = 1
st_clair_county_update.ACTIVE = 1
st_clair_county_update.monthly_price = 100
st_clair_county_update.annual_monthly_price = 90
try:
    db.session.commit()
except BaseException:
    db.session.rollback()

# macomb county = 26099
macomb_county_update = db.session.get(County, 26099)
macomb_county_update.LISTINGS_AVAILABLE = 1
macomb_county_update.APPROVAL = 1
macomb_county_update.ACTIVE = 1
macomb_county_update.monthly_price = 100
macomb_county_update.annual_monthly_price = 90
try:
    db.session.commit()
except BaseException:
    db.session.rollback()

db.session.close()
print("initial data added to database")
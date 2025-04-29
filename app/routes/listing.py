from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.classes.data import Listing
from app.classes.forms import ListingForm
import datetime as dt

@app.route('/listing/new', methods=['GET', 'POST'])
@login_required
def listingNew():
    form = ListingForm()

    if form.validate_on_submit():
        newListing = Listing(
            gym_location=form.gym_location.data,
            gym_picture=form.gym_picture.data,
            gym_quality=form.gym_quality.data,
            price=form.gym_price.data,
            gym_contact=form.gym_contact.data,
            author=current_user.id,
            modify_date=dt.datetime.utcnow()
        )
        newListing.save()
        return redirect(url_for('listing', listingID=newListing.id))

    return render_template('listingform.html', form=form)

@app.route('/listing/<listingID>')
@login_required
def listing(listingID):
    thisListing = Listing.objects.get(id=listingID)
    return render_template('listing.html', listing=thisListing)

@app.route('/listing/list')
@app.route('/listings')
@login_required
def listingList():
    listings = Listing.objects()
    return render_template('listings.html', listings=listings)

@app.route('/listing/edit/<listingID>', methods=['GET', 'POST'])
@login_required
def listingEdit(listingID):
    editListing = Listing.objects.get(id=listingID)

    if current_user != editListing.author:
        flash("You can't edit a listing you don't own.")
        return redirect(url_for('listing', listingID=listingID))

    form = ListingForm()

    if form.validate_on_submit():
        editListing.update(
            gym_location=form.gym_location.data,
            gym_picture=form.gym_picture.data,
            gym_quality=form.gym_quality.data,
            price=form.gym_price.data,
            gym_contact=form.gym_contact.data,
            modify_date=dt.datetime.utcnow()
        )
        return redirect(url_for('listing', listingID=listingID))

    form.gym_location.data = editListing.gym_location
    form.gym_picture.data = editListing.gym_picture
    form.gym_quality.data = editListing.gym_quality
    form.gym_price.data = editListing.price
    form.gym_contact.data = editListing.gym_contact

    return render_template('listingform.html', form=form)

@app.route('/listing/delete/<listingID>')
@login_required
def listingDelete(listingID):
    deleteListing = Listing.objects.get(id=listingID)

    if current_user == deleteListing.author:
        deleteListing.delete()
        flash('The Listing was deleted.')
    else:
        flash("You can't delete a listing you don't own.")

    listings = Listing.objects()
    return render_template('listings.html', listings=listings)
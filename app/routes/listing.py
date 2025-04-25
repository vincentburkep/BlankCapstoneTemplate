from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Listing
from app.classes.forms import ListingForm
from flask_login import login_required
import datetime as dt

@app.route('/listing/new', methods=['GET', 'POST'])
@login_required
def listingNew():
    # This gets the form object from the form.py classes that can be displayed on the template.
    form = ListingForm()

    if form.validate_on_submit():

        newListing = Listing(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.

            gym_location = form.gym_location.data,
            gym_picture = form.gym_picture.data,
            gym_quality = form.gym_quality.data,
            gym_price = form.gym_price.data,
            gym_contact = form.gym_contact.data,
            
            # This sets the modifydate to the current datetime.
            modify_date = dt.datetime.utcnow
        )
        # This is a method that saves the data to the mongoDB database.
        newListing.save()

        # Once the new blog is saved, this sends the user to that blog using redirect.
        # and url_for. Redirect is used to redirect a user to different route so that 
        # routes code can be run. In this case the user just created a blog so we want 
        # to send them to that blog. url_for takes as its argument the function name
        # for that route (the part after the def key word). You also need to send any
        # other values that are needed by the route you are redirecting to.
        return redirect(url_for('Listing',ListingID=newListing.id))

    # if form.validate_on_submit() is false then the user either has not yet filled out
    # the form or the form had an error and the user is sent to a blank form. Form errors are 
    # stored in the form object and are displayed on the form. take a look at blogform.html to 
    # see how that works.
    return render_template('Listingform.html',form=form)

# This route will get one specific blog and any comments associated with that blog.  
# The blogID is a variable that must be passsed as a parameter to the function and 
# can then be used in the query to retrieve that blog from the database. This route 
# is called when the user clicks a link on bloglist.html template.
# The angle brackets (<>) indicate a variable. 
@app.route('/Listing/<ListingID>')
# This route will only run if the user is logged in.
@login_required
def Listing(ListingID):
    # retrieve the blog using the blogID
    thisListing = Listing.objects.get(id=ListingID)
    # If there are no comments the 'comments' object will have the value 'None'. Comments are 
    # related to blogs meaning that every comment contains a reference to a blog. In this case
    # there is a field on the comment collection called 'blog' that is a reference the Blog
    # document it is related to.  You can use the blogID to get the blog and then you can use
    # the blog object (thisBlog in this case) to get all the comments.
    # Send the blog object and the comments object to the 'blog.html' template.
    return render_template('Listing.html',Listing=thisListing)

@app.route('/Listing/list')
@app.route('/Listing')
# This means the user must be logged in to see this page
@login_required
def ListingList():
    # This retrieves all of the 'blogs' that are stored in MongoDB and places them in a
    # mongoengine object as a list of dictionaries name 'blogs'.
    Listings = Listing.objects()
    # This renders (shows to the user) the blogs.html template. it also sends the blogs object 
    # to the template as a variable named blogs.  The template uses a for loop to display
    # each blog.
    return render_template('Listings.html',Listings=Listings)

@app.route('/Listing/edit/<ListingID>', methods=['GET', 'POST'])
@login_required
def ListingEdit(ListingID):
    editListing = Listing.objects.get(id=ListingID)
    # if the user that requested to edit this blog is not the author then deny them and
    # send them back to the blog. If True, this will exit the route completely and none
    # of the rest of the route will be run.
    if current_user != editListing.author:
        flash("You can't edit a listing you don't own.")
        return redirect(url_for('Listing',ListingID=ListingID))
    # get the form object
    form = ListingForm()
    # If the user has submitted the form then update the blog.
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editListing.update(
            gym_location = form.gym_location.data,
            gym_picture = form.gym_picture.data,
            gym_quality = form.gym_quality.data,
            gym_price = form.gym_price.data,
            gym_contact = form.gym_contact.data,
            modify_date = dt.datetime.utcnow
        )
        # After updating the document, send the user to the updated blog using a redirect.
        return redirect(url_for('Listing',ListingID=ListingID))

    # if the form has NOT been submitted then take the data from the editBlog object
    # and place it in the form object so it will be displayed to the user on the template.
    gym_location = form.gym_location.data,
    gym_picture = form.gym_picture.data,
    gym_quality = form.gym_quality.data,
    gym_price = form.gym_price.data,
    gym_contact = form.gym_contact.data,


    # Send the user to the blog form that is now filled out with the current information
    # from the form.
    return render_template('Listingform.html',form=form)

@app.route('/Listing/delete/<ListingID>')
# Only run this route if the user is logged in.
@login_required
def ListingDelete(ListingID):
    # retrieve the blog to be deleted using the blogID
    deleteListing = Listing.objects.get(id=ListingID)
    # check to see if the user that is making this request is the author of the blog.
    # current_user is a variable provided by the 'flask_login' library.
    if current_user == deleteListing.author:
        # delete the blog using the delete() method from Mongoengine
        deleteListing.delete()
        # send a message to the user that the blog was deleted.
        flash('The Listing was deleted.')
    else:
        # if the user is not the author tell them they were denied.
        flash("You can't delete a listing you don't own.")
    # Retrieve all of the remaining blogs so that they can be listed.
    Listings = Listing.objects()  
    # Send the user to the list of remaining blogs.
    return render_template('Listings.html',Listings=Listings)

from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import League
from app.classes.forms import LeagueForm
from flask_login import login_required
import datetime as dt

@app.route('/league/new', methods=['GET', 'POST'])
@login_required
def leagueNew():
    # This gets the form object from the form.py classes that can be displayed on the template.
    form = LeagueForm()

    if form.validate_on_submit():

        newLeague = League(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.
            name = form.name.data,
            founder = form.founder.data,
            sport = form.sport.data,
            num_of_teams = form.num_of_teams.data,
            author = current_user.id,
            
            # This sets the modifydate to the current datetime.
            modify_date = dt.datetime.utcnow
        )
        # This is a method that saves the data to the mongoDB database.
        newLeague.save()

        # Once the new blog is saved, this sends the user to that blog using redirect.
        # and url_for. Redirect is used to redirect a user to different route so that 
        # routes code can be run. In this case the user just created a blog so we want 
        # to send them to that blog. url_for takes as its argument the function name
        # for that route (the part after the def key word). You also need to send any
        # other values that are needed by the route you are redirecting to.
        return redirect(url_for('league',leagueID=newLeague.id))

    # if form.validate_on_submit() is false then the user either has not yet filled out
    # the form or the form had an error and the user is sent to a blank form. Form errors are 
    # stored in the form object and are displayed on the form. take a look at blogform.html to 
    # see how that works.
    return render_template('leagueform.html',form=form)

# This route will get one specific blog and any comments associated with that blog.  
# The blogID is a variable that must be passsed as a parameter to the function and 
# can then be used in the query to retrieve that blog from the database. This route 
# is called when the user clicks a link on bloglist.html template.
# The angle brackets (<>) indicate a variable. 
@app.route('/league/<leagueID>')
# This route will only run if the user is logged in.
@login_required
def league(leagueID):
    # retrieve the blog using the blogID
    thisLeague = League.objects.get(id=leagueID)
    # If there are no comments the 'comments' object will have the value 'None'. Comments are 
    # related to blogs meaning that every comment contains a reference to a blog. In this case
    # there is a field on the comment collection called 'blog' that is a reference the Blog
    # document it is related to.  You can use the blogID to get the blog and then you can use
    # the blog object (thisBlog in this case) to get all the comments.
    # Send the blog object and the comments object to the 'blog.html' template.
    return render_template('league.html',league=thisLeague)

@app.route('/league/list')
@app.route('/leagues')
# This means the user must be logged in to see this page
@login_required
def leagueList():
    # This retrieves all of the 'blogs' that are stored in MongoDB and places them in a
    # mongoengine object as a list of dictionaries name 'blogs'.
    leagues = League.objects()
    # This renders (shows to the user) the blogs.html template. it also sends the blogs object 
    # to the template as a variable named blogs.  The template uses a for loop to display
    # each blog.
    return render_template('leagues.html',leagues=leagues)

@app.route('/league/edit/<leagueID>', methods=['GET', 'POST'])
@login_required
def leagueEdit(leagueID):
    editLeague = League.objects.get(id=leagueID)
    # if the user that requested to edit this blog is not the author then deny them and
    # send them back to the blog. If True, this will exit the route completely and none
    # of the rest of the route will be run.
    if current_user != editLeague.author:
        flash("You can't edit a league you don't own.")
        return redirect(url_for('league',leagueID=leagueID))
    # get the form object
    form = LeagueForm()
    # If the user has submitted the form then update the blog.
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editLeague.update(
            name = form.name.data,
            founder = form.founder.data,
            sport = form.sport.data,
            num_of_teams = form.num_of_teams.data,
            modify_date = dt.datetime.utcnow
        )
        # After updating the document, send the user to the updated blog using a redirect.
        return redirect(url_for('league',leagueID=leagueID))

    # if the form has NOT been submitted then take the data from the editBlog object
    # and place it in the form object so it will be displayed to the user on the template.
    form.name.data = editLeague.name
    form.founder.data = editLeague.founder
    form.sport.data = editLeague.sport
    form.num_of_teams.data = editLeague.num_of_teams


    # Send the user to the blog form that is now filled out with the current information
    # from the form.
    return render_template('leagueform.html',form=form)

@app.route('/league/delete/<leagueID>')
# Only run this route if the user is logged in.
@login_required
def leagueDelete(leagueID):
    # retrieve the blog to be deleted using the blogID
    deleteLeague = League.objects.get(id=leagueID)
    # check to see if the user that is making this request is the author of the blog.
    # current_user is a variable provided by the 'flask_login' library.
    if current_user == deleteLeague.author:
        # delete the blog using the delete() method from Mongoengine
        deleteLeague.delete()
        # send a message to the user that the blog was deleted.
        flash('The League was deleted.')
    else:
        # if the user is not the author tell them they were denied.
        flash("You can't delete a league you don't own.")
    # Retrieve all of the remaining blogs so that they can be listed.
    leagues = League.objects()  
    # Send the user to the list of remaining blogs.
    return render_template('leagues.html',leagues=leagues)

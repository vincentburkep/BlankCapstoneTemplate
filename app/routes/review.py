from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Review, Reply
from app.classes.forms import ReviewForm, ReplyForm
from flask_login import login_required
import datetime as dt
from mongoengine.queryset.visitor import Q

@app.route('/review/new', methods=['GET', 'POST'])
# This means the user must be logged in to see this page
@login_required
# This is a function that is run when the user requests this route.
def reviewNew():
    # This gets the form object from the form.py classes that can be displayed on the template.
    form = ReviewForm()

    # This is a conditional that evaluates to 'True' if the user submitted the form successfully.
    # validate_on_submit() is a method of the form object. 
    if form.validate_on_submit():

        # This stores all the values that the user entered into the new blog form. 
        # Blog() is a mongoengine method for creating a new blog. 'newBlog' is the variable 
        # that stores the object that is the result of the Blog() method.  
        newReview = Review(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.
            name = form.name.data,
            subject = form.subject.data,
            text = form.text.data,
            rating = form.rating.data,
            author = current_user.id,
            # This sets the modifydate to the current datetime.
            modify_date = dt.datetime.utcnow
        )
        # This is a method that saves the data to the mongoDB database.
        newReview.save()

        # Once the new blog is saved, this sends the user to that blog using redirect.
        # and url_for. Redirect is used to redirect a user to different route so that 
        # routes code can be run. In this case the user just created a blog so we want 
        # to send them to that blog. url_for takes as its argument the function name
        # for that route (the part after the def key word). You also need to send any
        # other values that are needed by the route you are redirecting to.
        return redirect(url_for('review',reviewID=newReview.id))

    # if form.validate_on_submit() is false then the user either has not yet filled out
    # the form or the form had an error and the user is sent to a blank form. Form errors are 
    # stored in the form object and are displayed on the form. take a look at blogform.html to 
    # see how that works.
    return render_template('reviewsform.html',form=form)

@app.route('/review/list')
@app.route('/reviews')
# This means the user must be logged in to see this page
@login_required
def reviewList():
    # This retrieves all of the 'blogs' that are stored in MongoDB and places them in a
    # mongoengine object as a list of dictionaries name 'blogs'.
    reviews = Review.objects()
    # This renders (shows to the user) the blogs.html template. it also sends the blogs object 
    # to the template as a variable named blogs.  The template uses a for loop to display
    # each blog.
    return render_template('reviews.html',reviews=reviews)





@app.route('/review/<reviewID>')
# This route will only run if the user is logged in.
@login_required
def review(reviewID):
    # retrieve the blog using the blogID
    thisReview = Review.objects.get(id=reviewID)
    # If there are no comments the 'comments' object will have the value 'None'. Comments are 
    # related to blogs meaning that every comment contains a reference to a blog. In this case
    # there is a field on the comment collection called 'blog' that is a reference the Blog
    # document it is related to.  You can use the blogID to get the blog and then you can use
    # the blog object (thisBlog in this case) to get all the comments.
    theseReplies = Reply.objects(Q(review=thisReview) & Q(outer=True) & Q(dFromOuter=0))
    # Send the blog object and the comments object to the 'blog.html' template.
    return render_template('review.html',review=thisReview, replies=theseReplies)

@app.route('/review/edit/<reviewID>', methods=['GET', 'POST'])
@login_required
def reviewEdit(reviewID):
    editReview = Review.objects.get(id=reviewID)
    # if the user that requested to edit this blog is not the author then deny them and
    # send them back to the blog. If True, this will exit the route completely and none
    # of the rest of the route will be run.
    if current_user != editReview.author:
        flash("You can't edit a review you don't own.")
        return redirect(url_for('review',reviewID=reviewID))
    # get the form object
    form = ReviewForm()
    # If the user has submitted the form then update the blog.
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editReview.update(
            name = form.name.data,
            subject = form.subject.data,
            text = form.text.data,
            rating = form.rating.data,
            modify_date = dt.datetime.utcnow
        )
        theseReplies = Reply.objects(Q(review=editReview) & Q(outer=True) & Q(dFromOuter=0))
        # After updating the document, send the user to the updated blog using a redirect.
        return redirect(url_for('review',reviewID=reviewID, replies=theseReplies))

    # if the form has NOT been submitted then take the data from the editBlog object
    # and place it in the form object so it will be displayed to the user on the template.
    form.name.data = editReview.name
    form.subject.data = editReview.subject
    form.text.data = editReview.text
    form.rating.data = editReview.rating


    # Send the user to the blog form that is now filled out with the current information
    # from the form.
    return render_template('reviewsform.html',form=form)

@app.route('/review/delete/<reviewID>')
# Only run this route if the user is logged in.
@login_required
def reviewDelete(reviewID):
    # retrieve the blog to be deleted using the blogID
    deleteReview = Review.objects.get(id=reviewID)
    # check to see if the user that is making this request is the author of the blog.
    # current_user is a variable provided by the 'flask_login' library.
    if current_user == deleteReview.author:
        # delete the blog using the delete() method from Mongoengine
        deleteReview.delete()
        # send a message to the user that the blog was deleted.
        flash('The Review was deleted.')
    else:
        # if the user is not the author tell them they were denied.
        flash("You can't delete a review you don't own.")
    # Retrieve all of the remaining blogs so that they can be listed.
    reviews = Review.objects()  
    # Send the user to the list of remaining blogs.
    return render_template('reviews.html',reviews=reviews)

@app.route('/reply/newRev/<reviewID>', methods=['GET', 'POST'])
@login_required
def replyNewRev(reviewID):
    review = Review.objects.get(id=reviewID)
    form = ReplyForm()
    if form.validate_on_submit():
        newReply = Reply(
            author = current_user.id,
            review = reviewID,
            text = form.text.data,
            name = review.name,
            dFromOuter = 0,
            outer = True
        )
        newReply.save()
        theseReplies = Reply.objects(Q(review=review) & Q(outer=True) & Q(dFromOuter=0))
        return redirect(url_for('review',reviewID=review.id, replies=theseReplies))
    return render_template('replyform.html',form=form,review=review)

@app.route('/reply/newRep/<reviewID>/<replyID>', methods=['GET', 'POST'])
@login_required
def replyNewRep(reviewID, replyID):
    review = Review.objects.get(id=reviewID)
    reply = Reply.objects.get(id=replyID)
    form = ReplyForm()
    if form.validate_on_submit():
        newReply = Reply(
            author = current_user.id,
            review = reviewID,
            text = form.text.data,
            name = review.name,
            dFromOuter = reply.dFromOuter+1,
            outer = False
        )
        newReply.save()
        reply.replies.append(newReply)
        reply.save()
        return redirect(url_for('review',reviewID=review.id))
    return render_template('replyform.html',form=form,review=reply)


@app.route('/reply/edit/<replyID>', methods=['GET', 'POST'])
@login_required
def replyEdit(replyID):
    editReply = Reply.objects.get(id=replyID)
    if current_user != editReply.author:
        flash("You can't edit a reply you didn't write.")
        return redirect(url_for('review',reviewID=editReply.review.id))
    review = Review.objects.get(id=editReply.review.id)
    form = ReplyForm()
    if form.validate_on_submit():
        editReply.update(
            text = form.text.data,
            modify_date = dt.datetime.utcnow
        )
        theseReplies = Reply.objects(Q(review=review) & Q(outer=True) & Q(dFromOuter=0))
        return redirect(url_for('review',reviewID=editReply.review.id, replies=theseReplies))

    form.text.data = editReply.text

    return render_template('replyform.html',form=form,review=review)   

@app.route('/reply/delete/<replyID>')
@login_required
def replyDelete(replyID): 
    deleteReply = Reply.objects.get(id=replyID)
    for reply in Reply.objects(Q(review=deleteReply.review) & Q(dFromOuter=(deleteReply.dFromOuter-1))):
        if reply.replies is not None and deleteReply in reply.replies:
                replyReplies = reply.replies
                reply.replies = replyReplies.remove(deleteReply)
                reply.save()
    deleteReply.delete()
    flash('The reply was deleted.')
    theseReplies = Reply.objects(Q(review=deleteReply.review) & Q(outer=True) & Q(dFromOuter=0))
    return redirect(url_for('review',reviewID=deleteReply.review.id, replies=theseReplies)) 
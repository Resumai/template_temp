from flask import render_template, redirect, url_for, flash, Blueprint
from app import db, ContactForm


info_bp = Blueprint('info', __name__)


### Info routes ###
@info_bp.route('/privacy')
def privacy():
    return render_template('info/privacy.html')


@info_bp.route('/terms')
def terms():
    return render_template('info/terms.html')


@info_bp.route('/contact', methods=['GET', 'POST'])
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
    # Normally, you'd send an email or save the message to a database
        flash("Thank you for your message. We'll get back to you soon.", "success")
        return redirect(url_for('info.contact_us'))
    return render_template('info/contact_us.html', form=form)
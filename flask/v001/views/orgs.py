from flask import Blueprint, request, redirect, url_for, render_template, session

from models.forms import Organization, OrganizationForm

orgs_bp = Blueprint('orgss', __name__)


@orgs_bp.route('/orgs/', methods = ["GET", "POST"])
def orgs():
    return render_template("organization/organization_layout.html",
                           orgs=Organization.objects())


@orgs_bp.route('/orgs/new/', methods = ["GET", "POST"])
def neworg():
    form = OrganizationForm()
    if request.method == 'POST':
        print ("POSTING:")
        data = Organization()
        data.name = request.form["name"]
        data.description = request.form["description"]
        if 'id' in session.keys():
            data.creator = session['id']
        else:
            return 'No Session ID', 400
        data.save()
        return redirect(url_for('orgs'))

    return render_template("organization/organization_create.html",
                           form=form,
                           form_name="Organization")
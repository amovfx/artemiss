from flask import Blueprint, request, redirect, url_for, render_template, session
from flaskapp.models.orgs import Organization, OrganizationForm

orgs = Blueprint('orgs', __name__, template_folder='templates')


@orgs.route('/orgs/', methods = ["GET", "POST"])
def org_browse():
    return render_template("organization_layout.html",
                           orgs=Organization.objects())


@orgs.route('/orgs/new/', methods = ["GET", "POST"])
def create_org():
    form = OrganizationForm()
    if request.method == 'POST':
        print ("POSTING:")
        data = Organization()
        data.name = request.form["name"]
        data.description = request.form["description"]
        # if 'id' in session.keys():
        #     data.creator = session['id']
        # else:
        #     return 'No Session ID', 400
        data.save()
        return redirect(url_for('orgs.org_browse'))

    return render_template("organization_create.html",
                           form=form,
                           form_name="Organization")


@orgs.route('/orgs/<org_id>', methods = ['GET'])
def org(org_id):
    return render_template("org.html",
                           id=org_id)
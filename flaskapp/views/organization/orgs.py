from flask import (Blueprint,
                   request,
                   redirect,
                   url_for,
                   render_template,
                   session,
                   make_response,
                   jsonify)


from flaskapp.models.orgs import Organization, OrganizationForm, OrganizationLiteResponse

orgs = Blueprint('orgs',
                 __name__,
                 template_folder='templates')



@orgs.route('/orgs/', methods = ["GET", "POST"])
def org_browse():
    return render_template("organization_browser.html",
                           orgs=Organization.objects())


@orgs.route('/orgs/new/', methods = ["GET", "POST"])
def create_org():
    """

    This route allows the agent to create an organization and save it to the database.

    """

    form = OrganizationForm()
    if request.method == 'POST':

        data = Organization()
        data.name = request.form["name"]
        data.description = request.form["description"]
        data.save()

        return redirect(url_for('orgs.org_browse'))

    return render_template("organization_create.html",
                           form=form,
                           form_name="Organization")


@orgs.route('/orgs/<org_id>', methods = ['GET'])
def org(org_id):
    """

    This route views the organization and it's feed.

    :param org_id:
        The mongo ObjectID of the organization.

    :return:
        Renders the org.html template.
    """

    return render_template("org.html",
                           org_id=org_id,
                           org=org)

@orgs.route("/orgs/load", methods = ["GET"])
def load():
    """

    This is a route to handle infinite scroll. The relevant java script
    is in organization_browser.html.

    :return:
        A JSON of the OrganizationReponse, an object that just has the
        relevant data of what is needed.


    """

    def get_organizations(counter):
        """

        :param counter:

        :return:
        """

        quantity = 5

        light_response_objects = []
        organizations_slice = Organization.objects()[counter:counter+quantity]

        for obj in organizations_slice:
            light_response_objects.append(OrganizationLiteResponse(obj))

        return light_response_objects

    if request.args:

        counter = int(request.args.get("c"))

        if counter == 0:
            response = make_response(jsonify(get_organizations(0)), 200)

        elif counter == len(Organization.objects()):
            response = make_response(jsonify({}), 200)

        else:
            response = make_response(jsonify(get_organizations(counter)), 200)

    return response

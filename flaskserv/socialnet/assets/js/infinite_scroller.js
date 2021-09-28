
class AbstractTemplateUpdateStrategy
{
    /* Abstract class that stores cloned template and target. */
    constructor(template_name, dom_template_target)
    {
        var template = document.querySelector(template_name);
        this.template_clone = template.content.cloneNode(true);
        this.set_template_target(dom_template_target);

    }

    /*
    @abstract
     */
    update(data)
    {
        /*
            this is the abstract function that needs to be implemented to map the data
            to the html template.
         */
        throw new Error("update_template_clone function not implemented.")
    }

    set_template_target(dom_template_target)
    {
        /*
        template target is the dom object you would like to append the cloned template too once its updated.
         */
        this.template_target = dom_template_target;
    }

    get_template_target()
    {
        /*
        Get the template_target.
         */
        return this.template_target;
    }
}


class TemplateCloner
/*
Dependent on a child of a AbstractTemplateAssetUpdateStrategy

*/

{
    constructor (template_update_strategy)
    {
        this.template_update_strategy = template_update_strategy;
    }

    build_template(data)
    {
        let template_clone = this.template_update_strategy.update(data);
        this.template_update_strategy.get_template_target().append(template_clone);
    }
}

class InfiniteLoaderFactory
    /*
    This class makes a call to an endpoint to get json.
    It then populates Template Cloner to update the template with the json data and append it to the strategy's target.
    The observe function produces an intersection observer
     */
{
    constructor(template_cloner, endpoint)
    {
        this.endpoint = endpoint;
        this.counter = 0;
        this.template_cloner = template_cloner;
    }

    load_data()
    {
    /*

    Loads comments and then makes a template for each comment.

    */
        fetch(`${this.endpoint}?c=${this.counter}`)
            .then(response => response.json())
            .then(json => {
                for (const comment_data of json) {
                    this.template_cloner.build_template(comment_data);
                }
                this.counter++;
            })

    }

    observe(sentinel_id = "#sentinel")
    {
        /*
        produces an intersectionObserver targeting the setinel_id
         */
        let sentinel = document.querySelector(sentinel_id);
        var intersectionObserver = new IntersectionObserver(entries =>
            {

                if (entries[0].intersectionRatio <= 0) {
                    return;
                }

                // Call the loadItems function
                this.load_data();
            });
        intersectionObserver.observe(document.querySelector(sentinel_id));
    }
}



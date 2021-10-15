    var scroller = document.querySelector("#scroller");
    var template = document.querySelector("#post_template");

    var sentinel = document.querySelector("#sentinel");

    var counter = 0;

    function loadItems() {
        fetch(`/orgs/load?c=${counter}`).then(( response) => {
            response.json().then((data) => {
                if (!data.length) {
                    sentinel.innerHTML = "No More Orgs. ";
                }
                for (var i = 0; i < data.length; i++) {

                    let template_clone = template.content.cloneNode(true);
                    template_clone.querySelector("#title").innerHTML = `${data[i]["name"]}`;
                    template_clone.querySelector("#description").innerHTML = `${data[i]["description"]}`;
                    template_clone.querySelector("#org_link").href = `/orgs/${data[i]["id"]}`;
                    scroller.append(template_clone);
                    counter += 1;
                }
                // would like to unobserve the lazy loader.
            })
        })
    }


var intersectionObserver = new IntersectionObserver(entries => {

// Uncomment below to see the entry.intersectionRatio when
// the sentinel comes into view

// entries.forEach(entry => {
//   console.log(entry.intersectionRatio);
// })

// If intersectionRatio is 0, the sentinel is out of view
// and we don't need to do anything. Exit the function
if (entries[0].intersectionRatio <= 0) {
return;
}

// Call the loadItems function
loadItems();
});

// Instruct the IntersectionObserver to watch the sentinel
intersectionObserver.observe(sentinel);

class InfiniteLoader
{
    constructor(scroller, html_template, sentinel, endpoint)
    {
        this.set_scroller(scroller);
        this.set_template(html_template);
        this.set_sentinel(sentinel);
        this._template = document.querySelector(html_template);
        this._endpoint = endpoint;
    }

    set_scroller(scroller_element_name)
    {
        this._scroller = document.querySelector(scroller_element_name);
    }

    set_template(html_template)
    {
        this._template = document.querySelector(html_template);
    }

    get_template()
    {
        return this._template;
    }

    set_sentinel(sentinel_element)
    {
        this._sentinel = document.querySelector(sentinel_element)
    }

    get_sentinel()
    {
        return this._sentinel
    }

    set_endpoint(api_endpoint)
    {
        /*
        This is a call to the end point to get paginated data
        from an sql db.
         */

        this._endpoint = api_endpoint
    }

    get_endpoint()
    {
        return this._endpoint
    }

    load_items(template_populator_function,
               empty_message="No More Data")
    {

        fetch(this.get_endpoint()).then(
            ( response) =>
            {
                response.json().then((data) =>
                {
                    if (!data.length) {
                        this.get_sentinel().innerHTML = empty_message;
                    }
                    for (var i = 0; i < data.length; i++) {

                        let template_clone = template.content.cloneNode(true);
                        template_populator_function(template_clone);
                        template_clone.querySelector("#title").innerHTML = `${data[i]["name"]}`;
                        template_clone.querySelector("#description").innerHTML = `${data[i]["description"]}`;
                        template_clone.querySelector("#org_link").href = `/orgs/${data[i]["id"]}`;
                        scroller.append(template_clone);
                        counter += 1;
                    }
                // would like to unobserve the lazy loader.
            })
        })

    }

    observe_intersection(sentinel)
    {
        var intersectionObserver = new IntersectionObserver(entries => {

        // Uncomment below to see the entry.intersectionRatio when
        // the sentinel comes into view

        // entries.forEach(entry => {
        //   console.log(entry.intersectionRatio);
        // })

        // If intersectionRatio is 0, the sentinel is out of view
        // and we don't need to do anything. Exit the function
        if (entries[0].intersectionRatio <= 0) {
            return;
        }

        // Call the loadItems function
            this.load_items();
        });

        // Instruct the IntersectionObserver to watch the sentinel
        intersectionObserver.observe(sentinel);
    }


}

class TemplateClone
{

}
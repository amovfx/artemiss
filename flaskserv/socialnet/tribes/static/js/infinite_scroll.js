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
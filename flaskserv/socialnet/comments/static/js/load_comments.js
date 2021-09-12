


class CommentTemplate
{
    constructor(template_name="#comment_template")
    {
        /*



         */
        this.clone_template(template_name)
    }

    clone_template(template_name)
    {
        /*

        Clone the comment template.

        */
        var template = document.querySelector(template_name);
        this.template_clone = template.content.cloneNode(true);
    }

    parse_comment_data(comment_data)
    {
        this.title = comment_data['title'];
        this.message = comment_data['message'];
        this.uuid = comment_data['uuid'];
        this.path = comment_data['path'];
        this.author = comment_data['author'];
        this.parent = comment_data['parent'];

        //set path data
        let split_path = this.path.split(".");
        this.is_reply = split_path.length > 1;


        if (this.is_reply) {
            this.path_leaf = split_path[(split_path.length) - 1];
            this.path_parent = split_path[(split_path.length) - 2];
        }
        else
        {
            this.path_leaf = this.path;
        }

    }

    set_content()
    {
        if (this.hasOwnProperty('path') ||
            this.hasOwnProperty('author') ||
            this.hasOwnProperty('message'))
        {
            this.template_clone
                .getElementById("comment")
                .setAttribute("data-path", this.path);
            this.template_clone
                .getElementById("comment-author")
                .innerHTML = this.title;

            //This will be replaced by a function to call ipfs and decode.
            this.template_clone
                .getElementById("comment-message")
                .innerHTML = this.message;
        }
        else
        {
            throw "parse comment data hasn't been called."
        }
    }

    //set reply button functionality to toggle visibility.

    set_reply_form_data()
    {

        //toggle reply display
        let toggle_comment_form_display = () =>
        {
            let comment_reply_form = document.querySelector(`[data-reply_form_id="${this.path_leaf}"]`);
            if (comment_reply_form.style.display === "none") {

                comment_reply_form.style.display = "block";
            }
            else
            {
                comment_reply_form.style.display = "none";
            }
        }

        this.template_clone
            .getElementById("reply-button")
            .onclick = toggle_comment_form_display;

        this.template_clone
            .getElementById("reply-cancel")
            .onclick = toggle_comment_form_display;
        //set reply form unique identifier to grab the form
        this.template_clone
            .getElementById("reply-form")
            .setAttribute("data-reply_form_id", this.path_leaf)

        this.template_clone
            .getElementById('reply-form')
            .action = `/comments/reply?post_uuid=${this.uuid}`;

        this.template_clone.getElementById("form_tag")
            .setAttribute("value", this.uuid);



        //set the replies div so it can be referenced by children.
        //This allows us to attach replies.

        this.template_clone
            .getElementById("replies")
            .setAttribute("data-reply_parent", this.path_leaf);

    }


    append_to_comment_thread()
    {
        /*
        Probably parameterize this function.
         */
        var comment_thread;
        if (this.is_reply)
        {
            comment_thread = document.querySelector(`[data-reply_parent="${this.path_parent}"]`);

        }
        else
        {


            //the comment_data is a reply to the topic.

            comment_thread = document.getElementById("infinite-scroller");
        }
        comment_thread.append(this.template_clone)

    }



    build_template()
    {
        this.set_content();
        this.set_reply_form_data();
        this.append_to_comment_thread();
    }
}

class InfiniteLoader
{
    constructor(endpoint,
                Templator)
    {
        this.endpoint = endpoint;
        this.counter = 0;
        this.templator = Templator
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
                    let Comment = new this.templator();
                    Comment.parse_comment_data(comment_data);
                    Comment.build_template();
                }
                this.counter++;
            })

    }

    observe(sentinel_id = "#sentinel")
    {
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



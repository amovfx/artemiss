


class CommentTemplator
{
    constructor(data, template_name)
    {
        this.endpoint = endpoint;
        this.parse_comment_data(data, template_name)
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
            this.path_leaf = split_path[this.split_path.length - 1];
            this.path_parent = split_path[this.split_path.length - 2];
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
            .setAttribute("data-form_id", this.path_leaf)

        //set reply form action
        this.template_clone
            .getElementById('reply-form')
            .action = `/comments/reply?t=${this.is_reply}`;



        //set the replies div so it can be referenced by children.
        //This allows us to attach replies.

        this.template_clone
            .getElementById("replies")
            .setAttribute("data-reply_parent", this.path_leaf);

    }

    set_comment_thread()
    {
        /*

         */

        if (this.is_reply)
        {
            this.comment_thread = document.querySelector(`[data-parent="${this.path_parent}"]`);

        }


        //the comment_data is a reply to the topic.


        this.comment_thread = document.getElementById("scroller");

    }

    append_template()
    {
        this.comment_thread.append(this.template_clone)
    }





    build_comment()
    {
        this.set_content();
        this.set_reply_form_data();
        this.set_comment_thread();
        this.append_template()



    }

    load_data()
    {
    /*

    Loads comments and then makes a template for each comment.

     */
        fetch(this.endpoint)
            .then(response => response.json())
            .then(json => {
                for (const comment_data of json) {
                    this.parse_comment_data(comment_data);
                    clone_comment_template();
                    set_comment_data(template,comment_data);
                    let comment_thread = get_comment_parent(template, comment_data);
                    comment_thread.append(template);

                }
                counter++;
            })

    }


}

function load_data(endpoint)
    {
    /*

    Loads comments and then makes a template for each comment.

     */
        fetch(endpoint)
            .then(response => response.json())
            .then(json => {
                for (const comment_data of json) {
                    let Comment = new CommentTemplator(comment_data, "#comment_template");
                    Comment.build_comment()



                }
                counter++;
            })

    }


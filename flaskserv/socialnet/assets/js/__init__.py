from flask_assets import Bundle

infinite_loader_js = Bundle('infinite_scroller.js',
                            output='gen/assets.js',
                            filters='jsmin')

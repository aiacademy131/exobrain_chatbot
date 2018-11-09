

class data_send:

    def return_buttons(message, buttons):
        datasend = {
            "message" : {
                "text" : message
            },
            "keyboard" : {
                "type" : "buttons",
                "buttons" : buttons
            }
        }
        return datasend

    def return_buttons_with_url(message, buttons, label, url):
        datasend = {
            "message" : {
                "text" : message,
                "message_button" : {
                    "label" : label,
                    "url" : url
                }
            },
            "keyboard" : {
                "type" : "buttons",
                "buttons" : buttons
            }
        }
        return datasend

    def return_buttons_with_pic(message, buttons, pic_url, buttons_label, buttons_url):
        datasend = {
            "message" : {
                "text" : message,
                "photo" : {
                    "url" : pic_url,
                    "width" : 720,
                    "height" : 630
                },
                "message_button" : {
                    "label" : buttons_label,
                    "url"  : buttons_url
                }
            },
            "keyboard" : {
                "type" : "buttons",
                "buttons" : buttons
            }
        }

        return datasend

    def return_message(message):
        datasend = {
            "message" : {
                "text" : message
            },
            "keyboard" : {
                "type" : "text"
            }
        }

        return datasend



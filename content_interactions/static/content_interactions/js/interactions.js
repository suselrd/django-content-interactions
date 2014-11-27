/* Creates a new interaction class */
function iClazz(SuperClass, methods) {

    var subClass = function () {
        this.config.apply(this, arguments);
    };
    subClass.prototype = Object.create(SuperClass.prototype);
    subClass.prototype.constructor = subClass;
    subClass.prototype.parent = SuperClass.prototype;
    subClass.prototype = $.extend(subClass.prototype, methods);

    return subClass;
}

var Interaction = iClazz(Object, {
    config: function(options) {},

    init: function() {}
});


var ToggleInteraction = iClazz(Interaction, {

    config: function(options) {
        this.options = {
            selector: '.toggle_relationship',
            eventType: 'click',
            container: $('body')
        };

        if (typeof options == 'object') $.extend(this.options, options);

        this.init();
    },

    init: function() {
        var container = this.options.container,
            $class = this;

        if (container && (typeof container == 'object' && container[0] instanceof Element)) {
            container.delegate(this.options.selector, this.options.eventType, function(e) {
                e.preventDefault();

                var $this = $(this),
                    url = $this.attr('href') || $this.data('url'),
                    model = $this.data('model'),
                    pk = $this.data('pk');

                if (typeof model !== 'undefined' && typeof pk !== 'undefined' && typeof url !== 'undefined') {
                    $.ajax(url, {
                        type: 'POST',
                        data: {
                            "model": model,
                            "pk": pk
                        },
                        context: this,
                        success: function(response, status, xhr) {
                            $class.success(response, status, xhr, this);
                        },
                        error: function(response, status, xhr) {
                            $class.error(response, status, xhr, this);
                        },
                        dataType: "json"
                    });

                } else {
                    throw new Error('Error: the values of (url, model, and pk) must be specified.');
                }
            });

        } else {
            throw new Error('Error: this.options.container expects an HTML Element.');
        }
    },

    success: function(response, status, xhr, context) {
        if (status == "success" && response['result']) {
            $(context).addClass((response['toggle_status']) ? 'on' : 'off');
        }
    },

    error: function(response, status, xhr, context) {}
});


var FormInteraction = iClazz(Interaction, {

    config: function(options) {
        this.options = {
            selector: '',
            eventType: ''
        };

        if (typeof options == 'object') $.extend(this.options, options);

        this.init();
    },

    init: function() {
        var eventTrigger = $(this.options.selector).first(),
            $class = this;

        eventTrigger.on(this.options.eventType, function() {
            $class.eventImpl(eventTrigger);
        })
    },

    eventImpl: function(eventTrigger) {}
});
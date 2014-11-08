$(function() {

    /* Default configuration for toggle interactions */
    var basicToggleInteraction = new ToggleInteraction();
    basicToggleInteraction.config();

    /*
    // Advanced configuration [Example]

    // Extends the ToggleInteraction class behavior
    var MyToggleInteractionClass = iClazz(ToggleInteraction, {
        // Overrides a super class method
        success: function(response, status, xhr, context) {
            // Overrides completely the method, or override calling the supper class method too
            ToggleInteraction.prototype.success(response, status, xhr, context);
        }
    });

    // Creates a new instance of MyToggleInteractionClass
    var advancedToggleInteraction = new MyToggleInteractionClass();
    // config the instance with specific data
    advancedToggleInteraction.config({
        // Redefines the options
        container: $('selector')
    });

    */


    // Extends the FormInteraction class behavior
    var MyFormInteractionClass = iClazz(FormInteraction, {

        // Defines the super class method
        eventImpl: function(eventTrigger) {
            // --------------
        }
    });

    var formInteraction = new MyFormInteractionClass();
    // config the instance with specific data
    formInteraction.config({
        // Redefines the options
        selector: '.selector',
        eventType: 'shown.bs.modal'
    });

});
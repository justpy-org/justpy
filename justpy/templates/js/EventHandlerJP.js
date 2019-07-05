// {% raw %}
function eventHandler(props, event, form_data) {
    console.log('-------------------------');
        console.log('In eventHandler: ' + event.type + '  ' + props.jp_props.vue_type + '  ' + props.jp_props.class_name);
    // console.log(JSON.stringify(props, null, 2));
    console.log( event);
    console.log('-------------------------');
        e = {
            'event_type': event.type,
            'id': props.jp_props.id,
            'class_name': props.jp_props.class_name,
            'html_tag': props.jp_props.html_tag,
            'comp_type': props.jp_props.type,
            'event_target': event.target.id,
            'event_current_target': event.currentTarget.id,
            //'running_id': props.jp_props.running_id,
            'input_type': props.jp_props.input_type,
            'checked': event.target.checked,
            'data': event.data,
            'value': event.target.value,
            'page_id': page_id,
            'websocket_id': websocket_id,
            'form_data':  form_data
        };

        if (event instanceof KeyboardEvent){
        // it is a keyboard event!
        // https://developer.mozilla.org/en-US/docs/Web/Events/keydown   keyup, keypress
            e['key_data'] = {
                altKey: event.altKey,
                ctrlKey: event.ctrlKey,
                shiftKey: event.shiftKey,
                metaKey: event.metaKey,
                code: event.code,
                key: event.key,
                repeat: event.repeat,
                locale: event.locale


            }
                        }
        if (use_websockets){
        if (websocket_ready)
            socket.send(JSON.stringify({'type': 'event'  ,'event_data': e}));
            }
        else{

            d = JSON.stringify({'type': 'event'  ,'event_data': e});
            $.ajax({
            type: "POST",
            url: "/zzz_justpy_ajax",
            data: JSON.stringify({'type': 'event'  ,'event_data': e}),
            success: function( msg ) {
  //$( ".result" ).html( data );
            console.log( "Ajax from eventhandler done was performed." );
            console.log(msg);
            if (msg) app1.justpyComponents = msg.data;
        },
            dataType: 'json'
        });
        }
    // Check for scrolling https://stackoverflow.com/questions/7717527/smooth-scrolling-when-clicking-an-anchor-link
    if (props.jp_props.scroll && (event.type=='click')) {
        event.preventDefault();
        c = document.getElementById(props.jp_props.scroll_to);
        c.scrollIntoView({
            behavior: props.jp_props.scroll_option    // Default is 'smooth'
        });

    }
}


// {% endraw %}
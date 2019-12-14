// {% raw %}


function eventHandler(props, event, form_data, aux) {
    console.log('-------------------------');
    console.log('In eventHandler: ' + event.type + '  ' + props.jp_props.vue_type + '  ' + props.jp_props.class_name);
    // console.log(JSON.stringify(props, null, 2));
    console.log(event);
    console.log(props.jp_props);
    console.log(websocket_ready);
    console.log(use_websockets);
    console.log('debounce');
    console.log(props.jp_props.debounce);
    console.log('-------------------------');
    if (!websocket_ready && use_websockets) return;

    e = {
        'event_type': event.type,
        'id': props.jp_props.id,
        'class_name': props.jp_props.class_name,
        'html_tag': props.jp_props.html_tag,
        'vue_type': props.jp_props.vue_type,
        'event_target': event.target.id,
        'event_current_target': event.currentTarget.id,
        'input_type': props.jp_props.input_type,
        'checked': event.target.checked,
        'data': event.data,
        'value': event.target.value,
        'page_id': page_id,
        'websocket_id': websocket_id
    };
    if (form_data) e['form_data'] = form_data;
    if (aux) e['aux'] = aux;
    if (event instanceof KeyboardEvent) {
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

    //send_to_server(e);
    if (props.jp_props.debounce) {
        clearTimeout(props.timeout);
        props.timeout = setTimeout(function () {
                send_to_server(e);
            }
            , props.jp_props.debounce);
    }
    else {
        send_to_server(e);
    }

    // https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView
    if (props.jp_props.scroll && (event.type == 'click')) {
        event.preventDefault();
        c = document.getElementById(props.jp_props.scroll_to);

        c.scrollIntoView({
            behavior: props.jp_props.scroll_option,    // Default is 'smooth'
            block: props.jp_props.block_option,
            inline: props.jp_props.inline_option,
        });

    }
}

function send_to_server(e) {
    if (use_websockets) {
        if (websocket_ready)
            socket.send(JSON.stringify({'type': 'event', 'event_data': e}));
        else {
            setTimeout(function () {
                socket.send(JSON.stringify({'type': 'event', 'event_data': e}));
            }, 1000);
        }
    } else {

        d = JSON.stringify({'type': 'event', 'event_data': e});
        $.ajax({
            type: "POST",
            url: "/zzz_justpy_ajax",
            data: JSON.stringify({'type': 'event', 'event_data': e}),
            success: function (msg) {
                console.log("Ajax from eventhandler done was performed.");
                console.log(msg);
                if (msg) app1.justpyComponents = msg.data;
            },
            dataType: 'json'
        });
    }
}

// {% endraw %}
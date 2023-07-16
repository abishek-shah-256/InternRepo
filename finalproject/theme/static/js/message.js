let loc = window.location
let wsStart = 'ws://'

let input_message = $('.input-message')
let message_body = $('.messages-wrapper')
let send_message_form = $('.send-message-form')
let user_id = $('.logged-in-user').val()


if(location.protocol === 'https'){
    wsStart = 'wss://'
}
let endpoint = wsStart + loc.host + loc.pathname
var socket = new WebSocket(endpoint)


socket.onopen = async function(e){
    console.log('open', e);

    send_message_form.on('submit', function(e){
        e.preventDefault();
        let message = input_message.val();
        let send_to = get_active_other_user_id();
        let thread_id = get_active_thread_id();
        // let send_to;
        // if(user_id == 2)
        //     send_to = 5
        // else
        //     send_to = 2
            
        let data = {
            'message': message,
            'sent_by': user_id,
            'send_to': send_to,
            'thread_id': thread_id,
        }
        data = JSON.stringify(data)

        socket.send(data)
        $(this)[0].reset()
    })



};


socket.onmessage = async function(e){
    console.log('message', e);
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    console.log('aetaaaaaa', message)
    newMessage(message, sent_by_id, thread_id)
};

socket.onerror = async function(e){
    console.log('error', e);
};

socket.onclose = async function(e){
    console.log('close', e);
};




// debugger;
let countt = 0;
function newMessage(message, sent_by_id, thread_id){
    if($.trim(message) === ''){
        return false;
    }
    countt = countt+1;
    console.log("kina vayena    "+countt)

    let message_element;
    let chat_id = 'chat_'+ thread_id

    if(sent_by_id == user_id){
        message_element = `
        <div class="flex justify-end mb-2">
        <div class="rounded py-2 px-3" style="background-color: #E2F7CB">
        <p class="text-sm mt-1">
        ${message}
        </p>
        <p class="text-right text-xs text-grey-dark mt-1">
        12:45 pm
        </p>
        </div>
        </div>
        `
    }
    else {
        message_element = `
        <div class="flex mb-2">
            <div class="rounded py-2 px-3" style="background-color: #F2F2F2">
            <p class="text-sm text-purple">
            Other user--
            </p>
            <p class="text-sm mt-1">
            ${message}
            </p>
            <p class="text-right text-xs text-grey-dark mt-1">
            2:45 pm
            </p>
            </div>
        </div>
        `
                }
                
   let message_body =  $('.messages-wrapper[chat-id="' + chat_id + '"] ')
    message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100
    );
    input_message.val(null);
}


$('.contact-list').on('click', function(){
    $('.contacts .active').removeClass('active')
    $(this).addClass('active')


    let chat_id = $(this).attr('chat-id')
    $('.messages-wrapper.is_active').removeClass('is_active')
    $('.messages-wrapper[chat-id="' + chat_id + '"]').addClass('is_active')
    
})

function get_active_other_user_id(){
    let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}


function get_active_thread_id(){
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}
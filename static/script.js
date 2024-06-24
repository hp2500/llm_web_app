// Function to delete a cookie
function deleteCookie(name) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
}

// Delete the 'session_id' cookie when the page is refreshed
deleteCookie('session_id');

function scrollToBottom() {
    $('#messages').scrollTop($('#messages')[0].scrollHeight);
}

function updateMessagesHeight() {
    const messagesDiv = $('#messages');
    const formHeight = $('form').outerHeight(true);
    const newHeight = $(window).height() - formHeight - 20;
    messagesDiv.css('height', newHeight + 'px');
    scrollToBottom();
}

// Function to delete a cookie
function deleteCookie(name) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
}

// Delete the 'session_id' cookie when the page is refreshed
deleteCookie('session_id');

function scrollToBottom() {
    $('#messages').scrollTop($('#messages')[0].scrollHeight);
}

function updateMessagesHeight() {
    const messagesDiv = $('#messages');
    const formHeight = $('form').outerHeight(true);
    const newHeight = $(window).height() - formHeight - 20;
    messagesDiv.css('height', newHeight + 'px');
    scrollToBottom();
}

$(document).ready(function () {
    $(window).on('resize', updateMessagesHeight);
    updateMessagesHeight();

    // Disable the chat window and send button by default
    $('#chat_window').prop('disabled', true);
    $('#send_message').prop('disabled', true);

    let userName = '';

    $('#submit_name').on('click', function (event) {
        event.preventDefault();
        userName = $('#user_name').val().trim();

        if (userName.length > 0) {
            $('#user-details').hide();
            $('#chat_window').prop('disabled', false);
            $('#send_message').prop('disabled', false);
        } else {
            alert('Please enter a name.');
        }
    });

    $('#send_message').on('click', function (event) {
        event.preventDefault();
        let chat_window = $('#chat_window').val();

        // Update chat window with user message
        $('#messages').append('<div class="message user"><p>' + chat_window + '</p></div>');
        scrollToBottom(); // Scroll to bottom

        // Clear input field and disable it
        $('#chat_window').val('').prop('disabled', true);

        // Disable the send button
        $('#send_message').prop('disabled', true);

        // Add typing animation
        $('#messages').append('<div class="message bot" id="typing-animation"><span class="typing-dots"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></span></div>');
        scrollToBottom(); // Scroll to bottom

        $.ajax({
            url: '/process_message',
            type: 'POST',
            data: {'chat_window': chat_window, 'user_id': userName},
            success: function (data, textStatus, request) {
                // Remove typing animation
                $('#typing-animation').remove();

                // Set the cookie using JavaScript
                let cookie = request.getResponseHeader('Set-Cookie');
                if (cookie) {
                    let cookieName = cookie.split('=')[0];
                    let cookieValue = cookie.split('=')[1].split(';')[0];
                    document.cookie = cookieName + "=" + cookieValue + ";path=/";
                }
                // Update chat window with bot response
                $('#messages').append('<div class="message bot"><p>' + data.bot_response + '</p></div>');
                scrollToBottom(); // Scroll to bottom

                // Enable the input field and set focus
                $('#chat_window').prop('disabled', false).focus();

                // Enable the send button
                $('#send_message').prop('disabled', false);
            },
            error: function () {
                // Remove typing animation
                $('#typing-animation').remove();

                // Enable the input field and send button in case of an error, and set focus
                $('#chat_window').prop('disabled', false).focus();
                $('#send_message').prop('disabled', false);
            }
        });
    });
});
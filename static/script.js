document.addEventListener("DOMContentLoaded", function() {
    const sendButton = document.getElementById("sen_bt");
    const chatbox = document.querySelector(".chatbox");

    sendButton.addEventListener("click", function(event) {
        event.preventDefault(); // Prevent default form submission behavior
        sendMessage();
    });

    function sendMessage() {
        const textarea = document.querySelector(".chat-input textarea");
        const messageText = textarea.value.trim();
        
        if (messageText === "") {
            return;
        }

        const newMessage = document.createElement("li");
        newMessage.classList.add("chat", "outgoing", "new-message");
        newMessage.innerHTML = `
            <p>${messageText}</p>
        `;
        
        chatbox.appendChild(newMessage);
        textarea.value = "";
        
        // Scroll to the bottom of the chatbox
        scrollToBottom();
        
        // Send message to the server
        sendToServer(messageText);
    }

    function sendToServer(messageText) {
        // Send message to Flask route via AJAX
        fetch("/chatbot1/<username>/", {
            method: "POST",
            body: new URLSearchParams({msg: messageText}),
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
        .then(response => response.json())
        .then(data => {
            // Handle response from server
            sendBotResponse(data.response);
        })
        .catch(error => console.error("Error:", error));
    }

    function sendBotResponse(responseText) {
        const botResponse = document.createElement("li");
        botResponse.classList.add("chat", "incoming", "new-message");
        botResponse.innerHTML = `
            <span class="material-symbols-outlined">deployed_code</span>
            <p>${responseText}</p>
        `;

        chatbox.appendChild(botResponse);
        
        // Scroll to the bottom of the chatbox
        scrollToBottom();
    }

    function scrollToBottom() {
        // Calculate the maximum scroll position while leaving space for the textarea
        const maxScroll = chatbox.scrollHeight - chatbox.clientHeight;
        chatbox.scrollTop = maxScroll > 0 ? maxScroll : 0;
    }
});
document.addEventListener("DOMContentLoaded", function() {
    const toggleNav = document.querySelector('.toggle');
    const nav = document.querySelector('.hidebar');
  
    toggleNav.addEventListener('click', function() {
      if (nav.style.right === '-250px') {
        nav.style.right = '0'; // Slide in the nav
        toggleNav.style.right = '250px';
      } else {
        nav.style.right = '-250px';
        toggleNav.style.right = '0px'; // Slide out the nav
      }
    });
});
function showChatinput(){
    const chatinput=documen.querySelector('.chat-input')
    chatinput.style.display = 'flex'

}
document.addEventListener("DOMContentLoaded", function () {

    const toggleButton = document.getElementById("chatbot-toggle");
    const closeButton = document.getElementById("chatbot-close");
    const chatbotWindow = document.getElementById("chatbot-window");
    const ctaChatbot = document.getElementById("cta-chatbot");

    const input = document.getElementById("chatbot-input");
    const sendButton = document.getElementById("chatbot-send");
    const messages = document.getElementById("chatbot-messages");


    // Open chatbot
    toggleButton.addEventListener("click", function () {
        chatbotWindow.style.display = "flex";
        input.focus();
    });
    // Open chatbot from CTA button
    ctaChatbot.addEventListener("click", function () {
        chatbotWindow.style.display = "flex";
        input.focus();
    });

    // Close chatbot
    closeButton.addEventListener("click", function () {
        chatbotWindow.style.display = "none";
    });


    // Get CSRF token
    function getCSRFToken() {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith("csrftoken=")) {
                return cookie.substring("csrftoken=".length);
            }
        }

        return "";
    }


    // Add message to chat
    function addMessage(text, type) {

        const message = document.createElement("div");

        message.classList.add(
            type === "user" ? "user-message" : "bot-message"
        );

        message.textContent = text;

        messages.appendChild(message);

        messages.scrollTop = messages.scrollHeight;
    }


    // Send message
    async function sendMessage() {

        const message = input.value.trim();

        if (!message) {
            return;
        }

        // Show user message
        addMessage(message, "user");

        input.value = "";

        // Temporary loading message
        const loading = document.createElement("div");

        loading.classList.add("bot-message");
        loading.textContent = "Thinking...";

        messages.appendChild(loading);

        messages.scrollTop = messages.scrollHeight;


        try {

            const response = await fetch("/chatbot/api/chat/", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },

                body: JSON.stringify({
                    message: message
                })
            });


            const data = await response.json();

            loading.remove();


            if (data.success) {

                addMessage(data.response, "bot");

            } else {

                addMessage(
                    "Sorry, I couldn't process your message.",
                    "bot"
                );
            }


        } catch (error) {

            console.error("Chatbot Error:", error);

            loading.remove();

            addMessage(
                "Sorry, I am unable to connect to the AI assistant right now.",
                "bot"
            );
        }
    }


    // Send button
    sendButton.addEventListener("click", sendMessage);


    // Enter key
    input.addEventListener("keydown", function (event) {

        if (event.key === "Enter") {
            sendMessage();
        }

    });

});
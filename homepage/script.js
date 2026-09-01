document.addEventListener("DOMContentLoaded", function () {
    const welcomeButton = document.querySelector("#welcomeButton");

    if (welcomeButton) {
        welcomeButton.addEventListener("click", function () {
            alert("Welcome to my homepage!");
        });
    }

    const sendButton = document.querySelector("#sendButton");

    if (sendButton) {
        sendButton.addEventListener("click", function () {
            alert("Your message has been sent!");
        });
    }
});

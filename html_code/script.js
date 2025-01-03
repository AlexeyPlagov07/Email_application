// Select all buttons in the sidebar
const buttons = document.querySelectorAll('.sidebar button');

// Add click event listener to each button
buttons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove 'active' class from all buttons
        buttons.forEach(btn => btn.classList.remove('active'));
        
        // Add 'active' class to the clicked button
        button.classList.add('active');

        if (button.id == "button1") {
            window.location.href = 'website2.html';
        }
    });
});



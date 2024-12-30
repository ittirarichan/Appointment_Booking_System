document.getElementById('booking-form').addEventListener('submit', function(event) {
    event.preventDefault();
  
    // Hide form and show confirmation message
    document.querySelector('.token-booking').style.display = 'none';
    document.getElementById('confirmation-message').style.display = 'block';
  
    // Optionally, reset the form (if required after booking)
    // event.target.reset();
  });
  
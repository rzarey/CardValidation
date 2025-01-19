document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("paymentForm");
    const fields = ["email", "name", "card_number", "expiry_date", "cvv"];
    
     fields.forEach(field => {
       const inputField = document.getElementById(field);
       inputField.addEventListener('input', async () => {
         const warningSpan = document.getElementById(`${field}-warning`);
          const value = inputField.value;
          if (value.trim() === "") {
             warningSpan.textContent = "";
             return;
           }

          const response = await fetch('/validate', {
               method: 'POST',
               headers: {
                   'Content-Type': 'application/x-www-form-urlencoded',
               },
               body: `field=${field}&value=${encodeURIComponent(value)}`
          });
            const data = await response.json();
            if (!data.is_valid) {
                warningSpan.textContent = "Invalid input";
                inputField.classList.add("invalid-input");
                
            } else {
                warningSpan.textContent = "";
                inputField.classList.remove("invalid-input")
            }

        });

      inputField.addEventListener('focus', () => {
            inputField.classList.remove("invalid-input");
        });
    });


  form.addEventListener('submit', function(event) {
      let hasInvalidInput = false;
        fields.forEach(field => {
          const warningSpan = document.getElementById(`${field}-warning`);
          if (warningSpan.textContent !== "") {
             hasInvalidInput = true;
          }
        });

      if (hasInvalidInput) {
          event.preventDefault();
         alert("Please correct invalid input before submitting.");
      } else {
           // Animation for successful submission
         form.classList.add('submitted');
             setTimeout(() => {
               form.classList.remove('submitted');
             }, 500);
      }
  })
});
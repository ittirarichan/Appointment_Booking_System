        // City dropdown update based on state selection
        document.getElementById('state').addEventListener('change', function () {
            const state = this.value;
            const cityDropdown = document.getElementById('city');
            cityDropdown.innerHTML = '<option value="">Select City</option>';
            
            if (state) {
                fetch(`/get-cities/?state=${encodeURIComponent(state)}`)
                    .then(response => response.json())
                    .then(data => {
                        data.cities.forEach(city => {
                            const option = document.createElement('option');
                            option.value = city;
                            option.textContent = city;
                            cityDropdown.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Error fetching cities:', error));
            }
        });

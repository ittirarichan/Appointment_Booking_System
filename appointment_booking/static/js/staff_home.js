function generateToken() {
    const patientName = document.getElementById('patient-name').value;
    const doctorName = document.getElementById('doctor-name').value;
    if (patientName && doctorName) {
        const token = `Token for ${patientName} with ${doctorName}`;
        document.getElementById('token-display').innerText = token;
        alert(token);
    } else {
        alert('Please fill out all fields.');
    }
}

function addCategory() {
    const categoryName = document.getElementById('category-name').value;
    if (categoryName) {
        const categoriesList = document.getElementById('categories-list');
        const newCategory = document.createElement('li');
        newCategory.textContent = categoryName;
        categoriesList.appendChild(newCategory);
        document.getElementById('category-name').value = '';
    } else {
        alert('Please enter a category name.');
    }
}

function addDoctor() {
    const doctorName = document.getElementById('doctor-name-add').value;
    const specialization = document.getElementById('doctor-specialization').value;
    if (doctorName && specialization) {
        const doctorsList = document.getElementById('doctors-list');
        const newDoctor = document.createElement('li');
        newDoctor.textContent = `${doctorName} (${specialization})`;
        doctorsList.appendChild(newDoctor);
        document.getElementById('doctor-name-add').value = '';
        document.getElementById('doctor-specialization').value = '';
    } else {
        alert('Please fill out all fields.');
    }
}

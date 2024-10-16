document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loanForm');
    const result = document.getElementById('result');
    const predictionText = document.getElementById('predictionText');

    window.predictLoan = function() {
        const formData = {
            gender: document.getElementById('gender').value,
            age: document.getElementById('age').value,
            income: document.getElementById('income').value,
            employmentStatus: document.getElementById('employmentStatus').value,
            creditScore: document.getElementById('creditScore').value,
            loanAmount: document.getElementById('loanAmount').value,
            loanTerm: document.getElementById('loanTerm').value,
            propertyValue: document.getElementById('propertyValue').value
        };

        fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            result.classList.remove('hidden');
            predictionText.textContent = `Loan ${data.prediction}`;
            predictionText.className = data.prediction === 'Approved' ? 'approved' : 'not-approved';
        })
        .catch((error) => {
            result.classList.remove('hidden');
            predictionText.textContent = 'An error occurred during prediction';
            predictionText.className = 'not-approved';
        });
    };
});

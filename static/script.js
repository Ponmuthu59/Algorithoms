document.getElementById('algorithm').addEventListener('change', (event) => {
    const dhInputs = document.getElementById('dh-inputs');
    const stepsContainer = document.getElementById('steps-container');
    const decryptButton = document.getElementById('decrypt-button');

    const selectedAlgorithm = event.target.value;

    dhInputs.classList.toggle('hidden', selectedAlgorithm !== 'diffie_hellman');
    stepsContainer.style.display = selectedAlgorithm === 'diffie_hellman' ? 'block' : 'none';
    decryptButton.style.display = selectedAlgorithm === 'base64' ? 'block' : 'none';

    const rightPanelTitle = document.querySelector('#right-panel h2');
    rightPanelTitle.textContent = 
        selectedAlgorithm === 'diffie_hellman' ? 'Step-by-Step Process' : 'Generated Result';
});

document.getElementById('algorithm-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const response = await fetch('/generate', { method: 'POST', body: formData });

    if (response.ok) {
        const data = await response.json();

        if (data.steps) {
            const steps = data.steps;
            let currentStepIndex = 0;

            const currentStepElement = document.getElementById('current-step');
            const nextButton = document.getElementById('next-button');

            currentStepElement.textContent = steps[currentStepIndex];
            nextButton.onclick = () => {
                if (currentStepIndex < steps.length - 1) {
                    currentStepIndex++;
                    currentStepElement.textContent = steps[currentStepIndex];
                } else {
                    alert("You have reached the final step!");
                }
            };

            document.getElementById('steps-container').style.display = 'block';
        } else {
            alert(`Result: ${data.result}`);
        }
    } else {
        alert("An error occurred. Please check your input.");
    }
});

document.getElementById('decrypt-button').addEventListener('click', async () => {
    const formData = new FormData(document.getElementById('algorithm-form'));
    formData.append('action', 'decrypt');

    const response = await fetch('/generate', { method: 'POST', body: formData });

    if (response.ok) {
        const data = await response.json();
        alert(`Decrypted Result: ${data.result}`);
    } else {
        alert("Error decrypting data.");
    }
});

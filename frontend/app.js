const micBtn = document.getElementById('mic_btn');
const statusText = document.getElementById('status_text');
const userQueryElement = document.getElementById('user_query');
const responseTextElement = document.getElementById('response_text');
const dataContainer = document.getElementById('data_container');
const visualizer = document.getElementById('visualizer');
const agentName = document.getElementById('agent_name');

// Web Speech API setup
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;

if (recognition) {
    recognition.continuous = false;
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    micBtn.addEventListener('click', () => {
        try {
            recognition.start();
        } catch (e) {
            console.error('Speech recognition already started', e);
        }
    });

    recognition.onstart = () => {
        statusText.innerText = "Listening...";
        micBtn.classList.add('active');
        visualizer.classList.add('listening');
        userQueryElement.innerText = "Listening...";
        userQueryElement.classList.remove('placeholder');
    };

    recognition.onspeechend = () => {
        recognition.stop();
        micBtn.classList.remove('active');
        visualizer.classList.remove('listening');
        statusText.innerText = "Processing...";
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        userQueryElement.innerText = transcript;
        sendQueryToBackend(transcript);
    };

    recognition.onerror = (event) => {
        statusText.innerText = `Error: ${event.error}`;
        micBtn.classList.remove('active');
        visualizer.classList.remove('listening');
    };

} else {
    statusText.innerText = "Speech Recognition API not supported in this browser.";
    micBtn.disabled = true;
}

// Speak response via browser TTS (optional but nice)
function speakResponse(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        window.speechSynthesis.speak(utterance);
    }
}

async function sendQueryToBackend(query) {
    responseTextElement.innerText = "Coordinator Agent is determining intent...";
    agentName.innerText = "Coordinator Agent";
    dataContainer.innerHTML = '';
    
    try {
        const response = await fetch(`http://127.0.0.1:5000/voice-query?q=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        agentName.innerText = data.response.agent || "Coordinator Agent";
        
        statusText.innerText = "Tap the microphone to speak";
        
        const message = data.response.message;
        responseTextElement.innerText = message;
        speakResponse(message);

        // Display additional data payload if it exists
        if (data.response.trace) {
            dataContainer.innerHTML += `<div class="data-card"><strong>Trace:</strong> ${data.response.trace.join(' -> ')}</div>`;
        }

        if (data.response.tool) {
            dataContainer.innerHTML += `<div class="data-card"><strong>Tool:</strong> ${data.response.tool}</div>`;
        }

        if (data.response.data) {
            let html = '';
            if (Array.isArray(data.response.data)) {
                data.response.data.forEach(item => {
                    html += `<div class="data-card">${JSON.stringify(item)}</div>`;
                });
            } else {
                for (const [key, value] of Object.entries(data.response.data)) {
                    html += `<div class="data-card"><strong>${key}:</strong> ${value}</div>`;
                }
            }
            dataContainer.innerHTML += html;
        }

    } catch (error) {
        console.error('Error:', error);
        responseTextElement.innerText = "Error connecting to the backend. Is the Flask server running?";
        agentName.innerText = "System Error";
        statusText.innerText = "Server Error";
    }
}

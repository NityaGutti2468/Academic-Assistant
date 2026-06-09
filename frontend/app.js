const { useEffect, useMemo, useRef, useState } = React;
const h = React.createElement;

const API_BASE_URL = "http://127.0.0.1:5000";

function speakResponse(text) {
    if ("speechSynthesis" in window && text) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        window.speechSynthesis.speak(utterance);
    }
}

function MicIcon() {
    return h(
        "svg",
        {
            viewBox: "0 0 24 24",
            width: 32,
            height: 32,
            stroke: "currentColor",
            strokeWidth: 2,
            fill: "none",
            strokeLinecap: "round",
            strokeLinejoin: "round",
            "aria-hidden": "true",
        },
        h("path", { d: "M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z" }),
        h("path", { d: "M19 10v2a7 7 0 0 1-14 0v-2" }),
        h("line", { x1: 12, y1: 19, x2: 12, y2: 22 })
    );
}

function AgentIndicator({ agent }) {
    return h(
        "div",
        { className: "agent-indicator" },
        h("span", { className: "dot" }),
        h("span", null, agent || "Agent Context")
    );
}

function DataCards({ response }) {
    if (!response) {
        return null;
    }

    const cards = [];

    if (response.trace?.length) {
        cards.push(h("div", { className: "data-card", key: "trace" }, h("strong", null, "Trace: "), response.trace.join(" -> ")));
    }

    if (response.tool) {
        cards.push(h("div", { className: "data-card", key: "tool" }, h("strong", null, "Tool: "), response.tool));
    }

    if (response.planner) {
        cards.push(h("div", { className: "data-card", key: "planner" }, h("strong", null, "Planner: "), response.planner));
    }

    if (Array.isArray(response.data)) {
        response.data.forEach((item, index) => {
            cards.push(h("div", { className: "data-card", key: `data-${index}` }, JSON.stringify(item)));
        });
    } else if (response.data && typeof response.data === "object") {
        Object.entries(response.data).forEach(([key, value]) => {
            cards.push(h("div", { className: "data-card", key }, h("strong", null, `${key}: `), String(value)));
        });
    }

    return h("div", { className: "data-container" }, cards);
}

function VoiceAssistant() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = useMemo(() => {
        if (!SpeechRecognition) {
            return null;
        }

        const instance = new SpeechRecognition();
        instance.continuous = false;
        instance.lang = "en-US";
        instance.interimResults = false;
        instance.maxAlternatives = 1;
        return instance;
    }, [SpeechRecognition]);

    const recognitionRef = useRef(recognition);
    const [status, setStatus] = useState(recognition ? "Tap the microphone to speak" : "Speech Recognition API not supported in this browser.");
    const [isListening, setIsListening] = useState(false);
    const [query, setQuery] = useState("");
    const [manualQuery, setManualQuery] = useState("show my marks");
    const [backendStatus, setBackendStatus] = useState("Checking backend...");
    const [response, setResponse] = useState({
        agent: "Agent Context",
        message: "Ready to help you track your academics, attendance, and fees.",
    });

    useEffect(() => {
        async function checkBackend() {
            try {
                const result = await fetch(`${API_BASE_URL}/`);
                if (!result.ok) {
                    throw new Error(`Backend returned ${result.status}`);
                }
                setBackendStatus("Backend connected");
            } catch (error) {
                setBackendStatus("Backend not connected");
            }
        }

        checkBackend();
    }, []);

    async function sendQueryToBackend(nextQuery) {
        if (!nextQuery.trim()) {
            setStatus("Enter a question first");
            return;
        }

        setStatus("Processing...");
        setQuery(nextQuery);
        setResponse({
            agent: "Coordinator Agent",
            message: "Coordinator Agent is determining intent...",
        });

        try {
            const result = await fetch(`${API_BASE_URL}/voice-query?q=${encodeURIComponent(nextQuery)}`);
            if (!result.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await result.json();
            const agentResponse = data.response || {};
            setResponse(agentResponse);
            setBackendStatus("Backend connected");
            setStatus("Tap the microphone to speak");
            speakResponse(agentResponse.message);
        } catch (error) {
            console.error("Error:", error);
            setBackendStatus("Backend not connected");
            setResponse({
                agent: "System Error",
                message: `Error connecting to the backend at ${API_BASE_URL}. Keep Flask running, then try again.`,
            });
            setStatus("Server Error");
        }
    }

    function submitManualQuery(event) {
        event.preventDefault();
        sendQueryToBackend(manualQuery);
    }

    function startListening() {
        if (!recognitionRef.current) {
            return;
        }

        recognitionRef.current.onstart = () => {
            setStatus("Listening...");
            setIsListening(true);
            setQuery("Listening...");
        };

        recognitionRef.current.onspeechend = () => {
            recognitionRef.current.stop();
            setIsListening(false);
            setStatus("Processing...");
        };

        recognitionRef.current.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            setQuery(transcript);
            sendQueryToBackend(transcript);
        };

        recognitionRef.current.onerror = (event) => {
            setStatus(`Error: ${event.error}`);
            setIsListening(false);
        };

        try {
            recognitionRef.current.start();
        } catch (error) {
            console.error("Speech recognition already started", error);
        }
    }

    return h(
        React.Fragment,
        null,
        h("div", { className: "overlay" }),
        h(
            "div",
            { className: "container" },
            h(
                "header",
                null,
                h("div", { className: "logo" }, h("div", { className: "orb" }), h("h1", null, "Nexia Assistant")),
                h("p", null, "Your Voice-Active Multi-Agent ERP"),
                h("div", { className: backendStatus === "Backend connected" ? "backend-status connected" : "backend-status" }, backendStatus)
            ),
            h(
                "main",
                null,
                h(
                    "section",
                    { className: "voice-interaction" },
                    h(
                        "div",
                        { className: `ai-visualizer ${isListening ? "listening" : ""}` },
                        h("div", { className: "ring r1" }),
                        h("div", { className: "ring r2" }),
                        h("div", { className: "ring r3" })
                    ),
                    h("h2", null, status),
                    h("button", { className: `mic-btn ${isListening ? "active" : ""}`, onClick: startListening, disabled: !recognition }, h(MicIcon))
                ),
                h(
                    "form",
                    { className: "query-form", onSubmit: submitManualQuery },
                    h("input", {
                        value: manualQuery,
                        onChange: (event) => setManualQuery(event.target.value),
                        placeholder: "Ask about marks, attendance, fees...",
                    }),
                    h("button", { type: "submit" }, "Ask")
                ),
                h("section", { className: "transcript-box" }, h("h3", null, "You:"), h("p", { className: query ? "" : "placeholder" }, query || "Awaiting input...")),
                h("section", { className: "response-box" }, h(AgentIndicator, { agent: response.agent }), h("h3", null, response.message), h(DataCards, { response }))
            )
        )
    );
}

ReactDOM.createRoot(document.getElementById("root")).render(h(VoiceAssistant));

export class SpeechRecognitionService {
    constructor(language = "fa-IR") {
        window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!window.SpeechRecognition) {
            throw new Error("مرورگر شما از Web Speech API پشتیبانی نمی‌کند.");
        }

        this.recognition = new window.SpeechRecognition();
        this.recognition.lang = language;
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
    }

    startListening(onResult, onError) {
        this.recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            onResult(text);
        };

        this.recognition.onerror = (event) => {
            if (onError) onError(event.error);
        };

        this.recognition.start();
    }
}

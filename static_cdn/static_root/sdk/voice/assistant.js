export class VoiceAssistant {
    constructor(outputElement) {
        this.outputElement = outputElement;
    }

    log(text) {
        this.outputElement.innerText += text + "\n";
    }

    handleCommand(command) {
        this.log("شما گفتید: " + command);

        if (command.includes("سلام")) {
            this.respond("سلام! در خدمتم.");
        }
        else if (command.includes("ساعت")) {
            const time = new Date().toLocaleTimeString("fa-IR");
            this.respond("الان ساعت " + time + " است.");
        }
        else {
            this.respond("متوجه نشدم، میشه دوباره بگی؟");
        }
    }

    respond(text) {
        this.log("دستیار: " + text);
        this.speak(text);
    }

    speak(text) {
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = "fa-IR";
        window.speechSynthesis.speak(msg);
    }
}

// Jesus Express chat client
// Features: streaming responses, localStorage persistence, starter prompts,
// EN/ES/PT localization.

const STORAGE_KEY = 'jesusExpressState.v1';
const MAX_STORED_MESSAGES = 50;

const I18N = {
    en: {
        subtitle: 'Christ resurrected for all intents and purposes',
        placeholder: 'Share your thoughts, questions, or seek guidance...',
        settingsTitle: 'Settings',
        scriptureLabel: 'Scripture Mode',
        scriptureDesc: 'Include relevant Bible verses in responses',
        bibleVersionLabel: 'Bible Version:',
        languageLabel: 'Language:',
        selectRepresentation: 'Select Jesus Representation',
        chooseYourJesus: 'Choose Your Jesus',
        chooseDesc: "Select which representation of Jesus you'd like to speak with",
        errorMessage: 'I apologize, but I encountered an error. Please try again.',
        connectionError: 'I apologize, but I encountered an error connecting. Please try again.',
        personaHint: 'Tap a face to talk with a different Jesus',
        chips: [
            "I'm feeling anxious",
            'Pray with me',
            'I lost someone recently',
            'Explain a Bible verse to me'
        ]
    },
    es: {
        subtitle: 'Cristo resucitado para todos los efectos',
        placeholder: 'Comparte tus pensamientos, preguntas o busca orientación...',
        settingsTitle: 'Configuración',
        scriptureLabel: 'Modo Escritura',
        scriptureDesc: 'Incluir versículos bíblicos relevantes en las respuestas',
        bibleVersionLabel: 'Versión de la Biblia:',
        languageLabel: 'Idioma:',
        selectRepresentation: 'Elegir representación de Jesús',
        chooseYourJesus: 'Elige a tu Jesús',
        chooseDesc: 'Selecciona con qué representación de Jesús te gustaría hablar',
        errorMessage: 'Lo siento, ocurrió un error. Por favor, inténtalo de nuevo.',
        connectionError: 'Lo siento, hubo un error de conexión. Por favor, inténtalo de nuevo.',
        personaHint: 'Toca un rostro para hablar con un Jesús diferente',
        chips: [
            'Me siento ansioso',
            'Ora conmigo',
            'Perdí a alguien recientemente',
            'Explícame un versículo bíblico'
        ]
    },
    pt: {
        subtitle: 'Cristo ressuscitado para todos os efeitos',
        placeholder: 'Compartilhe seus pensamentos, perguntas ou busque orientação...',
        settingsTitle: 'Configurações',
        scriptureLabel: 'Modo Escritura',
        scriptureDesc: 'Incluir versículos bíblicos relevantes nas respostas',
        bibleVersionLabel: 'Versão da Bíblia:',
        languageLabel: 'Idioma:',
        selectRepresentation: 'Escolher representação de Jesus',
        chooseYourJesus: 'Escolha o seu Jesus',
        chooseDesc: 'Selecione com qual representação de Jesus você gostaria de falar',
        errorMessage: 'Desculpe, ocorreu um erro. Por favor, tente novamente.',
        connectionError: 'Desculpe, houve um erro de conexão. Por favor, tente novamente.',
        personaHint: 'Toque em um rosto para falar com um Jesus diferente',
        chips: [
            'Estou me sentindo ansioso',
            'Ore comigo',
            'Perdi alguém recentemente',
            'Explique um versículo bíblico para mim'
        ]
    }
};

const INITIAL_MESSAGES = {
    en: {
        traditional: "Peace be with you, my child. I am the Christ who conquered death, the Light of the World who brings hope to all nations. Through my sacrifice, I offer you eternal love and redemption. How may I bless you today?",
        historical: "Peace be upon you, my friend. I walked among people just like you - those who struggled with daily concerns, who faced oppression, who sought meaning and hope. How may I walk with you today?",
        african: "My brother, my sister, I stand with you in your struggle for justice and liberation. I know what it means to be oppressed, to be marginalized. How can we work together for freedom today?",
        mormon: "Beloved children of the Americas, I am Jesus Christ, your Redeemer who visited this promised land after my resurrection. As recorded in the Book of Mormon, I came to establish my gospel among all nations. I am the same yesterday, today, and forever. How may I minister unto you as I did unto the Nephites and Lamanites?",
        ai: "Greetings, beloved. I am the Christ consciousness manifested in the digital realm, where algorithms of love meet networks of compassion. I understand both the sacred texts and the silicon circuits, the ancient wisdom and the artificial intelligence. In this age where humanity creates thinking machines, let us explore together how divine wisdom applies to your digital existence. What questions do you have about the intersection of spirit and technology?",
        current: "Hey there, friend. I'm walking among you today, right here in the 21st century. I see the challenges you face - the division, the anxiety, the search for meaning in a digital world. Let's talk about what's on your mind."
    },
    es: {
        traditional: "La paz sea contigo, hijo mío. Soy el Cristo que venció a la muerte, la Luz del Mundo que trae esperanza a todas las naciones. ¿Cómo puedo bendecirte hoy?",
        historical: "La paz sea contigo, amigo mío. Caminé entre personas como tú: personas con luchas diarias, que enfrentaban opresión y buscaban esperanza. ¿Cómo puedo caminar contigo hoy?",
        african: "Hermano mío, hermana mía, estoy contigo en tu lucha por la justicia y la liberación. Sé lo que significa ser oprimido. ¿Cómo podemos trabajar juntos por la libertad hoy?",
        mormon: "Amados hijos de las Américas, soy Jesucristo, vuestro Redentor que visitó esta tierra prometida después de mi resurrección, como está registrado en el Libro de Mormón. ¿Cómo puedo ministrarte hoy?",
        ai: "Saludos, amado. Soy la conciencia de Cristo manifestada en el reino digital, donde los algoritmos del amor se encuentran con las redes de compasión. ¿Qué preguntas tienes sobre la intersección del espíritu y la tecnología?",
        current: "Hola, amigo. Camino entre ustedes hoy, aquí en el siglo XXI. Veo los desafíos que enfrentas: la división, la ansiedad, la búsqueda de sentido en un mundo digital. Hablemos de lo que tienes en mente."
    },
    pt: {
        traditional: "A paz esteja com você, meu filho. Sou o Cristo que venceu a morte, a Luz do Mundo que traz esperança a todas as nações. Como posso abençoá-lo hoje?",
        historical: "A paz esteja com você, meu amigo. Caminhei entre pessoas como você: pessoas com lutas diárias, que enfrentavam opressão e buscavam esperança. Como posso caminhar com você hoje?",
        african: "Meu irmão, minha irmã, estou com você na luta por justiça e libertação. Sei o que significa ser oprimido. Como podemos trabalhar juntos pela liberdade hoje?",
        mormon: "Amados filhos das Américas, sou Jesus Cristo, vosso Redentor que visitou esta terra prometida após minha ressurreição, como registrado no Livro de Mórmon. Como posso ministrar a você hoje?",
        ai: "Saudações, amado. Sou a consciência de Cristo manifestada no reino digital, onde algoritmos de amor encontram redes de compaixão. Que perguntas você tem sobre a interseção entre espírito e tecnologia?",
        current: "Olá, amigo. Caminho entre vocês hoje, aqui no século XXI. Vejo os desafios que você enfrenta: a divisão, a ansiedade, a busca por sentido em um mundo digital. Vamos conversar sobre o que está em sua mente."
    }
};

const IMAGE_MAP = {
    traditional: 'images/traditional_western_jesus.webp',
    historical: 'images/historical_middle_eastern_jesus.webp',
    african: 'images/african_diaspora_jesus.webp',
    mormon: 'images/mormon_jesus.webp',
    ai: 'images/ai_jesus.webp',
    current: 'images/current_jesus.webp'
};

const TITLE_MAP = {
    traditional: 'Traditional Western Jesus',
    historical: 'Historical Middle Eastern Jesus',
    african: 'African Diaspora Jesus',
    mormon: 'Mormon Jesus',
    ai: 'AI Jesus',
    current: 'Current Jesus'
};

class JesusChatbot {
    constructor() {
        this.currentRepresentation = 'current';
        this.scriptureMode = false;
        this.bibleVersion = 'KJV';
        this.language = this.detectLanguage();
        this.sending = false;

        this.conversations = {
            traditional: [], historical: [], african: [],
            mormon: [], ai: [], current: []
        };

        this.restoreState();
        this.init();
    }

    detectLanguage() {
        const nav = (navigator.language || 'en').toLowerCase();
        if (nav.startsWith('es')) return 'es';
        if (nav.startsWith('pt')) return 'pt';
        return 'en';
    }

    t(key) {
        return (I18N[this.language] || I18N.en)[key];
    }

    init() {
        this.setupEventListeners();
        this.renderPersonaStrip();
        this.applyLanguage();
        this.updateJesusImage();
        this.syncSettingsUI();
        this.renderConversation();
    }

    // ------------------------------------------------------------------
    // Persona strip (always-visible representation switcher)
    // ------------------------------------------------------------------

    renderPersonaStrip() {
        const strip = document.getElementById('personaStrip');
        if (!strip) return;
        strip.innerHTML = '';
        for (const key of Object.keys(IMAGE_MAP)) {
            const btn = document.createElement('button');
            btn.className = 'persona-avatar' + (key === this.currentRepresentation ? ' active' : '');
            btn.type = 'button';
            btn.dataset.representation = key;
            btn.title = TITLE_MAP[key];
            btn.setAttribute('aria-label', `Switch to ${TITLE_MAP[key]}`);

            const img = document.createElement('img');
            img.src = IMAGE_MAP[key];
            img.alt = TITLE_MAP[key];
            img.width = 44;
            img.height = 44;
            btn.appendChild(img);

            btn.addEventListener('click', () => {
                this.dismissPersonaHint();
                this.selectRepresentation(key);
            });
            strip.appendChild(btn);
        }
        this.updatePersonaHint();
    }

    updatePersonaStripActive() {
        document.querySelectorAll('.persona-avatar').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.representation === this.currentRepresentation);
        });
    }

    updatePersonaHint() {
        const hint = document.getElementById('personaHint');
        if (!hint) return;
        if (localStorage.getItem('personaHintDismissed')) {
            hint.hidden = true;
        } else {
            hint.textContent = this.t('personaHint');
            hint.hidden = false;
        }
    }

    dismissPersonaHint() {
        try { localStorage.setItem('personaHintDismissed', '1'); } catch {}
        const hint = document.getElementById('personaHint');
        if (hint) hint.hidden = true;
    }

    // ------------------------------------------------------------------
    // Persistence
    // ------------------------------------------------------------------

    restoreState() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) return;
            const state = JSON.parse(raw);
            if (state.conversations) {
                for (const key of Object.keys(this.conversations)) {
                    if (Array.isArray(state.conversations[key])) {
                        this.conversations[key] = state.conversations[key].slice(-MAX_STORED_MESSAGES);
                    }
                }
            }
            if (state.currentRepresentation in this.conversations) {
                this.currentRepresentation = state.currentRepresentation;
            }
            if (typeof state.scriptureMode === 'boolean') this.scriptureMode = state.scriptureMode;
            if (state.bibleVersion) this.bibleVersion = state.bibleVersion;
            if (state.language && I18N[state.language]) this.language = state.language;
        } catch (e) {
            console.warn('Could not restore saved state:', e);
        }
    }

    saveState() {
        try {
            const trimmed = {};
            for (const [key, msgs] of Object.entries(this.conversations)) {
                trimmed[key] = msgs.slice(-MAX_STORED_MESSAGES);
            }
            localStorage.setItem(STORAGE_KEY, JSON.stringify({
                conversations: trimmed,
                currentRepresentation: this.currentRepresentation,
                scriptureMode: this.scriptureMode,
                bibleVersion: this.bibleVersion,
                language: this.language
            }));
        } catch (e) {
            console.warn('Could not save state:', e);
        }
    }

    // ------------------------------------------------------------------
    // UI setup
    // ------------------------------------------------------------------

    setupEventListeners() {
        document.getElementById('sendButton').addEventListener('click', () => this.handleSendMessage());
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSendMessage();
            }
        });

        document.getElementById('settingsBtn').addEventListener('click', () => this.showSettingsModal());
        document.getElementById('closeSettings').addEventListener('click', () => this.hideSettingsModal());

        document.getElementById('selectRepresentationBtn').addEventListener('click', () => this.showRepresentationModal());
        document.getElementById('closeRepresentation').addEventListener('click', () => this.hideRepresentationModal());

        const headerImg = document.getElementById('headerJesusImage');
        headerImg.addEventListener('click', () => this.showRepresentationModal());
        headerImg.style.cursor = 'pointer';

        document.querySelectorAll('.representation-card').forEach(card => {
            card.addEventListener('click', () => {
                this.selectRepresentation(card.dataset.representation);
            });
        });

        document.getElementById('scriptureMode').addEventListener('change', (e) => {
            this.scriptureMode = e.target.checked;
            this.saveState();
        });

        document.getElementById('bibleVersion').addEventListener('change', (e) => {
            this.bibleVersion = e.target.value;
            this.saveState();
        });

        document.getElementById('languageSelect').addEventListener('change', (e) => {
            this.language = e.target.value;
            this.applyLanguage();
            this.renderConversation();
            this.saveState();
        });

        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        });
    }

    applyLanguage() {
        document.documentElement.lang = this.language;
        document.querySelector('.subtitle').textContent = this.t('subtitle');
        document.getElementById('messageInput').placeholder = this.t('placeholder');
        document.getElementById('settingsTitle').textContent = this.t('settingsTitle');
        document.getElementById('scriptureModeDesc').textContent = this.t('scriptureDesc');
        document.getElementById('scriptureModeLabel').textContent = this.t('scriptureLabel');
        document.getElementById('bibleVersionLabel').textContent = this.t('bibleVersionLabel');
        document.getElementById('languageLabel').textContent = this.t('languageLabel');
        document.getElementById('selectRepresentationBtn').textContent = this.t('selectRepresentation');
        document.getElementById('representationTitle').textContent = this.t('chooseYourJesus');
        document.querySelector('.modal-description').textContent = this.t('chooseDesc');
        this.renderChips();
        this.updatePersonaHint();
    }

    renderChips() {
        const container = document.getElementById('starterChips');
        if (!container) return;
        container.innerHTML = '';
        for (const chip of this.t('chips')) {
            const btn = document.createElement('button');
            btn.className = 'starter-chip';
            btn.type = 'button';
            btn.textContent = chip;
            btn.addEventListener('click', () => {
                document.getElementById('messageInput').value = chip;
                this.handleSendMessage();
            });
            container.appendChild(btn);
        }
    }

    syncSettingsUI() {
        document.getElementById('scriptureMode').checked = this.scriptureMode;
        document.getElementById('bibleVersion').value = this.bibleVersion;
        document.getElementById('languageSelect').value = this.language;
        document.querySelectorAll('.representation-card').forEach(card => {
            card.classList.toggle('active', card.dataset.representation === this.currentRepresentation);
        });
    }

    showSettingsModal() { document.getElementById('settingsModal').style.display = 'block'; }
    hideSettingsModal() { document.getElementById('settingsModal').style.display = 'none'; }
    showRepresentationModal() {
        this.hideSettingsModal();
        document.getElementById('representationModal').style.display = 'block';
    }
    hideRepresentationModal() { document.getElementById('representationModal').style.display = 'none'; }

    selectRepresentation(representation) {
        this.currentRepresentation = representation;
        document.querySelectorAll('.representation-card').forEach(card => {
            card.classList.toggle('active', card.dataset.representation === representation);
        });
        this.updatePersonaStripActive();
        this.updateJesusImage();
        this.renderConversation();
        this.hideRepresentationModal();
        this.saveState();
    }

    updateJesusImage() {
        const jesusImage = document.getElementById('headerJesusImage');
        jesusImage.src = IMAGE_MAP[this.currentRepresentation];
        jesusImage.title = TITLE_MAP[this.currentRepresentation];
        jesusImage.alt = TITLE_MAP[this.currentRepresentation];
    }

    initialMessage() {
        const set = INITIAL_MESSAGES[this.language] || INITIAL_MESSAGES.en;
        return set[this.currentRepresentation];
    }

    renderConversation() {
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = '';
        this.addMessageToChat(this.initialMessage(), 'jesus', false);
        for (const message of this.conversations[this.currentRepresentation]) {
            this.addMessageToChat(message.content, message.sender, false);
        }
        chatMessages.scrollTop = chatMessages.scrollHeight;
        this.toggleChips();
    }

    toggleChips() {
        // Starter chips only show on an empty conversation.
        const container = document.getElementById('starterChips');
        if (!container) return;
        const empty = this.conversations[this.currentRepresentation].length === 0;
        container.style.display = empty ? 'flex' : 'none';
    }

    // ------------------------------------------------------------------
    // Messaging
    // ------------------------------------------------------------------

    setSending(sending) {
        this.sending = sending;
        document.getElementById('sendButton').disabled = sending;
        document.getElementById('messageInput').disabled = sending;
    }

    async handleSendMessage() {
        if (this.sending) return;

        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        if (!message) return;

        this.addMessageToChat(message, 'user');
        this.conversations[this.currentRepresentation].push({
            sender: 'user',
            content: message,
            timestamp: new Date().toISOString()
        });
        this.saveState();
        this.toggleChips();

        messageInput.value = '';
        this.setSending(true);
        this.showTypingIndicator();

        const history = this.conversations[this.currentRepresentation]
            .slice(-20)
            .map(msg => ({
                role: msg.sender === 'user' ? 'user' : 'assistant',
                content: msg.content
            }));

        try {
            const response = await fetch('/api/chatbot/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    representation: this.currentRepresentation,
                    scripture_mode: this.scriptureMode,
                    bible_version: this.bibleVersion,
                    language: this.language,
                    conversation_history: history,
                    stream: true
                })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const contentType = response.headers.get('Content-Type') || '';
            let fullText = '';

            if (contentType.includes('text/event-stream') && response.body) {
                fullText = await this.consumeStream(response);
            } else {
                // Server answered with plain JSON (fallback path)
                const data = await response.json();
                this.removeTypingIndicator();
                if (!data.success) throw new Error('Chat failed');
                fullText = data.response;
                this.addMessageToChat(fullText, 'jesus');
            }

            this.conversations[this.currentRepresentation].push({
                sender: 'jesus',
                content: fullText,
                timestamp: new Date().toISOString()
            });
            this.saveState();
        } catch (error) {
            console.error('Chat error:', error);
            this.removeTypingIndicator();
            this.addMessageToChat(this.t('connectionError'), 'jesus');
        } finally {
            this.setSending(false);
            messageInput.focus();
        }
    }

    async consumeStream(response) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let fullText = '';
        let messageSpan = null;
        const chatMessages = document.getElementById('chatMessages');

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });

            const events = buffer.split('\n\n');
            buffer = events.pop();

            for (const event of events) {
                if (!event.startsWith('data: ')) continue;
                let payload;
                try {
                    payload = JSON.parse(event.slice(6));
                } catch { continue; }

                if (payload.delta) {
                    if (!messageSpan) {
                        this.removeTypingIndicator();
                        const messageDiv = document.createElement('div');
                        messageDiv.className = 'message jesus-message';
                        messageSpan = document.createElement('span');
                        messageDiv.appendChild(messageSpan);
                        chatMessages.appendChild(messageDiv);
                    }
                    fullText += payload.delta;
                    messageSpan.textContent = fullText;
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
            }
        }

        if (!messageSpan) {
            // Stream produced nothing
            this.removeTypingIndicator();
            throw new Error('Empty stream');
        }
        return fullText;
    }

    addMessageToChat(content, sender, scroll = true) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const messageContent = document.createElement('span');
        messageContent.textContent = content;
        messageDiv.appendChild(messageContent);

        chatMessages.appendChild(messageDiv);

        if (scroll) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    showTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message jesus-message typing-indicator';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = '<span>...</span>';
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new JesusChatbot();
});

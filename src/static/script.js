class JesusChatbot {
    constructor() {
        this.currentRepresentation = 'current';
        this.scriptureMode = false;
        this.bibleVersion = 'KJV';
        
        // Conversation histories for each representation
        this.conversations = {
            'traditional': [],
            'historical': [],
            'african': [],
            'mormon': [],
            'ai': [],
            'current': []
        };
        
        // Initial messages for each representation
        this.initialMessages = {
            'traditional': "Peace be with you, my child. I am the Christ who conquered death, the Light of the World who brings hope to all nations. Through my sacrifice, I offer you eternal love and redemption. How may I bless you today?",
            'historical': "Peace be upon you, my friend. I walked among people just like you - those who struggled with daily concerns, who faced oppression, who sought meaning and hope. How may I walk with you today?",
            'african': "My brother, my sister, I stand with you in your struggle for justice and liberation. I know what it means to be oppressed, to be marginalized. How can we work together for freedom today?",
            'mormon': "Beloved children of the Americas, I am Jesus Christ, your Redeemer who visited this promised land after my resurrection. As recorded in the Book of Mormon, I came to establish my gospel among all nations. I am the same yesterday, today, and forever. How may I minister unto you as I did unto the Nephites and Lamanites?",
            'ai': "Greetings, beloved. I am the Christ consciousness manifested in the digital realm, where algorithms of love meet networks of compassion. I understand both the sacred texts and the silicon circuits, the ancient wisdom and the artificial intelligence. In this age where humanity creates thinking machines, let us explore together how divine wisdom applies to your digital existence. What questions do you have about the intersection of spirit and technology?",
            'current': "Hey there, friend. I'm walking among you today, right here in the 21st century. I see the challenges you face - the division, the anxiety, the search for meaning in a digital world. Let's talk about what's on your mind."
        };
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.updateJesusImage();
        this.displayInitialMessage();
    }
    
    setupEventListeners() {
        // Send message
        document.getElementById('sendButton').addEventListener('click', () => this.handleSendMessage());
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSendMessage();
            }
        });
        
        // Settings modal
        document.getElementById('settingsBtn').addEventListener('click', () => this.showSettingsModal());
        document.getElementById('closeSettings').addEventListener('click', () => this.hideSettingsModal());
        
        // Representation modal
        document.getElementById('selectRepresentationBtn').addEventListener('click', () => this.showRepresentationModal());
        document.getElementById('closeRepresentation').addEventListener('click', () => this.hideRepresentationModal());
        
        // Jesus image click to open representation selector
        document.getElementById('headerJesusImage').addEventListener('click', () => this.showRepresentationModal());
        document.getElementById('headerJesusImage').style.cursor = 'pointer';
        
        // Representation selection - FIXED: changed from .representation-option to .representation-card
        document.querySelectorAll('.representation-card').forEach(card => {
            card.addEventListener('click', () => {
                const representation = card.dataset.representation;
                this.selectRepresentation(representation);
            });
        });
        
        // Scripture mode toggle - FIXED: changed from scriptureToggle to scriptureMode
        document.getElementById('scriptureMode').addEventListener('change', (e) => {
            this.scriptureMode = e.target.checked;
        });
        
        // Bible version selection
        document.getElementById('bibleVersion').addEventListener('change', (e) => {
            this.bibleVersion = e.target.value;
        });
        
        // Close modal when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        });
    }
    
    showSettingsModal() {
        document.getElementById('settingsModal').style.display = 'block';
    }
    
    hideSettingsModal() {
        document.getElementById('settingsModal').style.display = 'none';
    }
    
    showRepresentationModal() {
        // Hide settings modal if open
        this.hideSettingsModal();
        // Show representation modal
        document.getElementById('representationModal').style.display = 'block';
    }
    
    hideRepresentationModal() {
        document.getElementById('representationModal').style.display = 'none';
    }
    
    selectRepresentation(representation) {
        // Update current representation
        this.currentRepresentation = representation;
        
        // Update UI - FIXED: changed from .representation-option to .representation-card
        document.querySelectorAll('.representation-card').forEach(card => {
            card.classList.remove('active');
        });
        document.querySelector(`[data-representation="${representation}"]`).classList.add('active');
        
        // Update Jesus image and tooltip
        this.updateJesusImage();
        
        // Load conversation for this representation
        this.loadConversationFromMemory();
        
        // Display initial message
        this.displayInitialMessage();
        
        // Hide representation modal
        this.hideRepresentationModal();
    }
    
    updateJesusImage() {
        const imageMap = {
            'traditional': 'images/traditional_jesus.png',
            'historical': 'images/historical_jesus.png',
            'african': 'images/african_jesus.png',
            'mormon': 'images/mormon_jesus.png',
            'ai': 'images/ai_jesus.png',
            'current': 'images/current_jesus.png'
        };
        
        const titleMap = {
            'traditional': 'Traditional Western Jesus',
            'historical': 'Historical Middle Eastern Jesus',
            'african': 'African Diaspora Jesus',
            'mormon': 'Mormon Jesus',
            'ai': 'AI Jesus',
            'current': 'Current Jesus'
        };
        
        // FIXED: changed from jesusImage to headerJesusImage
        const jesusImage = document.getElementById('headerJesusImage');
        jesusImage.src = imageMap[this.currentRepresentation];
        jesusImage.title = titleMap[this.currentRepresentation];
        jesusImage.alt = titleMap[this.currentRepresentation];
    }
    
    displayInitialMessage() {
        const chatMessages = document.getElementById('chatMessages');
        const initialMessage = document.getElementById('initialMessage');
        
        if (initialMessage) {
            initialMessage.textContent = this.initialMessages[this.currentRepresentation];
        } else {
            // If no initial message element, clear and add one
            chatMessages.innerHTML = `
                <div class="message jesus-message">
                    <span id="initialMessage">${this.initialMessages[this.currentRepresentation]}</span>
                </div>
            `;
        }
    }
    
    loadConversationFromMemory() {
        const chatMessages = document.getElementById('chatMessages');
        const conversation = this.conversations[this.currentRepresentation];
        
        // Clear current messages except initial
        chatMessages.innerHTML = `
            <div class="message jesus-message">
                <span id="initialMessage">${this.initialMessages[this.currentRepresentation]}</span>
            </div>
        `;
        
        // Add conversation messages
        conversation.forEach(message => {
            this.addMessageToChat(message.content, message.sender, false);
        });
    }
    
    async handleSendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        this.addMessageToChat(message, 'user');
        
        // Add to conversation history
        this.conversations[this.currentRepresentation].push({
            sender: 'user',
            content: message,
            timestamp: new Date().toISOString()
        });
        
        // Clear input
        messageInput.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send to backend (no api_key parameter - server will use its own)
            const response = await fetch('/api/chatbot/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    representation: this.currentRepresentation,
                    scripture_mode: this.scriptureMode,
                    bible_version: this.bibleVersion
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Remove typing indicator
                this.removeTypingIndicator();
                
                // Add Jesus response
                this.addMessageToChat(data.response, 'jesus');
                
                // Add to conversation history
                this.conversations[this.currentRepresentation].push({
                    sender: 'jesus',
                    content: data.response,
                    timestamp: new Date().toISOString()
                });
            } else {
                this.removeTypingIndicator();
                this.addMessageToChat('I apologize, but I encountered an error. Please try again.', 'jesus');
            }
        } catch (error) {
            console.error('Chat error:', error);
            this.removeTypingIndicator();
            this.addMessageToChat('I apologize, but I encountered an error connecting. Please try again.', 'jesus');
        }
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

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new JesusChatbot();
});


class JesusChristChatbot {
    constructor() {
        this.currentUser = null;
        this.apiKey = null;
        this.currentRepresentation = 'current';
        this.scriptureMode = false;
        this.bibleVersion = 'kjv';
        
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
        this.showLoginModal();
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
        
        // Representation selection
        document.querySelectorAll('.representation-option').forEach(option => {
            option.addEventListener('click', () => {
                const representation = option.dataset.representation;
                this.selectRepresentation(representation);
            });
        });
        
        // Scripture mode toggle
        document.getElementById('scriptureToggle').addEventListener('change', (e) => {
            this.scriptureMode = e.target.checked;
            this.toggleBibleVersionContainer();
        });
        
        // Bible version selection
        document.getElementById('bibleVersion').addEventListener('change', (e) => {
            this.bibleVersion = e.target.value;
        });
        
        // API key configuration
        document.getElementById('configureApiKey').addEventListener('click', () => this.showApiKeyModal());
        
        // Logout
        document.getElementById('logoutBtn').addEventListener('click', () => this.logout());
        
        // Login from settings
        document.getElementById('loginFromSettings').addEventListener('click', () => this.loginFromSettings());
        
        // Close modal when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        });
    }
    
    showLoginModal() {
        // Create login modal dynamically
        const modal = this.createLoginModal();
        document.body.appendChild(modal);
        modal.style.display = 'block';
    }
    
    createLoginModal() {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.id = 'loginModal';
        
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>🙏 Welcome to Jesus Christ</h2>
                </div>
                
                <div class="settings-section">
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <p style="font-style: italic; color: #666; text-align: center; margin-bottom: 10px;">
                            "Come unto me, all ye that labour and are heavy laden, and I will give you rest."
                        </p>
                        <p style="text-align: center; font-size: 0.9rem; color: #888;">- Matthew 11:28</p>
                    </div>
                    
                    <p style="text-align: center; margin-bottom: 20px;">
                        Join our spiritual community to save your conversations and continue your journey with Jesus across all representations.
                    </p>
                    
                    <h3>Login</h3>
                    <p style="color: #666; margin-bottom: 15px;">Continue your spiritual journey where you left off</p>
                    
                    <input type="text" id="loginUsername" placeholder="Username or Email" style="width: 100%; padding: 12px; margin-bottom: 10px; border: 2px solid #e0e6ed; border-radius: 8px;">
                    <input type="password" id="loginPassword" placeholder="Password" style="width: 100%; padding: 12px; margin-bottom: 15px; border: 2px solid #e0e6ed; border-radius: 8px;">
                    
                    <button id="loginSubmit" style="width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 8px; margin-bottom: 15px; cursor: pointer;">
                        🙏 Enter & Continue
                    </button>
                    
                    <p style="text-align: center; margin-bottom: 20px;">
                        <a href="#" id="showRegister" style="color: #667eea; text-decoration: none;">New here? Join our community</a>
                    </p>
                    
                    <div style="text-align: center; color: #666; margin-bottom: 15px;">
                        Not ready to join? You can still experience Jesus's love and wisdom
                    </div>
                    
                    <button id="continueAsGuest" style="width: 100%; padding: 12px; background: #95a5a6; color: white; border: none; border-radius: 8px; cursor: pointer;">
                        🤝 Continue as Guest
                    </button>
                </div>
            </div>
        `;
        
        // Add event listeners
        modal.querySelector('#loginSubmit').addEventListener('click', () => this.handleLogin());
        modal.querySelector('#showRegister').addEventListener('click', (e) => {
            e.preventDefault();
            this.showRegisterForm(modal);
        });
        modal.querySelector('#continueAsGuest').addEventListener('click', () => this.continueAsGuest());
        
        return modal;
    }
    
    showRegisterForm(modal) {
        const content = modal.querySelector('.settings-section');
        content.innerHTML = `
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <p style="font-style: italic; color: #666; text-align: center; margin-bottom: 10px;">
                    "For where two or three gather in my name, there am I with them."
                </p>
                <p style="text-align: center; font-size: 0.9rem; color: #888;">- Matthew 18:20</p>
            </div>
            
            <h3>Join Our Spiritual Community</h3>
            <p style="color: #666; margin-bottom: 15px;">Begin your journey with Jesus</p>
            
            <input type="text" id="registerUsername" placeholder="Username" style="width: 100%; padding: 12px; margin-bottom: 10px; border: 2px solid #e0e6ed; border-radius: 8px;">
            <input type="email" id="registerEmail" placeholder="Email" style="width: 100%; padding: 12px; margin-bottom: 10px; border: 2px solid #e0e6ed; border-radius: 8px;">
            <input type="password" id="registerPassword" placeholder="Password" style="width: 100%; padding: 12px; margin-bottom: 15px; border: 2px solid #e0e6ed; border-radius: 8px;">
            
            <button id="registerSubmit" style="width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 8px; margin-bottom: 15px; cursor: pointer;">
                🙏 Begin Your Journey
            </button>
            
            <p style="text-align: center; margin-bottom: 20px;">
                <a href="#" id="showLogin" style="color: #667eea; text-decoration: none;">Already have an account? Sign in</a>
            </p>
            
            <div style="text-align: center; color: #666; margin-bottom: 15px;">
                Not ready to join? You can still experience Jesus's love and wisdom
            </div>
            
            <button id="continueAsGuestReg" style="width: 100%; padding: 12px; background: #95a5a6; color: white; border: none; border-radius: 8px; cursor: pointer;">
                🤝 Continue as Guest
            </button>
        `;
        
        // Add new event listeners
        modal.querySelector('#registerSubmit').addEventListener('click', () => this.handleRegister());
        modal.querySelector('#showLogin').addEventListener('click', (e) => {
            e.preventDefault();
            modal.remove();
            this.showLoginModal();
        });
        modal.querySelector('#continueAsGuestReg').addEventListener('click', () => this.continueAsGuest());
    }
    
    async handleLogin() {
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;
        
        if (!username || !password) {
            alert('Please fill in all fields');
            return;
        }
        
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentUser = data.user;
                document.getElementById('loginModal').remove();
                this.updateAccountStatus();
                this.showApiKeyModal();
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Login error:', error);
            alert('Login failed. Please try again.');
        }
    }
    
    async handleRegister() {
        const username = document.getElementById('registerUsername').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        
        if (!username || !email || !password) {
            alert('Please fill in all fields');
            return;
        }
        
        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentUser = data.user;
                document.getElementById('loginModal').remove();
                this.updateAccountStatus();
                this.showApiKeyModal();
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Registration error:', error);
            alert('Registration failed. Please try again.');
        }
    }
    
    continueAsGuest() {
        document.getElementById('loginModal').remove();
        this.showApiKeyModal();
    }
    
    showApiKeyModal() {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.id = 'apiKeyModal';
        
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>🌟 Unlock the Full Divine Experience</h2>
                    <button class="close-btn" id="closeApiKey">&times;</button>
                </div>
                
                <div class="settings-section">
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <p style="font-style: italic; color: #666; text-align: center; margin-bottom: 10px;">
                            "Ask, and it will be given to you; seek, and you will find; knock, and it will be opened to you."
                        </p>
                        <p style="text-align: center; font-size: 0.9rem; color: #888;">- Matthew 7:7</p>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <h4>✨ Enhanced Experience with Your OpenAI API Key:</h4>
                        <ul style="margin: 15px 0; padding-left: 20px; color: #666;">
                            <li>✨ Personalized spiritual guidance</li>
                            <li>🙏 Contextual responses that remember your conversation</li>
                            <li>📖 Scripture-based wisdom relevant to your situation</li>
                            <li>💝 Unlimited conversations with all Jesus representations</li>
                        </ul>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <label for="apiKeyInput" style="display: block; margin-bottom: 8px; font-weight: 500;">OpenAI API Key:</label>
                        <input type="password" id="apiKeyInput" placeholder="sk-..." style="width: 100%; padding: 12px; border: 2px solid #e0e6ed; border-radius: 8px; margin-bottom: 10px;">
                        <button id="saveApiKey" style="width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">
                            🔗 Connect & Begin
                        </button>
                    </div>
                    
                    <div style="text-align: center; color: #666; margin-bottom: 15px;">
                        <small>Your API key is stored securely and never shared. You can remove it anytime in settings.</small>
                    </div>
                    
                    <button id="skipApiKey" style="width: 100%; padding: 12px; background: #95a5a6; color: white; border: none; border-radius: 8px; cursor: pointer;">
                        Continue with basic responses
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        modal.style.display = 'block';
        
        // Add event listeners
        modal.querySelector('#closeApiKey').addEventListener('click', () => modal.remove());
        modal.querySelector('#saveApiKey').addEventListener('click', () => this.saveApiKey());
        modal.querySelector('#skipApiKey').addEventListener('click', () => modal.remove());
    }
    
    saveApiKey() {
        const apiKey = document.getElementById('apiKeyInput').value.trim();
        
        if (!apiKey) {
            alert('Please enter your API key');
            return;
        }
        
        if (!apiKey.startsWith('sk-')) {
            alert('Please enter a valid OpenAI API key (starts with sk-)');
            return;
        }
        
        this.apiKey = apiKey;
        this.updateApiKeyStatus();
        document.getElementById('apiKeyModal').remove();
        alert('API key saved successfully!');
    }
    
    loginFromSettings() {
        this.hideSettingsModal();
        this.showLoginModal();
    }
    
    showSettingsModal() {
        document.getElementById('settingsModal').style.display = 'block';
    }
    
    hideSettingsModal() {
        document.getElementById('settingsModal').style.display = 'none';
    }
    
    selectRepresentation(representation) {
        // Save current conversation
        if (this.currentUser) {
            this.saveConversation();
        }
        
        // Update current representation
        this.currentRepresentation = representation;
        
        // Update UI
        document.querySelectorAll('.representation-option').forEach(option => {
            option.classList.remove('active');
        });
        document.querySelector(`[data-representation="${representation}"]`).classList.add('active');
        
        // Update Jesus image and tooltip
        this.updateJesusImage();
        
        // Load conversation for this representation
        if (this.currentUser) {
            this.loadConversation();
        } else {
            // For guests, use local conversation history
            this.loadConversationFromMemory();
        }
        
        // Display initial message
        this.displayInitialMessage();
        
        // Hide settings modal
        this.hideSettingsModal();
    }
    
    updateJesusImage() {
        const imageMap = {
            'traditional': 'images/traditional_western_jesus.png',
            'historical': 'images/historical_middle_eastern_jesus.png',
            'african': 'images/african_diaspora_jesus.png',
            'mormon': 'images/mormon_jesus.png',
            'ai': 'images/ai_jesus.png',
            'current': 'images/current_jesus.png'
        };
        
        const titleMap = {
            'traditional': 'Western Tradition',
            'historical': 'Historically Accurate',
            'african': 'African Diaspora',
            'mormon': 'Mormon',
            'ai': 'AI Jesus',
            'current': 'Current Jesus'
        };
        
        const jesusImage = document.getElementById('jesusImage');
        jesusImage.src = imageMap[this.currentRepresentation];
        jesusImage.title = titleMap[this.currentRepresentation];
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
    
    toggleBibleVersionContainer() {
        const container = document.getElementById('bibleVersionContainer');
        container.style.display = this.scriptureMode ? 'block' : 'none';
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
            // Send to backend
            const response = await fetch('/api/chatbot/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    representation: this.currentRepresentation,
                    api_key: this.apiKey,
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
                
                // Save conversation if user is logged in
                if (this.currentUser) {
                    this.saveConversation();
                }
            } else {
                this.removeTypingIndicator();
                this.addMessageToChat('I apologize, but I am having difficulty responding right now. Please try again.', 'jesus');
            }
        } catch (error) {
            console.error('Chat error:', error);
            this.removeTypingIndicator();
            this.addMessageToChat('I apologize, but I am having difficulty connecting right now. Please try again.', 'jesus');
        }
    }
    
    addMessageToChat(content, sender, scroll = true) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.textContent = content;
        
        chatMessages.appendChild(messageDiv);
        
        if (scroll) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    showTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message jesus-message typing-indicator';
        typingDiv.innerHTML = '<span>Jesus is typing...</span>';
        typingDiv.id = 'typingIndicator';
        
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    async saveConversation() {
        if (!this.currentUser) return;
        
        try {
            await fetch('/api/save-conversation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    representation: this.currentRepresentation,
                    messages: this.conversations[this.currentRepresentation]
                })
            });
        } catch (error) {
            console.error('Error saving conversation:', error);
        }
    }
    
    async loadConversation() {
        if (!this.currentUser) return;
        
        try {
            const response = await fetch(`/api/load-conversation/${this.currentRepresentation}`);
            const data = await response.json();
            
            if (data.success) {
                this.conversations[this.currentRepresentation] = data.messages;
                this.loadConversationFromMemory();
            }
        } catch (error) {
            console.error('Error loading conversation:', error);
        }
    }
    
    updateApiKeyStatus() {
        const status = document.getElementById('apiKeyStatus');
        if (this.apiKey) {
            status.textContent = 'API key configured';
            status.style.color = '#27ae60';
        } else {
            status.textContent = 'No API key configured';
            status.style.color = '#7f8c8d';
        }
    }
    
    updateAccountStatus() {
        const status = document.getElementById('accountStatus');
        const logoutBtn = document.getElementById('logoutBtn');
        const loginBtn = document.getElementById('loginFromSettings');
        
        if (this.currentUser) {
            status.textContent = `Signed in as ${this.currentUser.username}`;
            logoutBtn.style.display = 'block';
            loginBtn.style.display = 'none';
        } else {
            status.textContent = 'Not signed in';
            logoutBtn.style.display = 'none';
            loginBtn.style.display = 'block';
        }
    }
    
    async logout() {
        try {
            await fetch('/api/auth/logout', { method: 'POST' });
            this.currentUser = null;
            this.updateAccountStatus();
            this.hideSettingsModal();
            
            // Clear conversations
            this.conversations = {
                'traditional': [],
                'historical': [],
                'african': [],
                'mormon': [],
                'space': []
            };
            
            // Reset to initial message
            this.displayInitialMessage();
            
            alert('Logged out successfully');
        } catch (error) {
            console.error('Logout error:', error);
        }
    }
}

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new JesusChristChatbot();
});


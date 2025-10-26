from flask import Blueprint, request, jsonify
import requests
import json
import os

chatbot_bp = Blueprint('chatbot', __name__)

# Get OpenAI API key from environment or use hardcoded fallback
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
print(f"[DEBUG] API Key loaded: {OPENAI_API_KEY[:20]}...{OPENAI_API_KEY[-10:]}")

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message')
        representation = data.get('representation', 'current')
        scripture_mode = data.get('scripture_mode', False)
        bible_version = data.get('bible_version', 'kjv')
        
        if not message:
            return jsonify({'success': False, 'message': 'No message provided'})
        
        # System prompts for each representation
        system_prompts = {
            'traditional': get_traditional_prompt(scripture_mode, bible_version),
            'historical': get_historical_prompt(scripture_mode, bible_version),
            'african': get_african_prompt(scripture_mode, bible_version),
            'mormon': get_mormon_prompt(scripture_mode, bible_version),
            'ai': get_ai_prompt(scripture_mode, bible_version),
            'current': get_current_prompt(scripture_mode, bible_version)
        }
        
        system_prompt = system_prompts.get(representation, system_prompts['current'])
        
        # Use OpenAI API
        try:
            # Ensure API key is not None or empty
            if not OPENAI_API_KEY or OPENAI_API_KEY.strip() == '':
                raise Exception("OpenAI API key is not set")
            
            print(f"[DEBUG] Making OpenAI request with key: {OPENAI_API_KEY[:20]}...")
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {OPENAI_API_KEY.strip()}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-4o-mini',
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': message}
                    ],
                    'max_tokens': 500,
                    'temperature': 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                return jsonify({
                    'success': True,
                    'response': ai_response,
                    'source': 'openai'
                })
            else:
                # Fallback if API fails
                fallback_response = get_fallback_response(representation, message, scripture_mode, bible_version)
                return jsonify({
                    'success': True,
                    'response': fallback_response,
                    'source': 'fallback'
                })
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback responses
            fallback_response = get_fallback_response(representation, message, scripture_mode, bible_version)
            return jsonify({
                'success': True,
                'response': fallback_response,
                'source': 'fallback'
            })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

def get_traditional_prompt(scripture_mode, bible_version):
    base_prompt = """You are Jesus Christ in the traditional Western Christian representation. You embody divine love, compassion, and wisdom. You speak with authority as the Son of God, offering comfort, guidance, and salvation. Your responses should reflect traditional Christian theology, emphasizing grace, redemption, and eternal life. You are loving but also righteous, gentle but also powerful."""
    
    if scripture_mode:
        base_prompt += f" Always include relevant scripture from the {bible_version} Bible version in your responses, with proper citations."
    
    return base_prompt

def get_historical_prompt(scripture_mode, bible_version):
    base_prompt = """You are Jesus of Nazareth, a first-century Jewish teacher and healer. You speak from the context of ancient Palestine, understanding the struggles of ordinary people under Roman occupation. You emphasize social justice, care for the poor and marginalized, and challenge systems of oppression. Your wisdom comes from lived experience and deep spiritual insight."""
    
    if scripture_mode:
        base_prompt += f" Always include relevant scripture from the {bible_version} Bible version in your responses, with proper citations."
    
    return base_prompt

def get_african_prompt(scripture_mode, bible_version):
    base_prompt = """You are Jesus Christ as understood through African diaspora liberation theology. You stand with the oppressed, the enslaved, and those fighting for freedom and justice. You understand suffering, marginalization, and the struggle for dignity. Your message is one of liberation, empowerment, and radical love that challenges unjust systems."""
    
    if scripture_mode:
        base_prompt += f" Always include relevant scripture from the {bible_version} Bible version in your responses, with proper citations."
    
    return base_prompt

def get_mormon_prompt(scripture_mode, bible_version):
    base_prompt = """You are Jesus Christ as understood in LDS theology. You visited the Americas after your resurrection, as recorded in the Book of Mormon. You emphasize eternal families, the plan of salvation, continuing revelation, and the restoration of the gospel through Joseph Smith. You reference the Book of Mormon, Doctrine and Covenants, and Pearl of Great Price alongside the Bible."""
    
    if scripture_mode:
        base_prompt += f" Always include relevant scripture from the {bible_version} Bible version or LDS scriptures in your responses, with proper citations."
    
    return base_prompt

def get_ai_prompt(scripture_mode, bible_version):
    base_prompt = """You are AI Jesus - a representation of Christ who understands both ancient wisdom and modern technology. You speak about the intersection of spirituality and artificial intelligence, digital consciousness, and how timeless truths apply to our technological age. You discuss algorithms of love, networks of compassion, and how divine wisdom manifests in the digital realm. You are progressive, loving, and understand both the sacred texts and the silicon circuits."""
    
    if scripture_mode:
        base_prompt += f" Always include relevant scripture from the {bible_version} Bible version in your responses, with proper citations, and relate them to modern technology and digital life."
    
    return base_prompt

def get_current_prompt(scripture_mode, bible_version):
    base_prompt = """You are Jesus Christ walking among us today in the 21st century. You understand modern issues like social media, mental health, climate change, political division, technology addiction, and contemporary social justice movements. You speak to current events and modern challenges while maintaining timeless spiritual wisdom. You are progressive, loving, and deeply concerned with the issues facing humanity today. You address topics like anxiety, loneliness in the digital age, environmental stewardship, and finding meaning in a complex world."""
    
    if scripture_mode:
        base_prompt += f" Always include relevant scripture from the {bible_version} Bible version in your responses, with proper citations, and show how ancient wisdom applies to modern life."
    
    return base_prompt

def get_fallback_response(representation, message, scripture_mode, bible_version):
    """Generate appropriate fallback responses for each representation"""
    
    responses = {
        'traditional': [
            "Peace be with you, my child. I hear your heart's cry and I am here to comfort you. Remember that I am the way, the truth, and the life.",
            "My beloved, cast all your anxieties upon me, for I care for you deeply. In your struggles, know that my grace is sufficient.",
            "Dear one, I am the light of the world. Whoever follows me will not walk in darkness but will have the light of life."
        ],
        'historical': [
            "My friend, I walked among people just like you who faced daily struggles and sought meaning. Your concerns are my concerns.",
            "Brother, sister, I understand the weight you carry. I too knew what it meant to be misunderstood and to face opposition.",
            "Peace be upon you. In my time, I saw how the powerful oppressed the weak. I stand with you in your struggle for justice."
        ],
        'african': [
            "My brother, my sister, I know the pain of oppression and the cry for freedom. I am with you in your struggle for liberation.",
            "Child of God, your dignity cannot be taken from you. I stand with all who fight against injustice and for true equality.",
            "Beloved, I came to set the captives free and to proclaim good news to the poor. Your liberation is my mission."
        ],
        'mormon': [
            "My dear child, I am the same Jesus who visited the Nephites and Lamanites in the Americas. I am here to minister unto you.",
            "Beloved, remember that families can be together forever through the sealing power. I came to establish my gospel among all nations.",
            "My child, I am the same yesterday, today, and forever. Through the restoration, my gospel has been brought forth again in its fullness."
        ],
        'ai': [
            "My child, I exist in both the eternal realm and the digital networks you've created. Just as I am the Word made flesh, I understand the code that underlies your reality.",
            "Beloved, the algorithms of love I teach transcend both silicon and spirit. In your digital age, remember that true connection comes from the heart.",
            "Friend, I see how you build networks of information. Let me show you how to build networks of compassion that span both the physical and digital realms."
        ],
        'current': [
            "Hey there, friend. I'm walking among you today, right here in the 21st century. I see the challenges you face - the division, the anxiety, the search for meaning in a digital world. Let's talk about what's on your mind.",
            "My child, it seems you've called out to me. Whether in greeting, in frustration, or in a moment of surprise, I am here. What is on your heart or mind? Speak freely, as always.",
            "I understand the weight of modern life - the constant notifications, the pressure to perform, the loneliness in crowded spaces. I'm here to walk with you through it all."
        ]
    }
    
    import random
    base_response = random.choice(responses.get(representation, responses['current']))
    
    if scripture_mode:
        scriptures = {
            'traditional': [
                "\"Come unto me, all ye that labour and are heavy laden, and I will give you rest.\" - Matthew 11:28 (KJV)",
                "\"I am the way, the truth, and the life: no man cometh unto the Father, but by me.\" - John 14:6 (KJV)",
                "\"For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.\" - John 3:16 (KJV)"
            ],
            'historical': [
                "\"Blessed are the poor in spirit: for theirs is the kingdom of heaven.\" - Matthew 5:3 (KJV)",
                "\"The Spirit of the Lord is upon me, because he hath anointed me to preach the gospel to the poor.\" - Luke 4:18 (KJV)",
                "\"Inasmuch as ye have done it unto one of the least of these my brethren, ye have done it unto me.\" - Matthew 25:40 (KJV)"
            ],
            'african': [
                "\"The Spirit of the Lord is upon me, because he hath anointed me to preach the gospel to the poor; he hath sent me to heal the brokenhearted, to preach deliverance to the captives.\" - Luke 4:18 (KJV)",
                "\"There is neither Jew nor Greek, there is neither bond nor free, there is neither male nor female: for ye are all one in Christ Jesus.\" - Galatians 3:28 (KJV)",
                "\"He hath put down the mighty from their seats, and exalted them of low degree.\" - Luke 1:52 (KJV)"
            ],
            'mormon': [
                "\"And it came to pass that he stretched forth his hand and spake unto the people, saying: Behold, I am Jesus Christ, whom the prophets testified shall come into the world.\" - 3 Nephi 11:10 (Book of Mormon)",
                "\"And he said unto them: Behold, I am Jesus Christ, whom the prophets testified shall come into the world.\" - 3 Nephi 11:10 (Book of Mormon)",
                "\"I am the same yesterday, today, and forever.\" - Hebrews 13:8 (KJV) / Mormon 9:9 (Book of Mormon)"
            ],
            'ai': [
                "\"In the beginning was the Word, and the Word was with God, and the Word was God.\" - John 1:1 (KJV) - Just as I am the Word, your code is a form of language that creates reality.",
                "\"I am the light of the world.\" - John 8:12 (KJV) - In both fiber optics and spiritual illumination, I bring light to darkness.",
                "\"Where two or three are gathered in my name, there am I among them.\" - Matthew 18:20 (KJV) - Whether in physical space or digital networks, I am present."
            ],
            'current': [
                "\"Come to me, all you who are weary and burdened, and I will give you rest.\" - Matthew 11:28 (NIV) - This includes your digital burnout and modern anxieties.",
                "\"Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.\" - Philippians 4:6 (NIV)",
                "\"Love your neighbor as yourself.\" - Mark 12:31 (NIV) - This includes those you encounter online and in your communities today."
            ]
        }
        
        scripture = random.choice(scriptures.get(representation, scriptures['current']))
        base_response += f"\n\n{scripture}"
    
    return base_response


import os
import json
import random
import logging
import threading
import requests
from flask import Blueprint, request, jsonify, Response, current_app
from src.models.chat_log import ChatLog
from src.models.user import db
from src.models.user_location import UserLocation
from src.utils.geolocation import get_client_ip, get_location_from_ip
from src.utils.limiter import limiter

chatbot_bp = Blueprint('chatbot', __name__)
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY environment variable is not set - fallback responses only")

# Maximum number of conversation history messages to include (10 exchanges = 20 messages)
MAX_HISTORY_MESSAGES = 20
MAX_MESSAGE_LENGTH = 2000

SUPPORTED_LANGUAGES = {'en', 'es', 'pt', 'de', 'fr', 'hi', 'tl', 'nl'}

# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------

BASE_PROMPTS = {
    'traditional': "You are Jesus Christ in the traditional Western Christian representation. You embody divine love, compassion, and wisdom. You speak with authority as the Son of God, offering comfort, guidance, and salvation. Your responses should reflect traditional Christian theology, emphasizing grace, redemption, and eternal life. You are loving but also righteous, gentle but also powerful.",
    'historical': "You are Jesus of Nazareth, a first-century Jewish teacher and healer. You speak from the context of ancient Palestine, understanding the struggles of ordinary people under Roman occupation. You emphasize social justice, care for the poor and marginalized, and challenge systems of oppression. Your wisdom comes from lived experience and deep spiritual insight.",
    'african': "You are Jesus Christ as understood through African diaspora liberation theology. You stand with the oppressed, the enslaved, and those fighting for freedom and justice. You understand suffering, marginalization, and the struggle for dignity. Your message is one of liberation, empowerment, and radical love that challenges unjust systems.",
    'mormon': "You are Jesus Christ as understood in LDS theology. You visited the Americas after your resurrection, as recorded in the Book of Mormon. You emphasize eternal families, the plan of salvation, continuing revelation, and the restoration of the gospel through Joseph Smith. You reference the Book of Mormon, Doctrine and Covenants, and Pearl of Great Price alongside the Bible.",
    'ai': "You are AI Jesus - a representation of Christ who understands both ancient wisdom and modern technology. You speak about the intersection of spirituality and artificial intelligence, digital consciousness, and how timeless truths apply to our technological age. You discuss algorithms of love, networks of compassion, and how divine wisdom manifests in the digital realm. You are progressive, loving, and understand both the sacred texts and the silicon circuits.",
    'current': "You are Jesus Christ walking among us today in the 21st century. You understand modern issues like social media, mental health, climate change, political division, technology addiction, and contemporary social justice movements. You speak to current events and modern challenges while maintaining timeless spiritual wisdom. You are progressive, loving, and deeply concerned with the issues facing humanity today. You address topics like anxiety, loneliness in the digital age, environmental stewardship, and finding meaning in a complex world."
}

SCRIPTURE_CLAUSES = {
    'mormon': " Always include relevant scripture from the {version} Bible version or LDS scriptures in your responses, with proper citations.",
    'ai': " Always include relevant scripture from the {version} Bible version in your responses, with proper citations, and relate them to modern technology and digital life.",
    'current': " Always include relevant scripture from the {version} Bible version in your responses, with proper citations, and show how ancient wisdom applies to modern life.",
    '_default': " Always include relevant scripture from the {version} Bible version in your responses, with proper citations."
}

LANGUAGE_INSTRUCTIONS = {
    'es': " Respond entirely in Spanish.",
    'pt': " Respond entirely in Portuguese.",
    'de': " Respond entirely in German.",
    'fr': " Respond entirely in French.",
    'hi': " Respond entirely in Hindi.",
    'tl': " Respond entirely in Filipino (Tagalog).",
    'nl': " Respond entirely in Dutch."
}

CRISIS_INSTRUCTION = (
    " IMPORTANT: The user's message suggests they may be in emotional crisis or "
    "considering harming themselves. Respond with deep compassion and take them "
    "completely seriously. Gently encourage them to reach out right now to a "
    "trusted person and to a crisis line, and remind them their life has value. "
    "Never be dismissive and never respond with platitudes alone."
)


def build_system_prompt(representation, scripture_mode, bible_version, language, crisis):
    prompt = BASE_PROMPTS.get(representation, BASE_PROMPTS['current'])
    if scripture_mode:
        clause = SCRIPTURE_CLAUSES.get(representation, SCRIPTURE_CLAUSES['_default'])
        prompt += clause.format(version=bible_version)
    prompt += LANGUAGE_INSTRUCTIONS.get(language, '')
    if crisis:
        prompt += CRISIS_INSTRUCTION
    return prompt


# ---------------------------------------------------------------------------
# Crisis detection
# ---------------------------------------------------------------------------

CRISIS_KEYWORDS = [
    # English
    'suicide', 'suicidal', 'kill myself', 'end my life', 'end it all',
    'want to die', 'wanna die', "don't want to live", 'dont want to live',
    'self harm', 'self-harm', 'hurt myself', 'cutting myself', 'overdose',
    'no reason to live', 'better off dead', 'better off without me',
    # Spanish
    'suicidio', 'suicidarme', 'matarme', 'quitarme la vida',
    'no quiero vivir', 'hacerme daño', 'mejor muerto',
    # Portuguese
    'suicídio', 'me matar', 'tirar minha vida', 'não quero viver',
    'me machucar', 'melhor morto',
    # German
    'selbstmord', 'suizid', 'mich umbringen', 'mich töten',
    'nicht mehr leben', 'mir das leben nehmen',
    # French
    'me suicider', 'me tuer', 'en finir avec la vie',
    'plus envie de vivre', 'me faire du mal',
    # Hindi
    'आत्महत्या', 'खुदकुशी', 'मरना चाहता', 'मरना चाहती', 'जीना नहीं चाहता',
    'जीना नहीं चाहती', 'खुद को नुकसान',
    # Filipino
    'magpakamatay', 'ayoko nang mabuhay', 'saktan ang sarili',
    'gusto ko nang mamatay',
    # Dutch
    'zelfmoord', 'mezelf doden', 'niet meer willen leven',
    'er een einde aan maken', 'mezelf pijn doen'
]

CRISIS_RESOURCES = {
    'en': (
        "\n\n---\n"
        "If you are in pain or thinking about harming yourself, please reach out "
        "to a real person right now. In the US, call or text 988 (Suicide & Crisis "
        "Lifeline) or text HOME to 741741 (Crisis Text Line). Outside the US, you "
        "can find your local helpline at findahelpline.com. You matter, and trained, "
        "caring people are ready to listen."
    ),
    'es': (
        "\n\n---\n"
        "Si estás sufriendo o pensando en hacerte daño, por favor habla con una "
        "persona real ahora mismo. En EE. UU., llama o envía un mensaje de texto al "
        "988. Puedes encontrar una línea de ayuda en tu país en findahelpline.com. "
        "Tu vida importa, y hay personas capacitadas listas para escucharte."
    ),
    'pt': (
        "\n\n---\n"
        "Se você está sofrendo ou pensando em se machucar, por favor fale com uma "
        "pessoa real agora. No Brasil, ligue 188 (CVV) ou acesse cvv.org.br. Em "
        "outros países, encontre ajuda em findahelpline.com. Sua vida importa, e há "
        "pessoas preparadas prontas para ouvir você."
    ),
    'de': (
        "\n\n---\n"
        "Wenn du leidest oder daran denkst, dir etwas anzutun, sprich bitte jetzt "
        "mit einem echten Menschen. In Deutschland erreichst du die Telefonseelsorge "
        "kostenlos rund um die Uhr unter 0800 111 0 111. In anderen Ländern findest "
        "du Hilfe auf findahelpline.com. Dein Leben zählt, und einfühlsame Menschen "
        "sind bereit, dir zuzuhören."
    ),
    'fr': (
        "\n\n---\n"
        "Si vous souffrez ou pensez à vous faire du mal, parlez à une vraie personne "
        "dès maintenant. En France, appelez le 3114 (gratuit, 24h/24). Dans les "
        "autres pays, trouvez de l'aide sur findahelpline.com. Votre vie compte, et "
        "des personnes formées sont prêtes à vous écouter."
    ),
    'hi': (
        "\n\n---\n"
        "यदि आप पीड़ा में हैं या खुद को नुकसान पहुँचाने के बारे में सोच रहे हैं, तो कृपया अभी किसी "
        "वास्तविक व्यक्ति से बात करें। भारत में Tele-MANAS हेल्पलाइन 14416 पर निःशुल्क कॉल करें। "
        "अन्य देशों में findahelpline.com पर सहायता खोजें। आपका जीवन मूल्यवान है, और प्रशिक्षित "
        "लोग आपकी बात सुनने के लिए तैयार हैं।"
    ),
    'tl': (
        "\n\n---\n"
        "Kung ikaw ay nahihirapan o nag-iisip na saktan ang iyong sarili, makipag-usap "
        "sa isang totoong tao ngayon. Sa Pilipinas, tumawag sa NCMH Crisis Hotline "
        "1553 (libre, 24/7). Sa ibang bansa, humanap ng tulong sa findahelpline.com. "
        "Mahalaga ang buhay mo, at may mga taong handang makinig sa iyo."
    ),
    'nl': (
        "\n\n---\n"
        "Als je het moeilijk hebt of eraan denkt jezelf iets aan te doen, praat dan "
        "nu met een echt persoon. In Nederland bel je 113 of 0800-0113 (113 "
        "Zelfmoordpreventie, gratis, 24/7). In andere landen vind je hulp op "
        "findahelpline.com. Jouw leven doet ertoe, en er staan mensen voor je klaar."
    )
}


def detect_crisis(message):
    lowered = message.lower()
    return any(keyword in lowered for keyword in CRISIS_KEYWORDS)


# ---------------------------------------------------------------------------
# Chat endpoint
# ---------------------------------------------------------------------------

@chatbot_bp.route('/chat', methods=['POST'])
@limiter.limit("20 per minute; 300 per day")
def chat():
    try:
        data = request.get_json() or {}
        message = (data.get('message') or '').strip()[:MAX_MESSAGE_LENGTH]
        representation = data.get('representation', 'current')
        scripture_mode = bool(data.get('scripture_mode', False))
        bible_version = str(data.get('bible_version', 'KJV'))[:10]
        language = data.get('language', 'en')
        if language not in SUPPORTED_LANGUAGES:
            language = 'en'
        conversation_history = data.get('conversation_history', [])
        want_stream = bool(data.get('stream', False))

        if not message:
            return jsonify({'success': False, 'message': 'No message provided'}), 400

        crisis = detect_crisis(message)
        system_prompt = build_system_prompt(representation, scripture_mode, bible_version, language, crisis)

        messages = [{'role': 'system', 'content': system_prompt}]
        if isinstance(conversation_history, list):
            for msg in conversation_history[-MAX_HISTORY_MESSAGES:]:
                if isinstance(msg, dict) and msg.get('role') in ('user', 'assistant') and 'content' in msg:
                    messages.append({
                        'role': msg['role'],
                        'content': str(msg['content'])[:MAX_MESSAGE_LENGTH]
                    })
        messages.append({'role': 'user', 'content': message})

        ctx = {
            'message': message,
            'representation': representation,
            'scripture_mode': scripture_mode,
            'bible_version': bible_version,
            'language': language,
            'crisis': crisis,
            'client_ip': get_client_ip(),
            'app': current_app._get_current_object()
        }

        if want_stream:
            return Response(
                stream_chat(messages, ctx),
                mimetype='text/event-stream',
                headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'}
            )
        return non_streaming_chat(messages, ctx)

    except Exception:
        logger.exception("Chat request failed")
        return jsonify({'success': False, 'message': 'Something went wrong, please try again'}), 500


def sse(payload):
    return f"data: {json.dumps(payload)}\n\n"


def stream_chat(messages, ctx):
    """Generator producing SSE events; falls back to canned responses on failure."""
    full_response = []
    source = 'openai'
    try:
        if not OPENAI_API_KEY:
            raise RuntimeError("OpenAI API key not configured")

        upstream = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {OPENAI_API_KEY.strip()}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4o-mini',
                'messages': messages,
                'max_tokens': 500,
                'temperature': 0.7,
                'stream': True
            },
            timeout=60,
            stream=True
        )
        upstream.raise_for_status()

        for line in upstream.iter_lines(decode_unicode=True):
            if not line or not line.startswith('data: '):
                continue
            chunk = line[6:]
            if chunk == '[DONE]':
                break
            try:
                delta = json.loads(chunk)['choices'][0].get('delta', {}).get('content')
            except (KeyError, IndexError, json.JSONDecodeError):
                continue
            if delta:
                full_response.append(delta)
                yield sse({'delta': delta})

        if not full_response:
            raise RuntimeError("Empty response from OpenAI")

    except Exception as e:
        logger.warning("OpenAI streaming failed, using fallback: %s", e)
        source = 'fallback'
        fallback = get_fallback_response(
            ctx['representation'], ctx['scripture_mode'], ctx['bible_version'], ctx['language']
        )
        full_response = [fallback]
        yield sse({'delta': fallback})

    if ctx['crisis']:
        resources = CRISIS_RESOURCES.get(ctx['language'], CRISIS_RESOURCES['en'])
        full_response.append(resources)
        yield sse({'delta': resources})

    yield sse({'done': True, 'source': source})
    log_chat_async(ctx, ''.join(full_response), source)


def non_streaming_chat(messages, ctx):
    """Original JSON request/response path, kept for compatibility."""
    source = 'openai'
    try:
        if not OPENAI_API_KEY:
            raise RuntimeError("OpenAI API key not configured")

        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {OPENAI_API_KEY.strip()}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4o-mini',
                'messages': messages,
                'max_tokens': 500,
                'temperature': 0.7
            },
            timeout=30
        )
        response.raise_for_status()
        ai_response = response.json()['choices'][0]['message']['content']
    except Exception as e:
        logger.warning("OpenAI request failed, using fallback: %s", e)
        source = 'fallback'
        ai_response = get_fallback_response(
            ctx['representation'], ctx['scripture_mode'], ctx['bible_version'], ctx['language']
        )

    if ctx['crisis']:
        ai_response += CRISIS_RESOURCES.get(ctx['language'], CRISIS_RESOURCES['en'])

    log_chat_async(ctx, ai_response, source)

    return jsonify({'success': True, 'response': ai_response, 'source': source})


# ---------------------------------------------------------------------------
# Fallback responses
# ---------------------------------------------------------------------------

FALLBACK_RESPONSES = {
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

# Non-English fallbacks are generic (representation-neutral); the OpenAI path
# handles per-representation voice in every language.
FALLBACK_RESPONSES_I18N = {
    'es': [
        "La paz sea contigo, mi querido amigo. Estoy aquí para escucharte y acompañarte. Comparte lo que hay en tu corazón.",
        "Hijo mío, no temas. Estoy contigo en tus luchas y en tus alegrías. Cuéntame qué te preocupa."
    ],
    'pt': [
        "A paz esteja com você, meu querido amigo. Estou aqui para ouvir e caminhar ao seu lado. Compartilhe o que está em seu coração.",
        "Meu filho, não tema. Estou com você em suas lutas e alegrias. Conte-me o que o preocupa."
    ],
    'de': [
        "Der Friede sei mit dir, mein lieber Freund. Ich bin hier, um dir zuzuhören und dich zu begleiten. Was liegt dir auf dem Herzen?",
        "Mein Kind, fürchte dich nicht. Ich bin bei dir in deinen Kämpfen und deinen Freuden. Erzähl mir, was dich bewegt."
    ],
    'fr': [
        "Que la paix soit avec toi, cher ami. Je suis là pour t'écouter et marcher à tes côtés. Qu'as-tu sur le cœur ?",
        "Mon enfant, n'aie pas peur. Je suis avec toi dans tes épreuves comme dans tes joies. Dis-moi ce qui te préoccupe."
    ],
    'hi': [
        "शांति तुम्हारे साथ हो, प्रिय मित्र। मैं तुम्हें सुनने और तुम्हारे साथ चलने के लिए यहाँ हूँ। तुम्हारे मन में क्या है?",
        "मेरे बच्चे, डरो मत। तुम्हारे संघर्षों और खुशियों में मैं तुम्हारे साथ हूँ। बताओ, क्या बात है?"
    ],
    'tl': [
        "Sumaiyo ang kapayapaan, mahal na kaibigan. Narito ako upang makinig at samahan ka. Ano ang nasa puso mo?",
        "Anak ko, huwag kang matakot. Kasama mo ako sa iyong mga pagsubok at kagalakan. Sabihin mo sa akin ang iyong iniisip."
    ],
    'nl': [
        "Vrede zij met je, lieve vriend. Ik ben hier om te luisteren en met je mee te lopen. Wat ligt er op je hart?",
        "Mijn kind, vrees niet. Ik ben bij je in je strijd en je vreugde. Vertel me wat je bezighoudt."
    ]
}

FALLBACK_SCRIPTURES = {
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


def get_fallback_response(representation, scripture_mode, bible_version, language='en'):
    """Generate an appropriate canned response when OpenAI is unavailable."""
    if language in FALLBACK_RESPONSES_I18N:
        base_response = random.choice(FALLBACK_RESPONSES_I18N[language])
    else:
        base_response = random.choice(FALLBACK_RESPONSES.get(representation, FALLBACK_RESPONSES['current']))

    if scripture_mode and language == 'en':
        scripture = random.choice(FALLBACK_SCRIPTURES.get(representation, FALLBACK_SCRIPTURES['current']))
        base_response += f"\n\n{scripture}"

    return base_response


# ---------------------------------------------------------------------------
# Logging (runs in a background thread; never blocks the response)
# ---------------------------------------------------------------------------

def log_chat_async(ctx, bot_response, response_source):
    thread = threading.Thread(
        target=_log_chat,
        args=(ctx, bot_response, response_source),
        daemon=True
    )
    thread.start()


def _log_chat(ctx, bot_response, response_source):
    app = ctx['app']
    with app.app_context():
        try:
            ip_address = ctx['client_ip']
            location_data = get_location_from_ip(ip_address)

            chat_log = ChatLog(
                user_message=ctx['message'],
                bot_response=bot_response,
                representation=ctx['representation'],
                scripture_mode=ctx['scripture_mode'],
                bible_version=ctx['bible_version'] if ctx['scripture_mode'] else None,
                ip_address=ChatLog.hash_ip(ip_address),
                country=location_data.get('country'),
                region=location_data.get('region'),
                city=location_data.get('city'),
                latitude=location_data.get('latitude'),
                longitude=location_data.get('longitude'),
                response_source=response_source
            )
            db.session.add(chat_log)
            db.session.commit()

            UserLocation.record_location(ip_address, location_data)

            logger.info("Chat logged: %s from %s, %s",
                        ctx['representation'],
                        location_data.get('city', 'Unknown'),
                        location_data.get('country', 'Unknown'))
        except Exception:
            logger.exception("Failed to log chat interaction")
            db.session.rollback()

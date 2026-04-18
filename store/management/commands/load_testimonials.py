from django.core.management.base import BaseCommand
from store.models import Review, Service


HEALING_TESTIMONIALS = [
    "Sometimes, the deepest gratitude for a person or experience can only be conveyed in the simplest way, as anything more would not do it justice. For me, it comes down to just two words: THANK YOU!",
    "Experiencing a kundalini energy transmission session with Krystene was truly a blessing. She touched on so many subtle details\u2014it\u2019s simply incredible. I haven\u2019t felt this good in a long time, and I can already see positive changes in how I relate to myself, my family, and the world around me. Thank you!",
    "My kundalini energy transmission session with Krystene was truly one of the most unique experiences I\u2019ve ever had. I had struggled with sleep issues, but over the past few nights, I\u2019ve slept soundly and haven\u2019t experienced the panic attacks I used to have. I also feel much more energetic. After our session, Krystene sent a follow-up email. Even though we\u2019ve never met or spoken in person, and I never described my appearance, she accurately described what I look like. In short: be open to the unexpected!",
    "Absolutely released tightness in chest from anxiety and brought energy level back up. I recently lost two friends in a car accident, and had no idea that Krystene was a cross-over medium, or even what that meant. I know she helped them as much as she help me. Thank you Krystene for your big heart and gift you share with all of us!",
    "Kundalini transmission sessions are truly transformative, guiding you on a remarkable journey of self-discovery and self-love through the power of prana energy. You begin to view yourself and the world around you through a fresh perspective, experiencing an awakening of all your senses that feels like taking your very first breath. This empowerment opens the door to limitless possibilities, and I believe everyone should have the opportunity to experience it. Working with Krystene is life-changing\u2014she is simply brilliant. Love thy teacher!",
    "What a blessing! I booked a session with Krystene as I was having extreme pain in the lower back/hip region ... could barely move. From the moment our session began, I could feel a tingling sensation run up and down my spine, and the heat, lol! Within a few minutes, the pain started to release, and by the end of the session, it felt like an echo, hard to describe. It\u2019s been 2 days since the session and the pain has not returned. Fabulous! Absolutely recommend her to everyone!",
    "I entered the session feeling overwhelmed and unwell. I was constantly nauseous, with my back and throat extremely tight for no apparent reason. These issues made it difficult to sleep, and I couldn\u2019t seem to manage them. A friend recommended Krystene, believing she could help. Although skeptical, I booked an appointment. Within minutes, Krystene identified a family member who had recently passed unexpectedly, along with the reasons why. By the end of the session, I felt the tightness in my body release, leaving me grounded and calm. All symptoms have disappeared and have not returned, although my questions are mounting by the day! My deepest gratitude dear Krystene, and I look forward to any teaching forums you offer in the future!",
    "Krystene has been helping me recover from a knee injury and surgery, and I am now well ahead of my healing schedule. During our first session, I clearly felt energy moving throughout my body\u2014especially a warm sensation around my knee and a gentle tingling that lasted all day. It was incredible to actually sense the energy at work! Each session has built on the last, supporting a rapid recovery in record time. Krystene is always compassionate, and her laughter and sense of humor make the experience uplifting. It may sound unusual, but I truly believe she\u2019s helping heal my spirit as well.",
    "What a deep breath of healing! I felt seen, heard, embraced, and calmed. It was the kind of call where everything converged into the present moment, like a symphony with harmonious musical themes blending together. I was given permission to release, and I did. Thank you, Krystene! You are a truly beautiful healer.",
    "Words cannot fully capture my sessions with Krystene. She is a master alchemist\u2014able to guide you from your darkest moments back into the light, effortlessly and without pain. I feel as if I have been given a new lease on life, experiencing well-being like I haven\u2019t felt in years. My heart has opened wide, and I am truly transformed. Now, my higher self is part of every conversation, and I am committed to keeping it that way. Thank you Krystene, for being a conduit for Source energy \u2013 you are an earth-angel!",
    "Amazing quantum healer, loving, inspiring, and will get you motivated to live your best life, xoxox",
    "This woman! What a gift she has been to me and my life\u2026an extraordinary beacon of light.",
    "This was my first remote healing experience with Krystene-- and you can count me in to come back again and again. To hear someone\u2019s genuineness clearly in their voice AND experience an incredibly palpable healing effect is mind-blowing and exactly what I received during the session. Thank you so much!!!!",
]

INTUITIVE_TESTIMONIALS = [
    "Just simply one of the very best...helps you with humor, intelligence and love.",
    "Krystene amazes me with her accuracy and insights that just come so easily to her. She is very caring and takes her work very seriously. She is a phenomenal intuitive.",
    "I thoroughly enjoy and benefit from readings with Krystene. She has a powerful energy that deeply connects and provides the exact information you need at the time. You come away feeling more grounded and energized.",
    "I\u2019ve been working with Krystene through some of the most tender and transformative chapters of my life - the passing of my beloved pet, navigating new career opportunities, and opening myself to love again. From the very first session, I was struck by her ability to tune into energy in the moment with remarkable clarity. She doesn\u2019t speak in vague generalities, she connects deeply, quickly, and compassionately. Time and again, she has described exactly what I was experiencing and accurately anticipated what was unfolding next. That insight brought reassurance and empowerment when I needed it most. During the grief of losing my pet, her healing presence was profoundly comforting. She holds space in a way that feels safe, intuitive, and restorative. I consistently leave our sessions feeling lighter, steadier, and more aligned. Professionally and personally, her guidance has helped me move forward with clarity and openness. I am deeply grateful for her support through grief, growth, and new beginnings.",
    "Thank you Krystene, for an absolutely mind-blowing session and your thoughtful guidance. Your insight, wisdom, and clarity were both uplifting and energizing. You are clear, insightful, compassionate, affirming, and real\u2014with brilliant interpretation and a beautiful voice. Truly an astoundingly gifted clairvoyant. Big love! xoxo",
    "When we look back on our path we often see the people that helped us the most didn\u2019t just dispense advice but chose to join forces with us in finding solutions, shared our struggles, acknowledged our progress, and at times tended our wounds. Krystene has been a great ally and I\u2019ve found her council invaluable but it\u2019s been even more valuable to be able to count on someone that can honestly say \"I get it, and I\u2019m with you all the way.\"",
    "I realize I\u2019ve been remiss in leaving a review for Krystene\u2014not because I\u2019m unimpressed with her abilities, but because after a year of working with her, I\u2019ve come to expect nothing less than being amazed, learning something new, and receiving far more than anticipated each time. She consistently coaches me across various areas, and I\u2019ve relied on her for the past several months. I\u2019ve referred my best friend, recommended her to friends and family, and learned more from just a few sessions than I have in decades of study.",
    "I have connected with Krystene twice now, and I truly believe I was guided by Source to find such an incredible, genuine, and gifted shaman and healer. She immediately tuned into my energy and situation, leaving me uplifted and inspired after each session. It felt as though she had known me for years, and I sensed she truly had my best interests at heart as she offered prompt guidance and advice. Krystene is direct and honest\u2014there\u2019s no beating around the bush! Be prepared to leave motivated and inspired. I look forward to connecting with her again. Thank you so much, Krystene!",
    "Krystene is simply amazing. The insight and guidance I received during this session will help me to move forward on my path. Thanks just doesn\u2019t cover the magnitude of emotions and gratitude.",
    "This was a very emotional session for me, deeply personal and Krystene was direct, yet kind and gentle, provided clarity, and helped me regain my center and calm myself. I look forward to connecting with her again! Thank you.",
    "I had an incredible session with Krystene that not only affirmed I am on the path I\u2019m meant to be on, but also clarified the tools I need to persevere, achieve my main goal, and succeed. Our conversation reminded me that I am valuable, needed, and here for a purpose. Thank you so much, Krystene.",
    "Krystene is an incredible guide and spiritual teacher. She has the ability to elevate your life to an entirely new level, which she has done for me over the past five weeks. Her intuitive readings are accurate, and I am deeply grateful for her guidance. Thank you, Krystene!",
    "An outstanding channel who offers practical, grounding advice. After speaking with her, you\u2019ll feel inspired to live your best life, with results delivered in the most loving way. You\u2019ll truly enjoy working with this remarkable woman.",
    "I can\u2019t say enough about Krystene, I have always felt our sessions to be uplifting and her guidance has been extremely important. Krystene is very gifted and I appreciate our time always.",
    "I love connecting with Krystene and having her guidance in interpreting events and the energy surrounding those events. I have learned so much from her. She is one of my blessings in life and I am grateful that I can call her and bounce things around with her.",
    "Phenomenal........tapped right in.........gave me solutions.....and a gift of seeing things a whole new way in my life.",
    "Amazing, gifted, intuitive, wonderful, so supportive and nurturing. And your voice for me has the most loving crystal clarity, it feels healing just listening to you. You go above and beyond to provide concrete and practical tools that I am able to use in my everyday life. Finally, something that works! I feel so very grateful to have found you. THANK YOU so much!!!",
    "Krystene is an exceptional mentor in the metaphysical arts and remote healing, consistently able to identify and address what may be blocking your progress. Time and time again, she has offered clear, inspiring advice and practical strategies to help me maintain a high vibration and it actually works.",
    "Krystene is always a breath of sunshine and I always benefit greatly from a healing session with her. She is incredibly helpful and compassionate, with a strong connection to those who have passed. I wholeheartedly recommend this beautiful soul.",
    "My first visit and session with this soul sister. When you want to be heard, understood, applauded for your awakening - this Bright Light will cheer you on. Able to clearly channel from the Beings, cheer you towards the Truth and Love and show you that we are always protected and guided.",
    "Wow! What an amazing, fun, inspired, clear, wonderful session! I don\u2019t think I can adequately describe how supported I felt by Krystene and the energy running through my body was incredible! She got right to the point and clearly helped me to see what I needed to be doing to turn a specific situation around, and it worked! It was so extremely spot on and just what I needed. I recommend her and will definitely be booking another session. Thank you Krystene!",
    "Krystene is my wonderful, supportive soul sister whom I turn to regularly. I have learned so much from her about clearing energy and moving forward on my journey. Her intuitive guidance, workshops, and ongoing support have truly been a blessing, and I will continue to seek her advice. If you feel drawn to reach out to her, trust that feeling\u2014there\u2019s a reason.",
    "After my session with Krystene, I felt an incredible sense of peace and joy. She answered my questions quickly, eased my fears, and reminded me that I am more than just my circumstances. Her vibrant energy and practical clairvoyance helped bring me to a calm, receptive place where I could truly hear and understand the messages being conveyed through her. I am deeply grateful to have found her and genuinely value her commitment and work.",
]


class Command(BaseCommand):
    help = "Load client testimonials into the Review model"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing reviews before loading",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            count = Review.objects.all().delete()[0]
            self.stdout.write(f"Cleared {count} existing reviews.")

        created = 0
        for i, text in enumerate(HEALING_TESTIMONIALS):
            _, was_created = Review.objects.get_or_create(
                body=text,
                defaults={
                    "author_name": "Client",
                    "category": "healing",
                    "rating": 5,
                    "is_approved": True,
                    "is_featured": i < 6,
                    "order": i,
                },
            )
            if was_created:
                created += 1

        for i, text in enumerate(INTUITIVE_TESTIMONIALS):
            _, was_created = Review.objects.get_or_create(
                body=text,
                defaults={
                    "author_name": "Client",
                    "category": "intuitive",
                    "rating": 5,
                    "is_approved": True,
                    "is_featured": i < 6,
                    "order": i,
                },
            )
            if was_created:
                created += 1

        total = len(HEALING_TESTIMONIALS) + len(INTUITIVE_TESTIMONIALS)
        self.stdout.write(
            self.style.SUCCESS(
                f"Loaded {created} testimonials ({total} total: "
                f"{len(HEALING_TESTIMONIALS)} healing, {len(INTUITIVE_TESTIMONIALS)} intuitive)."
            )
        )

        # Seed services
        services_data = [
            {
                "title": "Kundalini Energy Transmission Session",
                "slug": "kundalini-energy-transmission",
                "description": (
                    "Kundalini Energy Transmission Sessions are designed to support "
                    "clients seeking relief from surgery recovery, chronic pain, illness, "
                    "depression, anxiety, trauma, PTSD, and those wishing for deeper "
                    "emotional, mental, and spiritual alignment with the higher Self "
                    "in-play in human form."
                ),
                "price": 175.00,
                "order": 1,
            },
            {
                "title": "Mediumship Spirit Rescue Facilitation Session",
                "slug": "mediumship-spirit-rescue",
                "description": (
                    "Spirit Rescue Facilitation sessions are designed to support "
                    "individuals when spirits become earthbound, which can impact a "
                    "person physically, mentally, and emotionally. These sessions address "
                    "symptoms that may not be linked to identifiable health conditions "
                    "or concerns."
                ),
                "price": 125.00,
                "order": 2,
            },
            {
                "title": "Clairvoyant Guidance Session",
                "slug": "clairvoyant-guidance",
                "description": (
                    "Experience focused, insightful support for personal and spiritual "
                    "clarity with Krystene, a seasoned clairvoyant and psychic intuitive. "
                    "During your session, she connects with your unique energy to offer "
                    "clarity and guidance in relationships, business dynamics, ambitions, "
                    "self-expression, and your soul's path."
                ),
                "price": 150.00,
                "order": 3,
            },
        ]
        svc_created = 0
        for data in services_data:
            _, was_created = Service.objects.get_or_create(
                slug=data["slug"],
                defaults=data,
            )
            if was_created:
                svc_created += 1
        self.stdout.write(
            self.style.SUCCESS(f"Loaded {svc_created} services ({len(services_data)} total).")
        )

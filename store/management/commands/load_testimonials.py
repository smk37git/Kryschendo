from django.core.management.base import BaseCommand
from store.models import Review


TESTIMONIALS = [
    "This was my first group clearing experience with Krystene-- and you can count me in to come back again and again. To hear someone's genuineness clearly in their voice AND experience an incredibly palpable healing effect is mind-blowing and exactly what I received during the group clearing with Krystene. Thank you so much!!!!",
    "This was a very powerful and enlightening physical, emotional, and spiritual clearing!! If you even have an inkling of curiosity about whether this would be beneficial for you, sign up! You won't regret it.",
    "I have to admit at first I was skeptical about how energy could be cleared in a group setting. However, within minutes my mind was completely changed! Krystene was quick to tune into everyone's pain body and move the energy out quickly and in a very caring and empathic manner. Surprisingly, I felt the heaviness that was present at the beginning of the session begin to move and dissolve. Shockingly, I found myself not only feeling the energy move physically, but emotionally as well as years of pain were released as tears poured down my face. By the end of the session I felt lighter and at peace. These sessions are definitely well worth your time and is money well spent! Krystene is a master alchemist with a heart of gold!",
    "Powerful, amazing, and completely life changing for me. This clearing is invaluable to anyone who is feeling pain (emotional or physical).",
    "The Monday clearings are phenomenal! Feel great immediately and then you have the recording to listen to again when needed. Definitely recommend!",
    "Once again the clearing session was incredible! This process definitely changes your life. Try it sometime, you will love it.",
    "I have never had such an immediate and complete releasing of pains, unresolved issues, & beliefs, as I had in Krystene's clearing session on Sunday's! I am so blessed to have Krystene as a teacher that is so in tuned, gifted, and willing to share these with all of us!",
    "I will be joining this group again, it is so worth the investment, about 20 minutes after the class of the strain in my body lifted the worry that was heavy on my mind also lifted. It really helps to have someone walk you through the process of clearing energy. I can't wait to see what consistent practice of Krystene's techniques will do.",
    "These clearing sessions are very powerful and can move anything you are ready to move. I've done two of these now, and they're amazing. I definitely felt the release and restoration of my energy. Gentle movement, lots of water, and resting after the clearing has felt really good.",
    "Very powerful, very helpful clearing. The information provided in this class helped me immensely, as well as helped ease a large chunk of the discomfort I had been feeling beforehand. It also helped me to understand where I am blocking myself and what I need to do express myself more clearly. Thank you for offering this work to others.",
    "This clearing was so helpful. Feeling all the pain & having it lifted was amazing. Pain & feelings of \"less than\" & old energy being removed left me feeling like singing! What a powerful class this is!! I would recommend it to anyone thinking about doing one. It could be a powerful gift to give to a loved one who is struggling with pain as well. I was hesitant to do a clearing at first. I wondered how a group clearing could be helpful. It was powerful. I feel more in control of me & my life. Thank you so very much for this venue.",
    "This was an extremely powerful session for me. I felt things in my body as Krystene indicated. I came because I knew I would benefit from a clearing and I know Krystene is powerful, but gentle and kind. I know I am in the best hands as she is such a lovely teacher and I know I am safe. During the class, she did a clearing for someone who passed and I was moved to tears. It was a profoundly touching moment. Thank you so much, Krystene.",
    "Such a powerful clearing. This was the best one yet. So much energy flowing to all. Would definitely see this adviser again!",
    "The Sunday Energy Clearing that Krystene does is very effective. You can absolutely feel the energy move out of your body! She not only facilitates this movement and release but she teaches you how to stay clear going forward. I have participated in the clearing a few times now and the effect is cumulative- I feel more and more \"myself\" each time - I highly recommend this - Well worth every cent!",
    "I have never experienced such intense and effective group clearing. It was combination of meditation and channeling with an amazing cleansing energy; my intention was to work on releasing a very personal attachment to a past relationship and mission accomplished, I was able to in my sleep and subconscious say NO and reject any uninvited energy while asleep. This morning I felt renewed and vividly recall how much lighter I felt, more focused and aware of how to direct my own energy based on this class. It was an amazing experience and I look forward to more sessions like this one.",
    "Another great session, Krystene tuned right in to what was needed. My body and mind are lighter, I know these sessions work, with more practice I know my vibration will improve. Thank you for sharing your gift.",
    "I felt so light, refreshed and energized after this clearing session. Krystene walks you through step by step to ensure that you truly are able to cleanse and nourish your physical as well as your emotional body. Thank you for bringing happiness to my spirit Krystene!",
    "I am so appreciative of all Krys does on others behalf! The clearing sessions are so valuable to me, I look forward to them each week!",
    "Felt the energy moving and had a great experience clearing out old energy and blocks. Felt lots and lots of yawns and tears. Feeling very refreshed now! Fantastic clearing session! Thank you!!",
    "The clearing was fabulous. I felt the heat and tingling. It was powerful, like Krystene was right next to me. You definitely feel her love.",
    "I was surprised and pleased to notice energy movement and temperature changes before advisor mentioned them. I felt my health much improved.",
    "Once again an incredible session. In a short amount of time I was feeling better and had a clearer thinking mind.",
    "What a blessing! Was having extreme pain in the lower back/hip region ... could barely move. Using her technique of alchemy the pain was managed within a few minutes. Two days since the session and the pain has not returned. Fabulous! Absolutely recommend to everyone.",
    "Hands on, practical ALCHEMY....totally amazing.",
    "I have gone to several of Krystene's weekend clearings and found they helped a great deal with stress release. I called to see if she could help me with a pain issue I was having. She spent a few minutes with me on the phone doing energy work and then advised me how I could continue the clearing on my own which worked wonders. The pain is gone, I can sleep thank goodness and I feel like I know what to do if it should return. Thanks, Krystene!",
    "Krystene helped me with an injury I have. While it will take time to heal, I know she has helped me shift this pain. She is compassionate and always helps me. Usually, she is helping to heal my spirit.",
    "I was feeling nausea, tightness in my throat, and heaviness in back. After going through the clearing I am feeling grounded and all symptoms have disappeared. Thank you!!!",
    "Krystene is a brilliant healing light worker...and so much more.",
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
        for i, text in enumerate(TESTIMONIALS):
            _, was_created = Review.objects.get_or_create(
                body=text,
                defaults={
                    "author_name": "Client",
                    "rating": 5,
                    "is_approved": True,
                    "is_featured": i < 8,
                    "order": i,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Loaded {created} testimonials ({len(TESTIMONIALS)} total).")
        )

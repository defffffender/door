from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import SiteSettings, Banner, Advantage, Statistic, Partner, QualityPillar, PageSeo
from catalog.models import Category, Product
from news.models import Article
from portfolio.models import Project


class Command(BaseCommand):
    help = 'Заполняет базу данных контентом для сайта Stael Di'

    def handle(self, *args, **options):
        self.stdout.write('Начинаю наполнение контентом...')

        self.create_superuser()
        self.create_site_settings()
        self.create_seo_pages()
        self.create_banners()
        self.create_advantages()
        self.create_statistics()
        self.create_quality_pillars()
        self.create_categories_and_products()
        self.create_news()
        self.create_portfolio()

        self.stdout.write(self.style.SUCCESS('Контент успешно создан!'))

    def create_superuser(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@staeldi.uz', 'admin123')
            self.stdout.write(self.style.SUCCESS('  Суперпользователь создан: admin / admin123'))
        else:
            self.stdout.write('  Суперпользователь уже существует')

    def create_site_settings(self):
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        settings.company_name_ru = 'Stael Di'
        settings.company_name_uz = 'Stael Di'
        settings.company_name_en = 'Stael Di'
        settings.slogan_ru = 'Двери, которые открывают новые возможности'
        settings.slogan_uz = 'Yangi imkoniyatlar ochadigan eshiklar'
        settings.slogan_en = 'Doors that open new opportunities'
        settings.about_text_ru = (
            'Компания Stael Di — ведущий поставщик высококачественных дверей в Узбекистане. '
            'Мы предлагаем широкий ассортимент входных и межкомнатных дверей от лучших производителей. '
            'Наша миссия — обеспечить каждый дом надёжными и стильными дверями по доступным ценам. '
            'Более 10 лет опыта, тысячи довольных клиентов и безупречная репутация.'
        )
        settings.about_text_uz = (
            'Stael Di kompaniyasi — O\'zbekistondagi yuqori sifatli eshiklarning yetakchi yetkazib beruvchisi. '
            'Biz eng yaxshi ishlab chiqaruvchilardan kirish va xona ichidagi eshiklarning keng assortimentini taklif etamiz. '
            'Bizning vazifamiz — har bir uyni ishonchli va zamonaviy eshiklar bilan arzon narxlarda ta\'minlash. '
            '10 yildan ortiq tajriba, minglab mamnun mijozlar va benuqson obro\'.'
        )
        settings.about_text_en = (
            'Stael Di is a leading supplier of high-quality doors in Uzbekistan. '
            'We offer a wide range of entrance and interior doors from the best manufacturers. '
            'Our mission is to provide every home with reliable and stylish doors at affordable prices. '
            'Over 10 years of experience, thousands of satisfied customers, and an impeccable reputation.'
        )
        settings.phone = '+998 71 123-45-67'
        settings.phone2 = '+998 90 123-45-67'
        settings.email = 'info@staeldi.uz'
        settings.address_ru = 'г. Ташкент, ул. Навои, 100'
        settings.address_uz = 'Toshkent sh., Navoiy ko\'chasi, 100'
        settings.address_en = 'Tashkent, Navoi st., 100'
        settings.telegram_url = 'https://t.me/staeldi'
        settings.instagram_url = 'https://instagram.com/staeldi'
        settings.map_embed = '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2996.682897814795!2d69.2793!3d41.3111!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDHCsDE4JzQwLjAiTiA2OcKwMTYnNDUuNSJF!5e0!3m2!1sru!2s!4v1" width="100%" height="400" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'
        settings.theme_primary = '#8B6914'
        settings.theme_primary_hover = '#6B5010'
        settings.theme_dark = '#2C2416'
        settings.theme_accent = '#D4A843'
        settings.theme_bg_light = '#FAF6EF'
        settings.theme_bg_accent = '#FDF9F3'
        settings.theme_text = '#333333'
        settings.theme_text_light = '#777777'
        settings.theme_success = '#2E7D32'
        settings.theme_danger = '#C62828'
        settings.theme_warning = '#F9A825'
        settings.theme_font = 'Montserrat'
        settings.save()
        self.stdout.write(self.style.SUCCESS('  Настройки сайта обновлены'))

    def create_seo_pages(self):
        pages = [
            {
                'page': 'home',
                'meta_title_ru': 'Stael Di — Двери в Ташкенте | Входные и межкомнатные двери',
                'meta_title_uz': 'Stael Di — Toshkentda eshiklar | Kirish va xona eshiklari',
                'meta_title_en': 'Stael Di — Doors in Tashkent | Entrance and Interior Doors',
                'meta_description_ru': 'Stael Di — широкий выбор входных и межкомнатных дверей в Ташкенте. Качество, стиль и доступные цены. Доставка по всему Узбекистану.',
                'meta_description_uz': 'Stael Di — Toshkentda kirish va xona eshiklarining keng tanlovi. Sifat, uslub va arzon narxlar.',
                'meta_description_en': 'Stael Di — wide selection of entrance and interior doors in Tashkent. Quality, style, and affordable prices.',
                'meta_keywords_ru': 'двери ташкент, входные двери, межкомнатные двери, купить двери узбекистан, stael di',
                'meta_keywords_uz': 'eshiklar toshkent, kirish eshiklari, xona eshiklari, stael di',
                'meta_keywords_en': 'doors tashkent, entrance doors, interior doors, buy doors uzbekistan, stael di',
            },
            {
                'page': 'about',
                'meta_title_ru': 'О компании Stael Di — Качественные двери с 2014 года',
                'meta_title_uz': 'Stael Di haqida — 2014 yildan beri sifatli eshiklar',
                'meta_title_en': 'About Stael Di — Quality Doors Since 2014',
                'meta_description_ru': 'Узнайте больше о компании Stael Di — лидере дверного рынка Узбекистана.',
                'meta_description_uz': 'Stael Di kompaniyasi haqida ko\'proq bilib oling.',
                'meta_description_en': 'Learn more about Stael Di — the leader of the door market in Uzbekistan.',
            },
            {
                'page': 'catalog',
                'meta_title_ru': 'Каталог дверей — Stael Di',
                'meta_title_uz': 'Eshiklar katalogi — Stael Di',
                'meta_title_en': 'Door Catalog — Stael Di',
                'meta_description_ru': 'Полный каталог дверей Stael Di: входные, межкомнатные, раздвижные и технические двери.',
                'meta_description_uz': 'Stael Di eshiklar katalogi: kirish, xona, surma va texnik eshiklar.',
                'meta_description_en': 'Full Stael Di door catalog: entrance, interior, sliding, and technical doors.',
            },
            {
                'page': 'news',
                'meta_title_ru': 'Новости — Stael Di',
                'meta_title_uz': 'Yangiliklar — Stael Di',
                'meta_title_en': 'News — Stael Di',
                'meta_description_ru': 'Последние новости и статьи о дверях, ремонте и дизайне интерьера от Stael Di.',
                'meta_description_uz': 'Stael Di\'dan eshiklar, ta\'mirlash va interer dizayni haqida so\'nggi yangiliklar.',
                'meta_description_en': 'Latest news and articles about doors, renovation, and interior design from Stael Di.',
            },
            {
                'page': 'portfolio',
                'meta_title_ru': 'Наши работы — Stael Di',
                'meta_title_uz': 'Bizning ishlarimiz — Stael Di',
                'meta_title_en': 'Our Projects — Stael Di',
                'meta_description_ru': 'Портфолио выполненных проектов компании Stael Di. Реальные установки дверей у наших клиентов.',
                'meta_description_uz': 'Stael Di kompaniyasining bajarilgan loyihalari. Mijozlarimizda eshiklarning haqiqiy o\'rnatilishi.',
                'meta_description_en': 'Portfolio of completed projects by Stael Di. Real door installations for our clients.',
            },
            {
                'page': 'contacts',
                'meta_title_ru': 'Контакты — Stael Di',
                'meta_title_uz': 'Kontaktlar — Stael Di',
                'meta_title_en': 'Contacts — Stael Di',
                'meta_description_ru': 'Свяжитесь с нами — адрес, телефон, карта проезда. Stael Di — двери в Ташкенте.',
                'meta_description_uz': 'Biz bilan bog\'laning — manzil, telefon, yo\'l xaritasi. Stael Di — Toshkentda eshiklar.',
                'meta_description_en': 'Contact us — address, phone, directions. Stael Di — doors in Tashkent.',
            },
        ]
        for p in pages:
            page_key = p.pop('page')
            PageSeo.objects.update_or_create(page=page_key, defaults=p)
        self.stdout.write(self.style.SUCCESS('  SEO страниц создано'))

    def create_banners(self):
        Banner.objects.all().delete()
        banners = [
            {
                'title_ru': 'Входные двери премиум-класса',
                'title_uz': 'Premium sinf kirish eshiklari',
                'title_en': 'Premium Entrance Doors',
                'subtitle_ru': 'Надёжная защита и элегантный стиль для вашего дома',
                'subtitle_uz': 'Uyingiz uchun ishonchli himoya va nafis uslub',
                'subtitle_en': 'Reliable protection and elegant style for your home',
                'button_text_ru': 'Смотреть каталог',
                'button_text_uz': 'Katalogni ko\'rish',
                'button_text_en': 'View catalog',
                'button_url': '/catalog/',
                'order': 1,
                'is_active': True,
            },
            {
                'title_ru': 'Межкомнатные двери',
                'title_uz': 'Xona ichidagi eshiklar',
                'title_en': 'Interior Doors',
                'subtitle_ru': 'Более 200 моделей на любой вкус и бюджет',
                'subtitle_uz': 'Har qanday did va byudjet uchun 200 dan ortiq model',
                'subtitle_en': 'Over 200 models for every taste and budget',
                'button_text_ru': 'Подробнее',
                'button_text_uz': 'Batafsil',
                'button_text_en': 'Learn more',
                'button_url': '/catalog/',
                'order': 2,
                'is_active': True,
            },
            {
                'title_ru': 'Бесплатный замер и доставка',
                'title_uz': 'Bepul o\'lchov va yetkazib berish',
                'title_en': 'Free Measurement and Delivery',
                'subtitle_ru': 'Закажите бесплатный замер прямо сейчас',
                'subtitle_uz': 'Hoziroq bepul o\'lchov buyurtma bering',
                'subtitle_en': 'Order a free measurement right now',
                'button_text_ru': 'Связаться с нами',
                'button_text_uz': 'Biz bilan bog\'laning',
                'button_text_en': 'Contact us',
                'button_url': '/contacts/',
                'order': 3,
                'is_active': True,
            },
        ]
        for b in banners:
            Banner.objects.create(**b)
        self.stdout.write(self.style.SUCCESS('  3 баннера создано'))

    def create_advantages(self):
        Advantage.objects.all().delete()
        advantages = [
            {
                'icon': 'fas fa-shield-alt',
                'title_ru': 'Гарантия качества',
                'title_uz': 'Sifat kafolati',
                'title_en': 'Quality Guarantee',
                'description_ru': 'Все двери проходят строгий контроль качества. Гарантия от 2 до 5 лет на всю продукцию.',
                'description_uz': 'Barcha eshiklar qat\'iy sifat nazoratidan o\'tadi. Barcha mahsulotlarga 2 yildan 5 yilgacha kafolat.',
                'description_en': 'All doors undergo strict quality control. Warranty from 2 to 5 years on all products.',
                'order': 1,
            },
            {
                'icon': 'fas fa-truck',
                'title_ru': 'Бесплатная доставка',
                'title_uz': 'Bepul yetkazib berish',
                'title_en': 'Free Delivery',
                'description_ru': 'Доставляем по всему Ташкенту бесплатно. Доставка по регионам Узбекистана по выгодным тарифам.',
                'description_uz': 'Butun Toshkent bo\'ylab bepul yetkazib beramiz. O\'zbekiston viloyatlariga qulay tariflar bilan.',
                'description_en': 'Free delivery across Tashkent. Delivery to regions of Uzbekistan at favorable rates.',
                'order': 2,
            },
            {
                'icon': 'fas fa-tools',
                'title_ru': 'Профессиональный монтаж',
                'title_uz': 'Professional montaj',
                'title_en': 'Professional Installation',
                'description_ru': 'Наши мастера установят двери быстро и аккуратно. Опыт работы более 10 лет.',
                'description_uz': 'Ustalarimiz eshiklarni tez va ehtiyotkorlik bilan o\'rnatadi. 10 yildan ortiq tajriba.',
                'description_en': 'Our craftsmen will install doors quickly and carefully. Over 10 years of experience.',
                'order': 3,
            },
            {
                'icon': 'fas fa-ruler-combined',
                'title_ru': 'Бесплатный замер',
                'title_uz': 'Bepul o\'lchov',
                'title_en': 'Free Measurement',
                'description_ru': 'Выезд замерщика бесплатно в удобное для вас время. Точные замеры — идеальная установка.',
                'description_uz': 'O\'lchov mutaxassisi sizga qulay vaqtda bepul keladi. Aniq o\'lchovlar — mukammal o\'rnatish.',
                'description_en': 'Free measurement specialist visit at your convenience. Precise measurements — perfect installation.',
                'order': 4,
            },
            {
                'icon': 'fas fa-wallet',
                'title_ru': 'Доступные цены',
                'title_uz': 'Arzon narxlar',
                'title_en': 'Affordable Prices',
                'description_ru': 'Работаем напрямую с производителями. Лучшие цены без посредников. Рассрочка до 12 месяцев.',
                'description_uz': 'Ishlab chiqaruvchilar bilan bevosita ishlaymiz. Vositachilarsiz eng yaxshi narxlar. 12 oygacha bo\'lib to\'lash.',
                'description_en': 'We work directly with manufacturers. Best prices without middlemen. Installments up to 12 months.',
                'order': 5,
            },
            {
                'icon': 'fas fa-headset',
                'title_ru': 'Консультация 24/7',
                'title_uz': 'Maslahat 24/7',
                'title_en': 'Consultation 24/7',
                'description_ru': 'Наши специалисты готовы ответить на ваши вопросы в любое время. Звоните или пишите!',
                'description_uz': 'Mutaxassislarimiz har qanday vaqtda savollaringizga javob berishga tayyor. Qo\'ng\'iroq qiling yoki yozing!',
                'description_en': 'Our specialists are ready to answer your questions at any time. Call or write!',
                'order': 6,
            },
        ]
        for a in advantages:
            Advantage.objects.create(**a)
        self.stdout.write(self.style.SUCCESS('  6 преимуществ создано'))

    def create_statistics(self):
        Statistic.objects.all().delete()
        stats = [
            {'number': '10+', 'label_ru': 'Лет на рынке', 'label_uz': 'Yillik tajriba', 'label_en': 'Years in the market', 'order': 1},
            {'number': '5000+', 'label_ru': 'Довольных клиентов', 'label_uz': 'Mamnun mijozlar', 'label_en': 'Satisfied customers', 'order': 2},
            {'number': '200+', 'label_ru': 'Моделей дверей', 'label_uz': 'Eshik modellari', 'label_en': 'Door models', 'order': 3},
            {'number': '15+', 'label_ru': 'Партнёров-производителей', 'label_uz': 'Ishlab chiqaruvchi hamkorlar', 'label_en': 'Manufacturing partners', 'order': 4},
        ]
        for s in stats:
            Statistic.objects.create(**s)
        self.stdout.write(self.style.SUCCESS('  4 статистики создано'))

    def create_quality_pillars(self):
        QualityPillar.objects.all().delete()
        pillars = [
            {
                'title_ru': 'Экологичные материалы',
                'title_uz': 'Ekologik materiallar',
                'title_en': 'Eco-friendly Materials',
                'description_ru': 'Мы используем только сертифицированные и безопасные материалы. Все двери соответствуют международным стандартам экологичности.',
                'description_uz': 'Biz faqat sertifikatlangan va xavfsiz materiallardan foydalanamiz. Barcha eshiklar xalqaro ekologik standartlarga mos.',
                'description_en': 'We use only certified and safe materials. All doors meet international environmental standards.',
                'order': 1,
            },
            {
                'title_ru': 'Современный дизайн',
                'title_uz': 'Zamonaviy dizayn',
                'title_en': 'Modern Design',
                'description_ru': 'Следим за мировыми трендами и предлагаем двери в самых актуальных стилях — от минимализма до классики.',
                'description_uz': 'Jahon tendensiyalarini kuzatamiz va eng dolzarb uslublardagi eshiklarni taklif etamiz — minimalizmdan klassikagacha.',
                'description_en': 'We follow global trends and offer doors in the most current styles — from minimalism to classic.',
                'order': 2,
            },
            {
                'title_ru': 'Надёжность и долговечность',
                'title_uz': 'Ishonchlilik va uzoq muddatlilik',
                'title_en': 'Reliability and Durability',
                'description_ru': 'Каждая дверь рассчитана на десятилетия эксплуатации. Прочная фурнитура и износостойкие покрытия.',
                'description_uz': 'Har bir eshik o\'n yillab foydalanish uchun mo\'ljallangan. Mustahkam furnitura va aşınmaya chidamli qoplamalar.',
                'description_en': 'Each door is designed for decades of use. Durable hardware and wear-resistant coatings.',
                'order': 3,
            },
        ]
        for p in pillars:
            QualityPillar.objects.create(**p)
        self.stdout.write(self.style.SUCCESS('  3 столпа качества создано'))

    def create_categories_and_products(self):
        Category.objects.all().delete()

        # Categories
        cat_entrance = Category.objects.create(
            name_ru='Входные двери', name_uz='Kirish eshiklari', name_en='Entrance Doors',
            slug='entrance-doors',
            description_ru='Надёжные входные двери для квартир и частных домов. Стальные, бронированные и утеплённые модели.',
            description_uz='Kvartiralar va xususiy uylar uchun ishonchli kirish eshiklari. Po\'lat, zirhli va issiqlik izolyatsiyali modellar.',
            description_en='Reliable entrance doors for apartments and houses. Steel, armored, and insulated models.',
            order=1,
        )
        cat_interior = Category.objects.create(
            name_ru='Межкомнатные двери', name_uz='Xona eshiklari', name_en='Interior Doors',
            slug='interior-doors',
            description_ru='Элегантные межкомнатные двери из массива, экошпона и ПВХ. Более 200 моделей в наличии.',
            description_uz='Massiv, ekoshpon va PVX dan tayyorlangan nafis xona eshiklari. 200 dan ortiq model mavjud.',
            description_en='Elegant interior doors made of solid wood, eco-veneer, and PVC. Over 200 models in stock.',
            order=2,
        )
        cat_sliding = Category.objects.create(
            name_ru='Раздвижные двери', name_uz='Surma eshiklar', name_en='Sliding Doors',
            slug='sliding-doors',
            description_ru='Современные раздвижные и откатные двери для экономии пространства. Стеклянные и деревянные модели.',
            description_uz='Joyni tejash uchun zamonaviy surma eshiklar. Shisha va yog\'och modellar.',
            description_en='Modern sliding doors to save space. Glass and wooden models.',
            order=3,
        )
        cat_technical = Category.objects.create(
            name_ru='Технические двери', name_uz='Texnik eshiklar', name_en='Technical Doors',
            slug='technical-doors',
            description_ru='Противопожарные, звукоизоляционные и влагостойкие двери для офисов и производств.',
            description_uz='Ofislar va ishlab chiqarish uchun yong\'inga chidamli, tovush izolyatsiyali va namlikka chidamli eshiklar.',
            description_en='Fireproof, soundproof, and moisture-resistant doors for offices and production facilities.',
            order=4,
        )

        # Products - Entrance Doors
        entrance_products = [
            {'name_ru': 'Стальная дверь «Фортеза»', 'name_uz': 'Po\'lat eshik «Forteza»', 'name_en': 'Steel Door "Forteza"',
             'slug': 'steel-forteza', 'price': 3500000,
             'description_ru': 'Стальная входная дверь с тройным контуром уплотнения. Толщина стали 2 мм, утеплитель — минеральная вата. Замок CISA с защитой от взлома.',
             'description_uz': 'Uch konturli zichlanishga ega po\'lat kirish eshigi. Po\'lat qalinligi 2 mm, izolyatsiya — mineral paxta. Buzilishdan himoya qiluvchi CISA qulfi.',
             'description_en': 'Steel entrance door with triple sealing contour. 2mm steel thickness, mineral wool insulation. CISA lock with anti-break protection.',
             'is_popular': True, 'order': 1},
            {'name_ru': 'Бронированная дверь «Титан»', 'name_uz': 'Zirhli eshik «Titan»', 'name_en': 'Armored Door "Titan"',
             'slug': 'armored-titan', 'price': 5200000,
             'description_ru': 'Бронированная дверь повышенной прочности. Двойной лист стали 3 мм, итальянская фурнитура. Класс защиты — 4.',
             'description_uz': 'Yuqori mustahkamlikdagi zirhli eshik. 3 mm ikki qatlamli po\'lat, italyan furniturasi. Himoya sinfi — 4.',
             'description_en': 'Heavy-duty armored door. Double 3mm steel sheet, Italian hardware. Protection class — 4.',
             'is_popular': True, 'order': 2},
            {'name_ru': 'Утеплённая дверь «Термо Люкс»', 'name_uz': 'Issiq izolyatsiyali eshik «Termo Lyuks»', 'name_en': 'Insulated Door "Thermo Lux"',
             'slug': 'thermo-lux', 'price': 4100000,
             'description_ru': 'Входная дверь с усиленной теплоизоляцией. Идеальна для частных домов. Терморазрыв, пенополиуретановый утеплитель.',
             'description_uz': 'Kuchaytirilgan issiqlik izolyatsiyali kirish eshigi. Xususiy uylar uchun ideal. Issiqlik uzilishi, poliuretan ko\'pik izolyatsiya.',
             'description_en': 'Entrance door with enhanced thermal insulation. Perfect for private houses. Thermal break, polyurethane foam insulation.',
             'is_popular': False, 'order': 3},
        ]

        # Products - Interior Doors
        interior_products = [
            {'name_ru': 'Дверь «Классика» из массива дуба', 'name_uz': 'Eman massividan «Klassika» eshigi', 'name_en': '"Classic" Solid Oak Door',
             'slug': 'classic-oak', 'price': 2800000,
             'description_ru': 'Межкомнатная дверь из натурального массива дуба. Классический дизайн с филёнками. Покрытие — итальянский лак.',
             'description_uz': 'Tabiiy eman massividan yasalgan xona eshigi. Filenkali klassik dizayn. Qoplama — italyan laki.',
             'description_en': 'Interior door made of natural solid oak. Classic design with panels. Finish — Italian lacquer.',
             'is_popular': True, 'order': 1},
            {'name_ru': 'Дверь «Модерн» экошпон', 'name_uz': 'Ekoshpon «Modern» eshigi', 'name_en': '"Modern" Eco-veneer Door',
             'slug': 'modern-eco', 'price': 1500000,
             'description_ru': 'Стильная дверь в современном дизайне. Покрытие — экошпон, устойчивый к царапинам и влаге. 6 цветов на выбор.',
             'description_uz': 'Zamonaviy dizayndagi zamonaviy eshik. Qoplama — tirnalish va namlikka chidamli ekoshpon. 6 rang tanlash uchun.',
             'description_en': 'Stylish door in modern design. Eco-veneer coating, resistant to scratches and moisture. 6 colors to choose from.',
             'is_popular': True, 'order': 2},
            {'name_ru': 'Дверь «Минимал» со стеклом', 'name_uz': 'Oynali «Minimal» eshigi', 'name_en': '"Minimal" Glass Door',
             'slug': 'minimal-glass', 'price': 1800000,
             'description_ru': 'Минималистичная дверь со вставкой из матового стекла. Идеальна для современных интерьеров. Покрытие — soft-touch.',
             'description_uz': 'Mat oyna qo\'shimchali minimalist eshik. Zamonaviy interyerlar uchun ideal. Qoplama — soft-touch.',
             'description_en': 'Minimalist door with frosted glass insert. Perfect for modern interiors. Soft-touch coating.',
             'is_popular': False, 'order': 3},
            {'name_ru': 'Дверь «Прима» ПВХ', 'name_uz': 'PVX «Prima» eshigi', 'name_en': '"Prima" PVC Door',
             'slug': 'prima-pvx', 'price': 1200000,
             'description_ru': 'Практичная дверь с ПВХ-покрытием. Устойчива к влаге и перепадам температур. Отличный выбор для ванной и кухни.',
             'description_uz': 'PVX qoplamalari bilan amaliy eshik. Namlik va harorat o\'zgarishlariga chidamli. Vanna va oshxona uchun ajoyib tanlov.',
             'description_en': 'Practical door with PVC coating. Resistant to moisture and temperature changes. Great choice for bathroom and kitchen.',
             'is_popular': False, 'order': 4},
        ]

        # Products - Sliding Doors
        sliding_products = [
            {'name_ru': 'Раздвижная дверь «Лофт»', 'name_uz': 'Surma eshik «Loft»', 'name_en': 'Sliding Door "Loft"',
             'slug': 'loft-sliding', 'price': 3200000,
             'description_ru': 'Раздвижная дверь в стиле лофт с амбарным механизмом. Натуральное дерево, металлическая фурнитура.',
             'description_uz': 'Omborxona mexanizmli loft uslubidagi surma eshik. Tabiiy yog\'och, metall furnitura.',
             'description_en': 'Loft-style sliding door with barn mechanism. Natural wood, metal hardware.',
             'is_popular': True, 'order': 1},
            {'name_ru': 'Стеклянная перегородка «Кристалл»', 'name_uz': 'Shisha to\'siq «Kristall»', 'name_en': 'Glass Partition "Crystal"',
             'slug': 'crystal-glass', 'price': 4500000,
             'description_ru': 'Раздвижная стеклянная перегородка из закалённого стекла 8 мм. Алюминиевый профиль, тихий ход.',
             'description_uz': '8 mm toblangan shishadan surma shisha to\'siq. Alyuminiy profil, sokin harakat.',
             'description_en': 'Sliding glass partition made of 8mm tempered glass. Aluminum profile, quiet operation.',
             'is_popular': False, 'order': 2},
        ]

        # Products - Technical Doors
        technical_products = [
            {'name_ru': 'Противопожарная дверь EI-60', 'name_uz': 'Yong\'inga chidamli eshik EI-60', 'name_en': 'Fireproof Door EI-60',
             'slug': 'fireproof-ei60', 'price': 4800000,
             'description_ru': 'Сертифицированная противопожарная дверь с пределом огнестойкости 60 минут. Для офисов, складов и производственных помещений.',
             'description_uz': '60 daqiqa yong\'inga chidamlilik chegarasiga ega sertifikatlangan yong\'inga chidamli eshik.',
             'description_en': 'Certified fireproof door with 60-minute fire resistance. For offices, warehouses, and production facilities.',
             'is_popular': False, 'order': 1},
            {'name_ru': 'Звукоизоляционная дверь «Тишина»', 'name_uz': 'Tovush izolyatsiyali eshik «Jimjitlik»', 'name_en': 'Soundproof Door "Silence"',
             'slug': 'silence-sound', 'price': 3900000,
             'description_ru': 'Дверь с повышенной звукоизоляцией до 42 дБ. Идеальна для студий, офисов и спален.',
             'description_uz': '42 dB gacha kuchaytirilgan tovush izolyatsiyali eshik. Studiyalar, ofislar va yotoqxonalar uchun ideal.',
             'description_en': 'Door with enhanced soundproofing up to 42 dB. Perfect for studios, offices, and bedrooms.',
             'is_popular': False, 'order': 2},
        ]

        for p in entrance_products:
            Product.objects.create(category=cat_entrance, **p)
        for p in interior_products:
            Product.objects.create(category=cat_interior, **p)
        for p in sliding_products:
            Product.objects.create(category=cat_sliding, **p)
        for p in technical_products:
            Product.objects.create(category=cat_technical, **p)

        self.stdout.write(self.style.SUCCESS('  4 категории и 11 товаров создано'))

    def create_news(self):
        Article.objects.all().delete()
        articles = [
            {
                'title_ru': 'Как выбрать входную дверь: полное руководство',
                'title_uz': 'Kirish eshigini qanday tanlash mumkin: to\'liq qo\'llanma',
                'title_en': 'How to Choose an Entrance Door: Complete Guide',
                'slug': 'how-to-choose-entrance-door',
                'content_ru': (
                    'Выбор входной двери — ответственное решение, от которого зависит безопасность вашего дома. '
                    'В этой статье мы расскажем о ключевых критериях выбора.\n\n'
                    '**1. Материал двери**\n'
                    'Стальные двери — самый популярный выбор. Они обеспечивают надёжную защиту от взлома и имеют долгий срок службы. '
                    'Обратите внимание на толщину стали — оптимально от 1.5 до 3 мм.\n\n'
                    '**2. Замковая система**\n'
                    'Рекомендуем устанавливать два замка разных типов: сувальдный и цилиндровый. '
                    'Лучшие производители замков: CISA, Mottura, Kale.\n\n'
                    '**3. Утепление**\n'
                    'Для частных домов важна теплоизоляция двери. Лучшие утеплители: минеральная вата и пенополиуретан. '
                    'Двери с терморазрывом предотвращают промерзание.\n\n'
                    '**4. Отделка**\n'
                    'Внешняя отделка должна быть устойчива к погодным условиям. Популярные варианты: порошковая покраска, '
                    'МДФ-панели, натуральный шпон.\n\n'
                    'Приходите в наш шоурум — наши консультанты помогут подобрать идеальную дверь!'
                ),
                'content_uz': (
                    'Kirish eshigini tanlash — uyingiz xavfsizligiga bog\'liq mas\'uliyatli qaror. '
                    'Ushbu maqolada biz tanlashning asosiy mezonlari haqida gapiramiz.\n\n'
                    '**1. Eshik materiali**\n'
                    'Po\'lat eshiklar — eng mashhur tanlov. Ular buzilishdan ishonchli himoya qiladi.\n\n'
                    '**2. Qulf tizimi**\n'
                    'Ikki xil turdagi qulfni o\'rnatishni tavsiya etamiz.\n\n'
                    '**3. Izolyatsiya**\n'
                    'Xususiy uylar uchun eshikning issiqlik izolyatsiyasi muhim.\n\n'
                    '**4. Pardozlash**\n'
                    'Tashqi pardozlash ob-havo sharoitlariga chidamli bo\'lishi kerak.\n\n'
                    'Shovrumimizga keling — maslahatchilarimiz ideal eshikni tanlashda yordam beradi!'
                ),
                'content_en': (
                    'Choosing an entrance door is a responsible decision that affects the security of your home. '
                    'In this article, we will tell you about the key selection criteria.\n\n'
                    '**1. Door Material**\n'
                    'Steel doors are the most popular choice. They provide reliable protection against break-ins.\n\n'
                    '**2. Lock System**\n'
                    'We recommend installing two locks of different types: lever and cylinder.\n\n'
                    '**3. Insulation**\n'
                    'For private houses, door thermal insulation is important.\n\n'
                    '**4. Finish**\n'
                    'The exterior finish should be weather-resistant.\n\n'
                    'Visit our showroom — our consultants will help you choose the perfect door!'
                ),
                'is_published': True,
            },
            {
                'title_ru': 'Тренды дверного дизайна 2025 года',
                'title_uz': '2025 yil eshik dizayni tendensiyalari',
                'title_en': 'Door Design Trends 2025',
                'slug': 'door-design-trends-2025',
                'content_ru': (
                    'Мир дизайна интерьера постоянно развивается, и двери — не исключение. '
                    'Рассмотрим главные тренды 2025 года.\n\n'
                    '**Скрытые двери**\n'
                    'Двери-невидимки, сливающиеся со стеной — абсолютный хит сезона. '
                    'Они создают ощущение единого пространства и минимализма.\n\n'
                    '**Натуральные текстуры**\n'
                    'Возвращение к природным материалам: массив дуба, ясеня, ореха. '
                    'Текстура дерева подчёркивается маслами и восками вместо глянцевого лака.\n\n'
                    '**Тёмные оттенки**\n'
                    'Чёрные и тёмно-серые двери набирают популярность. Они выглядят стильно и подходят к любому интерьеру.\n\n'
                    '**Стеклянные вставки**\n'
                    'Двери с рифлёным или тонированным стеклом добавляют лёгкости пространству, сохраняя приватность.'
                ),
                'content_uz': (
                    'Interer dizayni dunyosi doimiy rivojlanmoqda va eshiklar ham istisno emas. '
                    '2025 yilning asosiy tendensiyalarini ko\'rib chiqamiz.\n\n'
                    '**Yashirin eshiklar**\n'
                    'Devorga qo\'shilib ketadigan ko\'rinmas eshiklar — mavsumning mutlaq xiti.\n\n'
                    '**Tabiiy teksturalar**\n'
                    'Tabiiy materiallarga qaytish: eman, zarang, yong\'oq massivi.\n\n'
                    '**Qorong\'u ranglar**\n'
                    'Qora va to\'q kulrang eshiklar mashhurlik qozonmoqda.\n\n'
                    '**Shisha qo\'shimchalar**\n'
                    'Qirrali yoki tonlangan shishali eshiklar fazoga yengillik qo\'shadi.'
                ),
                'content_en': (
                    'The world of interior design is constantly evolving, and doors are no exception. '
                    'Let\'s look at the main trends of 2025.\n\n'
                    '**Hidden Doors**\n'
                    'Invisible doors that blend with the wall — the absolute hit of the season.\n\n'
                    '**Natural Textures**\n'
                    'Return to natural materials: solid oak, ash, walnut.\n\n'
                    '**Dark Shades**\n'
                    'Black and dark gray doors are gaining popularity.\n\n'
                    '**Glass Inserts**\n'
                    'Doors with ribbed or tinted glass add lightness to the space.'
                ),
                'is_published': True,
            },
            {
                'title_ru': 'Уход за межкомнатными дверями: советы эксперта',
                'title_uz': 'Xona eshiklariga g\'amxo\'rlik qilish: ekspert maslahatlari',
                'title_en': 'Interior Door Care: Expert Tips',
                'slug': 'interior-door-care-tips',
                'content_ru': (
                    'Правильный уход продлевает жизнь ваших дверей на десятилетия. '
                    'Делимся профессиональными советами.\n\n'
                    '**Ежедневный уход**\n'
                    'Протирайте двери мягкой влажной тряпкой. Не используйте абразивные средства и растворители.\n\n'
                    '**Уход за фурнитурой**\n'
                    'Смазывайте петли и замки маслом раз в полгода. Это обеспечит тихую и плавную работу механизмов.\n\n'
                    '**Защита от влаги**\n'
                    'Для дверей в ванной и кухне используйте специальные влагозащитные составы. '
                    'Не допускайте длительного контакта с водой.\n\n'
                    '**Мелкий ремонт**\n'
                    'Небольшие царапины можно устранить восковым карандашом подходящего цвета. '
                    'Для глубоких повреждений обратитесь к специалистам.'
                ),
                'content_uz': (
                    'To\'g\'ri parvarishlash eshiklaringiz umrini o\'n yilliklarga uzaytiradi.\n\n'
                    '**Kundalik parvarish**\n'
                    'Eshiklarni yumshoq nam latta bilan arting.\n\n'
                    '**Furnituraga g\'amxo\'rlik**\n'
                    'Ilgaklarni va qulflarni yarim yilda bir marta moylang.\n\n'
                    '**Namlikdan himoya**\n'
                    'Vanna va oshxonadagi eshiklar uchun maxsus namlikdan himoya vositalarini ishlating.\n\n'
                    '**Kichik ta\'mirlash**\n'
                    'Kichik chiziqlarni mos rangdagi mumli qalam bilan yo\'qotish mumkin.'
                ),
                'content_en': (
                    'Proper care extends the life of your doors for decades.\n\n'
                    '**Daily Care**\n'
                    'Wipe doors with a soft damp cloth. Do not use abrasive products or solvents.\n\n'
                    '**Hardware Care**\n'
                    'Lubricate hinges and locks with oil every six months.\n\n'
                    '**Moisture Protection**\n'
                    'For bathroom and kitchen doors, use special moisture-protective compounds.\n\n'
                    '**Minor Repairs**\n'
                    'Small scratches can be removed with a matching wax pencil.'
                ),
                'is_published': True,
            },
        ]
        for a in articles:
            Article.objects.create(**a)
        self.stdout.write(self.style.SUCCESS('  3 новости/статьи создано'))

    def create_portfolio(self):
        Project.objects.all().delete()
        projects = [
            {
                'title_ru': 'Жилой комплекс «Навруз Резиденс»',
                'title_uz': 'Turar-joy majmuasi «Navro\'z Rezidens»',
                'title_en': 'Residential Complex "Navruz Residence"',
                'slug': 'navruz-residence',
                'description_ru': 'Поставка и установка 120 входных и 480 межкомнатных дверей для жилого комплекса «Навруз Резиденс» в Ташкенте. Проект выполнен за 3 месяца. Использовались стальные входные двери «Фортеза» и межкомнатные двери «Модерн» в цвете белый дуб.',
                'description_uz': 'Toshkentdagi «Navro\'z Rezidens» turar-joy majmuasi uchun 120 ta kirish va 480 ta xona eshiklarini yetkazib berish va o\'rnatish. Loyiha 3 oyda bajarildi.',
                'description_en': 'Supply and installation of 120 entrance and 480 interior doors for the "Navruz Residence" complex in Tashkent. Project completed in 3 months.',
            },
            {
                'title_ru': 'Бизнес-центр «Тахир Плаза»',
                'title_uz': 'Biznes-markaz «Tohir Plaza»',
                'title_en': 'Business Center "Tahir Plaza"',
                'slug': 'tahir-plaza',
                'description_ru': 'Комплексное оснащение бизнес-центра: 50 противопожарных дверей EI-60, 200 офисных дверей с повышенной звукоизоляцией. Все двери выполнены в корпоративных цветах заказчика.',
                'description_uz': 'Biznes-markazni kompleks jihozlash: 50 ta yong\'inga chidamli EI-60 eshik, 200 ta kuchaytirilgan tovush izolyatsiyali ofis eshiklari.',
                'description_en': 'Comprehensive equipping of the business center: 50 EI-60 fireproof doors, 200 office doors with enhanced soundproofing.',
            },
            {
                'title_ru': 'Частный дом в Юнусабаде',
                'title_uz': 'Yunusobodda xususiy uy',
                'title_en': 'Private House in Yunusabad',
                'slug': 'private-house-yunusabad',
                'description_ru': 'Полное оснащение частного дома: входная бронированная дверь «Титан», 8 межкомнатных дверей из массива дуба, 2 раздвижные двери «Лофт». Индивидуальный дизайн под интерьер заказчика.',
                'description_uz': 'Xususiy uyni to\'liq jihozlash: zirhli kirish eshigi «Titan», 8 ta eman massividan xona eshiklari, 2 ta surma eshik «Loft».',
                'description_en': 'Complete furnishing of a private house: "Titan" armored entrance door, 8 solid oak interior doors, 2 "Loft" sliding doors.',
            },
            {
                'title_ru': 'Гостиница «Самарканд Палас»',
                'title_uz': 'Mehmonxona «Samarqand Palas»',
                'title_en': 'Hotel "Samarkand Palace"',
                'slug': 'samarkand-palace-hotel',
                'description_ru': 'Поставка 150 дверей для гостиницы в Самарканде: звукоизоляционные двери для номеров, противопожарные двери для коридоров, стеклянные перегородки для ресторана.',
                'description_uz': 'Samarqanddagi mehmonxona uchun 150 ta eshikni yetkazib berish: xonalar uchun tovush izolyatsiyali eshiklar, koridorlar uchun yong\'inga chidamli eshiklar.',
                'description_en': 'Supply of 150 doors for a hotel in Samarkand: soundproof doors for rooms, fireproof doors for corridors, glass partitions for the restaurant.',
            },
        ]
        for p in projects:
            Project.objects.create(**p)
        self.stdout.write(self.style.SUCCESS('  4 проекта в портфолио создано'))

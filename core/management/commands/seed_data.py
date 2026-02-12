from django.core.management.base import BaseCommand
from core.models import SiteSettings, Banner, Advantage, Statistic, Partner, QualityPillar, PageSeo
from catalog.models import Category, Product
from news.models import Article
from portfolio.models import Project


class Command(BaseCommand):
    help = 'Seed database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # --- SiteSettings ---
        s, _ = SiteSettings.objects.get_or_create(pk=1)
        s.company_name_ru = 'DOOR COMPANY'
        s.company_name_uz = 'DOOR COMPANY'
        s.company_name_en = 'DOOR COMPANY'
        s.slogan_ru = 'Производство и установка стальных дверей в Ташкенте'
        s.slogan_uz = 'Toshkentda po\'lat eshiklar ishlab chiqarish va o\'rnatish'
        s.slogan_en = 'Manufacturing and installation of steel doors in Tashkent'
        s.about_text_ru = 'Мы являемся ведущим производителем стальных дверей в Узбекистане. Наша компания сочетает современные технологии производства с индивидуальным подходом к каждому клиенту. Более 10 лет мы обеспечиваем безопасность и комфорт тысяч семей по всей стране.'
        s.about_text_uz = 'Biz O\'zbekistondagi yetakchi po\'lat eshiklar ishlab chiqaruvchisimiz. Kompaniyamiz zamonaviy ishlab chiqarish texnologiyalarini har bir mijozga individual yondashish bilan uyg\'unlashtiradi. 10 yildan ortiq vaqt davomida biz butun mamlakat bo\'ylab minglab oilalarning xavfsizligi va qulayligini ta\'minlaymiz.'
        s.about_text_en = 'We are a leading manufacturer of steel doors in Uzbekistan. Our company combines modern production technologies with an individual approach to each client. For over 10 years, we have been ensuring the safety and comfort of thousands of families across the country.'
        s.phone = '+998 97 444-05-30'
        s.phone2 = '+998 71 123-45-67'
        s.email = 'info@doorcompany.uz'
        s.address_ru = 'г. Ташкент, ул. Темирчи 19'
        s.address_uz = 'Toshkent sh., Temirchi ko\'chasi 19'
        s.address_en = 'Tashkent, Temirchi str. 19'
        s.telegram_url = 'https://t.me/doorcompany'
        s.instagram_url = 'https://instagram.com/doorcompany'
        s.map_embed = '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2996.0542689803045!2d69.27927!3d41.31115!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDHCsDE4JzQwLjEiTiA2OcKwMTYnNDUuNCJF!5e0!3m2!1sru!2s!4v1700000000000!5m2!1sru!2s" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'
        s.save()
        self.stdout.write(self.style.SUCCESS('  SiteSettings done'))

        # --- Banners ---
        Banner.objects.all().delete()
        Banner.objects.create(
            title_ru='Откройте дверь в безопасное будущее',
            title_uz='Xavfsiz kelajakka eshik oching',
            title_en='Open the door to a safe future',
            subtitle_ru='Производство и установка стальных дверей премиум-класса в Ташкенте',
            subtitle_uz='Toshkentda premium sinfli po\'lat eshiklar ishlab chiqarish va o\'rnatish',
            subtitle_en='Manufacturing and installation of premium steel doors in Tashkent',
            button_text_ru='Связаться с нами',
            button_text_uz='Biz bilan bog\'laning',
            button_text_en='Contact us',
            button_url='/contacts/',
            order=1, is_active=True,
        )
        Banner.objects.create(
            title_ru='Новая коллекция дверей уже в продаже!',
            title_uz='Yangi eshiklar to\'plami sotuvda!',
            title_en='New door collection now on sale!',
            subtitle_ru='Широкий выбор моделей для вашего дома и офиса',
            subtitle_uz='Uyingiz va ofisingiz uchun keng tanlov',
            subtitle_en='Wide selection of models for your home and office',
            button_text_ru='Смотреть каталог',
            button_text_uz='Katalogni ko\'rish',
            button_text_en='View catalog',
            button_url='/catalog/',
            order=2, is_active=True,
        )
        self.stdout.write(self.style.SUCCESS('  Banners done'))

        # --- Categories ---
        Category.objects.all().delete()
        cat1 = Category.objects.create(
            name_ru='Входные двери', name_uz='Kirish eshiklari', name_en='Entry doors',
            slug='vhodnye-dveri', order=1,
            description_ru='Надёжные стальные двери для квартир и частных домов',
            description_uz='Kvartiralar va xususiy uylar uchun ishonchli po\'lat eshiklar',
            description_en='Reliable steel doors for apartments and private houses',
        )
        cat2 = Category.objects.create(
            name_ru='Технические двери', name_uz='Texnik eshiklar', name_en='Technical doors',
            slug='tehnicheskie-dveri', order=2,
            description_ru='Противопожарные и технические двери для коммерческих объектов',
            description_uz='Tijorat ob\'ektlari uchun o\'tga chidamli va texnik eshiklar',
            description_en='Fire-resistant and technical doors for commercial buildings',
        )
        cat3 = Category.objects.create(
            name_ru='Металлические изделия', name_uz='Metall buyumlar', name_en='Metal products',
            slug='metallicheskie-izdeliya', order=3,
            description_ru='Металлические шкафы, щиты и решётки',
            description_uz='Metall shkaflar, qalqonlar va panjaralar',
            description_en='Metal cabinets, shields and grilles',
        )
        cat4 = Category.objects.create(
            name_ru='Фурнитура', name_uz='Furnitura', name_en='Hardware',
            slug='furnitura', order=4,
            description_ru='Замки, ручки и фурнитура для дверей',
            description_uz='Qulflar, tutqichlar va eshik furniturasi',
            description_en='Locks, handles and door hardware',
        )
        self.stdout.write(self.style.SUCCESS('  Categories done'))

        # --- Products ---
        Product.objects.all().delete()
        products_data = [
            ('MRAMOR', 'mramor', cat1, 5500000, True),
            ('AVANGARD', 'avangard', cat1, 4800000, True),
            ('TIARA', 'tiara', cat1, 6200000, True),
            ('GREENWICH', 'greenwich', cat1, 7100000, True),
            ('FORTIS', 'fortis', cat1, 3900000, False),
            ('ELEGANCE', 'elegance', cat1, 5100000, False),
            ('ТД-01 Противопожарная', 'td-01', cat2, 3200000, False),
            ('ТД-02 Техническая', 'td-02', cat2, 2800000, False),
            ('Шкаф металлический ШМ-1', 'shm-1', cat3, 1500000, False),
            ('Решётка оконная РО-1', 'ro-1', cat3, 800000, False),
            ('Замок CISA 5-ти точечный', 'cisa-5', cat4, 450000, False),
            ('Ручка дверная HD-01', 'hd-01', cat4, 120000, False),
        ]
        for name, slug, cat, price, popular in products_data:
            Product.objects.create(
                name_ru=name, name_uz=name, name_en=name,
                slug=slug, category=cat, price=price, is_popular=popular, order=0,
                description_ru=f'Высококачественный продукт {name} от нашего производства. Изготовлен из прочной стали с применением современных технологий.',
                description_uz=f'{name} — zamonaviy texnologiyalar yordamida mustahkam po\'latdan tayyorlangan yuqori sifatli mahsulot.',
                description_en=f'High-quality {name} product from our production. Made from durable steel using modern technology.',
            )
        self.stdout.write(self.style.SUCCESS('  Products done'))

        # --- Advantages ---
        Advantage.objects.all().delete()
        advs = [
            ('fas fa-shield-alt', 'Надёжность и безопасность', 'Ishonchlilik va xavfsizlik', 'Reliability and safety',
             'Наши двери проходят строгий контроль качества и соответствуют всем стандартам безопасности.',
             'Eshiklarimiz qat\'iy sifat nazoratidan o\'tadi va barcha xavfsizlik standartlariga javob beradi.',
             'Our doors undergo strict quality control and meet all safety standards.'),
            ('fas fa-user-cog', 'Индивидуальный подход', 'Individual yondashuv', 'Individual approach',
             'Мы подбираем оптимальное решение для каждого клиента с учётом всех пожеланий.',
             'Har bir mijozning barcha istaklarini hisobga olib, optimal yechimni tanlaymiz.',
             'We select the optimal solution for each client, considering all requirements.'),
            ('fas fa-leaf', 'Энергоэффективность', 'Energiya samaradorligi', 'Energy efficiency',
             'Двери с улучшенной теплоизоляцией помогают экономить на отоплении.',
             'Yaxshilangan issiqlik izolyatsiyali eshiklar isitish xarajatlarini tejashga yordam beradi.',
             'Doors with improved thermal insulation help save on heating costs.'),
        ]
        for i, (icon, ru, uz, en, d_ru, d_uz, d_en) in enumerate(advs, 1):
            Advantage.objects.create(
                icon=icon, title_ru=ru, title_uz=uz, title_en=en,
                description_ru=d_ru, description_uz=d_uz, description_en=d_en, order=i,
            )
        self.stdout.write(self.style.SUCCESS('  Advantages done'))

        # --- Quality Pillars ---
        QualityPillar.objects.all().delete()
        pillars = [
            ('Качество стали', 'Po\'lat sifati', 'Steel quality',
             'Используем только сертифицированную сталь толщиной от 1.5 мм.',
             'Faqat qalinligi 1,5 mm dan sertifikatlangan po\'latdan foydalanamiz.',
             'We use only certified steel with a thickness of 1.5 mm or more.'),
            ('Современные замки', 'Zamonaviy qulflar', 'Modern locks',
             'Многоточечные замковые системы от ведущих производителей.',
             'Yetakchi ishlab chiqaruvchilardan ko\'p nuqtali qulflash tizimlari.',
             'Multi-point locking systems from leading manufacturers.'),
            ('Теплоизоляция', 'Issiqlik izolyatsiyasi', 'Thermal insulation',
             'Трёхслойное утепление для максимальной энергоэффективности.',
             'Maksimal energiya samaradorligi uchun uch qatlamli izolyatsiya.',
             'Three-layer insulation for maximum energy efficiency.'),
            ('Дизайн', 'Dizayn', 'Design',
             'Более 50 вариантов отделки и цветовых решений на выбор.',
             '50 dan ortiq bezak va rang variantlari tanlash uchun.',
             'Over 50 finish options and color solutions to choose from.'),
        ]
        for i, (ru, uz, en, d_ru, d_uz, d_en) in enumerate(pillars, 1):
            QualityPillar.objects.create(
                title_ru=ru, title_uz=uz, title_en=en,
                description_ru=d_ru, description_uz=d_uz, description_en=d_en, order=i,
            )
        self.stdout.write(self.style.SUCCESS('  Quality Pillars done'))

        # --- Statistics ---
        Statistic.objects.all().delete()
        stats = [
            ('10+', 'лет на рынке', 'yil bozorda', 'years on the market'),
            ('48 000+', 'установленных дверей', 'o\'rnatilgan eshiklar', 'installed doors'),
            ('7', 'лет гарантии', 'yil kafolat', 'years warranty'),
            ('1500 м²', 'площадь производства', 'ishlab chiqarish maydoni', 'production area'),
        ]
        for i, (num, l_ru, l_uz, l_en) in enumerate(stats, 1):
            Statistic.objects.create(
                number=num,
                label_ru=l_ru, label_uz=l_uz, label_en=l_en, order=i,
            )
        self.stdout.write(self.style.SUCCESS('  Statistics done'))

        # --- Partners ---
        Partner.objects.all().delete()
        for i, name in enumerate(['CISA', 'Mottura', 'Kale Kilit', 'Mul-T-Lock', 'Северсталь', 'Severstal'], 1):
            Partner.objects.create(name=name, order=i)
        self.stdout.write(self.style.SUCCESS('  Partners done'))

        # --- Articles ---
        Article.objects.all().delete()
        articles = [
            ('Новая коллекция дверей MRAMOR', 'novaya-kollekciya-mramor',
             'Yangi MRAMOR eshiklar to\'plami', 'New MRAMOR door collection',
             'Представляем новую линейку дверей MRAMOR с улучшенной теплоизоляцией и современным дизайном. Двери доступны в 12 цветовых решениях.',
             'Yaxshilangan issiqlik izolyatsiyasi va zamonaviy dizaynli yangi MRAMOR eshiklar qatorini taqdim etamiz.',
             'Introducing the new MRAMOR door line with improved thermal insulation and modern design.'),
            ('Участие в выставке BuildExpo 2025', 'buildexpo-2025',
             'BuildExpo 2025 ko\'rgazmasida ishtirok', 'Participation in BuildExpo 2025',
             'Наша компания приняла участие в международной строительной выставке BuildExpo 2025 в Ташкенте, где представила последние разработки.',
             'Kompaniyamiz Toshkentdagi BuildExpo 2025 xalqaro qurilish ko\'rgazmasida ishtirok etdi.',
             'Our company participated in the international construction exhibition BuildExpo 2025 in Tashkent.'),
            ('Как выбрать входную дверь', 'kak-vybrat-dver',
             'Kirish eshigini qanday tanlash kerak', 'How to choose an entry door',
             'Полезные советы по выбору входной двери: на что обратить внимание при покупке, какие замки выбрать, какая толщина стали оптимальна.',
             'Kirish eshigini tanlash bo\'yicha foydali maslahatlar: sotib olishda nimaga e\'tibor berish kerak.',
             'Useful tips on choosing an entry door: what to pay attention to when buying.'),
        ]
        for i, (t_ru, slug, t_uz, t_en, c_ru, c_uz, c_en) in enumerate(articles):
            Article.objects.create(
                title_ru=t_ru, title_uz=t_uz, title_en=t_en,
                slug=slug,
                content_ru=c_ru, content_uz=c_uz, content_en=c_en,
                is_published=True,
            )
        self.stdout.write(self.style.SUCCESS('  Articles done'))

        # --- Projects ---
        Project.objects.all().delete()
        projects = [
            ('Golden House Residence', 'golden-house',
             'Установка 120 входных дверей премиум-класса в жилом комплексе Golden House.',
             'Golden House turar-joy majmuasiga 120 ta premium kirish eshiklari o\'rnatish.',
             'Installation of 120 premium entry doors in Golden House residential complex.'),
            ('Mirabad Avenue', 'mirabad-avenue',
             'Комплексное оснащение бизнес-центра Mirabad Avenue техническими и противопожарными дверями.',
             'Mirabad Avenue biznes markazini texnik va o\'tga chidamli eshiklar bilan jihozlash.',
             'Comprehensive equipping of Mirabad Avenue business center with technical and fire-resistant doors.'),
            ('ЖК «Сити Парк»', 'city-park',
             'Поставка и монтаж 250 входных дверей для нового жилого комплекса «Сити Парк».',
             'Yangi "City Park" turar-joy majmuasi uchun 250 ta kirish eshiklarini yetkazib berish va o\'rnatish.',
             'Supply and installation of 250 entry doors for the new City Park residential complex.'),
            ('Tashkent City Mall', 'tashkent-city-mall',
             'Изготовление и установка металлических противопожарных дверей для торгового центра.',
             'Savdo markazi uchun metall o\'tga chidamli eshiklar tayyorlash va o\'rnatish.',
             'Manufacturing and installation of metal fire-resistant doors for the shopping center.'),
        ]
        for p_data in projects:
            Project.objects.create(
                title_ru=p_data[0], title_uz=p_data[0], title_en=p_data[0],
                slug=p_data[1],
                description_ru=p_data[2], description_uz=p_data[3], description_en=p_data[4],
            )
        self.stdout.write(self.style.SUCCESS('  Projects done'))

        # --- PageSeo ---
        PageSeo.objects.all().delete()
        seo_data = [
            ('home', 'Door Company — Производитель стальных дверей в Ташкенте',
             'Производство и установка стальных входных дверей в Ташкенте. Более 10 лет опыта, гарантия до 7 лет.',
             'двери, входные двери, стальные двери, Ташкент, купить двери'),
            ('about', 'О компании — Door Company',
             'Door Company — ведущий производитель стальных дверей в Узбекистане. Современное производство, индивидуальный подход.',
             'о компании, производство дверей, Door Company'),
            ('catalog', 'Каталог дверей — Door Company',
             'Каталог входных, технических и противопожарных дверей. Широкий выбор моделей и цветовых решений.',
             'каталог дверей, входные двери, технические двери, цены'),
            ('news', 'Новости — Door Company',
             'Последние новости компании Door Company: новые коллекции, выставки, полезные советы.',
             'новости, Door Company, двери'),
            ('portfolio', 'Наши работы — Door Company',
             'Реализованные проекты компании Door Company. Жилые комплексы, бизнес-центры, торговые центры.',
             'наши работы, портфолио, установка дверей, проекты'),
            ('contacts', 'Контакты — Door Company',
             'Свяжитесь с нами: телефон, email, адрес. Оставьте заявку и мы перезвоним.',
             'контакты, адрес, телефон, Door Company'),
        ]
        for page, title, desc, keywords in seo_data:
            PageSeo.objects.create(
                page=page,
                meta_title_ru=title,
                meta_description_ru=desc,
                meta_keywords_ru=keywords,
            )
        self.stdout.write(self.style.SUCCESS('  PageSeo done'))

        self.stdout.write(self.style.SUCCESS('\nAll test data seeded successfully!'))

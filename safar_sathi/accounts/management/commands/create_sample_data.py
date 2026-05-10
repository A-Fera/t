from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import LocalGuide
from destinations.models import Destination, DestinationFeature
from bookings.models import Accommodation

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates sample data for Safar Sathi'

    def handle(self, *args, **kwargs):
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@safarsathi.com', 'admin123')
            admin.first_name = 'Admin'
            admin.last_name = 'User'
            admin.save()
            self.stdout.write('Created admin user (username: admin, password: admin123)')

        # Create sample destinations
        destinations_data = [
            {
                'name': "Cox's Bazar",
                'description': "Cox's Bazar is a town, a fishing port, a tourism centre in Bangladesh. It is famous for having the world's longest natural sea beach.",
                'location': "Cox's Bazar",
                'state': 'Chittagong',
                'category': 'beach',
                'best_time_to_visit': 'October to March',
                'entry_fee': 0,
                'latitude': 21.4272,
                'longitude': 92.0058,
                'is_featured': True,
            },
            {
                'name': 'Sundarbans',
                'description': 'The Sundarbans is the largest mangrove forest in the world, shared between Bangladesh and India. It is home to the Royal Bengal Tiger.',
                'location': 'Khulna',
                'state': 'Khulna',
                'category': 'forest',
                'best_time_to_visit': 'November to February',
                'entry_fee': 200,
                'latitude': 21.9497,
                'longitude': 89.1833,
                'is_featured': True,
            },
            {
                'name': 'Sajek Valley',
                'description': 'Sajek Valley is a union in Rangamati District in the Chittagong Hill Tracts of Bangladesh. It is known as the roof of Rangamati.',
                'location': 'Rangamati',
                'state': 'Chittagong',
                'category': 'mountain',
                'best_time_to_visit': 'September to April',
                'entry_fee': 0,
                'latitude': 23.3818,
                'longitude': 92.2939,
                'is_featured': True,
            },
            {
                'name': 'Srimangal',
                'description': "Srimangal is called the Tea Capital of Bangladesh. It is home to lush green tea gardens, Lawachara National Park, and diverse wildlife.",
                'location': 'Sylhet',
                'state': 'Sylhet',
                'category': 'rural',
                'best_time_to_visit': 'October to March',
                'entry_fee': 0,
                'latitude': 24.3065,
                'longitude': 91.7285,
                'is_featured': True,
            },
            {
                'name': 'Old Dhaka',
                'description': 'Old Dhaka is the historic heart of Bangladesh capital, filled with Mughal architecture, river ghats, and vibrant street food culture.',
                'location': 'Dhaka',
                'state': 'Dhaka',
                'category': 'historical',
                'best_time_to_visit': 'November to February',
                'entry_fee': 0,
                'latitude': 23.7104,
                'longitude': 90.4074,
                'is_featured': False,
            },
            {
                'name': 'Kuakata',
                'description': 'Kuakata, locally known as Sagar Kannya (Daughter of the Sea), is a rare sea beach in Bangladesh from where both sunrise and sunset can be seen.',
                'location': 'Patuakhali',
                'state': 'Barisal',
                'category': 'beach',
                'best_time_to_visit': 'October to March',
                'entry_fee': 0,
                'latitude': 21.8152,
                'longitude': 90.1201,
                'is_featured': True,
            },
        ]

        admin_user = User.objects.get(username='admin')
        created_destinations = []

        for data in destinations_data:
            dest, created = Destination.objects.get_or_create(
                name=data['name'],
                defaults={**data, 'created_by': admin_user}
            )
            created_destinations.append(dest)
            if created:
                self.stdout.write(f'Created destination: {dest.name}')

        # Create sample accommodations
        if created_destinations:
            acc_data = [
                {
                    'destination': created_destinations[0],
                    'name': 'Sea Pearl Beach Resort',
                    'accommodation_type': 'resort',
                    'description': 'Luxury beach resort with stunning ocean views and world-class amenities.',
                    'price_per_night': 8000,
                    'max_guests': 4,
                    'phone': '+880 1711-000001',
                    'email': 'info@seapearl.com',
                    'amenities': 'Pool WiFi Restaurant Gym Spa BeachAccess AirConditioning RoomService',
                },
                {
                    'destination': created_destinations[2],
                    'name': 'Sajek Resort',
                    'accommodation_type': 'resort',
                    'description': 'Hilltop resort with breathtaking views of the Sajek Valley and surrounding hills.',
                    'price_per_night': 5000,
                    'max_guests': 3,
                    'phone': '+880 1711-000002',
                    'email': 'info@sajekresort.com',
                    'amenities': 'WiFi Restaurant Bonfire HillView',
                },
                {
                    'destination': created_destinations[3],
                    'name': 'Grand Sultan Tea Resort',
                    'accommodation_type': 'resort',
                    'description': 'Exclusive tea resort nestled in the lush green tea gardens of Srimangal.',
                    'price_per_night': 6000,
                    'max_guests': 2,
                    'phone': '+880 1711-000003',
                    'email': 'info@grandsultan.com',
                    'amenities': 'WiFi Restaurant TeaGarden Pool Spa',
                },
            ]

            for data in acc_data:
                acc, created = Accommodation.objects.get_or_create(
                    name=data['name'],
                    defaults={**data, 'created_by': admin_user}
                )
                if created:
                    self.stdout.write(f'Created accommodation: {acc.name}')

        # Create sample guide users
        guide_data = [
            {
                'username': 'guide_karim',
                'first_name': 'Abdul',
                'last_name': 'Karim',
                'email': 'karim@guide.com',
                'region': "Cox's Bazar",
                'languages': 'Bengali, English',
                'description': 'Experienced sea beach guide with 10 years of expertise in Cox\'s Bazar. I know every corner of the longest sea beach in the world.',
                'experience_years': 10,
                'hourly_rate': 500,
                'phone': '+880 1811-111111',
            },
            {
                'username': 'guide_rahim',
                'first_name': 'Mohammad',
                'last_name': 'Rahim',
                'email': 'rahim@guide.com',
                'region': 'Sundarbans',
                'languages': 'Bengali, English, Hindi',
                'description': 'Wildlife expert and certified Sundarbans guide. I\'ll take you deep into the mangrove forest safely.',
                'experience_years': 8,
                'hourly_rate': 700,
                'phone': '+880 1811-222222',
            },
            {
                'username': 'guide_fatema',
                'first_name': 'Fatema',
                'last_name': 'Begum',
                'email': 'fatema@guide.com',
                'region': 'Sylhet',
                'languages': 'Bengali, English',
                'description': 'Tea garden specialist and Sylhet region expert. Let me show you the green beauty of Srimangal.',
                'experience_years': 5,
                'hourly_rate': 400,
                'phone': '+880 1811-333333',
            },
        ]

        for data in guide_data:
            if not User.objects.filter(username=data['username']).exists():
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password='guide@2025',
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                )
                LocalGuide.objects.create(
                    user=user,
                    region=data['region'],
                    languages=data['languages'],
                    description=data['description'],
                    experience_years=data['experience_years'],
                    hourly_rate=data['hourly_rate'],
                    phone=data['phone'],
                    rating=4.5,
                )
                self.stdout.write(f'Created guide: {user.get_full_name()}')

        self.stdout.write(self.style.SUCCESS('\n✅ Sample data created successfully!'))
        self.stdout.write('Admin: username=admin, password=admin123')
        self.stdout.write('Guide password: guide@2025')

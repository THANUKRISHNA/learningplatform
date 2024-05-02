import requests
from bs4 import BeautifulSoup
from front.models import ScrapeCourse
import time
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Scrape courses from multiple university websites'

    def handle(self, *args, **kwargs):
        urls = [
            'https://online-learning.harvard.edu/catalog',
            'https://online.stanford.edu/courses',
            'https://www.edx.org/courses',
            'https://www.coursera.org/courses',
            'https://www.udacity.com/courses/all',
           
        ]

        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            if 'harvard' in url:
                courses = soup.select('.views-row')
                for course in courses:
                    try:
                        title = course.select_one('h3').text.strip()
                        description = course.select_one('.views-field-field-short-description').text.strip() if course.select_one('.views-field-field-short-description') else ''
                        amount_element = course.select_one('.field-name-field-course-tuition')
                        amount = amount_element.text.strip() if amount_element and amount_element.text.strip() != 'Free' else '0'
                        num_modules = len(course.select('.views-field-field-sections'))

                       
                        url_element = course.select_one('a.views-field-title')
                        if url_element:
                            course_url = url_element['href']
                        else:
                            course_url = None

                        
                        new_course = ScrapeCourse(
                            title=title,
                            description=description,
                            amount=amount,
                            num_modules=num_modules,
                            url=course_url
                        )
                        new_course.save()

                    except requests.exceptions.RequestException as e:
                        self.stdout.write(self.style.ERROR(f'Error scraping course: {e}'))
                    except AttributeError as e:
                        self.stdout.write(self.style.ERROR(f'AttributeError: {e}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error scraping course: {e}'))

            elif 'stanford' in url:
                courses = soup.select('.views-row')
                for course in courses:
                    try:
                        title = course.select_one('.course-title').text.strip()
                        description = course.select_one('.views-field-field-short-description').text.strip() if course.select_one('.views-field-field-short-description') else ''
                        amount = '0'  
                        num_modules = len(course.select('.views-field-field-sections'))

                        
                        url_element = course.select_one('a.course-title')
                        if url_element:
                            course_url = url_element['href']
                        else:
                            course_url = None

                        
                        new_course = ScrapeCourse(
                            title=title,
                            description=description,
                            amount=amount,
                            num_modules=num_modules,
                            url=course_url
                        )
                        new_course.save()

                    except requests.exceptions.RequestException as e:
                        self.stdout.write(self.style.ERROR(f'Error scraping course: {e}'))
                    except AttributeError as e:
                        self.stdout.write(self.style.ERROR(f'AttributeError: {e}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error scraping course: {e}'))

            elif 'edx' in url:
                courses = soup.select('.discovery-card')
                for course in courses:
                    try:
                        title = course.select_one('.discovery-card-title').text.strip()
                        description = course.select_one('.discovery-card-description').text.strip() if course.select_one('.discovery-card-description') else ''
                        amount = '0'  
                        num_modules = len(course.select('.discovery-card-section'))

                
                        url_element = course.select_one('a.discovery-card-link')
                        if url_element:
                            course_url = urljoin(url, url_element['href'])
                        else:
                            course_url = None

                        
                        new_course = ScrapeCourse(
                            title=title,
                            description=description,
                            amount=amount,
                            num_modules=num_modules,
                            url=course_url
                        )
                        new_course.save()

                    except requests.exceptions.RequestException as e:
                        self.stdout.write(self.style.ERROR(f'Error scraping course: {e}'))
                    except AttributeError as e:
                        self.stdout.write(self.style.ERROR(f'AttributeError: {e}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error scraping course: {e}'))

            elif 'coursera' in url:
                courses = soup.select('.ais-InfiniteHits-item')
                for course in courses:
                    try:
                        title = course.select_one('.product-name').text.strip()
                        description = course.select_one('.product-headline').text.strip()
                        amount_element = course.select_one('.product-final-price')
                        amount = amount_element.text.strip() if amount_element else '0'
                        num_modules = len(course.select('.week'))

                        
                        url_element = course.select_one('a.product-box-listing')
                        if url_element:
                            course_url = urljoin(url, url_element['href'])
                        else:
                            course_url = None

                       
                        new_course = ScrapeCourse(
                            title=title,
                            description=description,
                            amount=amount,
                            num_modules=num_modules,
                            url=course_url
                        )
                        new_course.save()

                    except requests.exceptions.RequestException as e:
                        self.stdout.write(self.style.ERROR(f'Error scraping course: {e}'))
                    except AttributeError as e:
                        self.stdout.write(self.style.ERROR(f'AttributeError: {e}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error scraping course: {e}'))

            elif 'udacity' in url:
                courses = soup.select('.course-summary')
                for course in courses:
                    try:
                        title = course.select_one('.course-summary__title').text.strip()
                        description = course.select_one('.course-summary__details').text.strip()
                        amount = '0'  
                        num_modules = len(course.select('.lesson-list__item'))

                       
                        url_element = course.select_one('a.course-summary__title')
                        if url_element:
                            course_url = urljoin(url, url_element['href'])
                        else:
                            course_url = None

                    
                        new_course = ScrapeCourse(
                            title=title,
                            description=description,
                            amount=amount,
                            num_modules=num_modules,
                            url=course_url
                        )
                        new_course.save()

                    except requests.exceptions.RequestException as e:
                        self.stdout.write(self.style.ERROR(f'Error scraping course: {e}'))
                    except AttributeError as e:
                        self.stdout.write(self.style.ERROR(f'AttributeError: {e}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error scraping course: {e}'))

            self.stdout.write(self.style.SUCCESS(f'Successfully scraped courses from {url}'))
            time.sleep(1)  

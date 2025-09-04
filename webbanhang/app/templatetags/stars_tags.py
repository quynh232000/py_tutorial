
import random
from django import template

register = template.Library()

@register.simple_tag
def render_random_stars(max_stars=5):
    """
    Trả về HTML 5 sao, ngẫu nhiên 1-max_stars
    """
    stars = random.randint(1, max_stars)
    full_star = '<i class="fas fa-star text-primary"></i>'
    empty_star = '<i class="fas fa-star"></i>'
    return full_star * stars + empty_star * (max_stars - stars)

@register.simple_tag
def render_stars(value, max_stars=5):
    """
    Trả về HTML 5 sao:
    - value: số sao muốn hiển thị (int)
    - max_stars: tổng số sao (mặc định 5)
    """
    stars = min(int(value), max_stars)  # giới hạn không vượt max_stars
    full_star = '<i class="fas fa-star text-primary"></i>'
    empty_star = '<i class="fas fa-star"></i>'
    return full_star * stars + empty_star * (max_stars - stars)

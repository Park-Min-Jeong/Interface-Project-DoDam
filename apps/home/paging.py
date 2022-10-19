from django.core.paginator import Paginator


def make_pagenator(page, num, obj_list):
    paginator = Paginator(obj_list, num)
    page_obj = paginator.get_page(page)
    page_list = paginator.get_elided_page_range(number=page, on_each_side=2, on_ends=1)

    return page_obj, page_list
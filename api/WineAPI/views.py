from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from rest_framework.decorators import api_view
from django.db.models import Avg
import numpy as np
from .models import *
from .constants import *
from .cosine_similarity import cos_sim
from WineAPI import recommender_settings


@api_view(['GET'])
def search_wines(request, criteria=""):
    """
    Searches for wines based on given criteria
    :param request: http request object
    :param criteria: string criteria used for searching
    :return: List of wines found based on criteria
    """
    try:
        wines = Wine.objects.all().filter(wine_name__icontains=criteria)[:30]
        wines_list = list(wines)
        wines_result = '{ "wines": ['

        for wine in wines_list:
            winethumb = ''
            if wine.wine_thumb:
                winethumb = 'https:' + wine.wine_thumb
            wines_result = wines_result + \
                (WineDto(wine.wine_id, wine.wine_name, winethumb)).toJSON() + ','

        wines_result = wines_result + '] }'

    except BaseException as ex:
        return HttpResponseServerError(ex)

    return HttpResponse(wines_result)


@api_view(['GET'])
def get_recommendations(request, profile, recommender_settings=recommender_settings):
    """
    Gets wine-recommendations
    :param request: http request object
    :param profile: wine taste profile
    :return: list of wines recommended
    """
    profile = json.loads(profile)
    if len(profile.keys()) != 3:
        return HttpResponseBadRequest("Incomplete request data")
    wine_data = profile["wine_data"]
    taste_data = profile["taste_data"]
    structure_data = profile["structure_data"]
    structure_param = recommender_settings.structure_param
    taste_param = recommender_settings.taste_param
    ratings_param = recommender_settings.ratings_param
    num_recs = recommender_settings.num_recs

    try:
        types = [option["option"] for option in wine_data[0]
                 ["options"] if option["selected"] == True]
        origins = [option["option"] for option in wine_data[2]
                   ["options"] if option["selected"] == True]
        ranges = [option["option"] for option in wine_data[1]
                  ["options"] if option["selected"] == True]

        user_taste_dict = {taste["label"]: taste["percentage"]
                           for taste in taste_data}
        user_taste = np.asarray([user_taste_dict[key] for key in keys_taste])

        user_structure_dict = {
            struc["label"]: struc["percentage"] for struc in structure_data}
        user_structure = np.asarray(
            [user_structure_dict[key] for key in keys_structure])

        local_wines = LocalWine.objects.none()
        if "over 20€" in ranges:
            local_wines = local_wines.union(LocalWine.objects.filter(
                lw_country__in=origins, lw_type__in=types, lw_price__gt=20))
        if "10-20€" in ranges:
            local_wines = local_wines.union(LocalWine.objects.filter(
                lw_country__in=origins, lw_type__in=types, lw_price__gt=10, lw_price__lte=20))
        if "under 10€" in ranges:
            local_wines = local_wines.union(LocalWine.objects.filter(
                lw_country__in=origins, lw_type__in=types, lw_price__lt=10))

        wines = []

        for lw in local_wines:
            wine = {}
            wine["id"] = lw.lw_id
            wine["picture_url"] = lw.lw_thumb
            wine["seller"] = lw.lw_seller
            wine["label"] = lw.lw_name
            wine_flavor_dict = WineFlavor.objects.get(wine_id=lw.wine).__dict__
            wine_flavor = np.asarray([wine_flavor_dict[key]
                                      for key in keys_taste])

            wine_structure_dict = WineStructure.objects.get(
                wine_id=lw.wine).__dict__
            wine_structure = np.asarray(
                [wine_structure_dict[key] for key in keys_structure])

            wine["score"] = ((structure_param * cos_sim(user_structure, wine_structure)) + (
                taste_param * cos_sim(user_taste, wine_flavor))) + (ratings_param * float(lw.wine.wine_rating) / 5)
            wines.append(wine)

        wines = sorted(wines, key=lambda k: k["score"], reverse=True)

        vendors = sellers
        for v in vendors:
            v["score_total"] = np.sum(np.asarray(
                [wine["score"] for wine in wines if wine["seller"] == v["id"]]))

        wines = wines[:num_recs]
        for i in range(len(wines)):
            wines[i]["rank"] = i + 1

        vendors = [vendor for vendor in sorted(
            vendors, key=lambda k: k["score_total"], reverse=True) if vendor["score_total"] > 0]
        for i in range(len(vendors)):
            vendors[i]["rank"] = i + 1

        result = '{ "sellers":' + \
                 json.dumps(vendors) + ', "wines":' + json.dumps(wines) + ' }'

    except BaseException as ex:
        return HttpResponseServerError(ex)

    return HttpResponse(result)


@api_view(['GET'])
def get_profile(request, wine_ids=[]):
    """
    Gets wine profile specific for a user
    :param request: http object
    :param wine_ids: wineids
    :return: wine preferences profile
    """
    wine_ids = json.loads(wine_ids)
    if len(wine_ids) == 0:
        return HttpResponseBadRequest("Wine id must not be null or 0")

    try:
        wines = list(Wine.objects.filter(wine_id__in=wine_ids))

        if not wines:
            return HttpResponseBadRequest("No wines found for specified Ids")

        wine_flavors = WineFlavor.objects.all().filter(
            wine_id__in=[w.wine_id for w in wines])

        wine_flavors_averages = wine_flavors.aggregate(black_fruit=Avg('black_fruit'), citrus_fruit=Avg('citrus_fruit'),
                                                       dried_fruit=Avg(
                                                           'dried_fruit'),
                                                       earth=Avg('earth'), floral=Avg('floral'),
                                                       microbio=Avg(
                                                           'microbio'),
                                                       non_oak=Avg('non_oak'), oak=Avg('oak'),
                                                       red_fruit=Avg(
                                                           'red_fruit'),
                                                       spices=Avg('spices'), tree_fruit=Avg('tree_fruit'),
                                                       tropical_fruit=Avg(
                                                           'tropical_fruit'),
                                                       vegetal=Avg('vegetal'))

        taste_data = [
            {"label": key, 'percentage': wine_flavors_averages[key]} for key in keys_taste]

        wine_type_options = []
        wine_origin_options = []
        wine_price_options = []
        multi_select_type = {'selection_type': 'multiselect',
                             'name': 'Type of Wine', 'options': wine_type_options}
        multi_select_price = {'selection_type': 'multiselect',
                              'name': 'Price', 'options': wine_price_options}
        search_field_origin = {'selection_type': 'search_field',
                               'name': 'Origin', 'options': wine_origin_options}

        distinct_types = []
        distinct_prices = {'<10': False, '10-20': False, '>20': False}
        distinct_origin = []
        for wine in wines:
            if wine.wine_type not in distinct_types:
                distinct_types.append(wine.wine_type)
            if wine.wine_country.strip() not in distinct_origin:
                distinct_origin.append(wine.wine_country.strip())
            if wine.wine_price < 10:
                distinct_prices['<10'] = True
            if 10 <= wine.wine_price <= 20:
                distinct_prices['10-20'] = True
            if wine.wine_price > 20:
                distinct_prices['>20'] = True

        for wine_type in wine_types:
            wine_type_options.append({'option': wine_type, 'selected': False})

        for wine_country in countries:
            wine_origin_options.append(
                {'option': wine_country['wine_country'], 'selected': False})

        for w_type in distinct_types:
            for opt in wine_type_options:
                if opt['option'] == w_type:
                    opt['selected'] = True
        for w_origin in distinct_origin:
            for opt in wine_origin_options:
                if opt['option'] == w_origin:
                    opt['selected'] = True

        wine_price_options.append(
            {'option': 'under 10€', 'selected': distinct_prices['<10']})
        wine_price_options.append(
            {'option': '10-20€', 'selected': distinct_prices['10-20']})
        wine_price_options.append(
            {'option': 'over 20€', 'selected': distinct_prices['>20']})

        wine_structure_averages = WineStructure.objects.filter(wine_id__in=wine_ids).aggregate(
            wine_acidity=Avg('wine_acidity'), wine_fizziness=Avg('wine_fizziness'),
            wine_intensity=Avg('wine_intensity'),
            wine_tannin=Avg('wine_tannin'), wine_sweetness=Avg('wine_sweetness'))

        structure_data = [
            {"label": key, 'percentage': wine_structure_averages[key]} for key in keys_structure]

        # construct json result object
        result = '{ "wine_data": [' + json.dumps(multi_select_type) + ',' + json.dumps(
            multi_select_price) + ',' + json.dumps(search_field_origin) + '],'
        result += '"taste_data": ' + \
                  json.dumps(taste_data) + ', "structure_data": ' + \
                  json.dumps(structure_data) + ' }'
    except BaseException as ex:
        return HttpResponseServerError(ex)

    return HttpResponse(result)


@api_view(['GET'])
def get_wine_details(request, id=0):
    """
    Gets details for a wine
    :param request: http request object
    :param id: id of the wine
    :return: details of specified wine
    """
    if id <= 0:
        return HttpResponseBadRequest("Wine id must not be null or 0")

    try:
        wine = LocalWine.objects.get(lw_id=id)

        if wine is None:
            return HttpResponseBadRequest()

        wine_flavor_dict = WineFlavor.objects.get(wine_id=wine.wine).__dict__
        taste_data = [{"label": key, 'percentage': wine_flavor_dict[key]}
                      for key in keys_taste]

        wine_structure_dict = WineStructure.objects.get(
            wine_id=wine.wine).__dict__
        structure_data = [
            {"label": key, 'percentage': wine_structure_dict[key]} for key in keys_structure]

        facts = [{'label': 'country', 'content': wine.lw_country},
                 {'label': 'region', 'content': wine.lw_region},
                 {'label': 'style', 'content': wine.lw_type},
                 {'label': 'price', 'content': str(wine.lw_price) + '€'},
                 {'label': 'year', 'content': wine.lw_year},
                 {'label': 'seller', 'content': next(
                     (item["name"] for item in sellers if item["id"] == wine.lw_seller), None)},
                 ]

        wine_details_dto = {'id': wine.lw_id, 'name': wine.lw_name, 'description': wine.lw_description,
                            'link': wine.lw_url, 'picture_url': wine.lw_thumb,
                            'facts': facts, 'taste_data': taste_data, 'structure_data': structure_data}
        wine_details_dto = json.dumps(wine_details_dto)
    except BaseException as ex:
        return HttpResponseServerError(ex)

    return HttpResponse(wine_details_dto)

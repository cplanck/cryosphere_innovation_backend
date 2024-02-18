from django.db.models import Q
import re

def search_and_filter_queryset(queryset, request, search_fields, default_order_by):

    """
    Takes a queryset and refines it based on:
    q: a query string for searching
    sort_by: a index to search by like last_modified, status
    sort_dir: the direction so sort, either ascending or descending

    Written 18 Feb, 2024
    """

    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by')
    sort_dir = request.GET.get('sort_dir')
    
    if query:
        filter_conditions = Q()
        for field in search_fields:
            filter_conditions |= Q(**{f'{field}__icontains': query})
            print(filter_conditions)
        queryset = queryset.filter(filter_conditions).distinct()

    if sort_by:
        if sort_dir == 'asc':
            queryset = queryset.order_by( str(sort_by))
        elif sort_dir == 'desc':
            queryset = queryset.order_by('-' + str(sort_by))
        else:
            queryset = queryset.order_by(default_order_by)

    return queryset

def strip_data_ends(data, strip_from_start, strip_from_end):
    print(strip_from_start)
    if strip_from_start:
        data = data[strip_from_start:]
    if strip_from_end:
        data = data[:-strip_from_end]
    return data

def clean_headers(headers):

    """
    Takes a list of objects and sanitizes the keys so that there are:
    1) No characters other than lowercase a-z, 0-9
    2) Replaces spaces with underscores
    3) Removes any duplicates keys by iteratively appending numbers to them until they become unique

    Written 18 Feb, 2024
    """
    cleaned_headers = []
    unique_headers = set()
    empty_counter = 0
    cleaned_counter = 0

    for header in headers:
        
        if re.search(r'[^\w\s]', header):
            cleaned_counter += 1

        # Replace spaces with underscores
        cleaned_header = header.replace(' ', '_')
        # Remove any characters that are not a letter, a digit, or an underscore
        cleaned_header = re.sub(r'[^\w\s]', '', cleaned_header)
        # Convert to lowercase to make case-insensitive comparisons
        cleaned_header = cleaned_header.lower()

        # If the cleaned header is empty, replace it with "empty_<counter>"
        if not cleaned_header:
            cleaned_header = f'empty_{empty_counter}'
            empty_counter += 1
        # Ensure the cleaned header is unique
        elif cleaned_header not in unique_headers:
            cleaned_headers.append(cleaned_header)
            unique_headers.add(cleaned_header)
        else:
            # If header is not unique, add counter to make it unique
            while f'{cleaned_header}_{empty_counter}' in unique_headers:
                empty_counter += 1
            unique_header = f'{cleaned_header}_{empty_counter}'
            cleaned_headers.append(unique_header)
            unique_headers.add(unique_header)
            
    return cleaned_headers, cleaned_counter

def replace_key_names(single_object, new_key_names):

    """
    Replaces the keys in an object. 

    Written 18 Feb, 2024
    """
    old_key_names = list(single_object.keys())
    replaced_object = {new_key_names[i]: single_object[old_key_names[i]] for i in range(len(old_key_names))}
    return replaced_object
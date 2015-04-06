import scrapy

from job_runner.scrape import collapse_duplicates, create_duplicates_hash, get_ids_to_remove, get_items_to_add
from nose.tools import eq_

from scrapers.models.dog import Dog


def create_item(url, name, agency):
    item = Dog()

    item['url'] = [url]

    item['name'] = name

    item['breed'] = 'breed'

    item['age'] = '1'

    item['size'] = 'medium'

    item['desc'] = 'desc'

    item['img'] = 'img'

    item['agency'] = agency

    return item


def test_collapse_duplicates():

    results = [create_item('test_url', 'test_name', 'test_agency'),
               create_item('test_url2', 'test_name', 'test_agency'),
               create_item('test_url3', 'new_name', 'new_agency')]

    collapsed = collapse_duplicates(results)

    eq_(2, len(collapsed), "Expected only 2 elements")

    single_url = None
    for item in collapsed:
        if len(item['url']) == 1:
            single_url = item

    double_url = None
    for item in collapsed:
        if len(item['url']) == 2:
            double_url = item

    eq_(2, len(double_url['url']), "Expected 2 urls in the first element but was: {}".format(collapsed[0]['url']))
    eq_(1, len(single_url['url']), "Expected 1 url in the second element")
    assert 'test_url' in double_url['url']
    assert 'test_url2' in double_url['url']


def test_create_duplicates_hash():
    results = [create_item('test_url', 'test_name', 'test_agency'),
               create_item('test_url2', 'test_name', 'test_agency'),
               create_item('test_url', 'new_name', 'new_agency')]

    duplicates_hash = create_duplicates_hash(results)

    eq_(2, len(duplicates_hash), "Expected 2 keys in duplicates_hash")
    assert 'test_name|test_agency' in duplicates_hash
    assert 'new_name|new_agency' in duplicates_hash
    eq_(2, len(duplicates_hash['test_name|test_agency']), "Expected 2 items for key")


def test_get_ids_to_remove():
    results = [create_item('test_url', 'test_name', 'test_agency'),
               create_item('test_url', 'new_name', 'new_agency')]

    db_results = [{'_id': 1,
                   'name': 'test_name',
                   'agency': 'test_agency'},
                  {'_id': 2,
                   'name': 'test_remove',
                   'agency': 'remove_agency'}]

    ids_to_remove = get_ids_to_remove(results, db_results)

    assert len(ids_to_remove) == 1
    assert ids_to_remove[0] == 2


def test_get_items_to_add():
    results = [create_item('test_url', 'test_name', 'test_agency'),
               create_item('test_url', 'new_name', 'new_agency')]

    db_results = [{'_id': 1,
                   'name': 'test_name',
                   'agency': 'test_agency'},
                  {'_id': 2,
                   'name': 'test_remove',
                   'agency': 'remove_agency'}]

    items_to_add = get_items_to_add(results, db_results)

    assert len(items_to_add) == 1
    assert items_to_add[0]['name'] == 'new_name'




